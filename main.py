from emoji import *
from volume import *
from action import *
import schedule
import weather


"""
功能：
1. 每隔一个小时提醒喝水
2. 随机播放表情
3. 头部角度控制音量
4. 随时显示天气，半个小时更新一次天气
"""

lib = lib_init()

robot = lib.CreateElectronLowLevel()
if lib.myConnect(robot):
    robotIsConnected = True
    print("Robot connected!\n")
else:
    robotIsConnected = False
    print("Connect failed!\n")

emoji_name = ['angry', 'blink', 'disdain', 'excited', 'left', 'right', 'sad', 'scared']


weather.get_weather()
schedule.every(30).minutes.do(lambda: weather.get_weather())
schedule.every(60).minutes.do(lambda: play_weather(weather.current_weather, robot, lib))
schedule.every(60).minutes.do(lambda: play_img_with_action('./img/drink/Drink.png', time_to_drink, robot, lib))
schedule.every(3).seconds.do(lambda: play_random_emoji_with_weather(weather.current_weather, robot, lib))
schedule.every(0.5).seconds.do(lambda: set_volume(robot, lib, volume))

while True:
    schedule.run_pending()
    if keyboard.is_pressed('esc') and keyboard.is_pressed('q'):     # press 'esc' and 'q' to exit program
        break

if robotIsConnected:
    lib.myDisconnect(robot)     # directly cut off program will lead to a crash, reboot can solve it
    print("File play finished, robot Disconnected!\n")

# cv.destroyAllWindows()
