import cv2
import numpy as np

video_path = "/home/egli/development/uapvideos/clip.mp4"
cap = cv2.VideoCapture(video_path)

frames_dict = {}

current_idx = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    if current_idx in [368, 369, 370]:
        frames_dict[current_idx] = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    current_idx += 1
cap.release()

# Load the saved sequential PNG files
png_368 = cv2.imread("/home/egli/.gemini/antigravity/brain/c389e7ca-d9dd-451a-9838-cf1dec287928/scratch/sequential_frames/real_frame_368.png", cv2.IMREAD_GRAYSCALE)
png_369 = cv2.imread("/home/egli/.gemini/antigravity/brain/c389e7ca-d9dd-451a-9838-cf1dec287928/scratch/sequential_frames/real_frame_369.png", cv2.IMREAD_GRAYSCALE)

# Compare the sequential array directly
print("Difference between memory 368 and memory 369:")
diff_mem = np.mean(np.abs(frames_dict[368].astype(np.int32) - frames_dict[369].astype(np.int32)))
print(f"Mean Abs Diff: {diff_mem:.6f}")

print("\nDifference between memory 368 and saved PNG 368:")
diff_png368 = np.mean(np.abs(frames_dict[368].astype(np.int32) - png_368.astype(np.int32)))
print(f"Mean Abs Diff: {diff_png368:.6f}")

print("\nDifference between memory 369 and saved PNG 369:")
diff_png369 = np.mean(np.abs(frames_dict[369].astype(np.int32) - png_369.astype(np.int32)))
print(f"Mean Abs Diff: {diff_png369:.6f}")
