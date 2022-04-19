# Capture video from the webcam or other source
import cv2
import numpy as np


def stackImages(imgArray,scale,lables=[]):
    sizeW= imgArray[0][0].shape[1]
    sizeH = imgArray[0][0].shape[0]
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                imgArray[x][y] = cv2.resize(imgArray[x][y], (sizeW, sizeH), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
            hor_con[x] = np.concatenate(imgArray[x])
        ver = np.vstack(hor)
        ver_con = np.concatenate(hor)
    else:
        for x in range(0, rows):
            imgArray[x] = cv2.resize(imgArray[x], (sizeW, sizeH), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        hor_con= np.concatenate(imgArray)
        ver = hor
    if len(lables) != 0:
        eachImgWidth= int(ver.shape[1] / cols)
        eachImgHeight = int(ver.shape[0] / rows)
        print(eachImgHeight)
        for d in range(0, rows):
            for c in range (0,cols):
                cv2.rectangle(ver,(c*eachImgWidth,eachImgHeight*d),(c*eachImgWidth+len(lables[d][c])*13+27,30+eachImgHeight*d),(255,255,255),cv2.FILLED)
                cv2.putText(ver,lables[d][c],(eachImgWidth*c+10,eachImgHeight*d+20),cv2.FONT_HERSHEY_COMPLEX,0.7,(255,0,255),2)
    return ver

#################
imgWidth = 680
imgHeight = 480
#################

video = cv2.VideoCapture(0)
video.set(3,imgWidth) # 3 - Width
video.set(4,imgHeight) # 4 - Height
video.set(10,150) # 10 - Brightness

def preProcessing(img):
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(5,5),1)
    imgCanny = cv2.Canny(imgBlur,200,200)
    kernal = np.ones((5,5))
    imgDial = cv2.dilate(imgCanny,kernal,iterations=2)
    imgThres = cv2.erode(imgDial,kernal,iterations=2)
    return imgThres

def getContours(img):
    biggest = np.array([])
    maxArea = 0
    contours, hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        print(area)
        if area > 50:
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            print ("approx -- ",len(approx))
            if area >maxArea and len(approx) == 4:
                biggest = approx
                maxArea = area
                print ("biggest area -- : ", biggest)
    cv2.drawContours(imgContour, biggest, -1, (255, 0, 0), 2)
    return biggest

def reorder(myPoints):
    myPoints = myPoints.reshape((4,2))
    myPointsNew = np.zeros((4,1,2),np.int32)
    add = myPoints.sum(1)
    myPointsNew[0] = myPointsNew[np.argmin(add)]
    myPointsNew[3] = myPointsNew[np.argmax(add)]
    diff = np.diff(myPoints,axis=1)
    myPointsNew[1] = myPointsNew[np.argmin(diff)]
    myPointsNew[2] = myPointsNew[np.argmax(diff)]
    return myPointsNew

def getWarp(img,biggest):
    biggest = reorder(biggest)
    pt1 = np.float32(biggest)
    pt2 = np.float32([[0, 0], [imgWidth, 0], [0, imgHeight], [imgWidth, imgHeight]])
    matrix = cv2.getPerspectiveTransform(pt1, pt2)
    imgOutput = cv2.warpPerspective(img, matrix, (imgWidth, imgHeight))

    imgCropped = imgOutput[20:imgOutput.shape[0]-20, 20:imgOutput.shape[1]-20]
    imgCropped = cv2.resize(imgCropped,(imgWidth, imgHeight))

    return imgCropped

while True:
    Success, img = video.read()
    img = cv2.resize(img,(imgWidth,imgHeight))
    imgContour = img.copy()
    imgThres = preProcessing(img)
    biggest = getContours(imgThres)
    if biggest.size != 0:
        imgWarped = getWarp(img,biggest)
        imgArray = ([img, imgThres],[imgContour,imgWarped])
    else:
        imgArray = ([img, imgThres], [img, img])
    imgStacked = stackImages(imgArray,0.6)
    cv2.imshow("Result",imgStacked)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break