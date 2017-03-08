""" 网易云音乐评论爬虫(API版)---歌曲信息及评论获取 """

__author__ = 'Cichar'
__version__ = '0.2'

from urllib.request import urlopen
import json

music_list = []
music_comment = {}


def get_music_list(playlist_id):
    """

    从歌单中爬取该歌单所包含的歌曲ID
    歌单API：http://music.163.com/api/playlist/detail?id=playlist_id
    歌曲ID格式：R_SO_4_DDDDDDDD

    :param playlist_id: 歌单ID
    :return: 

    """

    # 通过歌单API获取JSON数据
    response = urlopen('http://music.163.com/api/playlist/detail?id={}'.format(playlist_id))
    data = response.read().decode()

    # 解析JSON数据
    result = json.loads(data)

    # 从解析过的数据中获取歌曲数据
    clear_result = result['result']['tracks']

    # 遍历数据中的歌曲ID
    for i in range(len(clear_result)):
        music_list.append(clear_result[i]['commentThreadId'])
        print('len:%s' % len(music_list))

        # for i in music_list:
        #     print('GET %s' % i)
        #     get_music_comment(i)


def get_music_comment(music_id):
    """

    通过歌曲API爬去该歌单的评论数量
    歌曲评论API：http://music.163.com/api/v1/resource/comments/music_id
    歌曲信息API：http://music.163.com/api/song/detail/?id=music_id&ids=[music_id]
    歌曲ID格式：R_SO_4_DDDDDDDD

    :param music_id: 歌曲ID
    :return: 

    """

    # 通过歌曲API获取JSON数据
    response = urlopen('http://music.163.com/api/v1/resource/comments/{}'.format(music_id))
    data = response.read().decode()

    # 解析JSON数据
    result = json.loads(data)

    # 保存歌曲评论数据
    music_comment[music_id[7:]] = result['total']
