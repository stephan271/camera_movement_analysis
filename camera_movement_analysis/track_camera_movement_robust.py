import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# 1. Optimal Static Mask from standard deviation
video_path = "/home/egli/development/uapvideos/clip.mp4"
cap = cv2.VideoCapture(video_path)

frames_sample = []
count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    if count % 10 == 0:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frames_sample.append(gray)
    count += 1
cap.release()

frames_sample = np.array(frames_sample)
std_img = np.std(frames_sample, axis=0)

# Mask out static regions (std < 5.0) and dilate
static_mask = std_img < 5.0
kernel = np.ones((25, 25), np.uint8) # large dilation to cover boundaries and text thoroughly
dilated_mask = cv2.dilate(static_mask.astype(np.uint8) * 255, kernel, iterations=1)
analysis_mask = cv2.bitwise_not(dilated_mask)

h, w = analysis_mask.shape

# 2. Add Center Mask (circle of radius 150) and Border Mask (40 pixels from active region border)
# Let's find the active area bounding box.
# Active area is where we don't have the static black boxes on the left/right/top/bottom.
# The large vertical box on the left is around x=0 to x=250.
# The large box on the bottom right is around x=900 to x=1280.
# So the safe active region for tracking is x from 260 to 900, y from 100 to 600.
safe_mask = np.zeros_like(analysis_mask)
safe_mask[100:620, 260:900] = 255

# Apply safe_mask to analysis_mask
analysis_mask = cv2.bitwise_and(analysis_mask, safe_mask)

# Exclude central area
cv2.circle(analysis_mask, (w//2, h//2), 150, 0, -1)

# Save refined analysis mask
cv2.imwrite("/home/egli/.gemini/antigravity/brain/c389e7ca-d9dd-451a-9838-cf1dec287928/scratch/refined_analysis_mask.png", analysis_mask)

# 3. Setup CLAHE for contrast normalization
clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))

# 4. Sequentially process the video
cap = cv2.VideoCapture(video_path)
ret, prev_frame = cap.read()
prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
prev_equalized = clahe.apply(prev_gray)

lk_params = dict(winSize=(31, 31), # larger window size for robust tracking across larger motions
                 maxLevel=4,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 40, 0.01))

feature_params = dict(maxCorners=500,
                      qualityLevel=0.01,
                      minDistance=8,
                      blockSize=7)

frame_idx = 0
cum_x = 0.0
cum_y = 0.0
cum_scale = 1.0
cum_angle = 0.0

data_points = []
data_points.append((0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0))

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame_idx += 1
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    equalized = clahe.apply(gray)
    
    # Detect features on background in prev_equalized
    p0 = cv2.goodFeaturesToTrack(prev_equalized, mask=analysis_mask, **feature_params)
    
    if p0 is not None and len(p0) > 10:
        # Calculate optical flow
        p1, st, err = cv2.calcOpticalFlowPyrLK(prev_equalized, equalized, p0, None, **lk_params)
        
        good_new = p1[st == 1]
        good_old = p0[st == 1]
        
        if len(good_new) > 8:
            M, inliers = cv2.estimateAffinePartial2D(good_old, good_new, method=cv2.RANSAC, ransacReprojThreshold=2.0)
            
            if M is not None:
                dx = M[0, 2]
                dy = M[1, 2]
                scale = np.sqrt(M[0, 0]**2 + M[0, 1]**2)
                angle = np.arctan2(M[1, 0], M[0, 0]) * 180 / np.pi
                num_inliers = np.sum(inliers)
                
                # Check for extreme outlier motion spikes
                # Normal frame-to-frame camera motion is < 5 pixels.
                # If we get a spike, print a warning but keep tracking
                if abs(dx) > 10 or abs(dy) > 10:
                    print(f"Warning: frame {frame_idx} detected larger motion: dx={dx:.2f}, dy={dy:.2f}, inliers={num_inliers}/{len(good_new)}")
                
                cum_x += dx
                cum_y += dy
                cum_scale *= scale
                cum_angle += angle
                
                data_points.append((frame_idx, dx, dy, scale, angle, cum_x, cum_y, cum_scale, cum_angle, num_inliers))
            else:
                data_points.append((frame_idx, 0.0, 0.0, 1.0, 0.0, cum_x, cum_y, cum_scale, cum_angle, 0))
        else:
            data_points.append((frame_idx, 0.0, 0.0, 1.0, 0.0, cum_x, cum_y, cum_scale, cum_angle, 0))
    else:
        data_points.append((frame_idx, 0.0, 0.0, 1.0, 0.0, cum_x, cum_y, cum_scale, cum_angle, 0))
        
    prev_equalized = equalized.copy()

cap.release()

print(f"Robust processing completed: {frame_idx} frames.")

# Save results to a CSV file
output_csv = "/home/egli/.gemini/antigravity/brain/c389e7ca-d9dd-451a-9838-cf1dec287928/scratch/camera_movement_robust.csv"
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

plt.subplot(3, 1, 1)
plt.plot(frames, cum_xs, label="Horizontal (Pan) Shift", color="blue", linewidth=2)
plt.plot(frames, cum_ys, label="Vertical (Tilt) Shift", color="green", linewidth=2)
plt.title("Robust Camera Background Displacement (Cumulative Pixels)")
plt.xlabel("Frame")
plt.ylabel("Displacement (pixels)")
plt.grid(True)
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(frames, cum_scales, label="Zoom (Cumulative Scale)", color="red", linewidth=2)
plt.title("Robust Camera Zoom (Cumulative Scale)")
plt.xlabel("Frame")
plt.ylabel("Scale Factor")
plt.grid(True)
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(frames, cum_angles, label="Roll (Cumulative Rotation)", color="purple", linewidth=2)
plt.title("Robust Camera Roll (Cumulative Rotation Angle)")
plt.xlabel("Frame")
plt.ylabel("Angle (degrees)")
plt.grid(True)
plt.legend()

plt.tight_layout()
plot_path = "/home/egli/.gemini/antigravity/brain/c389e7ca-d9dd-451a-9838-cf1dec287928/scratch/camera_movement_robust_plot.png"
plt.savefig(plot_path, dpi=300)
plt.close()
print(f"Saved robust trajectory plots to {plot_path}")
