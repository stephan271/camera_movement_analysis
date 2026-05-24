import cv2
import numpy as np

# Load static mask and dilate it to cover boundaries
static_mask_img = cv2.imread("/home/egli/.gemini/antigravity/brain/c389e7ca-d9dd-451a-9838-cf1dec287928/scratch/static_mask.png", cv2.IMREAD_GRAYSCALE)
kernel = np.ones((15, 15), np.uint8)
dilated_mask = cv2.dilate(static_mask_img, kernel, iterations=1)
# The analysis mask should be 255 where we WANT to detect keypoints, and 0 where we DON'T.
# So we invert the dilated static mask.
analysis_mask = cv2.bitwise_not(dilated_mask)

# Also let's mask out the central area (e.g., circle of radius 120 around center) to avoid HUD
h, w = analysis_mask.shape
cv2.circle(analysis_mask, (w//2, h//2), 120, 0, -1)

# Save analysis mask for checking
cv2.imwrite("/home/egli/.gemini/antigravity/brain/c389e7ca-d9dd-451a-9838-cf1dec287928/scratch/analysis_mask.png", analysis_mask)

# Test SIFT matching
sift = cv2.SIFT_create()

img1 = cv2.imread("/home/egli/.gemini/antigravity/brain/c389e7ca-d9dd-451a-9838-cf1dec287928/scratch/extracted_frames/frame_000.png", cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread("/home/egli/.gemini/antigravity/brain/c389e7ca-d9dd-451a-9838-cf1dec287928/scratch/extracted_frames/frame_043.png", cv2.IMREAD_GRAYSCALE)

kp1, des1 = sift.detectAndCompute(img1, mask=analysis_mask)
kp2, des2 = sift.detectAndCompute(img2, mask=analysis_mask)

print(f"Frame 000: found {len(kp1)} keypoints")
print(f"Frame 043: found {len(kp2)} keypoints")

bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
matches = bf.match(des1, des2)
print(f"Found {len(matches)} initial matches")

# Extract coordinates of matched keypoints
src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

# Estimate transformation (affine partial: translation + rotation + scaling)
M, inliers = cv2.estimateAffinePartial2D(src_pts, dst_pts, method=cv2.RANSAC, ransacReprojThreshold=3.0)

if M is not None:
    dx = M[0, 2]
    dy = M[1, 2]
    scale = np.sqrt(M[0, 0]**2 + M[0, 1]**2)
    angle = np.arctan2(M[1, 0], M[0, 0]) * 180 / np.pi
    num_inliers = np.sum(inliers)
    print(f"Transformation: dx={dx:.2f}, dy={dy:.2f}, scale={scale:.4f}, angle={angle:.2f} degrees")
    print(f"RANSAC Inliers: {num_inliers} / {len(matches)} ({num_inliers/len(matches)*100:.1f}%)")
else:
    print("Failed to estimate transformation")
