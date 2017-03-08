""" 网易云音乐评论爬虫(API版)---歌单获取 """

__author__ = 'Cichar'
__version__ = '0.2'


from selenium import webdriver

from control_db import ControlDB
from models import PlayList

db = ControlDB()


def search_playlist(page_num=None, music_style=None):
    """
    
    通过歌单列表获取列表中的歌单ID
    歌单列表格式：http://music.163.com/#/discover/playlist/?order=hot&cat=%s&limit=35&offset=
    歌单列表规则：cat=     后接歌单风格
               limit=35 为每页列表限制的歌单数量
               offset=  后接偏移量，以limit为基数，基于页码递增。 
    
    :return: 
    
    """

    driver = webdriver.PhantomJS()

    if not page_num:
        # 如果没有传入页码数，则获取页码数
        url = 'http://music.163.com/#/discover/playlist/?order=hot&cat=%s' % music_style
        driver.get(url)
        driver.switch_to.frame('g_iframe')
        pages = driver.find_elements_by_xpath('//a[@class="zpgi"]')
        page_num = int(pages[-1].text)

    for i in range(page_num):
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
    search_playlist(music_style='%E7%94%B5%E5%AD%90')
