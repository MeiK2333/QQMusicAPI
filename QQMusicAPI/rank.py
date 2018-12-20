from enum import Enum
import json
import re

import requests

from .song import Song
from .singer import Singer


class RankType(Enum):
    巅峰榜_欧美 = 3
    巅峰榜_流行指数 = 4
    巅峰榜_内地 = 5
    巅峰榜_港台 = 6
    巅峰榜_韩国 = 16
    巅峰榜_日本 = 17
    巅峰榜_热歌 = 26
    巅峰榜_新歌 = 27
    巅峰榜_网络歌曲 = 28
    巅峰榜_影视金曲 = 29
    巅峰榜_K歌金曲 = 36
    巅峰榜_腾讯音乐人原创榜 = 52
    说唱榜 = 58
    台湾Hito中文榜 = 103
    日本公信榜 = 105
    韩国Mnet榜 = 106
    英国UK榜 = 107
    美国公告牌榜 = 108
    香港电台榜 = 113
    香港商台榜 = 114
    美国iTunes榜 = 123


class Rank(object):
    def __init__(self, rank_type=RankType.巅峰榜_流行指数):
        """
        :param rank_type: RankType
        """
        self.date = None
        self.rank_type = rank_type
        self.song_list = []
        self.date_list = []
        self._get_date_list()

    def get(self, date=None):
        if date is None:
            self.date = self.date_list[0]
        else:
            self.date = date

        self._get_rank_list()
        return self.song_list

    def _get_date_list(self):
        """
        访问一次页面以获得可用的日期列表
        :return:
        """
        resp = requests.get('https://y.qq.com/n/yqq/toplist/{}.html'.format(self.rank_type.value))
        js_data = re.search(r'toplist.init(.*);', resp.text)
        data = json.loads(js_data.group()[13:-2])
        self.date_list = data['dateList']

    def _get_rank_list(self):
        params = {
            'date': self.date,
            'page': 'detail',
            'topid': self.rank_type.value,
            'type': 'top',
            'song_begin': '0',
            'song_num': '300',  # 最多的榜单也不过 300 条
            'jsonpCallback': '',
            'format': 'jsonp',
        }
        if isinstance(self.rank_type.value, int):
            if self.rank_type.value > 100:
                params['type'] = 'global'
        resp = requests.get('https://c.y.qq.com/v8/fcg-bin/fcg_v8_toplist_cp.fcg', params=params)
        data = json.loads(resp.text)['songlist']

        for item in data:
            sdata = item['data']
            song = Song(mid=sdata['songmid'],
                        title=sdata['songname'],
                        singer=[Singer(mid=x['mid'], name=x['name'], id=x['id'], data=x) for x in sdata['singer']])
            self.song_list.append(song)
