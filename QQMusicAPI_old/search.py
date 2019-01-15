import json
import math

import requests

from .song import Song
from .singer import Singer


class Search(object):
    def __init__(self, keyword):
        self.keyword = keyword
        self.total_num = self._get_total()  # 该关键词的结果条数
        self.page_size = math.ceil(self.total_num / 20)  # 该关键词的结果页数

    def _get_total(self):
        """
        获取总条数
        :return:
        """
        url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp'
        params = {
            'new_json': 1,
            'aggr': 1,
            'cr': 1,
            'flag_qc': 0,
            'p': 1,
            'n': 20,
            'w': self.keyword
        }
        resp = requests.get(url, params=params)
        data = json.loads(resp.text[9:-1])
        return data['data']['song']['totalnum']

    def page(self, page=1):
        """
        获取某一页的查询结果
        :param page: 页码
        :return: list(Song)
        """
        if page > self.page_size:
            raise IndexError('没有这么多页')

        url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp'
        params = {
            'new_json': 1,
            'aggr': 1,
            'cr': 1,
            'flag_qc': 0,
            'p': page,
            'n': 20,
            'w': self.keyword
        }
        resp = requests.get(url, params=params)
        data = json.loads(resp.text[9:-1])
        data_list = data['data']['song']['list']
        song_list = []

        for item in data_list:
            song = Song(mid=item['mid'],
                        media_mid=item['file']['media_mid'],
                        title=item['title'],
                        singer=[Singer(mid=x['mid'], name=x['name'], id=x['id'], data=x) for x in item['singer']],
                        album=item['album'],
                        data=item)
            song_list.append(song)
        return song_list
