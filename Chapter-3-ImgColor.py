import cv2
import os
import numpy as np

kernel = np.ones((5,5),np.uint8)

img = cv2.imread(os.path.join(os.getcwd(),"Data","AADYA-NAIK.jpg"))

imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
imgBlr = cv2.GaussianBlur(imgGray,(7,7),0)
imgCanny = cv2.Canny(img,100,100) # Edges of image
imgDialation = cv2.dilate(imgCanny,kernel,iterations=1) # Increage the eadge size
imgErode = cv2.erode(imgDialation,kernel,iterations=1)

cv2.imshow('Gray Image',imgGray)
cv2.imshow('Blur Image',imgBlr)
cv2.imshow('Canny Image',imgCanny)
cv2.imshow('Dialation Image',imgDialation)
cv2.imshow('Erode Image',imgErode)

cv2.waitKey(0)