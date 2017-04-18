""" 网易云音乐评论爬虫(API版) """

__author__ = 'Cichar'
__version__ = '0.2'

from models import PlayList, DzMusic, ACGMusic, LightMusic, ZyMusic, ZhiHuUserInfo
from spiders.NetEaseMusicCloudSpider import NetEaseMusicCloudSpider
from spiders.ZhiHuSpider import ZhiHuSpider
from spiders.music_style import music_style

spider = NetEaseMusicCloudSpider()


def zh_run(user_token=None, updata=False):
    ZhiHuSpider().get_start(user_token=user_token, updata=updata)


def run(tag_num=None):
    """ 歌单检索 """

    tag_dict = {
        '1': u'电子',
        '2': u'ACG',
        '3': u'轻音乐',
        '4': u'治愈'
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

    print('所有歌单获取完毕')


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
    zhihu_user_num = spider.db.session.query(ZhiHuUserInfo).count()

    print('待爬取歌单：{0}, 电子：{1}, ACG：{2}, 轻音乐：{3}, 治愈：{4}'.format(playlist_num,
                                                               dz_playlist_num, acg_playlist_num,
                                                               light_playlist_num, zy_playlist_num))

    all_music_num = dz_playlist_num + acg_music_num + light_music_num + zy_music_num
    print('电子歌曲：{}'.format(dz_music_num))
    print('ACG歌曲：{}'.format(acg_music_num))
    print('轻音乐：{}'.format(light_music_num))
    print('治愈：{}'.format(zy_music_num))
    print('总计：{}'.format(all_music_num))

    print('——————————————————————————————————————————————————')
    print('知乎用户数据：{}'.format(zhihu_user_num))


def filter_music():
    """ 过滤数据库 """

    filter_result = {}
    for style in music_style:
        delete_num = 0
        print(u'** -- 开始清洗 %s 中的数据 -- **' % style)
        model = spider.db_style[style]
        for music_singer in music_style[style]['filter_singer']:
            delete_musics = spider.db.session.query(model).filter_by(music_singer=music_singer).all()
            if delete_musics:
                delete_num += len(delete_musics)
                for delete_music in delete_musics:
                    try:
                        print(u'删除 {0} 的 {1}'.format(music_singer, delete_music.music_name))
                    except Exception as e:
                        pass
                    spider.db.session.delete(delete_music)
                spider.db.session.commit()
        print(u'** -- %s 清洗完毕 -- **' % style)
        if delete_num !=0:
            # 清洗结果统计
            filter_result[style] = delete_num

    print(u'** -- 数据清洗完毕 -- **')
    if filter_result:
        result_num = 0
        for success_style in filter_result:
            result_str = '{0}:{1}'.format(success_style, filter_result[success_style])
            result_num += int(filter_result[success_style])
            print(u'**' + ' '*5 + result_str)
        print(u'** -- ' + ' '*2 + '{0}'.format(result_num) + ' '*2 + ' -- **')

if __name__ == '__main__':
    # get_playlist()
    # run('2')
    # schemas_info()
    filter_music()
