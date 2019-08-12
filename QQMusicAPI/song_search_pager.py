from .base_pager import BasePager
import requests
import json
import math
from .song import Song
from .db import session


class SongSearchPager(BasePager):
    def extract(self):
        if not isinstance(self.keyword, str):
            raise ValueError

        url = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp"
        params = {
            "new_json": 1,
            "aggr": 1,
            "cr": 1,
            "flag_qc": 0,
            "p": self.cursor_page,
            "n": 20,
            "w": self.keyword,
        }
        resp = requests.get(url, params=params)
        data = json.loads(resp.text[9:-1])
        data_list = data["data"]["song"]["list"]

        for item in data_list:
            song = Song(mid=item["mid"])
            song._name = item["name"]
            song._title = item["title"]
            session.add(song)
            self.data.append(song)

        self.total_num = data["data"]["song"]["totalnum"]
        self.page_size = math.ceil(self.total_num / 20)
