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

# Load analysis mask
mask = cv2.imread("/home/egli/.gemini/antigravity/brain/c389e7ca-d9dd-451a-9838-cf1dec287928/scratch/analysis_mask.png", cv2.IMREAD_GRAYSCALE)

feature_params = dict(maxCorners=400,
                      qualityLevel=0.01,
                      minDistance=10,
                      blockSize=7)

lk_params = dict(winSize=(21, 21),
                 maxLevel=3,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01))

# 1. Run LK Flow on memory frames
p0_mem = cv2.goodFeaturesToTrack(mem368, mask=mask, **feature_params)
p1_mem, st_mem, err_mem = cv2.calcOpticalFlowPyrLK(mem368, mem369, p0_mem, None, **lk_params)
good_new_mem = p1_mem[st_mem == 1]
good_old_mem = p0_mem[st_mem == 1]
M_mem, inliers_mem = cv2.estimateAffinePartial2D(good_old_mem, good_new_mem, method=cv2.RANSAC, ransacReprojThreshold=2.0)
dx_mem = M_mem[0, 2] if M_mem is not None else 0

# 2. Run LK Flow on PNG frames
p0_png = cv2.goodFeaturesToTrack(png368, mask=mask, **feature_params)
p1_png, st_png, err_png = cv2.calcOpticalFlowPyrLK(png368, png369, p0_png, None, **lk_params)
good_new_png = p1_png[st_png == 1]
good_old_png = p0_png[st_png == 1]
M_png, inliers_png = cv2.estimateAffinePartial2D(good_old_png, good_new_png, method=cv2.RANSAC, ransacReprojThreshold=2.0)
dx_png = M_png[0, 2] if M_png is not None else 0

print(f"Memory frames: dx={dx_mem:.4f}")
print(f"PNG frames: dx={dx_png:.4f}")

# Let's compare p0_mem and p0_png
print(f"Number of corners in mem: {len(p0_mem)}, png: {len(p0_png)}")
diff_p0 = np.max(np.abs(p0_mem - p0_png))
print(f"Max absolute diff in detected corners p0: {diff_p0:.6f}")
