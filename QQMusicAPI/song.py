from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .db import Base


class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True)
    mid = Column(String)
    song_id = Column(String)
    filename = Column(String)
    name = Column(String)
    extras_name = Column(String)
    title = Column(String)
    subtitle = Column(String)
    trans_name = Column(String)

    comments = relationship("Comment", order_by="Comment.id", back_populates="song")

    # TODO
