import unittest

import requests

from QQMusicAPI import Song


class TestSong(unittest.TestCase):
    def test_song_extract(self):
        song = Song(mid="00394z9S2ciPAD")

        self.assertEqual(song.filename, "C40000394z9S2ciPAD.m4a")
        self.assertEqual(song.url, "https://y.qq.com/n/yqq/song/00394z9S2ciPAD.html")
        self.assertEqual(song.subtitle, "2017英雄联盟全球总决赛主题曲")
        self.assertEqual(song.extras_name, "Legends Never Die")
        self.assertEqual(song.name, "Legends Never Die")
        self.assertEqual(song.trans_name, "传奇永不熄灭")
        self.assertEqual(song.title, "Legends Never Die")

    def test_song_repr(self):
        song = Song(mid="002BbUoO2fU5cV")

        self.assertEqual(repr(song), "<Song: mid=002BbUoO2fU5cV, filename=C400002BbUoO2fU5cV.m4a>")

        # extract data
        song.extract()

        self.assertEqual(
            repr(song),
            "<Song: name=届かない恋, trans_name=无法传达的爱恋, title=届かない恋 (无法传达的爱恋), extras_name=届かない恋, mid=002BbUoO2fU5cV, filename=C400002BbUoO2fU5cV.m4a>",
        )

    @unittest.skip
    def test_song_url(self):
        song = Song(mid="000XEt9C1Uusae")

        url = song.song_url
        resp = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"
            },
        )
        self.assertEqual(resp.status_code, 200)
