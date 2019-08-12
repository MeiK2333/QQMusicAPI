import unittest

from QQMusicAPI.base_pager import BasePager


class TestBasePager(unittest.TestCase):
    def test_base_pager(self):
        keyword = "keyword"
        pager = BasePager(keyword=keyword)
        self.assertEqual(pager.keyword, keyword)

        pager.data = [0, 1, 2, 3, 4, 5]
        for i in pager:
            self.assertEqual(i, pager.data[i])
            self.assertEqual(pager[i], pager.data[i])
