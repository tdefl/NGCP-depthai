import logging
from collections import deque
from pathlib import Path
from typing import Union, Dict

try:
    import cv2
except ImportError:
    cv2 = None

import depthai as dai
import numpy as np

from depthai_sdk.recorders.video_writers import BaseWriter
from depthai_sdk.recorders.video_writers.utils import create_writer_dir


class VideoWriter(BaseWriter):
    def __init__(self, path: Path, name: str, fourcc: str, fps: float):  # TODO: fourcc is not used
        super().__init__(path, name)

        self._fourcc = None
        self._w, self._h = None, None
        self._fps = fps

        self._buffer = None
        self._is_buffer_enabled = False

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def init_buffer(self, name: str, max_seconds: int):
        if max_seconds > 0:
            self._buffers[name] = deque(maxlen=int(max_seconds * self._fps))
            self._is_buffer_enabled = True

    def set_fourcc(self, fourcc: str):
        self._fourcc = fourcc

    def create_file_for_buffer(self, subfolder: str, buf_name: str):
        if self._buffers[buf_name] is None:
            raise RuntimeError(f"Buffer {buf_name} is not enabled")

        if len(self._buffers[buf_name]) == 0:
            return None

        frame = self._buffers[buf_name][0]
        self.create_file(subfolder, frame)

    def create_file(self, subfolder: str, frame: Union[dai.ImgFrame, np.ndarray]):
        path_to_file = create_writer_dir(self.path / subfolder, self.name, 'avi')
        self._create_file(path_to_file, frame)

    def _create_file(self, path_to_file: str, frame: Union[dai.ImgFrame, np.ndarray]):
        if isinstance(frame, np.ndarray):
            self._h, self._w = frame.shape[:2]
        else:
            self._h, self._w = frame.getHeight(), frame.getWidth()

        # Disparity - RAW8
        # Depth - RAW16
        if self._fourcc is None:
            if isinstance(frame, np.ndarray):
                c = 1 if frame.ndim == 2 else frame.shape[2]
                self._fourcc = "GRAY" if c == 1 else "I420"
            else:
                if frame.getType() == dai.ImgFrame.Type.RAW16:  # Depth
                    self._fourcc = "FFV1"
                elif frame.getType() == dai.ImgFrame.Type.RAW8:  # Mono Cams
                    self._fourcc = "GREY"
                else:
                    self._fourcc = "I420"

        self._file = cv2.VideoWriter(path_to_file,
                                     cv2.VideoWriter_fourcc(*self._fourcc),
                                     self._fps,
                                     (self._w, self._h),
                                     isColor=self._fourcc != "GREY")

    def write(self, frame: Union[dai.ImgFrame, np.ndarray]):
        if self._file is None:
            self.create_file(subfolder='', frame=frame)
        self._file.write(frame if isinstance(frame, np.ndarray) else frame.getCvFrame())

    def close(self):
        if self._file is not None:
            self._file.release()
            self._file = None
