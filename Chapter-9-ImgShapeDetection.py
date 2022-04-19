import cv2
import os
import numpy as np

img = cv2.imread(os.path.join(os.getcwd(),"Data","shapes.png"))

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

def getContours(img):
    contours, hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        print(area)
        if area > 500:
            cv2.drawContours(imgContours,cnt,-1,(255,0,0),2)
            peri = cv2.arcLength(cnt,True)
            #print(peri)
            approx = cv2.approxPolyDP(cnt,0.04*peri,True)
            print(len(approx))
            object = len(approx)
            x, y, w, h = cv2.boundingRect(approx)

            if object == 3: objectType = "Tri"
            elif object == 4:
                aspRatio = w / float(h)
                if aspRatio>0.95 and aspRatio<1.05:objectType = "Sqr"
                else:objectType='Rec'
            elif object == 5: objectType = 'Pent'
            else:objectType="Cir"

            cv2.rectangle(imgContours,(x,y),(w+x,h+y),(0,0,255),2)
            cv2.putText(imgContours,objectType,(x+(w//2)-5,y+(h//2)-5),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),1)



imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(img,(7,7),1)
imgCanny = cv2.Canny(img,50,50)
imgContours = img.copy()
getContours(imgCanny)
imgBlank = np.zeros_like(img)

imgStack = stackImages(([img,imgGray,imgBlur],[imgCanny,imgContours,imgBlank]),0.6)

cv2.imshow("Image",imgStack)
cv2.waitKey(0)

# define a function for vertically
# concatenating images of different
# widths
def vconcat_resize(img_list, interpolation
= cv2.INTER_CUBIC):
    # take minimum width
    w_min = min(img.shape[1]
                for img in img_list)

    # resizing images
    im_list_resize = [cv2.resize(img,
                                 (w_min, int(img.shape[0] * w_min / img.shape[1])),
                                 interpolation = interpolation)
                      for img in img_list]
    # return final image
    return cv2.vconcat(im_list_resize)


# define a function for horizontally
# concatenating images of different
# heights
def hconcat_resize(img_list,
                   interpolation
                   = cv2.INTER_CUBIC):
    # take minimum hights
    h_min = min(img.shape[0]
                for img in img_list)

    # image resizing
    im_list_resize = [cv2.resize(img,
                                 (int(img.shape[1] * h_min / img.shape[0]),
                                  h_min), interpolation
                                 = interpolation)
                      for img in img_list]

    # return final image
    return cv2.hconcat(im_list_resize)