# coding=utf-8
import os
import subprocess
import time
from threading import Thread

from QQMusic import QQMusic, Song, SongList

try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty


def enqueue_output(out, queue):
    """
    将流里面的信息存入 Queue 中，以备之后使用
    当播放进程结束的时候，线程也会自动结束
    """
    for line in iter(out.readline, b''):
        s = line.strip()
        if s:
            queue.put(line.strip())
        else:
            break


class Player(object):
    """ 
    QQMusicAPI 的播放器
    通过调用 ffplay 的方式，利用生成的 cookies 和歌曲 url 直接请求 http 歌曲
    """

    def __init__(self):
        self.cookies = ''
        self.url = ''
        self.pid = ''
        self.queue = Queue()
        self.duration = -1  # 歌曲时间
        self.play_time = 0  # 已播放时间

    def get_pid(self):
        """ 获取播放的进程 ID """
        get_pid_cmd = "ps aux | grep 'ffplay -hide_banner -nodisp -autoexit -headers cookie:{} {}' | grep -v 'grep ' | awk {{'print $2'}}".format(
            self.cookies, self.url)
        self.popen_pid = subprocess.Popen(get_pid_cmd, shell=True,
                                          stdin=subprocess.PIPE,
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE)
        self.pid = bytes.decode(self.popen_pid.stdout.read())
        return self.pid.strip()

    def play(self, song):
        """ 播放指定的音乐 """
        assert isinstance(song, Song)
        # 判断歌曲是否可以播放
        if song.status != 0:
            return False
        # 重置歌曲时长
        self.duration = -1
        self.play_time = 0
        # 如果之前的音乐还在播放，则 kill 掉
        if self.get_pid():
            self._kill()
        self.cookies = song.headers['cookie']
        self.url = song.get_music_url()
        # 填入生成的 cookies 和 url ，直接由 http 播放
        cmd = 'ffplay -hide_banner -nodisp -autoexit -headers "cookie:{}" "{}"'.format(
            self.cookies, self.url)
        self.popen_play = subprocess.Popen(cmd, shell=True,
                                           stdin=subprocess.PIPE,
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
        self.popen_play_file = open(self.popen_play.stderr.fileno(), 'rU')

        # 新建线程解析输出流信息
        t = Thread(target=enqueue_output, args=(
            self.popen_play_file, self.queue,))
        t.daemon = True
        t.start()

        return True

    def get_play_status(self):
        if self.queue.empty():
            return self.play_time
        if self.duration == -1:
            # 首先尝试读取歌曲时长
            line = self.queue.get()
            args = line.split()
            if args[0] == 'Duration:':
                duration = args[1][:-1]
                print('duration:', duration)
                self.duration = time.strptime(duration, '%H:%M:%S.%f')
            return 0

        # 读取当前播放进度
        while not self.queue.empty():
            line = self.queue.get()
        args = line.split()
        try:
            t = float(args[0])
            self.play_time = t
        except:
            t = 0
        return t if t else self.play_time

    def _kill(self):
        """ 停止当前的播放进程 """
        kill_cmd = "kill " + self.pid
        subprocess.Popen(kill_cmd, shell=True,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)

    def stop(self):
        """ 暂停播放 """
        self.get_pid()
        # 利用 linux 1234 信号，暂时挂起进程
        stop_cmd = "kill -STOP 1234 " + self.pid
        subprocess.Popen(stop_cmd, shell=True,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)

    def cont(self):
        """ 继续播放 """
        self.get_pid()
        # 继续被挂起的进程
        cont_cmd = "kill -CONT 1234 " + self.pid
        subprocess.Popen(cont_cmd, shell=True,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)


if __name__ == '__main__':
    qq = QQMusic()
    key_word = input('key_word: ')
    rst = qq.search_song(key_word)
    print(rst)
    index = int(input('index: '))
    print(rst[index])
    player = Player()
    player.play(rst[index])
    while player.duration == -1:
        t = player.get_play_status()
    while True:
        input('按回车暂停')
        player.stop()
        print(player.get_play_status())
        input('按回车继续')
        player.cont()
        print(player.get_play_status())
