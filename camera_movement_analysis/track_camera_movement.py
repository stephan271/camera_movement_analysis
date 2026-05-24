import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# Load static mask and dilate it
static_mask_img = cv2.imread("/home/egli/.gemini/antigravity/brain/c389e7ca-d9dd-451a-9838-cf1dec287928/scratch/static_mask.png", cv2.IMREAD_GRAYSCALE)
kernel = np.ones((15, 15), np.uint8)
dilated_mask = cv2.dilate(static_mask_img, kernel, iterations=1)
analysis_mask = cv2.bitwise_not(dilated_mask)
h, w = analysis_mask.shape
# Mask out central area circle of radius 120
cv2.circle(analysis_mask, (w//2, h//2), 120, 0, -1)

video_path = "/home/egli/development/uapvideos/clip.mp4"
cap = cv2.VideoCapture(video_path)

ret, prev_frame = cap.read()
if not ret:
    print("Error reading first frame")
    exit()

prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

# LK flow parameters
lk_params = dict(winSize=(21, 21),
                 maxLevel=3,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01))

# Feature detection parameters
feature_params = dict(maxCorners=400,
                      qualityLevel=0.01,
                      minDistance=10,
                      blockSize=7)

frame_idx = 0
cum_x = 0.0
cum_y = 0.0
cum_scale = 1.0
cum_angle = 0.0

data_points = []
# Format: (frame_idx, dx, dy, scale, angle, cum_x, cum_y, cum_scale, cum_angle, inliers_count)
data_points.append((0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0))

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame_idx += 1
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect features on background in prev_frame
    p0 = cv2.goodFeaturesToTrack(prev_gray, mask=analysis_mask, **feature_params)
    
    if p0 is not None and len(p0) > 10:
        # Calculate optical flow
        p1, st, err = cv2.calcOpticalFlowPyrLK(prev_gray, gray, p0, None, **lk_params)
        
        # Select good points
        good_new = p1[st == 1]
        good_old = p0[st == 1]
        
        if len(good_new) > 6:
            # Estimate Affine Partial Transform (translation, rotation, scale)
            M, inliers = cv2.estimateAffinePartial2D(good_old, good_new, method=cv2.RANSAC, ransacReprojThreshold=2.0)
            
            if M is not None:
                dx = M[0, 2]
                dy = M[1, 2]
                scale = np.sqrt(M[0, 0]**2 + M[0, 1]**2)
                angle = np.arctan2(M[1, 0], M[0, 0]) * 180 / np.pi
                num_inliers = np.sum(inliers)
                
                # Update cumulative values
                cum_x += dx
                cum_y += dy
                cum_scale *= scale
                cum_angle += angle
                
                data_points.append((frame_idx, dx, dy, scale, angle, cum_x, cum_y, cum_scale, cum_angle, num_inliers))
            else:
                # If estimation failed, assume no motion
                data_points.append((frame_idx, 0.0, 0.0, 1.0, 0.0, cum_x, cum_y, cum_scale, cum_angle, 0))
        else:
            data_points.append((frame_idx, 0.0, 0.0, 1.0, 0.0, cum_x, cum_y, cum_scale, cum_angle, 0))
    else:
        data_points.append((frame_idx, 0.0, 0.0, 1.0, 0.0, cum_x, cum_y, cum_scale, cum_angle, 0))
        
    prev_gray = gray.copy()

cap.release()

print(f"Processed {frame_idx} transitions.")

# Save results to a CSV file
output_csv = "/home/egli/.gemini/antigravity/brain/c389e7ca-d9dd-451a-9838-cf1dec287928/scratch/camera_movement.csv"
header = "frame,dx,dy,scale,angle,cum_x,cum_y,cum_scale,cum_angle,inliers"
np.savetxt(output_csv, data_points, delimiter=",", header=header, comments="", fmt="%d,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%d")
print(f"Saved CSV results to {output_csv}")

# Generate Plots
data = np.array(data_points)
frames = data[:, 0]
cum_xs = data[:, 5]
cum_ys = data[:, 6]
cum_scales = data[:, 7]
cum_angles = data[:, 8]

plt.figure(figsize=(12, 10))

# Plot 1: Camera Pan/Tilt (X and Y cumulative movement)
plt.subplot(3, 1, 1)
plt.plot(frames, cum_xs, label="Horizontal (Pan) Shift", color="blue", linewidth=2)
plt.plot(frames, cum_ys, label="Vertical (Tilt) Shift", color="green", linewidth=2)
plt.title("Camera Background Displacement (Cumulative Pixels)")
plt.xlabel("Frame")
plt.ylabel("Displacement (pixels)")
plt.grid(True)
plt.legend()

# Plot 2: Camera Zoom (Cumulative Scale)
plt.subplot(3, 1, 2)
plt.plot(frames, cum_scales, label="Zoom (Cumulative Scale)", color="red", linewidth=2)
plt.title("Camera Zoom (Cumulative Scale)")
plt.xlabel("Frame")
plt.ylabel("Scale Factor")
plt.grid(True)
plt.legend()

# Plot 3: Camera Roll (Cumulative Rotation)
plt.subplot(3, 1, 3)
plt.plot(frames, cum_angles, label="Roll (Cumulative Rotation)", color="purple", linewidth=2)
plt.title("Camera Roll (Cumulative Rotation Angle)")
plt.xlabel("Frame")
plt.ylabel("Angle (degrees)")
plt.grid(True)
plt.legend()

plt.tight_layout()
plot_path = "/home/egli/.gemini/antigravity/brain/c389e7ca-d9dd-451a-9838-cf1dec287928/scratch/camera_movement_plot.png"
plt.savefig(plot_path, dpi=300)
plt.close()
print(f"Saved trajectory plots to {plot_path}")
