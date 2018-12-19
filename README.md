# QQMusicAPI

## Song

```python
from QQMusicAPI import Song

# 参数为歌曲的 mid
# 可以在网页 QQ 音乐获得
# 比如林俊杰的《那些你很冒险的梦》
# https://y.qq.com/n/yqq/song/002kADrZ01iC2L.html
# mid 就是 002kADrZ01iC2L
song = Song('002kADrZ01iC2L')

# 获得歌曲的歌词
# 格式为 {lyric: ..., trans: ...}
song.lyric
# 歌曲主页链接
song.url
# 歌曲下载链接，有时效性
# 每次请求重新获取
song.song_url
```

## Search

```python
from QQMusicAPI import Search

search = Search('年少有为')

# 关键词的结果个数
search.total_num
# 关键词的结果页数
search.page_size
# 获取某页数据: list(Song)
search.page(1)
```