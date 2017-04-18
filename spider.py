""" 
   **  爬虫基类  **
     
    初始化BaseSpider，会提供数据库连接实例
    
    基类中提供：
                构造随机头的函数
                解析URL的函数
    
"""

__author__ = 'Cichar'
__version__ = '0.2'

from urllib.request import urlopen, Request
from random import choice
import json

from control_db import ControlDB
from headers.headers import headers
from headers.user_agent import user_agent


class BaseSpider:

    def __init__(self):
        self.db = ControlDB()

    @staticmethod
    def create_header(flag='default'):
        """ 
        
        构建随机头，根据flag的不同，提供不同网站的随机header
        
        """

        header = headers[flag]
        header['User-Agent'] = choice(user_agent)
        return header

    def parse_url(self, url=None, timeout=2, charset='utf-8', header=None, parse_json=False):
        """ 
        
        解析URL，默认超时2秒，默认解析编码UTF-8
        如提供头部参数，则构建包含自定义的头部请求，否则默认不包含自定义头部
        默认模式不解析json数据
        
        """

        try:
            req = None
            if header:
                try:
                    if header in headers:
                        req = Request(url=url, headers=self.create_header(flag=header))
                    else:
                        req = Request(url=url, headers=self.create_header())
                except:
                    print(u'please choice the right header..')
            if req:
                response = urlopen(req, timeout=timeout)
            else:
                response = urlopen(url, timeout=timeout)
            data = response.read().decode(charset, 'ignore')
            # 如果需要用json解析
            if parse_json:
                json_data = json.loads(data)
                return json_data
            else:
                return data
        except Exception as e:
            print('** parse_url : %s **' % str(e))
            if '503' in str(e):
                print('** 服务器已进行限制 **')
                exit()

if __name__ == '__main__':
    test = BaseSpider()
    print(test.parse_url(url='http://www.baidu.com'))
#     while True:
#         header = test.create_header(flag='wyy')
#         print(header)

