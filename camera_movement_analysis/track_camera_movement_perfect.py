import cv2
import numpy as np
import matplotlib.pyplot as plt

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

# 1. Refined Static Mask with dilation and safe active area
static_mask = std_img < 5.0
kernel = np.ones((25, 25), np.uint8)
dilated_mask = cv2.dilate(static_mask.astype(np.uint8) * 255, kernel, iterations=1)
analysis_mask = cv2.bitwise_not(dilated_mask)

h, w = analysis_mask.shape
safe_mask = np.zeros_like(analysis_mask)
safe_mask[100:620, 260:900] = 255
analysis_mask = cv2.bitwise_and(analysis_mask, safe_mask)
cv2.circle(analysis_mask, (w//2, h//2), 150, 0, -1)

# 2. Sequential Tracking with CLAHE
clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))

cap = cv2.VideoCapture(video_path)
ret, prev_frame = cap.read()
prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
prev_equalized = clahe.apply(prev_gray)

lk_params = dict(winSize=(31, 31),
                 maxLevel=4,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 40, 0.01))

feature_params = dict(maxCorners=500,
                      qualityLevel=0.01,
                      minDistance=8,
                      blockSize=7)

raw_displacements = []
frame_idx = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame_idx += 1
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    equalized = clahe.apply(gray)
    
    p0 = cv2.goodFeaturesToTrack(prev_equalized, mask=analysis_mask, **feature_params)
    
    dx, dy, scale, angle = 0.0, 0.0, 1.0, 0.0
    num_inliers = 0
    valid = False
    
    if p0 is not None and len(p0) > 10:
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
                # We classify as valid if RANSAC inlier count is high enough
                if num_inliers >= 15:
                    valid = True
                    
    raw_displacements.append({
        'frame': frame_idx,
        'dx': dx,
        'dy': dy,
        'scale': scale,
        'angle': angle,
        'inliers': num_inliers,
        'valid': valid
    })
    
    prev_equalized = equalized.copy()

cap.release()

# 3. Clean and Interpolate Anomalies
clean_displacements = []
n = len(raw_displacements)

for i in range(n):
    curr = raw_displacements[i]
    if not curr['valid']:
        # Find nearest valid frames before and after
        prev_valid = None
        for j in range(i - 1, -1, -1):
            if raw_displacements[j]['valid']:
                prev_valid = raw_displacements[j]
                break
        next_valid = None
        for j in range(i + 1, n):
            if raw_displacements[j]['valid']:
                next_valid = raw_displacements[j]
                break
        
        # Interpolate
        if prev_valid is not None and next_valid is not None:
            # Linear interpolation
            weight = (i - prev_valid['frame'] + 1) / (next_valid['frame'] - prev_valid['frame'])
            dx = prev_valid['dx'] + weight * (next_valid['dx'] - prev_valid['dx'])
            dy = prev_valid['dy'] + weight * (next_valid['dy'] - prev_valid['dy'])
            scale = prev_valid['scale'] + weight * (next_valid['scale'] - prev_valid['scale'])
            angle = prev_valid['angle'] + weight * (next_valid['angle'] - prev_valid['angle'])
        elif prev_valid is not None:
            dx, dy, scale, angle = prev_valid['dx'], prev_valid['dy'], prev_valid['scale'], prev_valid['angle']
        elif next_valid is not None:
            dx, dy, scale, angle = next_valid['dx'], next_valid['dy'], next_valid['scale'], next_valid['angle']
        else:
            dx, dy, scale, angle = 0.0, 0.0, 1.0, 0.0
            
        print(f"Interpolated frame {curr['frame']}: dx={dx:.4f}, dy={dy:.4f}")
        clean_displacements.append({
            'frame': curr['frame'],
            'dx': dx,
            'dy': dy,
            'scale': scale,
            'angle': angle,
            'inliers': curr['inliers'],
            'interpolated': True
        })
    else:
        clean_displacements.append({
            'frame': curr['frame'],
            'dx': curr['dx'],
            'dy': curr['dy'],
            'scale': curr['scale'],
            'angle': curr['angle'],
            'inliers': curr['inliers'],
            'interpolated': False
        })

# 4. Accumulate clean trajectory
cum_x = 0.0
cum_y = 0.0
cum_scale = 1.0
cum_angle = 0.0

final_data = []
final_data.append((0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0, 0))

for item in clean_displacements:
    dx = item['dx']
    dy = item['dy']
    scale = item['scale']
    angle = item['angle']
    
    cum_x += dx
    cum_y += dy
    cum_scale *= scale
    cum_angle += angle
    
    final_data.append((
        item['frame'],
        dx, dy, scale, angle,
        cum_x, cum_y, cum_scale, cum_angle,
        item['inliers'],
        1 if item['interpolated'] else 0
    ))

# Save perfect trajectory to CSV
output_csv = "/home/egli/.gemini/antigravity/brain/c389e7ca-d9dd-451a-9838-cf1dec287928/scratch/camera_movement_perfect.csv"
header = "frame,dx,dy,scale,angle,cum_x,cum_y,cum_scale,cum_angle,inliers,interpolated"
np.savetxt(output_csv, final_data, delimiter=",", header=header, comments="", fmt="%d,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%d,%d")
print(f"Saved perfect CSV trajectory to {output_csv}")

# Generate beautiful plots
data = np.array(final_data)
frames = data[:, 0]
cum_xs = data[:, 5]
cum_ys = data[:, 6]
cum_scales = data[:, 7]
cum_angles = data[:, 8]

# Style plot beautifully (premium dark aesthetic)
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 12), sharex=True)

# 1. Panning & Tilting
ax1.plot(frames, cum_xs, label="Horizontal Pan (dx)", color="#1f77b4", linewidth=2.5)
ax1.plot(frames, cum_ys, label="Vertical Tilt (dy)", color="#2ca02c", linewidth=2.5)
ax1.axvline(x=280, color="#d62728", linestyle="--", alpha=0.7, label="Sensor Gain Transition (Frame 280)")
ax1.set_ylabel("Displacement (pixels)", fontsize=12, fontweight='bold')
ax1.set_title("Precise Camera Background Displacement (Cumulative)", fontsize=14, fontweight='bold', pad=15)
ax1.grid(True, linestyle=":", alpha=0.6)
ax1.legend(fontsize=10, loc="upper left")

# 2. Zoom (Scale)
ax2.plot(frames, cum_scales, label="Zoom Factor (Scale)", color="#ff7f0e", linewidth=2.5)
ax2.axvline(x=280, color="#d62728", linestyle="--", alpha=0.7)
ax2.set_ylabel("Scale Factor", fontsize=12, fontweight='bold')
ax2.set_title("Camera Zoom (Cumulative Scale)", fontsize=14, fontweight='bold', pad=15)
ax2.grid(True, linestyle=":", alpha=0.6)
ax2.legend(fontsize=10, loc="upper left")

# 3. Roll (Angle)
ax3.plot(frames, cum_angles, label="Roll (Rotation Angle)", color="#9467bd", linewidth=2.5)
ax3.axvline(x=280, color="#d62728", linestyle="--", alpha=0.7)
ax3.set_xlabel("Frame Number", fontsize=12, fontweight='bold')
ax3.set_ylabel("Angle (degrees)", fontsize=12, fontweight='bold')
ax3.set_title("Camera Roll (Cumulative Rotation)", fontsize=14, fontweight='bold', pad=15)
ax3.grid(True, linestyle=":", alpha=0.6)
ax3.legend(fontsize=10, loc="upper left")

plt.tight_layout()
plot_path = "/home/egli/.gemini/antigravity/brain/c389e7ca-d9dd-451a-9838-cf1dec287928/scratch/camera_movement_perfect_plot.png"
plt.savefig(plot_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"Saved perfect trajectory plot to {plot_path}")
