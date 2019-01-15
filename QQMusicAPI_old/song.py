import random
import time
import json
import base64
import re
import math

import requests
from bs4 import BeautifulSoup


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

        self.lyric = None
        self.song_id = None
        self.song_name = None
        self.song_title = None
        self.song_subtitle = None
        self.info = None
        self.image = None
        self.comment_total = None
        self.comment_page_size = None
        self.hot_comment = None

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

    def get_lyric(self):
        """
        获得歌词和翻译（如果有的话）
        :return: { lyric: ..., trans: ...}
        """
        lrc_url = self.lyric_url
        headers = {
            'Referer': 'https://y.qq.com/portal/player.html',
            'Cookie': 'skey=@LVJPZmJUX; p',  # 此处应该对应了 g_tk 和 skey 的关系，因此需要提供 skey 参数才可以获取
            # 我已经退出登录这个 skey 了，因此不会有安全问题的
        }
        resp = requests.get(lrc_url, headers=headers)
        lrc_dict = json.loads(resp.text[18:-1])
        data = {'lyric': '', 'trans': ''}
        if lrc_dict.get('lyric'):
            data['lyric'] = base64.b64decode(lrc_dict['lyric']).decode()
        if lrc_dict.get('trans'):
            data['trans'] = base64.b64decode(lrc_dict['trans']).decode()
        self.lyric = data
        return self.lyric

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

    def extract(self):
        self.get_lyric()
        self._get_song_info()
        self._get_hot_comment()

    def _get_song_info(self):
        """
        通过页面获得信息
        :return:
        """
        url = 'https://y.qq.com/n/yqq/song/{}.html'.format(self.mid)
        resp = requests.get(url)
        song_data = json.loads(re.search(r'g_SongData = .*};', resp.text).group()[13:-1])
        self.song_id = song_data['songid']
        self.song_subtitle = song_data['songsubtitle']
        self.song_name = song_data['songname']
        self.song_title = song_data['songtitle']
        if not self.title:
            self.title = self.song_title

        info_data = json.loads(re.search(r'info :.*}}', resp.text).group()[7:])
        self.info = info_data

        soup = BeautifulSoup(resp.text, 'html.parser')
        self.image = 'https:' + soup.find(class_='data__photo')['src']

    def _get_hot_comment(self):
        """
        获得热门评论与总评论数
        :return:
        """
        url = 'https://c.y.qq.com/base/fcgi-bin/fcg_global_comment_h5.fcg'
        params = {
            'format': 'json',
            'reqtype': '2',
            'biztype': '1',
            'topid': self.song_id,
            'cmd': '8',
            'pagenum': '0',
            'pagesize': '1'
        }
        resp = requests.get(url, params=params)
        data = json.loads(resp.text)
        self.comment_total = data['comment']['commenttotal']
        self.hot_comment = data['hot_comment']['commentlist']
        self.comment_page_size = math.ceil(self.comment_total / 25)

    def comment_page(self, page=1):
        """
        获得评论
        :param page:
        :return:
        """
        url = 'https://c.y.qq.com/base/fcgi-bin/fcg_global_comment_h5.fcg'
        params = {
            'format': 'json',
            'reqtype': '2',
            'biztype': '1',
            'topid': self.song_id,
            'cmd': '8',
            'pagenum': page - 1,
            'pagesize': '25'
        }
        resp = requests.get(url, params=params)
        data = json.loads(resp.text)
        return data['comment']['commentlist']
