import cv2
import numpy as np

img368 = cv2.imread("/home/egli/.gemini/antigravity/brain/c389e7ca-d9dd-451a-9838-cf1dec287928/scratch/transition_frames/frame_368.png", cv2.IMREAD_GRAYSCALE)
img369 = cv2.imread("/home/egli/.gemini/antigravity/brain/c389e7ca-d9dd-451a-9838-cf1dec287928/scratch/transition_frames/frame_369.png", cv2.IMREAD_GRAYSCALE)

# Load analysis mask
mask = cv2.imread("/home/egli/.gemini/antigravity/brain/c389e7ca-d9dd-451a-9838-cf1dec287928/scratch/analysis_mask.png", cv2.IMREAD_GRAYSCALE)

feature_params = dict(maxCorners=400,
                      qualityLevel=0.01,
                      minDistance=10,
                      blockSize=7)

lk_params = dict(winSize=(21, 21),
                 maxLevel=3,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01))

p0 = cv2.goodFeaturesToTrack(img368, mask=mask, **feature_params)
p1, st, err = cv2.calcOpticalFlowPyrLK(img368, img369, p0, None, **lk_params)

good_new = p1[st == 1]
good_old = p0[st == 1]

M, inliers = cv2.estimateAffinePartial2D(good_old, good_new, method=cv2.RANSAC, ransacReprojThreshold=2.0)

if M is not None:
    dx = M[0, 2]
    dy = M[1, 2]
    scale = np.sqrt(M[0, 0]**2 + M[0, 1]**2)
    angle = np.arctan2(M[1, 0], M[0, 0]) * 180 / np.pi
    print(f"LK Flow (368 to 369): dx={dx:.4f}, dy={dy:.4f}, scale={scale:.5f}, angle={angle:.4f} degrees")
    print(f"Inliers: {np.sum(inliers)} / {len(good_new)}")
else:
    print("LK Affine estimation failed")
