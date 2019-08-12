from .song_search_pager import SongSearchPager


class QQMusic(object):
    def __init__(self):
        pass

    @staticmethod
    def search(keyword: str) -> SongSearchPager:
        return SongSearchPager(keyword)
