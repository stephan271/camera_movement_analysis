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

feature_params = dict(maxCorners=400,
                      qualityLevel=0.01,
                      minDistance=10,
                      blockSize=7)

lk_params = dict(winSize=(21, 21),
                 maxLevel=3,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01))

p0_mem = cv2.goodFeaturesToTrack(mem368, mask=mask, **feature_params)
p1_mem, st_mem, err_mem = cv2.calcOpticalFlowPyrLK(mem368, mem369, p0_mem, None, **lk_params)

p0_png = cv2.goodFeaturesToTrack(png368, mask=mask, **feature_params)
p1_png, st_png, err_png = cv2.calcOpticalFlowPyrLK(png368, png369, p0_png, None, **lk_params)

# We want to find a corner that is exactly identical in p0_mem and p0_png
p0_mem_flat = p0_mem.squeeze()
p0_png_flat = p0_png.squeeze()

found = 0
for i, pt_mem in enumerate(p0_mem_flat):
    # Find matching point in p0_png
    dists = np.sqrt(np.sum((p0_png_flat - pt_mem)**2, axis=1))
    j = np.argmin(dists)
    if dists[j] < 0.1:
        # Check if they successfully tracked in both
        if st_mem[i] == 1 and st_png[j] == 1:
            tracked_mem = p1_mem[i].squeeze()
            tracked_png = p1_png[j].squeeze()
            
            shift_mem = tracked_mem - pt_mem
            shift_png = tracked_png - pt_mem
            
            print(f"Corner coordinate: {pt_mem.tolist()}")
            print(f"  Tracked in mem to: {tracked_mem.tolist()}, shift={shift_mem.tolist()}")
            print(f"  Tracked in png to: {tracked_png.tolist()}, shift={shift_png.tolist()}")
            
            # Let's inspect a 5x5 pixel region around this corner in mem369 and png369
            cx, cy = int(pt_mem[0]), int(pt_mem[1])
            patch_mem = mem369[cy-2:cy+3, cx-2:cx+3]
            patch_png = png369[cy-2:cy+3, cx-2:cx+3]
            print(f"  patch mem:\n{patch_mem}")
            print(f"  patch png:\n{patch_png}")
            
            found += 1
            if found >= 2:
                break
