import cv2
import os

video_path = "/home/egli/development/uapvideos/clip.mp4"
output_dir = "/home/egli/.gemini/antigravity/brain/c389e7ca-d9dd-451a-9838-cf1dec287928/scratch/sequential_frames"
os.makedirs(output_dir, exist_ok=True)

cap = cv2.VideoCapture(video_path)

frames_to_save = {278, 279, 280, 281, 282, 367, 368, 369, 370, 371}

current_idx = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    if current_idx in frames_to_save:
        output_path = os.path.join(output_dir, f"real_frame_{current_idx:03d}.png")
        cv2.imwrite(output_path, frame)
        print(f"Saved {output_path}")
    current_idx += 1

cap.release()
