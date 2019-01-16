# coding=utf-8
class Singer(object):

    def __init__(self, singer_mid, name=None, title=None):
        self.singer_mid = singer_mid
        self.name = name
        self.title = title

        self.url = 'https://y.qq.com/n/yqq/singer/{self.singer_mid}.html'.format(
            **locals())

    def __repr__(self):
        return '<Singer: name={self.name}, title={self.title}>'.format(**locals())

    def __str__(self):
        return self.__repr__()
