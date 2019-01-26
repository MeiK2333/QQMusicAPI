# coding=utf-8
import base64
import json
import random

import requests

import QQMusicAPI


class Song(object):

    def __init__(self, song_mid, name=None, title=None, extract=False):
        self.song_mid = song_mid

        # 获取一个十位随机数
        self.guid = random.randint(1000000000, 9999999999)
        # 歌曲 song_id
        self.song_id = None
        # 歌曲歌词
        self.lyric = SongLyric(self.song_mid)
        # C400{}.m4a 好像是最低音质，这个以后再说
        # 反正我糙耳朵听不出来……
        self.filename = 'C400{self.song_mid}.m4a'.format(**locals())
        # 歌名
        # QQ 音乐在不同的页面显示不同的歌名……
        self.name = name
        self.extras_name = None
        self.title = title
        # 歌曲副标题
        self.subtitle = None
        # 歌名翻译（如果有的话）
        self.transname = None
        # 歌手（可能不止一个）
        self.singer = []
        # 歌曲在 web 端的页面
        self.url = 'https://y.qq.com/n/yqq/song/{self.song_mid}.html'.format(
            **locals())
        # 未解析的歌曲信息
        self.raw_songinfo = None

        if extract:
            self.extract()

    def extract(self):
        self._get_info()

    def song_url(self):
        """
        歌曲的播放链接，每次访问生成一个新的
        """
        vkey = self._get_vkey()
        return 'http://dl.stream.qqmusic.qq.com/{self.filename}?vkey={vkey}&guid={self.guid}&fromtag=30'.format(**locals())

    def _get_vkey(self):
        url = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg'
        params = {
            'format': 'json',
            'platform': 'yqq',
            'cid': '205361747',
            'songmid': self.song_mid,
            'filename': self.filename,
            'guid': self.guid
        }
        resp = requests.get(url, params=params)
        return json.loads(resp.text)['data']['items'][0]['vkey']

    def _get_info(self):
        url = 'https://u.y.qq.com/cgi-bin/musicu.fcg'
        params = {
            'format': 'json',
            'inCharset': 'utf8',
            'outCharset': 'utf-8',
            'data': '%7b%22songinfo%22%3a%7b%22method%22%3a%22get_song_detail_yqq%22%2c%22param%22%3a%7b%22song_type%22%3a0%2c%22song_mid%22%3a%22{self.song_mid}%22%7d%2c%22module%22%3a%22music.pf_song_detail_svr%22%7d%7d'.format(**locals()),
        }
        resp = requests.get(url, params=params)
        self.raw_songinfo = resp.json()

        data = self.raw_songinfo.get('songinfo').get('data')

        self.name = data.get('track_info').get('name')
        self.title = data.get('track_info').get('title')
        self.extras_name = data.get('extras').get('name')
        self.subtitle = data.get('extras').get('subtitle')
        self.transname = data.get('extras').get('transname')
        self.singer = [
            QQMusicAPI.Singer(singer_mid=singer.get('mid'),
                              name=singer.get('name'),
                              title=singer.get('title'))
            for singer in data.get('track_info').get('singer')
        ]

    def __repr__(self):
        return '<Song: name={self.name}, title={self.title}>'.format(**locals())

    def __str__(self):
        return self.__repr__()


class SongLyric(object):

    def __init__(self, song_mid):
        self.song_mid = song_mid

        # 歌词
        self.lyric = None
        # 翻译歌词
        self.trans = None

    def extract(self):
        lrc_url = 'https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_new.fcg?g_tk=753738303&songmid=' + self.song_mid
        headers = {
            'Referer': 'https://y.qq.com/portal/player.html',
            'Cookie': 'skey=@LVJPZmJUX; p',
        }
        resp = requests.get(lrc_url, headers=headers)
        lrc_dict = json.loads(resp.text[18:-1])
        if lrc_dict.get('lyric'):
            self.lyric = base64.b64decode(lrc_dict['lyric']).decode()
        if lrc_dict.get('trans'):
            self.trans = base64.b64decode(lrc_dict['trans']).decode()
