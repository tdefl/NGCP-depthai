import os
import supervision as sv
from tqdm import tqdm
import gdown  # for downloading from google drive

# Get the home directory dynamically
HOME = os.path.expanduser('~')

# get current working directory
CURRENT_DIR = os.getcwd()

# Local directory where you want to save the downloaded video file
#LOCAL_VIDEO_DIR = f"{HOME}/videos"
LOCAL_VIDEO_DIR = f"{CURRENT_DIR}/videos"

# Google Drive link to the video file
GOOGLE_DRIVE_VIDEO_LINK = "https://drive.google.com/file/d/1hNCXtBr7XjTzV2uGNzDGgI4fuov1Y2bb/view?usp=sharing"

# Download the video file using gdown
gdown.download(GOOGLE_DRIVE_VIDEO_LINK, f"{LOCAL_VIDEO_DIR}/video.mp4", quiet=False)

# List the local directory to get the video path
video_paths = sv.list_files_with_extensions(directory=LOCAL_VIDEO_DIR, extensions=["mp4"])

TEST_VIDEO_PATHS, TRAIN_VIDEO_PATHS = video_paths[:2], video_paths[2:]
IMAGE_DIR_PATH = f"{CURRENT_DIR}/images"
FRAME_STRIDE = 10

for video_path in tqdm(TRAIN_VIDEO_PATHS):
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    image_name_pattern = video_name + "-{:05d}.png"
    with sv.ImageSink(target_dir_path=IMAGE_DIR_PATH, image_name_pattern=image_name_pattern) as sink:
        for image in sv.get_video_frames_generator(source_path=str(video_path), stride=FRAME_STRIDE):
            sink.save_image(image=image)
