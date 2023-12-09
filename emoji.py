import cv2 as cv
import numpy as np
from action import *
import time
import random


emoji_name = ['angry', 'blink', 'disdain', 'excited', 'left', 'right', 'sad', 'scared']


def play_img(img_root, robot, lib):
    """
    Display a static image on the screen.
    """
    img = cv.imread(img_root)
    img = cv.resize(img, (240, 240))
    lib.mySetImageSrc(robot, img)
    lib.mySync(robot)


def play_video(video_root, robot, lib):
    """
    Display a mp4 video on the screen.
    """
    cap = cv.VideoCapture(video_root)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if lib.myConnect(robot):
            frame = cv.resize(frame, (240, 240))
            frame = cv.cvtColor(frame, cv.COLOR_BGRA2RGB)
            lib.mySetImageSrc(robot, frame)
            lib.mySync(robot)


def play_weather(weather, robot, lib):
    """
    Display a static weather image on the screen.
    """
    play_img("./img/weather/" + weather + '.png', robot, lib)


def play_emoji(emoji, robot, lib):
    """
    Display a mp4 video on the screen.
    """
    play_video('./img/Emoji/'+emoji+'/4.mp4', robot, lib)


def play_img_with_action(img_root, action_sequence, robot, lib, delay=0.3, number=1):
    """
    Display a image and conduct a action sequence.
    """
    current_head_action = read_angles(robot, lib)[0]
    final_action = action_sequence[-1].copy()
    final_action[0] = current_head_action
    final_action = [float(i) for i in final_action]

    img = cv.imread(img_root)
    img = cv.resize(img, (240, 240))

    for i in range(number):
        for action in action_sequence:
            action = [float(j) for j in action]
            lib.mySetImageSrc(robot, img)
            lib.mySetJointAngles(robot, convert_type(action), convert_type(1))
            lib.mySync(robot)
            time.sleep(delay)

    lib.mySetJointAngles(robot, convert_type(final_action), convert_type(1))
    lib.mySync(robot)
    time.sleep(delay)
    lib.mySetJointAngles(robot, convert_type(final_action), convert_type(0))
    lib.mySync(robot)
    time.sleep(0.1)


def play_emoji_with_weather(emoji, weather, robot, lib):
    """
    Play the emoji video, add weather logo on it.
    """
    if not weather:
        play_emoji(emoji, robot, lib)
    else:
        cap = cv.VideoCapture('./img/Emoji/' + emoji + '/4.mp4')
        weather_img = cv.imread("./img/weather/" + weather + ".png")
        weather_img = cv.resize(weather_img, (60, 60))
        rows, cols = 60, 60
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            if lib.myConnect(robot):
                frame = cv.resize(frame, (240, 240))
                frame = cv.cvtColor(frame, cv.COLOR_BGRA2RGB)
                roi = frame[10:10+rows, 90:90+cols]
                img2gray = cv.cvtColor(weather_img, cv.COLOR_BGR2GRAY)
                ret, mask = cv.threshold(img2gray, 10, 255, cv.THRESH_BINARY)
                mask_inv = cv.bitwise_not(mask)
                img1_bg = cv.bitwise_and(roi, roi, mask=mask_inv)
                img2_fg = cv.bitwise_and(weather_img, weather_img, mask=mask)
                dst = cv.add(img1_bg, img2_fg)
                frame[10:10 + rows, 90:90 + cols] = dst

                lib.mySetImageSrc(robot, frame)
                lib.mySync(robot)


def play_random_emoji_with_weather(weather, robot, lib):
    """
    Play the random emoji video, add weather logo on it.
    """
    index = random.randint(0, 7)
    emoji = emoji_name[index]
    play_emoji_with_weather(emoji, weather, robot, lib)


def play_emoji_with_action(emoji, robot, lib, action_sequence, delay=0.3, number=5):
    """
    Play emoji video while simultaneously perform action sequence without losing frames.
    """
    sss = []
    for i in range(number):
        sss.append(action_sequence)
    action_sequence = sss

    action_sequence = np.array(action_sequence)     # 3×6
    action_sequence = np.squeeze(action_sequence)
    action_sequence = action_sequence.reshape(-1, 6)

    n_interval = action_sequence.shape[0] - 1   # assume 300ms per interval
    cap = cv.VideoCapture('./img/Emoji/' + emoji + '/4.mp4')
    frame_count = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv.CAP_PROP_FPS)
    cap.release()

    action_time = n_interval * delay    # total time for complete action
    emoji_time = frame_count / fps      # total time for complete emoji
    frame_per_interval = int(delay / (1 / fps))  # number of frames in single 300ms
    new_delay = delay / frame_per_interval

    action_change = np.array([action_sequence[i+1]-action_sequence[i] for i in range(n_interval)])  # 2×6
    action_change_per_interval = action_change / frame_per_interval     # 2×6
    new_action_sequence = np.zeros([n_interval, frame_per_interval, 6])     # 2×18×6
    ratio = 3
    for i in range(n_interval):
        new_action_sequence[i, 0] = action_sequence[i]
        # for j in range(frame_per_interval):
        #     new_action_sequence[i, j] = new_action_sequence[i, 0] + j * action_change_per_interval[i]

        for j in range(frame_per_interval):
            if j <= int(frame_per_interval / ratio):
                new_action_sequence[i, j] = new_action_sequence[i, 0] + ratio * j * action_change_per_interval[i]
            else:
                new_action_sequence[i, j] = new_action_sequence[i, int(frame_per_interval / ratio)]
    new_action_sequence = new_action_sequence.reshape(-1, 6).tolist()
    new_len = len(new_action_sequence)

    print(action_time, emoji_time)
    if action_time <= emoji_time:   # after action, play emoji until completion
        print(1)
        cap = cv.VideoCapture('./img/Emoji/' + emoji + '/4.mp4')
        for i in range(frame_count + 10):
            ret, frame = cap.read()
            if not ret:
                break
            if lib.myConnect(robot):
                if i <= (new_len-1):
                    lib.mySetJointAngles(robot, convert_type(new_action_sequence[i]), convert_type(1))
                frame = cv.resize(frame, (240, 240))
                frame = cv.cvtColor(frame, cv.COLOR_BGRA2RGB)
                lib.mySetImageSrc(robot, frame)
                lib.mySync(robot)
                time.sleep(new_delay)

    if action_time >= emoji_time:   # run another loop of emoji until action completion
        print(2)
        n = int(new_len / frame_count) + 1
        print(n)
        index = 0
        for i in range(n):
            cap = cv.VideoCapture('./img/Emoji/' + emoji + '/4.mp4')
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                if lib.myConnect(robot):
                    frame = cv.resize(frame, (240, 240))
                    frame = cv.cvtColor(frame, cv.COLOR_BGRA2RGB)
                    lib.mySetImageSrc(robot, frame)
                    if index <= (new_len - 1):
                        lib.mySetJointAngles(robot, convert_type(new_action_sequence[index]), convert_type(1))
                        index = index + 1
                    lib.mySync(robot)
                    time.sleep(new_delay)

    lib.mySetJointAngles(robot, convert_type(new_action_sequence[-1]), convert_type(0))
    lib.mySync(robot)
    time.sleep(new_delay)


def play_emoji_with_action_keep_head(emoji, robot, lib, action_sequence, delay=0.3, number=5):
    """
    Play emoji video while simultaneously perform action sequence without losing frames.
    The head angles at the end will be adapted to original value.
    """
    current_head_action = read_angles(robot, lib)[0]
    final_action = action_sequence[-1].copy()
    final_action[0] = current_head_action
    final_action = [float(i) for i in final_action]

    play_emoji_with_action(emoji, robot, lib, action_sequence, delay, number)

    lib.mySetJointAngles(robot, convert_type(final_action), convert_type(1))
    lib.mySync(robot)
    time.sleep(delay)
    lib.mySetJointAngles(robot, convert_type(final_action), convert_type(0))
    lib.mySync(robot)
    time.sleep(0.1)


if __name__ == '__main__':
    lib = lib_init()

    robot = lib.CreateElectronLowLevel()
    if lib.myConnect(robot):
        robotIsConnected = True
        print("Robot connected!\n")
    else:
        robotIsConnected = False
        print("Connect failed!\n")
    # ####################################################
    # play_emoji('blink', robot, lib)
    # #####################################################
    # play_emoji_with_weather('angry', 'Snow', robot, lib)
    # #####################################################
    # play_emoji_with_action_keep_head('angry', robot, lib, raise_hand_1, number=4)
    # #####################################################
    # play_weather('Thunderstorm', robot, lib)
    # time.sleep(1)
    # #####################################################
    # play_img_with_action('./img/weather/Drink.png', time_to_drink, robot, lib)
    # ####################################################

    if robotIsConnected:
        lib.myDisconnect(robot)
        print("File play finished, robot Disconnected!\n")
