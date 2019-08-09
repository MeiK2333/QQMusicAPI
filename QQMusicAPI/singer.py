from sqlalchemy import Integer, Column, Boolean, String

from .db import Base


class Singer(Base):
    id = Column(Integer, primary_key=True)
    mid = Column(String)

    _title = Column(String)
    _music_total_num = Column(Integer)
    _song_id = Column(String)

    extracted = Column(Boolean, default=False)

    def extract(self):
        self.extracted = True
