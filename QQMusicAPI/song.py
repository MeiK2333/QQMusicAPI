import random
import time
import json
import base64

import requests


class Song(object):
    def __init__(self, mid, **kwargs):
        self.guid = int(random.random() * 2147483647) * int(time.time() * 1000) % 10000000000
        self.headers = {
            "cookie": 'pgv_pvi=23333333; pgv_si=23333333; pgv_pvid={}; qqmusic_fromtag=30'.format(self.guid),
        }

        self.mid = mid
        self.media_mid = kwargs.get('media_mid')
        self.title = kwargs.get('title')
        self.singer = kwargs.get('singer')
        self.album = kwargs.get('album')

        self.filename = 'C400{}.m4a'.format(self.mid)

        self.kwargs = kwargs

    @property
    def url(self):
        """
        歌曲在 QQ 音乐 web 版中的页面链接
        :return:
        """
        return 'https://y.qq.com/n/yqq/song/{}.html'.format(self.mid)

    @property
    def song_url(self):
        """
        歌曲的播放链接，每次访问生成一个新的
        :return:
        """
        return 'http://dl.stream.qqmusic.qq.com/{}?vkey={}&guid={}&fromtag=30'.format(self.filename, self._get_vkey(),
                                                                                      self.guid)

    @property
    def lyric_url(self):
        return 'https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_new.fcg?g_tk=753738303&songmid=' + self.mid

    @property
    def lyric(self):
        """
        获得歌词和翻译（如果有的话）
        :return: { lyric: ..., trans: ...}
        """
        lrc_url = self.lyric_url
        headers = {
            'Referer': 'https://y.qq.com/portal/player.html',
            'Cookie': 'skey=23333333; p',
        }
        resp = requests.get(lrc_url, headers=headers)
        lrc_dict = json.loads(resp.text[18:-1])
        data = {'lyric': '', 'trans': ''}
        if lrc_dict.get('lyric'):
            data['lyric'] = base64.b64decode(lrc_dict['lyric']).decode()
        if lrc_dict.get('trans'):
            data['trans'] = base64.b64decode(lrc_dict['trans']).decode()
        return data

    def _get_vkey(self):
        url = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg'
        params = {
            'format': 'json',
            'platform': 'yqq',
            'cid': '205361747',
            'songmid': self.mid,
            'filename': self.filename,
            'guid': self.guid
        }
        rst = requests.get(url, params=params)
        return json.loads(rst.text)['data']['items'][0]['vkey']
