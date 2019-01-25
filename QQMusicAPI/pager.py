# coding=utf-8
import json
import math

import requests

import QQMusicAPI


class BasePager(object):

    def __init__(self, keyword, cursor_page=1):
        self.keyword = keyword
        self.cursor_page = cursor_page

        # 当页结果
        self.data = []
        # 结果页数
        self.page_size = None
        # 结果条数
        self.total_num = None

        self.extract()

    def extract(self):
        pass

    def next_page(self):
        # 检查越界
        if self.cursor_page >= self.page_size:
            raise IndexError

        _cls = self.__class__
        return _cls(keyword=self.keyword, cursor_page=self.cursor_page + 1)

    def prev_page(self):
        if self.cursor_page <= 1:
            raise IndexError

        _cls = self.__class__
        return _cls(keyword=self.keyword, cursor_page=self.cursor_page - 1)

    def __repr__(self):
        return '<{self.__class__.__name__}: keyword={self.keyword}, cursor_page={self.cursor_page},\
 page_size={self.page_size}, total_num={self.total_num}>'.format(**locals())

    def __str__(self):
        return self.__repr__()


class SongSearchPager(BasePager):
    """ 歌曲搜索分页 """

    def extract(self):
        url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp'
        params = {
            'new_json': 1,
            'aggr': 1,
            'cr': 1,
            'flag_qc': 0,
            'p': self.cursor_page,
            'n': 20,
            'w': self.keyword
        }
        resp = requests.get(url, params=params)
        data = json.loads(resp.text[9:-1])
        data_list = data['data']['song']['list']

        for item in data_list:
            song = QQMusicAPI.Song(song_mid=item['mid'],
                                   name=item['name'], title=item['title'])
            song.singer = [
                QQMusicAPI.Singer(singer_mid=singer['mid'],
                                  name=singer['name'],
                                  title=singer['title'])
                for singer in item['singer']
            ]
            self.data.append(song)

        self.total_num = data['data']['song']['totalnum']
        self.page_size = math.ceil(self.total_num / 20)

    def format_all(self):
        # 返回列表形式的数据
        return [self.format_one(i) for i in range(len(self.data))]

    def format_one(self, index):
        song_title = self.data[index].title
        song_singers = ' / '.join(
            [singer.name for singer in self.data[index].singer])
        return '{song_title} - {song_singers}'.format(**locals())


class SongCommentPager(BasePager):
    """ 歌曲评论分页 """
    # TODO
    pass


class ToplistPager(BasePager):
    """ 歌曲排行榜分页 """
    # TODO
    pass


class SingerListPager(BasePager):
    """ 歌手分页 """
    # TODO
    pass
