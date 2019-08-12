import unittest

from QQMusicAPI import QQMusic, Song
from QQMusicAPI.song_search_pager import SongSearchPager


class TestQQMusic(unittest.TestCase):
    def test_search(self):
        keyword = "Legends Never Die"
        qq = QQMusic.search(keyword)
        self.assertTrue(isinstance(qq, SongSearchPager))
        self.assertEqual(keyword, qq.keyword)
        self.assertEqual(qq.cursor_page, 1)

        for song in qq:
            self.assertTrue(isinstance(song, Song))

        next_page = qq.next_page()
        self.assertEqual(next_page.cursor_page, 2)
        songs = next_page.list()
        self.assertTrue(isinstance(songs, list))
        for song in songs:
            self.assertTrue(isinstance(song, Song))
