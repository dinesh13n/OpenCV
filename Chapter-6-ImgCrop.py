import cv2
import os
import numpy as np


img = cv2.imread(os.path.join(os.getcwd(),"Data","AADYA-NAIK.jpg"))
width, height = 90,114
pt1 = np.float32([[90,95],[90,114],[161,95],[160,114]])
pt2 = np.float32([[0,0],[width,0],[0,height],[width,height]])

matrix = cv2.getPerspectiveTransform(pt1,pt2)
imgOutput = cv2.warpPerspective(img,matrix,(width,height))

cv2.imshow("Original Image",img)
cv2.imshow("Image", imgOutput)
cv2.waitKey(0)