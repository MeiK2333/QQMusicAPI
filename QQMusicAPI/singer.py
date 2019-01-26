# coding=utf-8
import requests

import QQMusicAPI


class Singer(object):

    def __init__(self, singer_mid, name=None, title=None):
        self.singer_mid = singer_mid
        self.name = name
        self.title = title

        self.url = 'https://y.qq.com/n/yqq/singer/{self.singer_mid}.html'.format(
            **locals())

        self.hot_music = []
        self.music_total_num = 0
        self.singer_id = None

    def extract(self):
        self._get_singer_info()

    def songs(self):
        return QQMusicAPI.SingerSongPager(self)

    def _get_singer_info(self):
        url = 'https://c.y.qq.com/v8/fcg-bin/fcg_v8_singer_track_cp.fcg'
        params = {
            'format': 'json',
            'inCharset': 'utf8',
            'outCharset': 'utf-8',
            'singermid': self.singer_mid,
            'order': 'listen',
            'begin': '0',
            'num': '30',
            'songstatus': '1',
        }
        resp = requests.get(url, params=params)
        data = resp.json().get('data')
        self.name = data.get('singer_name')
        self.singer_id = data.get('id')
        self.music_total_num = data.get('total')

        for item in data.get('list'):
            music_data = item['musicData']
            song = QQMusicAPI.Song(song_mid=music_data['songmid'],
                                   name=music_data['songname'])
            song.singer = [
                Singer(singer_mid=singer['mid'],
                       name=singer['name'])
                for singer in music_data['singer']
            ]
            self.hot_music.append(song)

    def __repr__(self):
        return '<Singer: name={self.name}, title={self.title}>'.format(**locals())

    def __str__(self):
        return self.__repr__()
