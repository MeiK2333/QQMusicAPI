# QQMusicAPI
[![Build Status](https://travis-ci.org/MeiK2333/QQMusicAPI.svg?branch=master)](https://travis-ci.org/MeiK2333/QQMusicAPI)
![PyPI](https://img.shields.io/pypi/v/diego.svg?style=flat)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/MeiK-h/QQMusicAPI.svg)

## 支持的版本

本项目使用 python 3.6.7 进行开发，仅保证在该版本上可以运行。以下是经测试也可以使用的版本（但**不保证**所有功能正常可用）：

- python 2.6+
- python 3.5+

注意：因为对字符串的处理方式不同，在 Python2 中，所有类的 `__repr__` 方法与 `__str__` 方法将**不可用**。

## 支持的平台

本项目使用 Ubuntu 18.04 进行开发，仅保证在该平台上可用。

项目没有平台相关的依赖，**理论上**可以在任何可以使用 Python 的平台上运行。

## Usage

### SongSearchPager

```python
>>> from QQMusicAPI import QQMusic

>>> music_list = QQMusic.search('届かない恋')  # 我最喜欢的是学姐版的(茅野愛衣)

>>> type(music_list)
<class 'QQMusicAPI.pager.SongSearchPager'>

>>> music_list.data
[<Song: name=届かない恋 '13, title=届かない恋 '13 (无法传达的爱恋'13)>, <Song: name=届かない恋, title=届かない恋 (无法传达的爱恋)>, <Song: name=届かない恋, title=届かない恋 (无法传达的恋爱)>, <Song: name=届かない恋, title=届かない恋 (无法传达的爱恋) (Live at Campus Fes|TV Anime Ver.)>, <Song: name=届かない恋, title=届かない恋 (无法传达的爱恋)>, <Song: name=届かない恋, title=届かない恋>, <Song: name=届かない恋, title=届かない恋 (无法传达的爱恋) (Live at Campus Fes)>, <Song: name=届かない恋, title=届かない恋 (无法传达的爱恋) (Piano version)>, <Song: name=届かない恋, title=届かない恋>, <Song: name=届かない恋, title=届かない恋 (无法传达的爱恋) (Piano Solo Ver.)>, <Song: name=さよならのこと, title=さよならのこと (再见的事)>, <Song: name=Shiny Heart Shiny Smile, title=Shiny Heart Shiny Smile>, <Song: name=届かない恋 ~It Disappeared in Flakes~, title=届かない恋 ~It Disappeared in Flakes~>, <Song: name=届かない恋 '13, title=届かない恋 '13 (无法传达的爱恋 '13) (TV Version)>, <Song: name=届かない恋, title=届かない恋>, <Song: name=届かない恋, title=届かない恋>, <Song: name=closing '13, title=closing '13>, <Song: name=届かない恋, title=届かない恋 (铃声)>, <Song: name=届かない世界, title=届かない世界 (无法抵达的世界)>, <Song: name=沙耶の眠れるレクイエム, title=沙耶の眠れるレクイエム (沙耶沉睡的安魂曲)>]

>>> music_list.page_size
2
>>> music_list.total_num
39
>>> music_list.keyword
'届かない恋'
>>> music_list.cursor_page
1

>>> next_music_list = music_list.next_page()
>>> next_music_list.cursor_page
2
>>> prev_music_list = next_music_list.prev_page()
>>> prev_music_list.cursor_page
1
```

### Song

```python
>>> from QQMusicAPI import QQMusic
>>> music_list = QQMusic.search('届かない恋')

>>> song = music_list.data[0]
>>> type(song)
<class 'QQMusicAPI.song.Song'>
>>> song.song_mid
'0044XSxC3rZYir'
>>> song.url
'https://y.qq.com/n/yqq/song/0044XSxC3rZYir.html'
>>> song.name
"届かない恋 '13"
>>> song.title
"届かない恋 '13 (无法传达的爱恋'13)"
>>> song.singer
[<Singer: name=上原れな, title=上原れな (上原玲奈)>]

>>> song.song_url()
'http://dl.stream.qqmusic.qq.com/C4000044XSxC3rZYir.m4a?vkey=0E9DBFC4D180A631CD62ED0784E3DFA450F3B21148A4A9BD5C8E916B6EFDEF2C7A3EA45067C288890EC1D40F6603C9545FE65E49D53D2BC4&guid=8388983860&fromtag=30'
>>> import requests  # 生成的链接可以使用 requests 直接下载，也可以在浏览器中直接打开
>>> resp = requests.get(song.song_url(), headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'})
>>> with open('music.m4a', 'wb') as fw:
...     fw.write(resp.content)
... 
4210605
>>> song.subtitle  # 查询到的仅有基础信息
>>> song.extract()  # 获取歌曲的详细信息
>>> song.subtitle
'《白色相簿2》TV动画第1集片头曲|《白色相簿2》TV动画第7-8集片头曲|《白色相簿2》TV动画第10-12集片头曲'
>>> song.transname
"无法传达的爱恋'13"
>>> song.extras_name
"届かない恋 '13"
```

### Lyric

```python
>>> from QQMusicAPI import QQMusic
>>> music_list = QQMusic.search('届かない恋')
>>> song = music_list.data[0]
>>> lyric = song.lyric
>>> type(lyric)
<class 'QQMusicAPI.song.SongLyric'>
>>> lyric.extract()
>>> lyric.lyric
"[ti:届かない恋 &apos;13(TVアニメ「WHITE ALBUM2」OP)]\n[ar:上原れな]\n[al:TVアニメ「WHITE ALBUM2」OPテーマ「届かない恋’13」]\n[by:]\n[offset:0]\n[00:00.01]届かない恋 '13 (无法传达的爱恋'13) (《白色相簿2》TV动画第1集片头曲|《白色相簿2》TV动画第7-8集片头曲|《白色相簿2》TV动画第10-12集片头曲) - 上原れな (上原玲奈)\n[00:00.02]作詞：須谷尚子\n[00:00.03]作曲：石川真也\n \n[00:00.04]\n[00:25.10]孤独なふりをしてるの?\n[00:31.72]なぜだろう 気になっていた\n[00:38.15]気づけば いつのまにか\n[00:45.76]誰より 惹かれていた\n[00:54.06]どうすれば この心は 鏡に映るの?\n[01:08.47]届かない恋をしていても\n[01:15.21]映しだす日がくるかな\n[01:21.45]ぼやけた答えが 見え始めるまでは\n[01:29.38]今もこの恋は 動き出せない\n[01:40.77]\n[01:57.05]初めて声をかけたら\n[02:04.23]振り向いてくれたあの日\n[02:11.28]あなたは 眩しすぎて\n[02:18.08]まっすぐ見れなかった\n[02:25.82]どうすれば その心に 私を写すの?\n[02:37.67]\n[02:40.30]叶わない恋をしていても\n[02:47.66]写しだす日がくるかな\n[02:53.84]ぼやけた答えが 少しでも見えたら\n[03:02.26]きっとこの恋は 動きは始める\n[03:12.99]\n[03:34.65]どうすれば この心は 鏡に映るの?\n[03:45.32]\n[03:48.19]届かない恋をしていても\n[03:55.24]映しだす日がくるかな\n[04:01.67]ぼやけた答えが 見え始めるまでは\n[04:09.34]今もこの恋は 動き出せない"
>>> lyric.trans
"[ti:届かない恋 '13(TVアニメ「WHITE ALBUM2」OP)]\n[ar:上原れな]\n[al:TVアニメ「WHITE ALBUM2」OPテーマ「届かない恋’13」]\n[by:]\n[offset:0]\n[00:00.00]//\n[00:08.36]//\n[00:16.73]//\n[00:25.10]莫非你是在故作孤独？\n[00:31.72]为何心如此为你牵动\n[00:38.15]回过神来 不知不觉\n[00:45.76]我已经被你深深吸引\n[00:54.06]要怎样才能将我的心 映在镜中让你看清？\n[01:08.47]即使是场终成奢望的爱恋\n[01:15.21]是否也有映在镜中的一天\n[01:21.45]在能够看见隐约的曙光之前\n[01:29.38]这场爱恋如今依然寸步难行\n[01:40.77]\n[01:57.05]当我第一次出声相唤\n[02:04.23]当你第一次回首之时\n[02:11.28]你的身影是那么耀眼\n[02:18.08]让我不禁移开目光\n[02:25.82]要怎样才能将我的名深深印在你的心中？\n[02:37.67]\n[02:40.30]即使是场没有结果的爱恋\n[02:47.66]是否也有映在你心的一天\n[02:53.84]哪怕能看见一丝隐约的曙光\n[03:02.26]这份爱恋一定能够开始转动\n[03:12.99]\n[03:34.65]要怎样才能将我的心映在镜中让你看清？\n[03:45.32]\n[03:48.19]即使是场终成奢望的爱恋\n[03:55.24]是否也有映在镜中的一天\n[04:01.67]在能够看见隐约的曙光之前\n[04:09.34]这场爱恋如今依然寸步难行\n[04:20.90]"
```

### Singer

```python
>>> from QQMusicAPI import QQMusic
>>> music_list = QQMusic.search('届かない恋')
>>> song = music_list.data[0]
>>> song.singer  # 一首歌可能由多人合唱，因此结果为一个列表
[<Singer: name=上原れな, title=上原れな (上原玲奈)>]
>>> singer = song.singer[0]
>>> type(singer)
<class 'QQMusicAPI.singer.Singer'>
>>> singer.singer_mid
'003jYRDr3aQCKi'
>>> singer.name
'上原れな'
>>> singer.title
'上原れな (上原玲奈)'
>>> singer.url
'https://y.qq.com/n/yqq/singer/003jYRDr3aQCKi.html'
>>> singer.extract()  # 获取详细信息
>>> singer.hot_music
[<Song: name=届かない恋 (无法传达的恋爱), title=None>, <Song: name=届かない恋 '13 (无法传达的爱恋'13), title=None>, <Song: name=さよならのこと (再见的事), title=None>, <Song: name=After All ～綴る想い～ (After All ～编缀回忆～), title=None>, <Song: name=After All ～綴る想い～ (After All ～编缀回忆～), title=None>, <Song: name=優しい嘘, title=None>, <Song: name=closing '13, title=None>, <Song: name=closing, title=None>, <Song: name=幸せな記憶 (幸福的记忆), title=None>, <Song: name=恋のような (宛如恋爱), title=None>, <Song: name=After All～綴る想い～ '13 (After All ～编缀回忆～), title=None>, <Song: name=さよならのこと (再见的事) (TV Version), title=None>, <Song: name=Until (直到) (Acoustic Version), title=None>, <Song: name=届かない恋 '13 (无法传达的爱恋 '13) (TV Version), title=None>, <Song: name=After All ~綴る想い~ ’13, title=None>, <Song: name=夢のつづき, title=None>, <Song: name=Answer, title=None>, <Song: name=Free and Dream, title=None>, <Song: name=ただひとつの星, title=None>, <Song: name=いくつもの未来, title=None>, <Song: name=After All -TsuduruOmoi- (Acoustic), title=None>, <Song: name=birdcage (Instrumental), title=None>, <Song: name=トキメキ (心跳), title=None>, <Song: name=旅立ち, title=None>, <Song: name=手紙 ~10年後の私へ~, title=None>, <Song: name=Sparkling Heart, title=None>, <Song: name=Happy Ending, title=None>, <Song: name=Until -from Hispania-, title=None>, <Song: name=いくつもの未来 (ballad version), title=None>, <Song: name=birdcage, title=None>]

>>> singer_songs = singer.songs()
>>> singer_songs
<SingerSongPager: keyword=<Singer: name=上原れな (上原玲奈), title=上原れな (上原玲奈)>, cursor_page=1, page_size=3, total_num=74>
```

### SingerSongPager

类似 [SongSearchPager](#SongSearchPager)

## TODO

- 歌曲排行榜的获取
- 歌手查询
- 分类歌单
- 专辑
- MV

优先级：无（没有反馈，我的手会抖）
