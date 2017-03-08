""" 爬虫需要使用的数据库模型 """

__author__ = 'Cichar'
__version__ = '0.2'

from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class PlayList(Base):
    """
    
    歌单数据表，作为爬虫目标歌单的临时储存。
    
    """

    __tablename__ = 'playlists'

    id = Column(String(64), primary_key=True)

    def __repr__(self):
        return 'Playlist %r' % self.id
