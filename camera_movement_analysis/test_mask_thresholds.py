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
    if count % 10 == 0:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frames.append(gray)
    count += 1
cap.release()

frames = np.array(frames)
std_img = np.std(frames, axis=0)

for thresh in [1.0, 2.0, 3.0, 5.0, 8.0, 10.0]:
    mask = std_img < thresh
    print(f"Threshold {thresh:.1f}: {np.mean(mask)*100:.2f}% of pixels are static")
    cv2.imwrite(f"/home/egli/.gemini/antigravity/brain/c389e7ca-d9dd-451a-9838-cf1dec287928/scratch/static_mask_thresh_{thresh:.1f}.png", (mask * 255).astype(np.uint8))
