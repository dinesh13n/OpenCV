import cv2
import os

img = cv2.imread(os.path.join(os.getcwd(),"Data","3.jpg"))
cv2.imshow("image",img)
cv2.waitKey(0)