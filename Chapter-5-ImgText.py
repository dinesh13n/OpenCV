import cv2
import os
import numpy as np

img = np.zeros((512,512,3),np.uint8)

cv2.line(img,(0,0),(img.shape[1],img.shape[0]),(255,0,0),1)
cv2.rectangle(img,(0,0),(200,200),(0,0,255),2)
cv2.circle(img,(256,256),50,(255,255,200),2)
cv2.putText(img," Dinesh Naik ",(150,330),cv2.FONT_ITALIC,1,(255,225,0),1)
cv2.imshow("Image",img)

cv2.waitKey(0)