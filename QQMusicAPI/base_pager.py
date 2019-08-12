from typing import List


class BasePager(object):
    def __init__(self, keyword, cursor_page=1):
        self.keyword = keyword
        self.cursor_page = cursor_page

        # 当页结果
        self.data = []
        # 迭代游标
        self._iter_cur = 0
        # 结果页数
        self.page_size = 0
        # 结果条数
        self.total_num = 0

        self.extract()

    def extract(self):
        pass

    def next_page(self) -> "BasePager":
        # 检查越界
        if self.cursor_page >= self.page_size:
            raise IndexError

        _cls = self.__class__
        return _cls(keyword=self.keyword, cursor_page=self.cursor_page + 1)

    def prev_page(self) -> "BasePager":
        if self.cursor_page <= 1:
            raise IndexError

        _cls = self.__class__
        return _cls(keyword=self.keyword, cursor_page=self.cursor_page - 1)

    def list(self) -> List:
        return list(self)

    def __getitem__(self, item):
        return self.data[item]

    def __iter__(self):
        self._iter_cur = 0
        return self

    def __next__(self):
        if self._iter_cur >= len(self.data):
            raise StopIteration
        self._iter_cur += 1
        return self.data[self._iter_cur - 1]

    def __repr__(self):
        return f"<{self.__class__.__name__}: keyword={self.keyword}, cursor_page={self.cursor_page},\
 page_size={self.page_size}, total_num={self.total_num}>"
