from djitellopy import tello
import KeyPressModule as kpm
import cv2
import time

kpm.init()
drone = tello.Tello()
drone.connect()
print(drone.get_battery())
global img
drone.streamon()

def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50

    if kpm.getKey("LEFT"):
        lr = -speed
    elif kpm.getKey("RIGHT"):
        lr = speed

    if kpm.getKey("UP"):
        fb = speed
    elif kpm.getKey("DOWN"):
        fb = -speed

    if kpm.getKey("w"):
        ud = speed
    elif kpm.getKey("s"):
        ud = -speed

    if kpm.getKey("a"):
        yv = -speed
    elif kpm.getKey("d"):
        yv = speed

    if kpm.getKey('q'): drone.land(); time.sleep(3)

    if kpm.getKey('e'):
        drone.takeoff()

    if kpm.getKey('z'):
        cv2.imwrite(f'Resources/Images/{time.time()}.jpeg', img)
        time.sleep(0.3)

    return lr, fb, ud, yv


while True:
    vals =getKeyboardInput()
    drone.send_rc_control(vals[0],vals[1],vals[2],vals[3])
    img = drone.get_frame_read().frame
    #img = cv2.resize(img, (360, 240))
    cv2.imshow("Image", img)
    cv2.waitKey(1)