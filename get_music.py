""" 网易云音乐评论爬虫(API版) """

__author__ = 'Cichar'
__version__ = '0.2'


from urllib.request import urlopen
from selenium import webdriver
import json

from control_db import ControlDB
from models import PlayList

music_list = []
music_comment = {}
db = ControlDB()


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


def search_playlist(pages, music_style):
    """
    
    通过歌单列表获取列表中的歌单ID
    歌单列表格式：http://music.163.com/#/discover/playlist/?order=hot&cat=%s&limit=35&offset=
    歌单列表规则：cat=     后接歌单风格
               limit=35 为每页列表限制的歌单数量
               offset=  后接偏移量，以limit为基数，基于页码递增。 
    
    :return: 
    
    """

    driver = webdriver.PhantomJS()
    for i in range(pages):
        # 歌单列表URL规则，offset=后面接页码，从0开始，以35为基数递增
        base_url = 'http://music.163.com/#/discover/playlist/?order=hot&cat=%s&limit=35&offset=' % music_style

        pagenum = i * 35
        driver.get(base_url + str(pagenum))

        # 进入iframe
        driver.switch_to.frame('g_iframe')

        # 定位歌单ID
        ids = driver.find_elements_by_xpath('//a[@data-res-id]')

        for id in ids:
            playlist = PlayList(id=id.get_attribute('data-res-id'))
            db.session.add(playlist)
            db.session.commit()


if __name__ == '__main__':
    # get_music_list('612963791')
    # print(music_comment)
    search_playlist(pages=41, music_style='%E7%94%B5%E5%AD%90')
    # print(len(db.session.query(PlayList).all()))
