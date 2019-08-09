import unittest

from QQMusicAPI import Singer


class TestSong(unittest.TestCase):
    def test_singer_extract(self):
        singer = Singer(mid="004BsEon35Mmxz")

        self.assertEqual(singer.mid, "004BsEon35Mmxz")
        self.assertEqual(
            singer.url, "https://y.qq.com/n/yqq/singer/004BsEon35Mmxz.html"
        )
        self.assertEqual(singer.name, "茅野愛衣")
        self.assertEqual(singer.singer_id, 63263)

        self.assertTrue(isinstance(singer.brief, str))
        self.assertTrue(isinstance(singer.singer_id, int))
        self.assertTrue(isinstance(singer.total_song, int))
        self.assertTrue(isinstance(singer.total_mv, int))
        self.assertTrue(isinstance(singer.total_album, int))

    def test_singer_repr(self):
        singer = Singer(mid="000DQnc22YnDJM")
        self.assertEqual(repr(singer), "<Singer: mid=000DQnc22YnDJM>")

        singer.extract()

        self.assertEqual(repr(singer), "<Singer: name=fripSide, mid=000DQnc22YnDJM>")
