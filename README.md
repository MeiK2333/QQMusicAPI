# QQMusicAPI
网页QQ音乐的一些API

## 使用方法

### QQMusic

```python
>>> from QQMusic import QQMusic
>>> qqmusic = QQMusic()
>>> song_list = qqmusic.search_song('世界ノ歌')
>>> song_list
<QQMusic.SongList object at 0x7f9808406f98>
>>> print(song_list)
0. Weight of the World/壊レタ世界ノ歌 (Weight of the World/破灭的世界之歌) - 河野マリナ  < NieR:Automata Original Soundtrack >
1. 世界を変えるピアノが歌う - 末光篤 / 松本素生  < 色彩協奏曲 Colors Of Concerto >
2. 君のにる为赠诗 - RomariaCrusade  < 秋篝ノ歌 >
3. 落叶ぱねろ - 葉月ゆら  < 秋篝ノ歌 >
4. 刃 - RomariaCrusade  < 秋篝ノ歌 >
5. 守唄 - RomariaCrusade  < 秋篝ノ歌 >
6. 生死の誾 - RomariaCrusade  < 秋篝ノ歌 >
7. RPG - RomariaCrusade  < 秋篝ノ歌 >
8. 月と死神 (Another Moon Ver) - RomariaCrusade  < 秋篝ノ歌 >
9. 秋篝ノ歌 - RomariaCrusade  < 秋篝ノ歌 >
>>> song_list[0].save(path='song')
download: Weight of the World/壊レタ世界ノ歌 (Weight of the World/破灭的世界之歌) ------ 歌曲下载完成
True
>>> song_list.add(song_list[7])
>>> print(song_list)
0. Weight of the World/壊レタ世界ノ歌 (Weight of the World/破灭的世界之歌) - 河野マリナ  < NieR:Automata Original Soundtrack >
1. 世界を変えるピアノが歌う - 末光篤 / 松本素生  < 色彩協奏曲 Colors Of Concerto >
2. 君のにる为赠诗 - RomariaCrusade  < 秋篝ノ歌 >
3. 落叶ぱねろ - 葉月ゆら  < 秋篝ノ歌 >
4. 刃 - RomariaCrusade  < 秋篝ノ歌 >
5. 守唄 - RomariaCrusade  < 秋篝ノ歌 >
6. 生死の誾 - RomariaCrusade  < 秋篝ノ歌 >
7. RPG - RomariaCrusade  < 秋篝ノ歌 >
8. 月と死神 (Another Moon Ver) - RomariaCrusade  < 秋篝ノ歌 >
9. 秋篝ノ歌 - RomariaCrusade  < 秋篝ノ歌 >
10. RPG - RomariaCrusade  < 秋篝ノ歌 >
>>> song_list.save()
download: Weight of the World/壊レタ世界ノ歌 (Weight of the World/破灭的世界之歌) ------ 歌曲下载完成
download: 世界を変えるピアノが歌う ------ 歌曲下载完成
download: 君のにる为赠诗 ------ 歌曲下载完成
download: 落叶ぱねろ ------ 歌曲下载完成
download: 刃 ------ 歌曲下载完成
download: 守唄 ------ 歌曲下载完成
download: 生死の誾 ------ 歌曲下载完成
download: RPG ------ 歌曲下载完成
download: 月と死神 (Another Moon Ver) ------ 歌曲下载完成
download: 秋篝ノ歌 ------ 歌曲下载完成
download: RPG ------ 歌曲下载完成
>>> song_list[7].lrc_save()
download lrc: RPG ------ 歌词下载完成
True
```

### QQMusicPlayer

仅在 Linux 系统下可用，依赖 ffplay(ffmpeg) 。

```shell
sudo apt install ffmpeg
```

用法

```python
if __name__ == '__main__':
    qq = QQMusic()
    key_word = input('key_word: ')
    rst = qq.search_song(key_word)
    print(rst)
    index = int(input('index: '))
    print(rst[index])
    player = Player()
    player.play(rst[index])
    while True:
        input('按回车暂停')
        player.stop()
        input('按回车继续')
        player.cont()

```

## 未来可能会添加的功能

- 获得播放歌曲的具体信息（时长、已播放时间等）。
- 专辑、歌单、排行榜等信息（很简单，看什么时候有空吧）。
- 重新整理一遍逻辑


## 已知问题

- 播放结束后播放进程依旧存在。
- 在交互式控制台下暂停与继续无法正常使用，因为 QQMusicPlayer.get_pid() 无法获取播放器的 pid 。
- 在获取歌曲失败的时候（比如 vkey 认证未通过、网络错误等）没有完整的提示。
- 歌曲播放中失败的处理问题。
