import cv2
import numpy as np

# Load sequential memory frames
video_path = "/home/egli/development/uapvideos/clip.mp4"
cap = cv2.VideoCapture(video_path)
for _ in range(368):
    cap.read()
ret, f368 = cap.read()
ret, f369 = cap.read()
cap.release()

mem368 = cv2.cvtColor(f368, cv2.COLOR_BGR2GRAY)
mem369 = cv2.cvtColor(f369, cv2.COLOR_BGR2GRAY)

# Load PNG frames
png368 = cv2.imread("/home/egli/.gemini/antigravity/brain/c389e7ca-d9dd-451a-9838-cf1dec287928/scratch/sequential_frames/real_frame_368.png", cv2.IMREAD_GRAYSCALE)
png369 = cv2.imread("/home/egli/.gemini/antigravity/brain/c389e7ca-d9dd-451a-9838-cf1dec287928/scratch/sequential_frames/real_frame_369.png", cv2.IMREAD_GRAYSCALE)

print(f"mem368: shape={mem368.shape}, min={mem368.min()}, max={mem368.max()}, mean={mem368.mean():.4f}")
print(f"png368: shape={png368.shape}, min={png368.min()}, max={png368.max()}, mean={png368.mean():.4f}")

# Check if they are actually pixel-by-pixel identical or close
diff = np.abs(mem368.astype(np.float32) - png368.astype(np.float32))
print(f"Max diff: {np.max(diff)}, Mean diff: {np.mean(diff):.4f}")
print(f"Number of pixels with diff > 0: {np.sum(diff > 0)} / {diff.size}")
