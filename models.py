""" 爬虫需要使用的数据库模型 """

__author__ = 'Cichar'
__version__ = '0.2'

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


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
