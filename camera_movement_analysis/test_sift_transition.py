import cv2
import numpy as np

# Load static mask and dilate it
static_mask_img = cv2.imread("/home/egli/.gemini/antigravity/brain/c389e7ca-d9dd-451a-9838-cf1dec287928/scratch/static_mask.png", cv2.IMREAD_GRAYSCALE)
kernel = np.ones((15, 15), np.uint8)
dilated_mask = cv2.dilate(static_mask_img, kernel, iterations=1)
analysis_mask = cv2.bitwise_not(dilated_mask)
h, w = analysis_mask.shape
cv2.circle(analysis_mask, (w//2, h//2), 120, 0, -1)

img1 = cv2.imread("/home/egli/.gemini/antigravity/brain/c389e7ca-d9dd-451a-9838-cf1dec287928/scratch/transition_frames/frame_279.png", cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread("/home/egli/.gemini/antigravity/brain/c389e7ca-d9dd-451a-9838-cf1dec287928/scratch/transition_frames/frame_280.png", cv2.IMREAD_GRAYSCALE)

sift = cv2.SIFT_create()
kp1, des1 = sift.detectAndCompute(img1, mask=analysis_mask)
kp2, des2 = sift.detectAndCompute(img2, mask=analysis_mask)

print(f"Frame 279 SIFT keypoints: {len(kp1)}")
print(f"Frame 280 SIFT keypoints: {len(kp2)}")

# Use FLANN or BF matcher with Lowe's ratio test
bf = cv2.BFMatcher()
matches_all = bf.knnMatch(des1, des2, k=2)

good_matches = []
for m, n in matches_all:
    if m.distance < 0.75 * n.distance:
        good_matches.append(m)

print(f"Good matches with Lowe's ratio test: {len(good_matches)}")

if len(good_matches) > 4:
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    
    M, inliers = cv2.estimateAffinePartial2D(src_pts, dst_pts, method=cv2.RANSAC, ransacReprojThreshold=3.0)
    
    if M is not None:
        dx = M[0, 2]
        dy = M[1, 2]
        scale = np.sqrt(M[0, 0]**2 + M[0, 1]**2)
        angle = np.arctan2(M[1, 0], M[0, 0]) * 180 / np.pi
        print(f"SIFT TRANSITION: dx={dx:.4f}, dy={dy:.4f}, scale={scale:.5f}, angle={angle:.4f} degrees")
        print(f"Inliers: {np.sum(inliers)} / {len(good_matches)}")
    else:
        print("SIFT Affine estimation failed")
else:
    print("Not enough good matches")
