# Electronbot Python Extensions

dll file from [repository](https://github.com/gropery/ElectronBot)

## ElectronBotSDK-LowLevel.dll

主要有以下几个函数：

```Python
lib.CreateElectronLowLevel()
lib.myConnect()
lib.myDisconnect()
lib.myGetJointAngles()
lib.mySetImageSrc()
lib.mySetJointAngles()
lib.mySync()
```

- `lib.CreateElectronLowLevel()`: 创建一个electronbot对象

  ```Python
  robot = lib.CreateElectronLowLevel()
  ```

- `lib.myConnect()`: 连接electronbot，成功返回`True`

  ```python
  r = lib.myConnect(robot)
  ```

- `lib.myDisconnect()`: 断开electronbot连接；若直接终止程序会卡死，重新上电即可。
- `lib.myGetJointAngles()`: 读取当前6个舵机的角度
- `lib.mySetImageSrc()`: 设置想要显示的图片。注意，这一步不会直接显示，需要等待`lib.mySync()`
- `lib.mySetJointAngles()`：设置想要的姿态。注意，这一步不会直接调整，需要等待`lib.mySync()`
  - 第一个参数是六个舵机的角度，第二参数是舵机的使能。在掰舵机时要先设置其使能为0。为了安全考虑，在后面所有实现的函数中，都要在函数的最后设置使能为0.
- `lib.mySync()`：将设置的图片和姿态同步至electronbot。

在这些之上实现其他功能。

### convert_types.py

- `convert_type()`: 将python变量转成c变量

### Volume.py

通过读取electronbot头部角度来控制电脑音量。

- `set_volume()`: 设置系统音量。

### Action.py

- `read_angles()`: 读取electronbot当前姿态
- `play_action()`: 执行指定的动作序列。
  - 执行动作耗时150ms左右，所以相邻的两个动作之间最好相隔时间大于200ms，避免线程抢占。
- `play_action_keep_head()`: 执行指定的动作序列，最后恢复electronbot头部位置

### emoji.py

- `play_img()`: 播放一张图片
- `play_video()`: 播放一个mp4视频
- `play_img_with_action()`: 保持播放某张图片的状态下执行一个动作序列
- `play_emoji_with_weather()`: 播放emoji时将天气的logo也添加在上面方便浏览当前天气
- `play_emoji_with_action()`: 在播放emoji时同时进行动作执行，二者同步进行
  - 在普通情景下比较难实现，因为dll函数`lib.mySync()`会同时更新electronbot的显示屏和姿态，也就是说更新到下一个动作的时候同时也只会更新到下一帧图像；执行完整的动作序列也只会顺带着播放几帧emoji，而一套完整的emoji有一百多帧，只显示几帧根本看不出来emoji。所以要进行改进。
  - 看别人有一种做法，就是异步抽帧播放emoji，比如一个动作序列有16个动作，emoji有160帧，则在第i个动作同步播放第10×i帧emoji，但这样也有缺点，即emoji播放起来是卡顿的。
  - 最后`play_emoji_with_action()`选择插帧来播放emoji，比如一个动作序列有16个动作，emoji有160帧，则在相邻的两个动作之间进行线性插值，得到额外的9个插值动作，这样16个动作就通过插帧变成了160个动作，就能和emoji同步播放了。

### main.py

通过schedule来将各个任务（比如调节音量，播放表情，执行动作···）当作线程来在指定时间执行。