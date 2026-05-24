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

# Run LK Flow on memory frames
p0_mem = cv2.goodFeaturesToTrack(mem368, mask=mask, **feature_params)
p1_mem, st_mem, err_mem = cv2.calcOpticalFlowPyrLK(mem368, mem369, p0_mem, None, **lk_params)
good_new_mem = p1_mem[st_mem == 1]
good_old_mem = p0_mem[st_mem == 1]
M_mem, inliers_mem = cv2.estimateAffinePartial2D(good_old_mem, good_new_mem, method=cv2.RANSAC, ransacReprojThreshold=2.0)

# Run LK Flow on PNG frames
p0_png = cv2.goodFeaturesToTrack(png368, mask=mask, **feature_params)
p1_png, st_png, err_png = cv2.calcOpticalFlowPyrLK(png368, png369, p0_png, None, **lk_params)
good_new_png = p1_png[st_png == 1]
good_old_png = p0_png[st_png == 1]
M_png, inliers_png = cv2.estimateAffinePartial2D(good_old_png, good_new_png, method=cv2.RANSAC, ransacReprojThreshold=2.0)

print("MEMORY TRACKING:")
if M_mem is not None:
    print(f"dx={M_mem[0, 2]:.4f}, dy={M_mem[1, 2]:.4f}, scale={np.sqrt(M_mem[0,0]**2+M_mem[0,1]**2):.5f}")
    print(f"Inliers: {np.sum(inliers_mem)} / {len(good_new_mem)}")
    # Print the individual translations for the inliers to see if they are consistent!
    inlier_indices = np.where(inliers_mem.ravel() == 1)[0]
    inlier_shifts = good_new_mem[inlier_indices] - good_old_mem[inlier_indices]
    print(f"Sample inlier shifts: {inlier_shifts[:10].tolist()}")
    print(f"Mean inlier shift: {np.mean(inlier_shifts, axis=0)}")
else:
    print("M is None")

print("\nPNG TRACKING:")
if M_png is not None:
    print(f"dx={M_png[0, 2]:.4f}, dy={M_png[1, 2]:.4f}, scale={np.sqrt(M_png[0,0]**2+M_png[0,1]**2):.5f}")
    print(f"Inliers: {np.sum(inliers_png)} / {len(good_new_png)}")
    inlier_indices = np.where(inliers_png.ravel() == 1)[0]
    inlier_shifts = good_new_png[inlier_indices] - good_old_png[inlier_indices]
    print(f"Sample inlier shifts: {inlier_shifts[:10].tolist()}")
    print(f"Mean inlier shift: {np.mean(inlier_shifts, axis=0)}")
else:
    print("M is None")
