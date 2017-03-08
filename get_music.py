""" 网易云音乐评论爬虫(API版)---歌曲信息及评论获取 """

__author__ = 'Cichar'
__version__ = '0.2'

from urllib.request import urlopen
import json
from datetime import datetime

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

    通过歌曲评论API爬取该歌单的评论数量
    歌曲评论API：http://music.163.com/api/v1/resource/comments/music_id
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


def get_music_info(music_id):
    """

    通过歌曲API爬取该歌单的信息
    歌曲信息API：http://music.163.com/api/song/detail/?id=music_id&ids=[music_id]
    歌曲ID格式：R_SO_4_DDDDDDDD
    歌曲ID格式化：music_id[7:]

    :param music_id: 歌曲ID(未格式化)
    :return: 歌曲名，歌手，发行时间

    """

    # 通过歌曲API获取JSON数据
    response = urlopen('http://music.163.com/api/song/detail/?id={0}&ids=[{0}]'.format(music_id))
    data = response.read().decode()

    # 解析JSON数据
    result = json.loads(data)

    # 获取歌曲名，歌手，发行时间
    music_name, music_singer, publish_time = result['songs'][0]['name'], \
                                             result['songs'][0]['artists'][0]['name'], \
                                             result['songs'][0]['album']['publishTime']
    # 格式化时间
    date = lambda time: datetime.fromtimestamp(time/1000).date()

    return music_name, music_singer, date(publish_time)


if __name__ == '__main__':
    get_music_info(460514774)
