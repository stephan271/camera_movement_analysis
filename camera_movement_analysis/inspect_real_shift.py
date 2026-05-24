import cv2
import numpy as np

img368 = cv2.imread("/home/egli/.gemini/antigravity/brain/c389e7ca-d9dd-451a-9838-cf1dec287928/scratch/sequential_frames/real_frame_368.png", cv2.IMREAD_GRAYSCALE)
img369 = cv2.imread("/home/egli/.gemini/antigravity/brain/c389e7ca-d9dd-451a-9838-cf1dec287928/scratch/sequential_frames/real_frame_369.png", cv2.IMREAD_GRAYSCALE)

# Load analysis mask
mask = cv2.imread("/home/egli/.gemini/antigravity/brain/c389e7ca-d9dd-451a-9838-cf1dec287928/scratch/analysis_mask.png", cv2.IMREAD_GRAYSCALE)
mask_bin = (mask > 127).astype(np.float32)

best_shift = (0, 0)
min_ssd = float('inf')

for dy in range(-30, 31):
    for dx in range(-30, 31):
        T = np.float32([[1, 0, dx], [0, 1, dy]])
        shifted_img = cv2.warpAffine(img368, T, (img368.shape[1], img368.shape[0]))
        shifted_mask = cv2.warpAffine(mask_bin, T, (mask_bin.shape[1], mask_bin.shape[0]))
        combined_mask = mask_bin * shifted_mask
        
        diff = (img369.astype(np.float32) - shifted_img.astype(np.float32)) * combined_mask
        num_pixels = np.sum(combined_mask)
        if num_pixels > 10000:
            ssd = np.sum(diff**2) / num_pixels
            if ssd < min_ssd:
                min_ssd = ssd
                best_shift = (dx, dy)

print(f"Masked search best shift (368 to 369): dx={best_shift[0]}, dy={best_shift[1]} with NormSSD={min_ssd:.3f}")

# Compare to zero shift
diff_zero = (img369.astype(np.float32) - img368.astype(np.float32)) * mask_bin
num_pixels_zero = np.sum(mask_bin)
ssd_zero = np.sum(diff_zero**2) / num_pixels_zero
print(f"NormSSD at zero shift: {ssd_zero:.3f}")
