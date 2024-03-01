import os
import supervision as sv
from tqdm import tqdm

# Get the current working directory
CURRENT_DIR = os.getcwd()

# Local path to the downloaded video file
LOCAL_VIDEO_PATH = f"{CURRENT_DIR}/red_square.mp4"

# Ensure the video file exists
if not os.path.exists(LOCAL_VIDEO_PATH):
    raise FileNotFoundError(f"The video file '{LOCAL_VIDEO_PATH}' does not exist.")

# List containing the local path to the video file
VIDEO_PATHS = [LOCAL_VIDEO_PATH]

# Directory where you want to save the extracted images
IMAGE_DIR_PATH = f"{CURRENT_DIR}/images"

# Frame extraction parameters
FRAME_STRIDE = 10

# Loop through the video paths and extract frames
for video_path in tqdm(VIDEO_PATHS):
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    image_name_pattern = video_name + "-{:05d}.png"
    with sv.ImageSink(target_dir_path=IMAGE_DIR_PATH, image_name_pattern=image_name_pattern) as sink:
        for image in sv.get_video_frames_generator(source_path=str(video_path), stride=FRAME_STRIDE):
            sink.save_image(image=image)
