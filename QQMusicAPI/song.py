import base64
import json
import random

import requests


class Song(object):

    def __init__(self, song_mid: str, extract=False, **kwargs):
        self.song_mid = song_mid

        # 获取一个十位随机数
        self.guid = random.randint(1000000000, 9999999999)
        self.song_id = kwargs.get('song_id', None)
        self.lyric = SongLyric(self.song_mid)
        # C400{}.m4a 好像是最低音质，这个以后再说
        # 反正我糙耳朵听不出来……
        self.filename = 'C400{}.m4a'.format(self.song_mid)
        self.name = kwargs.get('name', None)
        self.singer = None

        if extract:
            self.extract()

    def extract(self):
        pass

    def song_url(self) -> str:
        """
        歌曲的播放链接，每次访问生成一个新的
        """
        vkey = self._get_vkey()
        return 'http://dl.stream.qqmusic.qq.com/{self.filename}?vkey={vkey}&guid={self.guid}&fromtag=30'.format(**locals())

    def _get_vkey(self) -> str:
        url = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg'
        params = {
            'format': 'json',
            'platform': 'yqq',
            'cid': '205361747',
            'songmid': self.song_mid,
            'filename': self.filename,
            'guid': self.guid
        }
        rst = requests.get(url, params=params)
        return json.loads(rst.text)['data']['items'][0]['vkey']


class SongLyric(object):

    def __init__(self, song_mid: str):
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


class SongComment(object):

    def __init__(self, song_id: str):
        self.song_id = song_id

    def extract(self):
        pass
