import cv2
import os
import numpy as np

def empty(a):
    pass



cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars",640,250)
cv2.createTrackbar("Hue Min","TrackBars",0,179,empty)
cv2.createTrackbar("Hue Max","TrackBars",170,179,empty)
cv2.createTrackbar("Sat Min","TrackBars",75,179,empty)
cv2.createTrackbar("Sat Max","TrackBars",135,179,empty)
cv2.createTrackbar("Val Min","TrackBars",4,179,empty)
cv2.createTrackbar("Val Max","TrackBars",173,255,empty)

while True:
    img = cv2.imread(os.path.join(os.getcwd(),"Data","AADYA-NAIK.jpg"))
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    h_min = cv2.getTrackbarPos("Hue Min","TrackBars")
    h_max = cv2.getTrackbarPos("Hue Max","TrackBars")
    s_min = cv2.getTrackbarPos("Sat Min","TrackBars")
    s_max = cv2.getTrackbarPos("Sat Max","TrackBars")
    v_min = cv2.getTrackbarPos("Val Min","TrackBars")
    v_max = cv2.getTrackbarPos("Val Max","TrackBars")

    lower = np.array([h_min,s_min,v_min])
    upper = np.array([h_max,s_max,v_max])
    mask = cv2.inRange(imgHSV,lower,upper)
    imgResult = cv2.bitwise_and(img,img,mask=mask)


    cv2.imshow("Original Image",img)
    cv2.imshow("HSV Image",imgHSV)
    cv2.imshow("Mask Image",mask)
    cv2.imshow("Result Image", imgResult)
    cv2.waitKey(1)