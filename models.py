""" 爬虫需要使用的数据库模型 """

__author__ = 'Cichar'
__version__ = '0.2'

from sqlalchemy import Column, String, Integer, DateTime, TEXT, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ZhiHuUserInfo(Base):
    """

    知乎用户数据

    """

    __tablename__ = 'zhhuserinfos'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), default=u'未知')
    headline = Column(String(128), default=u'未知')
    location = Column(String(64), default=u'未知')
    description = Column(TEXT(), default=u'未知')
    voteup_count = Column(Integer)
    thanked_count = Column(Integer)
    favorited_count = Column(Integer)
    logs_count = Column(Integer)
    question_count = Column(Integer)
    url_token = Column(String(64), default=u'未知')
    follower_count = Column(Integer)
    following_count = Column(Integer)
    business = Column(String(64), default=u'未知')
    employment = Column(String(64), default=u'未知')
    company = Column(String(64), default=u'未知')
    update_time = Column(DateTime())
    updata_flag = Column(Boolean, default=True)
    crawl_flag = Column(Boolean, default=False)

    def __repr__(self):
        return 'ZhiHuUser %r' % self.name


class PlayList(Base):
    """
    
    歌单数据表，作为爬虫目标歌单的临时储存。
    
    """

    __tablename__ = 'playlists'

    id = Column(Integer, primary_key=True)
    playlist_id = Column(String(64))
    tag = Column(String(256))

    def __repr__(self):
        return 'Playlist %r' % self.id


class DzMusic(Base):
    """
    
    电子歌曲数据表
    
    """

    __tablename__ = 'dz_musics'

    id = Column(Integer(), primary_key=True)
    music_name = Column(String(256))
    music_singer = Column(String(128))
    publish_time = Column(DateTime())
    comments = Column(Integer())
    update_time = Column(DateTime())

    def __repr__(self):
        return 'DzMusic %r' % self.id


class ACGMusic(Base):
    """

    ACG歌曲数据表

    """

    __tablename__ = 'acg_musics'

    id = Column(Integer(), primary_key=True)
    music_name = Column(String(256))
    music_singer = Column(String(128))
    publish_time = Column(DateTime())
    comments = Column(Integer())
    update_time = Column(DateTime())

    def __repr__(self):
        return 'ACGMusic %r' % self.id


class LightMusic(Base):
    """

    轻音乐歌曲数据表

    """

    __tablename__ = 'light_musics'

    id = Column(Integer(), primary_key=True)
    music_name = Column(String(256))
    music_singer = Column(String(128))
    publish_time = Column(DateTime())
    comments = Column(Integer())
    update_time = Column(DateTime())

    def __repr__(self):
        return 'LightMusic %r' % self.id


class ZyMusic(Base):
    """

    治愈歌曲数据表

    """

    __tablename__ = 'zy_musics'

    id = Column(Integer(), primary_key=True)
    music_name = Column(String(256))
    music_singer = Column(String(128))
    publish_time = Column(DateTime())
    comments = Column(Integer())
    update_time = Column(DateTime())

    def __repr__(self):
        return 'ZyMusic %r' % self.id
