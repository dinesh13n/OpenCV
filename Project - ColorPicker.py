import cv2
import numpy as np

video = cv2.VideoCapture(0)
video.set(3,400)
video.set(4,400)
video.set(10,150)

myColors = [[0,92,119,4,176,255],[0,90,170,173,149,255]]
myColorValues = [[0,0,255],[51,153,255]] # BGR Choose the color based on the object color
myPoints = [] # (x, y, mycolorid)

def findcolor(img, myColors,myColorValues):
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    newPoints = []
    for cnt,color in enumerate(myColors):
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV,lower,upper)
        x,y = getContours(mask)
        cv2.circle(imResult,(x,y),10,myColorValues[cnt],cv2.FILLED)
        if x!=0 and y!=0:
            newPoints.append([x,y,cnt])
        #cv2.imshow(str(color[1]),mask)
    return newPoints

def getContours(img):
    contours, hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            #cv2.drawContours(imResult,cnt,-1,(255,0,0),2)
            peri = cv2.arcLength(cnt,True)
            #print(peri)
            approx = cv2.approxPolyDP(cnt,0.04*peri,True)
            x, y, w, h = cv2.boundingRect(approx)
    return x+w//2,y

def drawOnCanvas(myPoints, myColorValues):
    for point in myPoints:
        cv2.circle(imResult,(point[0],point[1]),10,myColorValues[point[2]],cv2.FILLED)

while True:
    _, img = video.read()
    imResult = img.copy()
    newPoints = findcolor(img,myColors,myColorValues)
    if len(newPoints) >0:
        for newP in newPoints:
            myPoints.append(newP)
        if len(myPoints)>0:
            drawOnCanvas(myPoints,myColorValues)
    #cv2.imshow("Image",img)
    cv2.imshow("Image Result",imResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break