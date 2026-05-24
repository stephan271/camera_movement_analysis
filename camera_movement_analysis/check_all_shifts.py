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

shifts_mem = []
for i in range(len(p0_mem)):
    if st_mem[i] == 1:
        shifts_mem.append(p1_mem[i].squeeze() - p0_mem[i].squeeze())
shifts_mem = np.array(shifts_mem)

shifts_png = []
for i in range(len(p0_png)):
    if st_png[i] == 1:
        shifts_png.append(p1_png[i].squeeze() - p0_png[i].squeeze())
shifts_png = np.array(shifts_png)

print("MEMORY SHIFTS DISTRIBUTION:")
print(f"Total tracked: {len(shifts_mem)}")
print(f"Mean: {np.mean(shifts_mem, axis=0)}")
print(f"Std: {np.std(shifts_mem, axis=0)}")
# Bin the horizontal shifts
hist_mem, bins_mem = np.histogram(shifts_mem[:, 0], bins=[-30, -20, -10, -5, -2, -0.5, 0.5, 2, 5, 10, 20, 30])
for b, count in zip(bins_mem[:-1], hist_mem):
    print(f"  [{b:5.1f}, {bins_mem[bins_mem.tolist().index(b)+1]:5.1f}]: {count}")

print("\nPNG SHIFTS DISTRIBUTION:")
print(f"Total tracked: {len(shifts_png)}")
print(f"Mean: {np.mean(shifts_png, axis=0)}")
print(f"Std: {np.std(shifts_png, axis=0)}")
# Bin the horizontal shifts
hist_png, bins_png = np.histogram(shifts_png[:, 0], bins=[-30, -20, -10, -5, -2, -0.5, 0.5, 2, 5, 10, 20, 30])
for b, count in zip(bins_png[:-1], hist_png):
    print(f"  [{b:5.1f}, {bins_png[bins_png.tolist().index(b)+1]:5.1f}]: {count}")
