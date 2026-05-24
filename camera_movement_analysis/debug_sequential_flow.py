import cv2
import numpy as np

static_mask_img = cv2.imread("/home/egli/.gemini/antigravity/brain/c389e7ca-d9dd-451a-9838-cf1dec287928/scratch/static_mask.png", cv2.IMREAD_GRAYSCALE)
kernel = np.ones((15, 15), np.uint8)
dilated_mask = cv2.dilate(static_mask_img, kernel, iterations=1)
analysis_mask = cv2.bitwise_not(dilated_mask)
h, w = analysis_mask.shape
cv2.circle(analysis_mask, (w//2, h//2), 120, 0, -1)

video_path = "/home/egli/development/uapvideos/clip.mp4"
cap = cv2.VideoCapture(video_path)

# Skip to frame 360
for _ in range(360):
    cap.read()

ret, prev_frame = cap.read()
prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

lk_params = dict(winSize=(21, 21),
                 maxLevel=3,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01))

feature_params = dict(maxCorners=400,
                      qualityLevel=0.01,
                      minDistance=10,
                      blockSize=7)

for idx in range(361, 375):
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    p0 = cv2.goodFeaturesToTrack(prev_gray, mask=analysis_mask, **feature_params)
    
    if p0 is not None:
        p1, st, err = cv2.calcOpticalFlowPyrLK(prev_gray, gray, p0, None, **lk_params)
        good_new = p1[st == 1]
        good_old = p0[st == 1]
        
        M, inliers = cv2.estimateAffinePartial2D(good_old, good_new, method=cv2.RANSAC, ransacReprojThreshold=2.0)
        
        if M is not None:
            dx = M[0, 2]
            dy = M[1, 2]
            scale = np.sqrt(M[0, 0]**2 + M[0, 1]**2)
            angle = np.arctan2(M[1, 0], M[0, 0]) * 180 / np.pi
            print(f"Frame {idx}: dx={dx:.4f}, dy={dy:.4f}, scale={scale:.5f}, angle={angle:.4f}, inliers={np.sum(inliers)}/{len(good_new)}")
        else:
            print(f"Frame {idx}: M is None")
    else:
        print(f"Frame {idx}: p0 is None")
        
    prev_gray = gray.copy()

cap.release()
