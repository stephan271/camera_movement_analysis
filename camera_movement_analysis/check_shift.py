import cv2
import numpy as np

img368 = cv2.imread("/home/egli/.gemini/antigravity/brain/c389e7ca-d9dd-451a-9838-cf1dec287928/scratch/transition_frames/frame_368.png", cv2.IMREAD_GRAYSCALE)
img370 = cv2.imread("/home/egli/.gemini/antigravity/brain/c389e7ca-d9dd-451a-9838-cf1dec287928/scratch/transition_frames/frame_370.png", cv2.IMREAD_GRAYSCALE)

# Crop a region in the middle that does not have black boxes or HUD
# Let's crop x from 400 to 800, y from 300 to 500
crop368 = img368[300:500, 400:800]
crop370 = img370[300:500, 400:800]

# Compute correlation or SSD at different shifts
min_ssd = float('inf')
best_shift = (0, 0)

for dy in range(-25, 26):
    for dx in range(-25, 26):
        # Shift crop368 by (dx, dy) and compare with crop370
        # To avoid boundary issues, we crop a smaller sub-region
        y1, y2 = 50, 150
        x1, x2 = 50, 350
        
        ref = crop370[y1:y2, x1:x2]
        shifted = crop368[y1+dy:y2+dy, x1+dx:x2+dx]
        
        ssd = np.sum((ref.astype(np.float32) - shifted.astype(np.float32))**2)
        if ssd < min_ssd:
            min_ssd = ssd
            best_shift = (dx, dy)

print(f"Direct pixel search best shift (368 to 370): dx={best_shift[0]}, dy={best_shift[1]} with SSD={min_ssd:.1f}")

# Also compare SSD at 0 shift vs best shift
ssd_zero = np.sum((crop370[50:150, 50:350].astype(np.float32) - crop368[50:150, 50:350].astype(np.float32))**2)
print(f"SSD at zero shift: {ssd_zero:.1f}")
