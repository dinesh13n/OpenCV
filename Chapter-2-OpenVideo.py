import cv2
import os

# Read existing video
#video = cv2.VideoCapture(os.path.join(os.getcwd(),"Data","Aadya-Video.mp4"))

# Capture video from the webcam or other source
video = cv2.VideoCapture(0)
video.set(3,680) # 3 - Width
video.set(4,480) # 4 - Height
video.set(10,100) # 10 - Brightness


while True:
    Success, img = video.read()
    cv2.imshow("Video",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
