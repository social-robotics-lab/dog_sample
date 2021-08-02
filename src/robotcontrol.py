import json
import os.path
import socket
import subprocess
from pydub import AudioSegment
from typing import Dict, List


class RCClient(object):
    """
    RobotControllerを操作するためのクラス
    """
    def __init__(self, host:str, speech_port=22222, pose_port=22223, read_port=22224):
        self.host = host
        self.speech_port = speech_port
        self.pose_port = pose_port
        self.read_port = read_port
        self.home_servomap = dict(HEAD_R=0, HEAD_P=0, HEAD_Y=0, BODY_Y=0, L_SHOU=-90, L_ELBO=0, R_SHOU=90, R_ELBO=0)
        self.home_ledmap = dict(L_EYE_R=255, L_EYE_G=255, L_EYE_B=255, R_EYE_R=255, R_EYE_G=255, R_EYE_B=255)
 
    def say_text(self, text:str, speed=1.0, emotion='normal') -> float:
        """
        発話させる。
        """
        output_file = '{}_say.wav'.format(self.host)
        make_wav(text, speed, emotion, output_file)
        with open(output_file, 'rb') as f:
            data = f.read()
            send(self.host, self.speech_port, data)
        sound = AudioSegment.from_file(output_file, 'wav')
        return sound.duration_seconds

    def play_wav(self, wav_file:str) -> float:
        """
        音声ファイルを再生する。
        """
        with open(wav_file, 'rb') as f:
            data = f.read()
            send(self.host, self.speech_port, data)
        sound = AudioSegment.from_file(wav_file, 'wav')
        return sound.duration_seconds

    def read_axes(self) -> dict:
        """
        現在の全関節の角度値を読む。
        """
        data = recv(self.host, self.read_port)
        axes = json.loads(data)
        return axes

    def play_pose(self, pose:dict) -> float:
        """
        ポーズを実行する。
        """
        data = json.dumps(pose).encode('utf-8')
        send(self.host, self.pose_port, data)
        return pose['Msec'] / 1000.0

    def reset_pose(self, speed=1.0):
        """
        ポーズをホームポジションに戻す関数。
        """
        msec = int(1000 / speed)
        pose = dict(Msec=msec, ServoMap=self.home_servomap, LedMap=self.home_ledmap)
        data = json.dumps(pose).encode('utf-8')
        send(self.host, self.pose_port, data)


#---------------------
# Low level functions
#---------------------
def recv(ip:str, port:int) -> str:
    conn = connect(ip, port)
    size = read_size(conn)
    data = read_data(conn, size)
    close(conn)
    return data.decode('utf-8')

def send(ip:str, port:int, data:str):
    conn = connect(ip, port)
    size = len(data)
    conn.send(size.to_bytes(4, byteorder='big'))
    conn.send(data)
    close(conn)

def connect(ip:str, port:int):
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((ip, port))
    return conn

def close(conn:socket):
    conn.shutdown(1)
    conn.close()

def read_size(conn:socket):
    b_size = conn.recv(4)
    return int.from_bytes(b_size, byteorder='big')

def read_data(conn:socket, size:int):
    chunks = []
    bytes_recved = 0
    while bytes_recved < size:
        chunk = conn.recv(size - bytes_recved)
        if chunk == b'':
            raise RuntimeError("socket connection broken")
        chunks.append(chunk)
        bytes_recved += len(chunk)
    return b''.join(chunks)


# Path to which OpenJTalk was installed
OPENJTALK_BINPATH = '/usr/bin'
OPENJTALK_DICPATH = '/var/lib/mecab/dic/open-jtalk/naist-jdic'
OPENJTALK_VOICEPATH = '/usr/share/hts-voice/mei/mei_{emotion}.htsvoice'

def make_wav(text, speed=1.0, emotion='normal', output_file='__temp.wav', output_dir=os.getcwd()):
    """
    Function to make a wav file using OpenJTalk.
    args:
        speed: The speed of speech. (Default: 1.0)
        emotion: Voice emotion. You can specify 'normal', 'happy', 'bashful', 'angry', or 'sad'.
        output_file: The file name made by this function. (Default: '__temp.wav')
        output_dir: The directory of output_file. (Default: Current directory)
    """
    open_jtalk = [OPENJTALK_BINPATH + '/open_jtalk']
    mech = ['-x', OPENJTALK_DICPATH]
    htsvoice = ['-m', OPENJTALK_VOICEPATH.format(emotion=emotion)]
    speed = ['-r', str(speed)]
    outwav = ['-ow', os.path.join(output_dir, output_file)]
    cmd = open_jtalk + mech + htsvoice + speed + outwav
    c = subprocess.Popen(cmd,stdin=subprocess.PIPE)
    c.stdin.write(text.encode('utf-8'))
    c.stdin.close()
    c.wait()
    return os.path.join(output_dir, output_file)
