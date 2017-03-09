""" 操作数据库 """

__author__ = 'Cichar'
__version__ = '0.2'

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base


class ControlDB:
    """
    
    完成对数据库的连接及操作，提供session实例
    
    """

    def __init__(self):
        self.engine = self.create_the_engine()
        self.session = self.create_session()

    @staticmethod
    def create_the_engine():
        """
        
        创建数据库连接
         
        """

        created_engine = create_engine('mysql+pymysql://xxxx:xxxx@localhost:3306/xxxx?charset=utf8', encoding='utf-8')
        return created_engine

    def init_db(self):
        """
    
        在数据库中创建表
    
        """

        Base.metadata.create_all(self.engine)

    def create_session(self):
        """
        
        创建session实例
        
        """

        create_session = sessionmaker(bind=self.engine)
        created_session = create_session()
        return created_session
