import functools

from sqlalchemy.ext.hybrid import hybrid_property


def extract_property(func):
    """
    在需要加载的数据第一次被请求时执行加载过程
    :param func:
    :return:
    """

    @hybrid_property
    @functools.wraps(func)
    def wrapper(self, *args, **kw):
        if not self.extracted:
            self.extract()
        return func(self, *args, **kw)

    return wrapper
