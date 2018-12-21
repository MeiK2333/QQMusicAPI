import QQMusicAPI

if __name__ == '__main__':
    search = QQMusicAPI.Search(input('请输入搜索条件：'))
    song_list = search.page(1)
    for i, song in enumerate(song_list):
        singers = ' / '.join([singer.name for singer in song.singer])
        print('{}: {} - {}'.format(i, song.title, singers))

    i = int(input('请选择一首音乐（输入编号）：'))

    song = song_list[i]
    while True:
        j = int(input('0: 歌手信息\n1: 歌曲信息\n2: 退出\n请选择操作：'))
        if j == 0:
            while True:
                if len(song.singer) == 0:
                    print('无歌手！')
                    break
                if len(song.singer) > 1:
                    for m, s in enumerate(song.singer):
                        print('{}: {}'.format(m, s.name))
                    l = int(input('请选择一位歌手：'))
                    singer = song.singer[l]
                else:
                    singer = song.singer[0]
                if singer.info is None:
                    singer.extract()
                k = int(input('0: 歌手名\n1: 歌手介绍\n2: 歌手信息\n3: 歌手其他信息\n4: 退出\n请选择操作：'))
                if k == 0:
                    print(singer.name)
                elif k == 1:
                    print(singer.info)
                elif k == 2:
                    data = '\n'.join(['{}: {}'.format(x['key'], x['value']) for x in singer.basic])
                    print(data)
                elif k == 3:
                    data = '\n'.join(['{}: {}'.format(x['key'], x['value']) for x in singer.other])
                    print(data)
                elif k == 4:
                    break
        elif j == 1:
            while True:
                if song.lyric is None:
                    song.extract()
                k = int(input('0: 歌曲名\n1: 歌词\n2: 歌曲信息\n3: 歌曲下载链接\n4: 退出\n请选择操作：'))
                if k == 0:
                    print(song.title)
                elif k == 1:
                    print('原始歌词：')
                    print(song.lyric['lyric'])
                    print('翻译歌词（如果有的话）:')
                    print(song.lyric['trans'])
                elif k == 2:
                    print(song.info)
                elif k == 3:
                    print(song.song_url)
                elif k == 4:
                    break
        elif j == 2:
            break
