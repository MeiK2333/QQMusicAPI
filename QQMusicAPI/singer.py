import requests
from sqlalchemy import Integer, Column, Boolean, String
from sqlalchemy.ext.hybrid import hybrid_property

from .db import Base
from .utils import extract_property


class Singer(Base):
    __tablename__ = "singers"

    id = Column(Integer, primary_key=True)
    mid = Column(String)

    _name = Column(String)
    _brief = Column(String)
    _singer_id = Column(Integer)
    _fans = Column(Integer)
    _total_album = Column(Integer)
    _total_mv = Column(Integer)
    _total_song = Column(Integer)

    extracted = Column(Boolean, default=False)

    def __repr__(self):
        body = []
        if self._name:
            body.append(f"name={self._name}")
        body.append(f"mid={self.mid}")

        body = ", ".join(body)
        return f"<Singer: {body}>"

    @extract_property
    def name(self):
        return self._name

    @extract_property
    def fans(self):
        return self._fans

    @extract_property
    def brief(self):
        return self._brief

    @extract_property
    def total_song(self):
        return self._total_song

    @extract_property
    def total_album(self):
        return self._total_album

    @extract_property
    def total_mv(self):
        return self._total_mv

    @extract_property
    def singer_id(self):
        return self._singer_id

    @hybrid_property
    def url(self):
        return f"https://y.qq.com/n/yqq/singer/{self.mid}.html"

    def extract(self):
        url = "https://u.y.qq.com/cgi-bin/musicu.fcg"
        params = {
            "format": "json",
            "inCharset": "utf8",
            "outCharset": "utf-8",
            "notice": "0",
            "platform": "yqq.json",
            "needNewCode": "0",
            "data": f'{{"comm":{{"ct":24,"cv":0}},"singer":{{"method":"get_singer_detail_info","param":{{"sort":5,"singermid":"{self.mid}","sin":0,"num":10}},"module":"music.web_singer_info_svr"}}}}',
        }
        resp = requests.get(url, params=params)
        data = resp.json()["singer"]["data"]
        self._name = data["singer_info"]["name"]
        self._singer_id = data["singer_info"]["id"]
        self._brief = data["singer_brief"]
        self._fans = data["singer_info"]["fans"]
        self._total_song = data["total_song"]
        self._total_mv = data["total_mv"]
        self._total_album = data["total_album"]

        self.extracted = True
