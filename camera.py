from emoji import *
from action import *
import keyboard

lib = lib_init()

robot = lib.CreateElectronLowLevel()
if lib.myConnect(robot):
    robotIsConnected = True
    print("Robot connected!\n")
else:
    robotIsConnected = False
    print("Connect failed!\n")

jointAngles1 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
jointAnglesEn = 0

if __name__ == '__main__':
    cap = cv.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        if robotIsConnected:
            frame = cv.resize(frame, (240, 240))
            frame = cv.cvtColor(frame, cv.COLOR_BGRA2RGB)
            frame = cv.transpose(frame)
            frame = cv.flip(frame, 0)
            lib.mySetImageSrc(robot, frame)
            lib.mySetJointAngles(robot, convert_type(jointAngles1), convert_type(jointAnglesEn))
            lib.mySync(robot)
            jointAngles2 = lib.myGetJointAngles(robot)
            if keyboard.is_pressed('q'):
                break
    if robotIsConnected:
        lib.myDisconnect(robot)
        print("File play finished, robot Disconnected!\n")
