import cv2
import os

video_path = "/home/egli/development/uapvideos/clip.mp4"
output_dir = "/home/egli/development/uapvideos/camera_movement_analysis/frame_243_sequence"
os.makedirs(output_dir, exist_ok=True)

cap = cv2.VideoCapture(video_path)

target_frame = 243
start_frame = max(0, target_frame - 5)
end_frame = min(int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1, target_frame + 5)

print(f"Extracting frames {start_frame} to {end_frame}...")

# Sequentially read and save the frames
current_frame = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    if start_frame <= current_frame <= end_frame:
        # Save as 0-indexed filename with 1-indexed VLC equivalence in name
        filename = f"frame_{current_frame:03d}_vlc_{current_frame+1:03d}.png"
        output_path = os.path.join(output_dir, filename)
        cv2.imwrite(output_path, frame)
        print(f"Saved frame {current_frame} to {output_path}")
        
    current_frame += 1

cap.release()
print("All frames extracted successfully.")
