import cv2
import numpy as np

video_path = "/home/egli/development/uapvideos/clip.mp4"
cap = cv2.VideoCapture(video_path)

cap.set(cv2.CAP_PROP_POS_FRAMES, 368)
ret, f368 = cap.read()

ret, f369 = cap.read()

ret, f370 = cap.read()
cap.release()

f368_gray = cv2.cvtColor(f368, cv2.COLOR_BGR2GRAY)
f369_gray = cv2.cvtColor(f369, cv2.COLOR_BGR2GRAY)
f370_gray = cv2.cvtColor(f370, cv2.COLOR_BGR2GRAY)

print(f"Diff 368-370 mean abs diff: {np.mean(np.abs(f368_gray.astype(np.int32) - f370_gray.astype(np.int32)))}")
print(f"Diff 368-369 mean abs diff: {np.mean(np.abs(f368_gray.astype(np.int32) - f369_gray.astype(np.int32)))}")
print(f"Diff 369-370 mean abs diff: {np.mean(np.abs(f369_gray.astype(np.int32) - f370_gray.astype(np.int32)))}")

# Save frame 369
cv2.imwrite("/home/egli/.gemini/antigravity/brain/c389e7ca-d9dd-451a-9838-cf1dec287928/scratch/transition_frames/frame_369.png", f369)
