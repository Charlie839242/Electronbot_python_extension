from convert_type import convert_type
import time
from lib import lib_init


"""
pose = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
第一个数控制抬头幅度: [-15.0, 15.0]
第二个数控制左臂向两侧抬起幅度: [0.0, 30.0]
第三个数控制左臂向前抬起幅度: [0.0, 180.0]
第四个数控制右臂向两侧抬起幅度: [0.0, 30.0]
第五个数控制右臂向前抬起幅度: [0.0, 180.0]
第六个数控制底座旋转角度: [-90.0, 90.0]
"""
sample = [10.0, 30.0, 90.0, 0.0, 90.0, 0.0]


def angles_refine(angles):
    """
    Cut the angle values to multiples of the pre-defined base.
    """
    base = 1
    duration = [[-15.0, 15.0], [0.0, 30.0], [0.0, 180.0], [0.0, 30.0], [0.0, 180.0], [-90.0, 90.0]]
    for i in range(len(angles)):
        angles[i] = float(base * round(angles[i]/base))
        angles[i] = duration[i][0] if angles[i] < duration[i][0] else angles[i]
        angles[i] = duration[i][1] if angles[i] > duration[i][1] else angles[i]
    return angles


def read_angles(robot, lib):
    """
    Read current pose.
    """
    for i in range(5):
        lib.mySetJointAngles(robot, convert_type([0.0, 0.0, 0.0, 0.0, 0.0, 0.0]), convert_type(0))
        lib.mySync(robot)  # Sync两次才能读出来，不知道为什么
        angles = lib.myGetJointAngles(robot)
    angles = [angles[i] for i in range(6)]
    angles = angles_refine(angles)
    return angles


def play_action(robot, lib, action_sequence, delay=0.3, number=1):
    """
    Play an action sequence several times.
    """
    for i in range(number):
        for action in action_sequence:
            action = [float(j) for j in action]
            lib.mySetJointAngles(robot, convert_type(action), convert_type(1))
            lib.mySync(robot)
            time.sleep(delay)
    lib.mySetJointAngles(robot, convert_type([float(j) for j in action_sequence[-1]]), convert_type(0))
    lib.mySync(robot)
    time.sleep(delay)


def play_action_keep_head(robot, lib, action_sequence, delay=0.3, number=1):
    """
    Play an action sequence several times.
    The head angles at the end will be adapted to original value.
    """
    current_head_action = read_angles(robot, lib)[0]
    final_action = action_sequence[-1].copy()
    final_action[0] = current_head_action

    for i in range(number):
        for action in action_sequence:
            action = [float(j) for j in action]
            lib.mySetJointAngles(robot, convert_type(action), convert_type(1))
            lib.mySync(robot)
            time.sleep(delay)
    lib.mySetJointAngles(robot, convert_type(final_action), convert_type(1))
    lib.mySync(robot)
    time.sleep(delay)

    lib.mySetJointAngles(robot, convert_type([float(j) for j in action_sequence[-1]]), convert_type(0))
    lib.mySync(robot)
    time.sleep(delay)


wave_left_hand = [[15, 0, 180, 0, 0, 0], [15, 30, 180, 0, 0, 0]]    # 挥舞左手
rotate_with_up_down_hand = [[15, 30, 180, 30, 180, 30], [15, 30, 0, 30, 0, 20], [15, 30, 180, 30, 180, -30],
                       [15, 30, 180, 30, 180, 30], [15, 30, 180, 30, 180, 0]]   # 旋转并上下挥舞双手
rotate_with_down_hand = [[15, 30, 0, 30, 0, 20], [15, 0, 0, 0, 0, 20], [15, 30, 0, 30, 0, -20],
     [15, 0, 0, 0, 0, -20], [15, 30, 0, 30, 0, 20], [15, 0, 0, 0, 0, 0]]    # 旋转并拍打双手
raise_hand_1 = [[15, 0, 180, 0, 180, 0], [15, 0, 0, 0, 0, 0]]     # 抬手到头顶
raise_hand_2 = [[15, 8, 0, 8, 0, 20], [15, 8, 100, 8, 100, 20],
              [15, 8, 0, 8, 0, -20], [15, 8, 100, 8, 100, -20]]  # 抬手到胸口
posing = [[15, 30, -20, 30, 180, 20], [15, 30, 180, 30, -20, 0]]  # 摆造型
rotate_with_up_hand = [[15, 20, 180, 20, 180, 40], [15, 20, 180, 20, 180, 0]]     # 旋转并举起双手
time_to_drink = rotate_with_down_hand + posing + posing


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
    # 测试读取舵机角度
    # lib.mySetJointAngles(robot, convert_type(sample), convert_type(1))
    # lib.mySync(robot)
    # time.sleep(0.2)
    #
    # angles = read_angles(robot, lib)
    # print(angles)
    # ####################################################

    ####################################################
    # 测试一套动作
    # play_action_keep_head(robot, lib, time_to_drink, number=2)
    ####################################################

    if robotIsConnected:
        lib.myDisconnect(robot)
        print("File play finished, robot Disconnected!\n")
