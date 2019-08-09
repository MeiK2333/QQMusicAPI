from .comment import Comment
from .db import engine, Base, session
from .song import Song

Base.metadata.create_all(engine)
