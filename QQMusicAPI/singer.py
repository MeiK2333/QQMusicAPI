class Singer(object):

    def __init__(self, singer_mid: str, name=None, title=None):
        self.singer_mid = singer_mid
        self.name = name
        self.title = title

    def __repr__(self):
        return '<Singer: name={self.name}, title={self.title}>'.format(**locals())

    def __str__(self):
        return self.__repr__()
