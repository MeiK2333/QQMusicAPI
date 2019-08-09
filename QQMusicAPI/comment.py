from sqlalchemy import Integer, Column, ForeignKey
from sqlalchemy.orm import relationship

from .db import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    song_id = Column(Integer, ForeignKey("songs.id"))
    # TODO

    song = relationship("Song", back_populates="comments")
