import cv2
import numpy as np

video_path = "/home/egli/development/uapvideos/clip.mp4"
cap = cv2.VideoCapture(video_path)

frames = []
count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    # Sample every 10th frame to keep memory usage low
    if count % 10 == 0:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frames.append(gray)
    count += 1
cap.release()

frames = np.array(frames) # Shape: (NumFrames, Height, Width)
std_img = np.std(frames, axis=0)
mean_img = np.mean(frames, axis=0)

# A pixel is static if its standard deviation is extremely low
# HUD lines are static (white/gray) and redaction boxes are static (black)
static_mask = std_img < 1.0 # threshold of 1.0 gray level variation

print(f"Total sampled frames: {len(frames)}")
print(f"Static mask percentage: {np.mean(static_mask)*100:.2f}% of pixels are static")

# Save the mean, std, and static mask as images for visual inspection
cv2.imwrite("/home/egli/.gemini/antigravity/brain/c389e7ca-d9dd-451a-9838-cf1dec287928/scratch/mean_img.png", mean_img.astype(np.uint8))
cv2.imwrite("/home/egli/.gemini/antigravity/brain/c389e7ca-d9dd-451a-9838-cf1dec287928/scratch/std_img.png", (std_img * 10).astype(np.uint8)) # scale std for visibility
cv2.imwrite("/home/egli/.gemini/antigravity/brain/c389e7ca-d9dd-451a-9838-cf1dec287928/scratch/static_mask.png", (static_mask * 255).astype(np.uint8))
