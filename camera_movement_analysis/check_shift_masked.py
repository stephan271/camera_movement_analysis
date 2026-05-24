import cv2
import numpy as np

img368 = cv2.imread("/home/egli/.gemini/antigravity/brain/c389e7ca-d9dd-451a-9838-cf1dec287928/scratch/transition_frames/frame_368.png", cv2.IMREAD_GRAYSCALE)
img370 = cv2.imread("/home/egli/.gemini/antigravity/brain/c389e7ca-d9dd-451a-9838-cf1dec287928/scratch/transition_frames/frame_370.png", cv2.IMREAD_GRAYSCALE)

# Load analysis mask (255 inside background, 0 inside static overlays)
mask = cv2.imread("/home/egli/.gemini/antigravity/brain/c389e7ca-d9dd-451a-9838-cf1dec287928/scratch/analysis_mask.png", cv2.IMREAD_GRAYSCALE)
mask_bin = (mask > 127).astype(np.float32)

best_shift = (0, 0)
min_ssd = float('inf')

# We'll search in a larger range, e.g., -40 to 40
for dy in range(-40, 41):
    for dx in range(-40, 41):
        # We want to shift img368 by (dx, dy) and compare it to img370.
        # To handle shifts properly, we translate img368 using an affine warp
        T = np.float32([[1, 0, dx], [0, 1, dy]])
        shifted_img = cv2.warpAffine(img368, T, (img368.shape[1], img368.shape[0]))
        
        # We only compare in the active background of BOTH the reference (img370) and shifted mask
        shifted_mask = cv2.warpAffine(mask_bin, T, (mask_bin.shape[1], mask_bin.shape[0]))
        combined_mask = mask_bin * shifted_mask
        
        # Compute SSD only on the active pixels
        diff = (img370.astype(np.float32) - shifted_img.astype(np.float32)) * combined_mask
        num_pixels = np.sum(combined_mask)
        if num_pixels > 10000:
            ssd = np.sum(diff**2) / num_pixels # normalized SSD
            if ssd < min_ssd:
                min_ssd = ssd
                best_shift = (dx, dy)

print(f"Masked search best shift (368 to 370): dx={best_shift[0]}, dy={best_shift[1]} with NormSSD={min_ssd:.3f}")

# Compare to zero shift
diff_zero = (img370.astype(np.float32) - img368.astype(np.float32)) * mask_bin
num_pixels_zero = np.sum(mask_bin)
ssd_zero = np.sum(diff_zero**2) / num_pixels_zero
print(f"NormSSD at zero shift: {ssd_zero:.3f}")
