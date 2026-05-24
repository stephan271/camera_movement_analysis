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

# Verify image identities
print(f"mem368 vs png368 max diff: {np.max(np.abs(mem368.astype(np.float32) - png368.astype(np.float32)))}")
print(f"mem369 vs png369 max diff: {np.max(np.abs(mem369.astype(np.float32) - png369.astype(np.float32)))}")

# Compare corners
feature_params = dict(maxCorners=400,
                      qualityLevel=0.01,
                      minDistance=10,
                      blockSize=7)

p0_mem = cv2.goodFeaturesToTrack(mem368, mask=mask, **feature_params)
p0_png = cv2.goodFeaturesToTrack(png368, mask=mask, **feature_params)

print(f"p0_mem shape: {p0_mem.shape}, p0_png shape: {p0_png.shape}")

# Print first 5 corners of both
print("\nFirst 5 corners p0_mem:")
print(p0_mem[:5].squeeze())

print("\nFirst 5 corners p0_png:")
print(p0_png[:5].squeeze())

# Check if the mask is exactly identical to png368's loaded mask
# Wait! In cv2.goodFeaturesToTrack, does png368 find the exact same corners as mem368?
# Let's test if we detect corners on png368 using the same mask
p0_png_test = cv2.goodFeaturesToTrack(png368, mask=mask, **feature_params)
print(f"\np0_png vs p0_png_test max diff: {np.max(np.abs(p0_png - p0_png_test))}")

# Check if mem368 and png368 find different corners because of minor pixel differences
p0_mem_flat = p0_mem.squeeze()
p0_png_flat = p0_png.squeeze()

# Let's count how many corners are exactly identical (to within 0.1 pixel)
matching_corners = 0
for pt_mem in p0_mem_flat:
    # Find nearest point in p0_png
    dists = np.sqrt(np.sum((p0_png_flat - pt_mem)**2, axis=1))
    if np.min(dists) < 0.1:
        matching_corners += 1

print(f"\nNumber of matching corners (dist < 0.1): {matching_corners} / 400")
