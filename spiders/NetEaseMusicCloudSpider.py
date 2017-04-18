""" 网易云音乐评论爬虫(API版) """

__author__ = 'Cichar'
__version__ = '0.2'

import json
from datetime import datetime
from time import sleep

from selenium import webdriver

from decorator import retry
from models import PlayList, DzMusic, ACGMusic, LightMusic, ZyMusic
from spider import BaseSpider
from spiders.music_style import music_style


class NetEaseMusicCloudSpider(BaseSpider):
    def __init__(self):
        super().__init__()
        self.style = music_style
        self.db_style = {
            u'电子': DzMusic,
            u'ACG': ACGMusic,
            u'轻音乐': LightMusic,
            u'治愈': ZyMusic
        }

    def search_playlist(self, page_num=None, music_style=None):
        """
    
        通过歌单列表获取列表中的歌单ID
        歌单列表格式：http://music.163.com/#/discover/playlist/?order=hot&cat=%s&limit=35&offset=
        歌单列表规则：cat=     后接歌单风格
                   limit=35 为每页列表限制的歌单数量
                   offset=  后接偏移量，以limit为基数，基于页码递增。 
    
        :return: 
    
        """

        driver = webdriver.PhantomJS('G:/Python/PhantomJS/phantomjs-2.1.1-windows/bin/phantomjs')

        tag = self.style[music_style]['style']

        if not page_num:
            # 如果没有传入页码数，则获取页码数
            url = 'http://music.163.com/#/discover/playlist/?order=hot&cat=%s' % tag
            driver.get(url)
            driver.switch_to.frame('g_iframe')
            pages = driver.find_elements_by_xpath('//a[@class="zpgi"]')
            page_num = int(pages[-1].text)

        for i in range(page_num):
            # 歌单列表URL规则，offset=后面接页码，从0开始，以35为基数递增
            base_url = 'http://music.163.com/#/discover/playlist/?order=hot&cat=%s&limit=35&offset=' % tag

            pagenum = i * 35
            driver.get(base_url + str(pagenum))

            # 进入iframe
            driver.switch_to.frame('g_iframe')

            # 定位歌单ID
            ids = driver.find_elements_by_xpath('//a[@data-res-id]')

            for id in ids:
                playlist = PlayList(playlist_id=id.get_attribute('data-res-id'), tag=music_style)
                self.db.session.add(playlist)
            self.db.session.commit()
        print('{0} 扫描完毕'.format(music_style))

    @retry
    def get_music_list(self, playlist_id, tag=None):
        """
    
        从歌单中爬取该歌单所包含的歌曲ID
        歌单API：http://music.163.com/api/playlist/detail?id=playlist_id
        歌曲ID格式：R_SO_4_DDDDDDDD
    
        :param tag: 歌单标签
        :param playlist_id: 歌单ID
        :return: 
    
        """

        try:
            sleep(0.5)
            url = 'http://music.163.com/api/playlist/detail?id={}'.format(playlist_id)

            # 通过歌单API获取JSON数据
            result = self.parse_url(url=url, header='wyy', parse_json=True)

            # 从解析过的数据中获取歌曲数据
            clear_result = result['result']['tracks']

            if clear_result:
                # 遍历数据中的歌曲ID
                for i in range(len(clear_result)):
                    self.get_music_info(music_id=clear_result[i]['commentThreadId'], tag=tag)
            else:
                print('歌单数据解析失败')
        except Exception as e:
            print(e)

    @retry
    def get_music_comment(self, music_id):
        """
    
        通过歌曲评论API爬取该歌单的评论数量
        歌曲评论API：http://music.163.com/api/v1/resource/comments/music_id
        歌曲ID格式：R_SO_4_DDDDDDDD
    
        :param music_id: 歌曲ID
        :return: 
    
        """

        url = 'http://music.163.com/api/v1/resource/comments/{}'.format(music_id)

        # 通过歌曲API获取JSON数据
        result = self.parse_url(url=url, header='wyy', parse_json=True)

        comment_num = result['total']

        if comment_num:
            return comment_num
        else:
            print('歌曲评论数据获取失败')

    @retry
    def get_music_info(self, music_id=None, tag=None):
        """
    
        通过歌曲API爬取该歌单的信息
        歌曲信息API：http://music.163.com/api/song/detail/?id=music_id&ids=[music_id]
        歌曲ID格式：R_SO_4_DDDDDDDD
        歌曲ID格式化：music_id[7:]
    
        :param tag: 歌曲标签
        :param music_id: 歌曲ID(未格式化)
        :return: 歌曲名，歌手，发行时间, 歌曲评论数，歌曲标签
    
        """

        sleep(0.8)
        url = 'http://music.163.com/api/song/detail/?id={0}&ids=[{0}]'.format(music_id[7:])

        # 通过歌曲API获取JSON数据
        result = self.parse_url(url=url, header='wyy', parse_json=True)

        # 获取歌曲名，歌手，发行时间
        music_name, music_singer, publish_time = result['songs'][0]['name'], \
                                                 result['songs'][0]['artists'][0]['name'], \
                                                 result['songs'][0]['album']['publishTime']

        # 如果在过滤列表则直接返回
        if music_singer in self.style[tag]['filter_singer']:
            print('* -------- 过滤歌曲 -------- *')
            return

        # 获取歌曲评论数
        music_comment_num = self.get_music_comment(music_id)

        # 格式化时间
        date = lambda time: datetime.fromtimestamp(time/1000).date()

        # 根据tag选择对应的数据模型
        model = self.db_style[tag]

        # 已存在的数据进行更新，否则创建
        music = self.db.session.query(model).filter_by(id=music_id[7:]).first()
        if music:
            current_comments_num = music.comments
            if current_comments_num != music_comment_num:
                music.comments = music_comment_num
                music.update_time = datetime.utcnow()
                self.db.session.commit()
                update_comments_num = music.comments
                print('更新歌曲信息:{0}  成功, {1} --> {2}'.format(music_id[7:], current_comments_num, update_comments_num))
            else:
                return
        else:
            music = model(id=music_id[7:], music_name=music_name, music_singer=music_singer,
                          publish_time=date(publish_time), comments=music_comment_num, update_time=datetime.utcnow())
            self.db.session.add(music)
            self.db.session.commit()
            print('创建歌曲信息:%s  成功' % (music_id[7:]))
