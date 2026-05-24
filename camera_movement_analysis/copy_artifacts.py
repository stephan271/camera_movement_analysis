import os
import shutil

src_dir = "/home/egli/.gemini/antigravity/brain/c389e7ca-d9dd-451a-9838-cf1dec287928"
dest_dir = "/home/egli/development/uapvideos/camera_movement_analysis"

os.makedirs(dest_dir, exist_ok=True)

# List of files to copy (source path relative to src_dir, destination filename/path)
files_to_copy = [
    ("camera_movement_report.md", "camera_movement_report.md"),
    ("scratch/camera_movement_perfect.csv", "camera_movement_perfect.csv"),
    ("scratch/camera_movement_perfect_plot.png", "camera_movement_perfect_plot.png"),
    ("scratch/static_mask.png", "static_mask.png"),
    ("scratch/analysis_mask.png", "analysis_mask.png"),
    ("scratch/track_camera_movement_perfect.py", "track_camera_movement_perfect.py"),
    ("scratch/track_camera_movement_robust.py", "track_camera_movement_robust.py"),
    ("scratch/find_static_mask.py", "find_static_mask.py")
]

for src_rel, dest_rel in files_to_copy:
    src_path = os.path.join(src_dir, src_rel)
    dest_path = os.path.join(dest_dir, dest_rel)
    if os.path.exists(src_path):
        shutil.copy2(src_path, dest_path)
        print(f"Copied {src_path} -> {dest_path}")
    else:
        print(f"Source not found: {src_path}")

print("Copy completed successfully.")
