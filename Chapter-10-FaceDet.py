import cv2
import os

faceCascade = cv2.CascadeClassifier(os.path.join(os.getcwd(),"Data","opencv_haarcascade_frontalface_default.xml"))

img = cv2.imread(os.path.join(os.getcwd(),"Data","AADYA-NAIK.jpg"))
imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

faces = faceCascade.detectMultiScale(imgGray,1.1,4)

for x,y,w,h in faces:
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

cv2.imshow("Result",img)
cv2.waitKey(0)
