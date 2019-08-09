from .comment import Comment
from .db import engine, Base, session
from .singer import Singer
from .song import Song

Base.metadata.create_all(engine)
