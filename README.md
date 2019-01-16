# QQMusicAPI

## [Next](https://github.com/MeiK-h/QQMusicAPI/tree/Next)

正在开发中的新版本。

## Song

```python
from QQMusicAPI import Song

# 参数为歌曲的 mid
# 可以在网页 QQ 音乐获得
# 比如林俊杰的《那些你很冒险的梦》
# https://y.qq.com/n/yqq/song/002kADrZ01iC2L.html
# mid 就是 002kADrZ01iC2L
song = Song('002kADrZ01iC2L')

# 获得歌曲信息
song.extract()
song.lyric
song.image
song.song_id
song.info
# 热门评论
song.hot_comment
# 评论总数
song.comment_total

# 获取某页评论
song.comment_page(1)

# 获得歌曲的歌词
# 格式为 {lyric: ..., trans: ...}
song.get_lyric()
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

## Rank

```python
from QQMusicAPI import Rank, RankType

# 直接 get 可以获得最近一期的数据
rank = Rank().get()
print(rank[0].title)
rank = Rank(RankType.巅峰榜_欧美).get()
print(rank[0].title)
rank = Rank(RankType.巅峰榜_流行指数).get()
print(rank[0].title)
rank = Rank(RankType.巅峰榜_内地).get()
print(rank[0].title)
rank = Rank(RankType.巅峰榜_港台).get()
print(rank[0].title)
rank = Rank(RankType.巅峰榜_韩国).get()
print(rank[0].title)
rank = Rank(RankType.巅峰榜_日本).get()
print(rank[0].title)
rank = Rank(RankType.巅峰榜_热歌).get()
print(rank[0].title)
rank = Rank(RankType.巅峰榜_新歌).get()
print(rank[0].title)
rank = Rank(RankType.巅峰榜_网络歌曲).get()
print(rank[0].title)
rank = Rank(RankType.巅峰榜_影视金曲).get()
print(rank[0].title)
rank = Rank(RankType.巅峰榜_K歌金曲).get()
print(rank[0].title)
rank = Rank(RankType.巅峰榜_腾讯音乐人原创榜).get()
print(rank[0].title)
rank = Rank(RankType.说唱榜).get()
print(rank[0].title)
rank = Rank(RankType.台湾Hito中文榜).get()
print(rank[0].title)
rank = Rank(RankType.日本公信榜).get()
print(rank[0].title)
rank = Rank(RankType.韩国Mnet榜).get()
print(rank[0].title)
rank = Rank(RankType.英国UK榜).get()
print(rank[0].title)
rank = Rank(RankType.美国公告牌榜).get()
print(rank[0].title)
rank = Rank(RankType.香港电台榜).get()
print(rank[0].title)
rank = Rank(RankType.香港商台榜).get()
print(rank[0].title)
rank = Rank(RankType.美国iTunes榜).get()
print(rank[0].title)

# 可以查看可用的所有的日期
rank = Rank(RankType.巅峰榜_内地)
print(rank.date_list)  # 所有可用日期
rank_list = rank.get(rank.date_list[1])  # 获取指定日期的数据
print(rank_list[0].title)

```

## Singer

```python
from QQMusicAPI import Singer

# 参数要求 mid
# 以林俊杰为例：
# https://y.qq.com/n/yqq/singer/001BLpXF2DyJe2.html
singer = Singer('001BLpXF2DyJe2')

# 获取歌手信息
singer.extract()
print(singer.name)
print(singer.info)
print(singer.basic)
print(singer.other)

# 获取歌手所有歌曲
song_list = singer.song_all()
print(song_list[0].title)
```
