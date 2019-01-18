# coding=utf-8
import QQMusicAPI


class QQMusic(object):

    def __init__(self):
        pass

    def search(self, keyword):
        return QQMusicAPI.SongPager(keyword)
