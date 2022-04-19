import cv2
import os
import numpy as np


img = cv2.imread(os.path.join(os.getcwd(),"Data","AADYA-NAIK.jpg"))
imgCropped = img[5:200,0:300]

cv2.imshow("Original Image",img)
cv2.imshow("Cropped Image",imgCropped)
cv2.waitKey(0)
