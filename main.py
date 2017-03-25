""" 网易云音乐评论爬虫(API版) """

__author__ = 'Cichar'
__version__ = '0.2'

from NetEaseMusicCloudSpider import NetEaseMusicCloudSpider
from models import PlayList, DzMusic, ACGMusic, LightMusic, ZyMusic
from music_style import music_style

spider = NetEaseMusicCloudSpider()


def run(tag_num=None):
    """ 歌单检索 """

    tag_dict = {
        '1': '电子',
        '2': 'ACG',
        '3': '轻音乐',
        '4': '治愈'
    }

    while True:
        if spider.db.session.query(PlayList).first():
            # 如果有指定风格，则按照指定的风格进行扫描
            if tag_num:
                playlist = spider.db.session.query(PlayList).filter_by(tag=tag_dict[tag_num]).first()
            # 否则按照默认的数据库排序进行扫描
            else:
                playlist = spider.db.session.query(PlayList).first()
            playlist_id, tag = playlist.playlist_id, playlist.tag
            spider.db.session.delete(playlist)
            spider.db.session.commit()
            spider.get_music_list(playlist_id=playlist_id, tag=tag)
        else:
            print('无待爬取歌单')
            break
    print('数据库更新完毕')


def get_playlist():
    """
    
    获取需要扫描的歌单 
    
    """

    styles = [style for style in music_style]

    for style in styles:
        spider.search_playlist(music_style=style)

    print('歌单获取完毕')


def schemas_info():
    """ 检查数据库情况 """

    playlist_num = spider.db.session.query(PlayList).count()
    dz_playlist_num = spider.db.session.query(PlayList).filter_by(tag='电子').count()
    acg_playlist_num = spider.db.session.query(PlayList).filter_by(tag='ACG').count()
    light_playlist_num = spider.db.session.query(PlayList).filter_by(tag='轻音乐').count()
    zy_playlist_num = spider.db.session.query(PlayList).filter_by(tag='治愈').count()
    dz_music_num = spider.db.session.query(DzMusic).count()
    acg_music_num = spider.db.session.query(ACGMusic).count()
    light_music_num = spider.db.session.query(LightMusic).count()
    zy_music_num = spider.db.session.query(ZyMusic).count()

    print('待爬取歌单：{0}, 电子：{1}, ACG：{2}, 轻音乐：{3}, 治愈：{4}'.format(playlist_num,
                                                               dz_playlist_num, acg_playlist_num,
                                                               light_playlist_num, zy_playlist_num))
    print('电子歌曲：{}'.format(dz_music_num))
    print('ACG歌曲：{}'.format(acg_music_num))
    print('轻音乐：{}'.format(light_music_num))
    print('治愈：{}'.format(zy_music_num))


if __name__ == '__main__':
    # print(spider.db.session.query(PlayList).count())
    # spider.get_music_list(108600061)
    # spider.db.init_db()
    # get_playlist()
    # run('2')
    schemas_info()
