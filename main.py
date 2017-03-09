""" 网易云音乐评论爬虫(API版) """

__author__ = 'Cichar'
__version__ = '0.2'

from NetEaseMusicCloudSpider import NetEaseMusicCloudSpider
from models import PlayList, DzMusic

spider = NetEaseMusicCloudSpider()


def run():
    """ 歌单检索 """

    while spider.db.session.query(PlayList).first():
        playlist = spider.db.session.query(PlayList).first()
        playlist_id, tag = playlist.id, playlist.tag
        spider.db.session.delete(playlist)
        spider.db.session.commit()
        spider.get_music_list(playlist_id=playlist_id, tag=tag)
    print('数据库更新完毕')


def schemas_info():
    """ 检查数据库情况 """

    playlist_num = spider.db.session.query(PlayList).count()
    dz_music_num = spider.db.session.query(DzMusic).count()

    print('待爬取歌单：{}'.format(playlist_num))
    print('电子歌曲：{}'.format(dz_music_num))

if __name__ == '__main__':
    # print(spider.db.session.query(PlayList).count())
    # spider.get_music_list(108600061)
    # spider.db.init_db()
    # spider.search_playlist(music_style='ACG')
    # run()
    schemas_info()
