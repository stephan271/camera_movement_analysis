import os
import shutil

src_dir = "/home/egli/.gemini/antigravity/brain/c389e7ca-d9dd-451a-9838-cf1dec287928"
dest_dir = "/home/egli/development/uapvideos/camera_movement_analysis"

# Copy comparison frames
os.makedirs(dest_dir, exist_ok=True)
shutil.copy2(os.path.join(src_dir, "scratch/pan_frames/pan_frame_282.png"), os.path.join(dest_dir, "pan_frame_282.png"))
shutil.copy2(os.path.join(src_dir, "scratch/pan_frames/pan_frame_289.png"), os.path.join(dest_dir, "pan_frame_289.png"))

# Read report file
report_path = os.path.join(dest_dir, "camera_movement_report.md")
with open(report_path, "r") as f:
    content = f.read()

# Replace absolute paths with relative ones
content = content.replace(
    "/home/egli/.gemini/antigravity/brain/c389e7ca-d9dd-451a-9838-cf1dec287928/scratch/camera_movement_perfect_plot.png",
    "./camera_movement_perfect_plot.png"
)
content = content.replace(
    "/home/egli/.gemini/antigravity/brain/c389e7ca-d9dd-451a-9838-cf1dec287928/scratch/camera_movement_perfect.csv",
    "./camera_movement_perfect.csv"
)
content = content.replace(
    "/home/egli/.gemini/antigravity/brain/c389e7ca-d9dd-451a-9838-cf1dec287928/scratch/pan_frames/pan_frame_282.png",
    "./pan_frame_282.png"
)
content = content.replace(
    "/home/egli/.gemini/antigravity/brain/c389e7ca-d9dd-451a-9838-cf1dec287928/scratch/pan_frames/pan_frame_289.png",
    "./pan_frame_289.png"
)

with open(report_path, "w") as f:
    f.write(content)

print("Comparison frames copied and report relative paths updated.")
