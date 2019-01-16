from .search import SongSearchPager


class QQMusic(object):

    def __init__(self):
        pass

    def search(self, keyword: str):
        return SongSearchPager(keyword)
