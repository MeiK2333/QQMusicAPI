from xml.etree import ElementTree

from bs4 import BeautifulSoup
import json
import requests

from .song import Song


class Singer(object):
    def __init__(self, mid, **kwargs):
        self.mid = mid
        self.singer_id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.kwargs = kwargs

        self.info = None
        self.basic = None
        self.other = None
        self.image = None
        self.song_total = None

    def extract(self):
        """
        获得歌手信息
        :return:
        """
        self._get_page_info()
        self._get_desc()
        self._get_total()

    def song_all(self):
        """
        获取所有歌曲
        :return:
        """
        url = 'https://c.y.qq.com/v8/fcg-bin/fcg_v8_singer_track_cp.fcg'
        params = {
            'jsonpCallback': '',
            'format': 'jsonp',
            'singermid': self.mid,
            'order': 'listen',
            'begin': 0,
            'num': self.song_total,
            'songstatus': '1'
        }
        resp = requests.get(url, params=params)
        data = json.loads(resp.text)
        return [Song(i['musicData']['songmid'], title=i['musicData']['songname']) for i in data['data']['list']]

    def _get_page_info(self):
        """
        从歌手页面获得歌手姓名与头像信息
        :return:
        """
        url = 'https://y.qq.com/n/yqq/singer/{}.html'.format(self.mid)
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        self.name = soup.find(class_='data__name_txt').string
        self.image = 'https:' + soup.find(class_='data__photo')['src']

    def _get_desc(self):
        """
        获得歌手详细信息和获得奖项等信息
        :return:
        """
        url = 'https://c.y.qq.com/splcloud/fcgi-bin/fcg_get_singer_desc.fcg'
        headers = {
            'referer': 'https://c.y.qq.com/xhr_proxy_utf8.html',
        }
        params = {
            'singermid': self.mid,
            'utf8': '1',
            'outCharset': 'utf-8',
            'format': 'xml'
        }
        resp = requests.get(url, params=params, headers=headers)
        data = ElementTree.fromstring(resp.text).find('data').find('info')
        self.info = data.find('desc').text
        self.basic = [{'key': i.find('key').text, 'value': i.find('value').text} for i in data.find('basic')]
        self.other = [{'key': i.find('key').text, 'value': i.find('value').text} for i in data.find('other')]

    def _get_total(self):
        """
        获得歌手歌曲的数量
        :return:
        """
        url = 'https://c.y.qq.com/v8/fcg-bin/fcg_v8_singer_track_cp.fcg'
        params = {
            'jsonpCallback': '',
            'format': 'jsonp',
            'singermid': self.mid,
            'order': 'listen',
            'begin': 0,
            'num': '10',
            'songstatus': '1'
        }
        resp = requests.get(url, params=params)
        self.song_total = json.loads(resp.text)['data']['total']
