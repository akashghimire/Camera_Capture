from picamera import PiCamera
from time import sleep
import numpy as np
import cv2
import os

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

interval = 5
frame = 0

camera = PiCamera()
camera.resolution = (640, 400)
camera.start_preview()
sleep(2)
path, dirs, files = next(os.walk('/home/pi/Documents/Picture/'))
img_counter = len(files)+1
time = 0
duration = 30

while True:
    
    
    path = '/home/pi/Documents/Picture/Img_{counter:04d}.jpeg'
    path =path.format(counter = img_counter) 
    camera.capture(path)
    print('Captured %s' % path)
 
    img = cv2.imread(path)
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    kernel = np.ones((3,3),np.uint8)


    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(5,5),0, cv2.BORDER_DEFAULT)
    imgCanny = cv2.Canny(img,250,250)
    imgDialation = cv2.dilate(imgCanny,kernel,iterations=1)
    imgEroded = cv2.erode(imgDialation,kernel,iterations=1)

    imgStack = stackImages(0.45,([img,imgGray,imgBlur],[imgCanny,imgDialation,imgEroded]))
    imgStackName = path.replace("Picture","S_Picture")
    cv2.imwrite(imgStackName,imgStack)
    
        

    print(img_counter)
    img_counter += 1
    time += interval
    if(time >= duration):
        break;
    
    sleep(interval)
    
    




