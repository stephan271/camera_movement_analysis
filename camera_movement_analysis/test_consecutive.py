import cv2
import numpy as np

# Load static mask and dilate it
static_mask_img = cv2.imread("/home/egli/.gemini/antigravity/brain/c389e7ca-d9dd-451a-9838-cf1dec287928/scratch/static_mask.png", cv2.IMREAD_GRAYSCALE)
kernel = np.ones((15, 15), np.uint8)
dilated_mask = cv2.dilate(static_mask_img, kernel, iterations=1)
analysis_mask = cv2.bitwise_not(dilated_mask)
h, w = analysis_mask.shape
cv2.circle(analysis_mask, (w//2, h//2), 120, 0, -1)

video_path = "/home/egli/development/uapvideos/clip.mp4"
cap = cv2.VideoCapture(video_path)

# Read frame 0, 1, 2
ret, f0 = cap.read()
ret, f1 = cap.read()
cap.release()

f0_gray = cv2.cvtColor(f0, cv2.COLOR_BGR2GRAY)
f1_gray = cv2.cvtColor(f1, cv2.COLOR_BGR2GRAY)

sift = cv2.SIFT_create()
kp0, des0 = sift.detectAndCompute(f0_gray, mask=analysis_mask)
kp1, des1 = sift.detectAndCompute(f1_gray, mask=analysis_mask)

print(f"Frame 0: found {len(kp0)} keypoints")
print(f"Frame 1: found {len(kp1)} keypoints")

bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
matches = bf.match(des0, des1)
print(f"Found {len(matches)} initial matches")

src_pts = np.float32([kp0[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
dst_pts = np.float32([kp1[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

M, inliers = cv2.estimateAffinePartial2D(src_pts, dst_pts, method=cv2.RANSAC, ransacReprojThreshold=2.0)

if M is not None:
    dx = M[0, 2]
    dy = M[1, 2]
    scale = np.sqrt(M[0, 0]**2 + M[0, 1]**2)
    angle = np.arctan2(M[1, 0], M[0, 0]) * 180 / np.pi
    num_inliers = np.sum(inliers)
    print(f"Transformation: dx={dx:.4f}, dy={dy:.4f}, scale={scale:.5f}, angle={angle:.4f} degrees")
    print(f"RANSAC Inliers: {num_inliers} / {len(matches)} ({num_inliers/len(matches)*100:.1f}%)")
else:
    print("Failed to estimate transformation")
