import cv2
import os

video_path = "red_square.mp4"
output_folder = "red_square_frames/"

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

cap = cv2.VideoCapture(video_path)
frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    cv2.imwrite(f"{output_folder}/frame_{frame_count}.jpg", frame)

cap.release()
