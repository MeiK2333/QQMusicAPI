import json
import random

import requests
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from .db import Base
from .utils import extract_property


class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True)
    mid = Column(String)

    _song_id = Column(String)
    _name = Column(String)
    _extras_name = Column(String)
    _title = Column(String)
    _subtitle = Column(String)
    _trans_name = Column(String)
    # TODO: 添加歌手等信息

    comments = relationship("Comment", order_by="Comment.id", back_populates="song")

    extracted = Column(Boolean, default=False)

    guid = random.randint(1000000000, 9999999999)

    def __repr__(self):
        body = []
        if self._name:
            body.append(f"name={self._name}")
        if self._trans_name:
            body.append(f"trans_name={self._trans_name}")
        if self._title:
            body.append(f"title={self._title}")
        if self._subtitle:
            body.append(f"subtitle={self._subtitle}")
        if self._extras_name:
            body.append(f"extras_name={self._extras_name}")
        body.append(f"mid={self.mid}")
        body.append(f"filename={self.filename}")

        body = ", ".join(body)
        return f"<Song: {body}>"

    @extract_property
    def song_id(self):
        return self._song_id

    @hybrid_property
    def filename(self):
        return f"C400{self.mid}.m4a"

    @hybrid_property
    def url(self):
        return f"https://y.qq.com/n/yqq/song/{self.mid}.html"

    @extract_property
    def name(self):
        return self._name

    @extract_property
    def extras_name(self):
        return self._extras_name

    @extract_property
    def title(self):
        return self._title

    @extract_property
    def subtitle(self):
        return self._subtitle

    @extract_property
    def trans_name(self):
        return self._trans_name

    @extract_property
    def song_url(self):
        vkey = self._get_vkey()
        return f"http://dl.stream.qqmusic.qq.com/{self.filename}?vkey={vkey}&guid={self.guid}&fromtag=30"

    def _get_vkey(self):
        url = "https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg"
        params = {
            "format": "json",
            "platform": "yqq",
            "cid": "205361747",
            "songmid": self.mid,
            "filename": self.filename,
            "guid": self.guid,
        }
        resp = requests.get(url, params=params)
        return json.loads(resp.text)["data"]["items"][0]["vkey"]

    def extract(self):
        """
        通过请求加载数据
        :return:
        """
        url = "https://u.y.qq.com/cgi-bin/musicu.fcg"
        params = {
            "format": "json",
            "inCharset": "utf8",
            "outCharset": "utf-8",
            "data": f"%7b%22songinfo%22%3a%7b%22method%22%3a%22get_song_detail_yqq%22%2c%22param%22%3a%7b%22song_type%22%3a0%2c%22song_mid%22%3a%22{self.mid}%22%7d%2c%22module%22%3a%22music.pf_song_detail_svr%22%7d%7d",
        }
        resp = requests.get(url, params=params)
        raw_info = resp.json()
        data = raw_info.get("songinfo").get("data")

        self._name = data.get("track_info").get("name")
        self._title = data.get("track_info").get("title")
        self._extras_name = data.get("extras").get("name")
        self._subtitle = data.get("extras").get("subtitle")
        self._trans_name = data.get("extras").get("transname")

        self.extracted = True
