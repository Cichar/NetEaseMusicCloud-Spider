# NetEaseMusicCloud-Spider
简述：利用PhantomJS进入iframe爬取歌单，再通过API对歌单及歌曲信息进行爬取。

##### 工程说明：
```
NetEaseMusicCloud-Spider
    |-- main.py
    |-- NetEaseMusicCloudSpider.py
    |-- control_db.py
    |-- models.py
    |-- headers.py
    |-- decorator.py
    |-- proxy_pool
             |-- ip_spider.py
             |-- parse_html.py
```
##### 主入口：main.py     
       提供通过歌单来爬取及更新数据库歌曲信息的函数：run()     
       提供检查数据库数据详情的函数：schemas_info()
       
##### 爬取模块：NetEaseMusicCloudSpider.py  
       提供获取某风格热门歌单的函数：search_playlist()  
       提供获取某歌单中所有歌曲id的函数：get_music_list()  
       提供获取某歌曲评论数量的函数：get_music_comment()  
       提供获取某歌曲信息的函数：get_music_info()
       
##### 数据库操作模块：control_db.py  
       完成对数据库的连接及操作，提供session实例  
       提供对数据库建表的函数：init_db()  
       
##### 数据储存模型：models.py  
       PlayList：歌单数据表，作为爬虫目标歌单的临时储存  
       DzMusic：电子风格数据表  
       ACGMusic：ACG风格数据表
       
##### 爬虫头部定义模块：headers.py  
       提供十几种User-Agent定义
       
##### 装饰器：decorator.py  
       提供异常重试装饰器：retry()
       
##### 代理池：proxy_pool
```
   ip_spider.py
       代理池爬虫，目前提供两个代理ip网站的爬取
   parse_html.py
       为代理池爬虫提供网页解析及头部定义
```            
