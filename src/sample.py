import argparse
import PySimpleGUI as sg
import time
from robotcontrol import RCClient
from threading import Thread

# Commadline option
parse = argparse.ArgumentParser()
parse.add_argument('--host', required=True)
parse.add_argument('--speech_port', default=22222, type=int)
parse.add_argument('--pose_port', default=22223, type=int)
parse.add_argument('--read_port', default=22224, type=int)
args = parse.parse_args()

# Global variables
HOST = args.host
SPEECH_PORT = args.speech_port
POSE_PORT = args.pose_port
READ_PORT = args.read_port
RCC = RCClient(HOST, SPEECH_PORT, POSE_PORT, READ_PORT)


sg.theme('Black')
# Parts
reset_pose_btn   = sg.Button('ポーズリセット', key='reset')
right_arm_up_btn = sg.Button('右腕あげる', key='right_arm_up')
left_arm_up_btn  = sg.Button('左腕あげる', key='left_arm_up')
nod_motion_btn  = sg.Button('うなずきモーション', key='nod_motion')
motion_5s_btn  = sg.Button('モーション5s', key='motion_5s')
speech_1_btn = sg.Button('発話遅め', key='speech_1')
speech_2_btn = sg.Button('発話普通', key='speech_2')
speech_3_btn = sg.Button('発話速め', key='speech_3')
wav_btn = sg.Button('音声ファイルの再生', key='wav')
# Window layout
layout = [
    [reset_pose_btn],
    [right_arm_up_btn, left_arm_up_btn],
    [nod_motion_btn, motion_5s_btn],
    [speech_1_btn, speech_2_btn, speech_3_btn],
    [wav_btn]
]

window = sg.Window('Dog controller', layout)


# モーション実行用関数
def do_motion(motion):
    for pose in motion:
        RCC.play_pose(pose)
        time.sleep(pose['Msec'] / 1000.0)


# Event loop
while True:
    event, values = window.read(timeout=1)
    if event is None:
        print('Window event is None. exit')
        break
    elif event == 'reset':
        RCC.reset_pose()
    elif event == 'right_arm_up':
        pose = {"Msec": 1000, "ServoMap": {"R_ELBO": -90}}
        RCC.play_pose(pose)
    elif event == 'left_arm_up':
        pose = {"Msec": 1000, "ServoMap": {"L_ELBO": 90}}
        RCC.play_pose(pose)
    elif event == 'nod_motion':
        motion = [
            {"Msec": 500, "ServoMap": {"HEAD_P": 10}},
            {"Msec": 500, "ServoMap": {"HEAD_P":-50}},
            {"Msec": 500, "ServoMap": {"HEAD_P":  0}},
        ]
        Thread(target=do_motion, args=(motion,)).start()
    elif event == 'motion_5s':
        motion = [
            {"Msec": 500, "ServoMap": {"R_ELBO":-45, "L_ELBO": 45, "HEAD_R":  30}},
            {"Msec": 500, "ServoMap": {"R_ELBO":  0, "L_ELBO":  0, "HEAD_R": -30}},
            {"Msec": 500, "ServoMap": {"R_ELBO":-45, "L_ELBO": 45, "HEAD_R":  30}},
            {"Msec": 500, "ServoMap": {"R_ELBO":  0, "L_ELBO":  0, "HEAD_R": -30}}
        ]
        Thread(target=do_motion, args=(motion,)).start()
    elif event == 'speech_1':
        d = RCC.say_text('こんにちは。私は犬です。雨にも負けず風にも負けず。', speed=0.8, emotion='normal')
        print('発話時間：', d)
    elif event == 'speech_2':
        d = RCC.say_text('こんにちは。私は犬です。雨にも負けず風にも負けず。', speed=1.0, emotion='normal')
        print('発話時間：', d)
    elif event == 'speech_3':
        d = RCC.say_text('こんにちは。私は犬です。雨にも負けず風にも負けず。', speed=1.2, emotion='normal')
        print('発話時間：', d)
    elif event == 'wav':
        d = RCC.play_wav('sample.wav')
        print('再生時間：', d)
    else:
        pass

window.close()

