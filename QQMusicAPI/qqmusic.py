# coding=utf-8
from .search import SongSearchPager


class QQMusic(object):

    def __init__(self):
        pass

    def search(self, keyword):
        return SongSearchPager(keyword)
