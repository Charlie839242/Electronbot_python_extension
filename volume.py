from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from action import *
import schedule
import keyboard
from ctypes import *

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))


def set_volume(robot, lib, volume):
    """
    Set system volume to given 'volume'.
    """
    pose = read_angles(robot, lib)
    ratio = (pose[0] + 15) / 30
    volume.SetMasterVolumeLevelScalar(ratio, None)


if __name__ == '__main__':
    lib = lib_init()

    robot = lib.CreateElectronLowLevel()
    if lib.myConnect(robot):
        robotIsConnected = True
        print("Robot connected!\n")
    else:
        robotIsConnected = False
        print("Connect failed!\n")

    schedule.every(0.5).seconds.do(set_volume, robot, lib, volume)

    while True:
        schedule.run_pending()
        if keyboard.is_pressed('q'):
            break

    if robotIsConnected:
        lib.myDisconnect(robot)
        print("File play finished, robot Disconnected!\n")


