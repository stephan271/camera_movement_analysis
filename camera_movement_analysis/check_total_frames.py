import cv2

video_path = "/home/egli/development/uapvideos/clip.mp4"
cap = cv2.VideoCapture(video_path)

count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    count += 1

print(f"Actual readable frames in clip.mp4: {count}")
cap.release()
