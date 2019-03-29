#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
examples/test_api.py was created on 2019/03/29.
file in :relativeFile
Author: Charles_Lai
Email: lai.bluejay@gmail.com
"""
from QQMusicAPI import QQMusic

music_list = QQMusic.search('届かない恋')  # 我最喜欢的是学姐版的(茅野愛衣)
print(type(music_list))
print(music_list.data)
print(music_list.page_size)
print(music_list.total_num)
print(music_list.keyword)
next_music_list = music_list.next_page()
print(next_music_list.cursor_page)
print(next_music_list.prev_page)

song = music_list.data[0]
for k, v in song.__dict__.items():
    print(k, v)

print(song.song_url())