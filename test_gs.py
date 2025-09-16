import cv2
import os
import matplotlib.pyplot as plt

output_dir = "saved_videos"
os.makedirs(output_dir, exist_ok=True)

udp_url = "udp://127.0.0.1:5000"

cap = cv2.VideoCapture(udp_url, cv2.CAP_FFMPEG)

if not cap.isOpened():
    print("Không thể mở stream UDP")
    exit(1)

frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Không còn frame nào hoặc lỗi stream")
        break
    

    frame_path = os.path.join(output_dir, f"frame_{frame_count:05d}.jpg")
    cv2.imwrite(frame_path, frame)
    frame_count += 1

    plt.imshow(frame)
plt.show()

