import cv2

video_path = "/home/egli/development/uapvideos/clip.mp4"
cap = cv2.VideoCapture(video_path)

fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print(f"Exact Video FPS: {fps}")
print(f"Total Frames: {total_frames}")

# Calculate frame number for 8.1 seconds
# t = 8.1s
target_time = 8.1
frame_number = int(round(target_time * fps))
print(f"Calculated frame number for {target_time}s: {frame_number}")

# Set video position to frame_number
cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
ret, frame = cap.read()

if ret:
    output_path = "/home/egli/development/uapvideos/camera_movement_analysis/frame_8.1s.png"
    cv2.imwrite(output_path, frame)
    print(f"Successfully extracted frame {frame_number} and saved to {output_path}")
else:
    print(f"Failed to read frame {frame_number}")

cap.release()
