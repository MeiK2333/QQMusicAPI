# coding=utf-8
import os
import subprocess

from QQMusic import QQMusic, Song, SongList


class Player(object):
    """ 
    QQMusicAPI 的播放器
    通过调用 ffplay 的方式，利用生成的 cookies 和歌曲 url 直接请求 http 歌曲
    """

    def __init__(self):
        self.cookies = ''
        self.url = ''
        self.pid = ''

    def get_pid(self):
        """ 获取播放的进程 ID """
        get_pid_cmd = "ps aux | grep 'ffplay -nodisp -autoexit -headers cookie:{} {}' | grep -v 'grep ' | awk {{'print $2'}}".format(
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
        # 如果之前的音乐还在播放，则 kill 掉
        if self.get_pid():
            self._kill()
        self.cookies = song.headers['cookie']
        self.url = song.get_music_url()
        # 填入生成的 cookies 和 url ，直接由 http 播放
        cmd = 'ffplay -nodisp -autoexit -headers "cookie:{}" "{}"'.format(
            self.cookies, self.url)
        self.popen_play = subprocess.Popen(cmd, shell=True,
                                           stdin=subprocess.PIPE,
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)

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
    while True:
        input('按回车暂停')
        player.stop()
        input('按回车继续')
        player.cont()
