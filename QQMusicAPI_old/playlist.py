import json

import requests

from .song import Song
from .singer import Singer


class Playlist(object):
    def __init__(self, dissid):
        self.dissid = dissid

        self.name = None
        self.desc = None
        self.image = None
        self.visit_num = None  # 播放/访问量
        self.song_num = None
        self.song_list = []

    def extract(self):
        url = 'https://c.y.qq.com/qzone/fcg-bin/fcg_ucc_getcdinfo_byids_cp.fcg'
        params = {
            'type': '1',
            'json': '1',
            'format': 'json',
            'onlysong': '0',
            'disstid': self.dissid,
            'utf8': '1',
        }
        headers = {
            'Referer': 'https://y.qq.com/n/yqq/playsquare/{}.html'.format(self.dissid),
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }
        resp = requests.get(url, params=params, headers=headers)
        data = json.loads(resp.text)

        if len(data['cdlist']) > 1:
            assert ValueError('未定义的格式，请联系作者添加解析')

        data = data['cdlist'][0]
        self.name = data['dissname']
        self.desc = data['desc']
        self.image = data['logo']
        self.visit_num = data['visitnum']
        self.song_num = data['songnum']

        for item in data['songlist']:
            song = Song(mid=item['songmid'],
                        title=item['songname'],
                        singer=[Singer(mid=x['mid'], name=x['name'], id=x['id'], data=x) for x in item['singer']],
                        data=item)
            self.song_list.append(song)
