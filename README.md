# QQMusicAPI
网页QQ音乐的一些API

# 使用方法

```python
>>> from QQMusic import QQMusic
>>> qqmusic = QQMusic()
>>> song_list = qqmusic.search_song('hesitation snow')
>>> for song in song_list:
...   print(song)
... 
Hesitation Snow		fripSide		fripSide PC game compilation vol.2
>>> result = song_list[0].save()
歌曲下载完成
>>> result
True
>>> result = song_list[0].lrc_save(path='song')
歌词下载完成
```
