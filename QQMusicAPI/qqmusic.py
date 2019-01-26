# coding=utf-8
import QQMusicAPI


class QQMusic(object):

    def __init__(self):
        pass

    @staticmethod
    def search(keyword):
        return QQMusicAPI.SongSearchPager(keyword)
