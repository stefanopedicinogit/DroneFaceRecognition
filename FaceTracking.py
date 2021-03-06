import cv2
from djitellopy import tello
import numpy as np
import time

drone = tello.Tello()
drone.connect()
print(drone.get_battery())

drone.takeoff()
drone.send_rc_control(0,0,0,0)
time.sleep(1)
drone.send_rc_control(0,0,8,0)
time.sleep(1)

drone.streamon()

fbRange = [6200, 6800]
pid = [0.4, 0.4, 0]
pError = 0
w, h = (360, 240)

def findFace(img):
    faceCascade = cv2.CascadeClassifier('Resources/haarcascade_frontalface_default.xml')
    imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGrey, 1.2, 8)

    myFaceListC = []
    myFaceListArea = []

    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,255), 2)
        cx = x + w //2
        cy = y + h //2
        area = w * h
        cv2.circle(img,(cx,cy),5 ,(0,255,0), cv2.FILLED)
        myFaceListC.append([cx, cy])
        myFaceListArea.append(area)
    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i], myFaceListArea[i]]
    else:
        return img,[[0,0], 0]

def trackFace(info, w, pid, pError):
    area = info[1]
    x, y = info[0]
    fb = 0
    error = x - w //2
    speed = pid[0] * error + pid[1] * (error - pError)

    speed = int(np.clip(speed, - 50, 50))

    if area > fbRange[0] and area <fbRange[1]:
        fb = 0
    if area > fbRange[1]:
        fb = -15
    elif area < fbRange[0] and area != 0:
        fb = 15

    if x  ==0:
        speed = 0
        error = 0

    #print(speed, fb)


    drone.send_rc_control(0, fb, 0, speed)
    return error



#capture = cv2.VideoCapture(0)
while True:
    #_, img = capture.read()
    img = drone.get_frame_read().frame
    img = cv2.resize(img, (360,240))
    img, info = findFace(img)
    pError = trackFace(info, w, pid, pError)
    #print('Center', info[0], 'Area', info[1])
    cv2.imshow('Output', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        drone.land()
        break
