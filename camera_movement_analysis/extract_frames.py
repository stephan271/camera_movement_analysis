import cv2
import os

video_path = "/home/egli/development/uapvideos/clip.mp4"
output_dir = "/home/egli/.gemini/antigravity/brain/c389e7ca-d9dd-451a-9838-cf1dec287928/scratch/extracted_frames"
os.makedirs(output_dir, exist_ok=True)

cap = cv2.VideoCapture(video_path)
count = 392

# We want 10 frames
frame_indices = [int(i * (count - 1) / 9) for i in range(10)]
print(f"Target frame indices: {frame_indices}")

current_idx = 0
extracted_count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    if current_idx in frame_indices:
        output_path = os.path.join(output_dir, f"frame_{current_idx:03d}.png")
        cv2.imwrite(output_path, frame)
        print(f"Saved {output_path}")
        extracted_count += 1
    current_idx += 1

cap.release()
