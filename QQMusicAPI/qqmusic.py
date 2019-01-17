# coding=utf-8
from .pager import SongPager


class QQMusic(object):

    def __init__(self):
        pass

    def search(self, keyword):
        return SongPager(keyword)
