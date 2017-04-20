""" 知乎用户爬虫(API版) """

__author__ = 'Cichar'
__version__ = '0.1'

from datetime import datetime
from time import sleep

from spider import BaseSpider
from models import ZhiHuUserInfo
from decorator import retry


class ZhiHuSpider(BaseSpider):

    def __init__(self):
        super().__init__()
        # 关注者和被关注者查询参数
        self.follow_arg = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,' \
                          'is_following,badge[?(type=best_answerer)].topics'
        # 用户信息查询参数
        self.user_arg = 'locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,' \
                        'following_count,cover_url,following_topic_count,following_question_count,' \
                        'following_favlists_count,following_columns_count,avatar_hue,answer_count,articles_count,' \
                        'pins_count,question_count,commercial_question_count,favorite_count,favorited_count,' \
                        'logs_count,marked_answers_count,marked_answers_text,message_thread_token,account_status,' \
                        'is_active,is_force_renamed,is_bind_sina,sina_weibo_url,sina_weibo_name,show_sina_weibo,' \
                        'is_blocking,is_blocked,is_following,is_followed,mutual_followees_count,vote_to_count,' \
                        'vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,' \
                        'participated_live_count,allow_message,industry_category,org_name,org_homepage,' \
                        'badge[?(type=best_answerer)].topics'

    def get_user_info(self, user_token=None, updata=False):
        """
        
        获取用户信息
        http://www.zhihu.com/api/v4/members/{url_token}?include={user_arg}
        
        """

        user_info_url = 'http://www.zhihu.com/api/v4/members/{url_token}?include={user_arg}'
        sleep(0.5)
        try:
            data = self.parse_url(url=user_info_url.format(url_token=user_token, user_arg=self.user_arg),
                                  header='zhihu', parse_json=True)
            if data:
                # url_token
                url_token = data.get('url_token')
                if not url_token:
                    print('该用户为非法用户')
                    return

                # 昵称
                name = data['name']
                # headline
                headline = data.get('headline', '')
                # 居住地
                location = data.get('locations', '')
                if location:
                    location = data['locations'][0]['name']
                else:
                    location = ''
                # 个人简介
                description = data.get('description', '')
                # 获得的赞同
                voteup_count = data.get('voteup_count', '')
                # 获得的感谢
                thanked_count = data.get('thanked_count', '')
                # 获得的收藏
                favorited_count = data.get('favorited_count', '')
                # 公共编辑
                logs_count = data.get('logs_count', '')
                # 知乎收录
                question_count = data.get('question_count', '')
                # 被关注者
                follower_count = data.get('follower_count', '')
                # 关注者
                following_count = data.get('following_count', '')
                # 所在行业
                business = data.get('business', '')
                if business:
                    business = data['business']['name']

                # 职业经历
                employment, company = data.get('employments', ''), data.get('employments', '')
                if employment:
                    employment = data['employments'][0].get('company', '')
                    if employment:
                        employment = data['employments'][0]['company']['name']
                else:
                    employment = ''
                if company:
                    company = data['employments'][0].get('job', '')
                    if company:
                        company = data['employments'][0]['job']['name']
                else:
                    company = ''

                if updata:
                    user = self.db.session.query(ZhiHuUserInfo).filter_by(url_token=url_token).first()
                    if user:
                        user.headline = headline
                        user.location = location
                        user.description = description
                        user.voteup_count = voteup_count
                        user.thanked_count = thanked_count
                        user.favorited_count = favorited_count
                        user.logs_count = logs_count
                        user.question_count = question_count
                        user.follower_count = follower_count
                        user.following_count = following_count
                        user.business = business
                        user.employment = employment
                        user.company = company
                        user.update_time = datetime.utcnow()
                        self.db.session.commit()
                        print('更新用户 --> %s' % name)
                        return
                    else:
                        new_user = ZhiHuUserInfo(name=name, headline=headline, location=location,
                                                 description=description, voteup_count=voteup_count,
                                                 thanked_count=thanked_count, favorited_count=favorited_count,
                                                 logs_count=logs_count, question_count=question_count,
                                                 url_token=url_token, follower_count=follower_count,
                                                 following_count=following_count, business=business,
                                                 employment=employment,  company=company, update_time=datetime.utcnow())
                        self.db.session.add(new_user)
                        self.db.session.commit()
                        print('创建用户 --> %s' % name)
                        return
                else:
                    new_user = ZhiHuUserInfo(name=name, headline=headline, location=location, description=description,
                                             voteup_count=voteup_count, thanked_count=thanked_count,
                                             favorited_count=favorited_count, logs_count=logs_count,
                                             question_count=question_count, url_token=url_token,
                                             follower_count=follower_count, following_count=following_count,
                                             business=business, employment=employment, company=company,
                                             update_time=datetime.utcnow())
                    self.db.session.add(new_user)
                    self.db.session.commit()
                    print('创建用户 --> %s' % name)
                    return
            else:
                print('** get_user_info : 未获取到数据 **')
                return
        except Exception as e:
            print('** get_user_info : %s **' % str(e))

    @retry
    def get_followers(self, user_token=None, url=None, updata=False):
        """ 
        
        获取被关注者 
        http://www.zhihu.com/api/v4/members/{url_token}/followers?include={follow_arg}&offset={offset}&limit={limit}
        
        """

        follower_url = 'http://www.zhihu.com/api/v4/members/{url_token}/followers?include={follow_arg}&offset={offset}&limit={limit}'
        sleep(0.5)
        try:
            if user_token:
                followers = self.parse_url(url=follower_url.format(url_token=user_token, follow_arg=self.follow_arg,
                                                                   offset=0, limit=20), header='zhihu', parse_json=True)
            else:
                followers = self.parse_url(url=url, header='zhihu', parse_json=True)
            if followers:
                if followers.get('data'):
                    for follower in followers.get('data'):
                        url_token = follower.get('url_token', '')
                        if url_token:
                            # 默认包含更新数据
                            if updata:
                                self.get_user_info(user_token=url_token)
                                return
                            else:
                                user = self.db.session.query(ZhiHuUserInfo).filter_by(url_token=url_token).first()
                                if user:
                                    return
                                else:
                                    self.get_user_info(user_token=url_token, updata=updata)
                                return
                        else:
                            return
                # 递归
                if 'paging' in followers.keys() and followers.get('paging').get('is_end') is False:
                    url = followers.get('paging').get('next')
                    self.get_followers(url=url)
                    return
            else:
                print('** get_followers : 解析失败 **')
                return
        except Exception as e:
            print('** get_followers : %s **' % str(e))
            raise Exception(e)

    @retry
    def get_following(self, user_token=None, url=None, updata=False):
        """ 
        
        获取关注者
        https://www.zhihu.com/api/v4/members/{url_token}/followees?include={follow_arg}&offset={offset}&limit={limit}
        
        """

        following_url = 'http://www.zhihu.com/api/v4/members/{url_token}/followees?include={follow_arg}&offset={offset}&limit={limit}'
        sleep(0.5)
        try:
            if user_token:
                followings = self.parse_url(url=following_url.format(url_token=user_token, follow_arg=self.follow_arg,
                                                                     offset=0, limit=20), header='zhihu',
                                            parse_json=True)
            else:
                followings = self.parse_url(url=url, header='zhihu', parse_json=True)
            if followings:
                if followings.get('data'):
                    for following in followings.get('data'):
                        url_token = following.get('url_token', '')
                        if url_token:
                            # 默认包含更新数据
                            if updata:
                                self.get_user_info(user_token=url_token)
                                return
                            else:
                                user = self.db.session.query(ZhiHuUserInfo).filter_by(url_token=url_token).first()
                                if user:
                                    return
                                else:
                                    self.get_user_info(user_token=url_token, updata=updata)
                                return
                        else:
                            return
                # 递归
                if 'paging' in followings.keys() and followings.get('paging').get('is_end') is False:
                    url = followings.get('paging').get('next')
                    self.get_following(url=url)
                    return
            else:
                print('** get_following : 解析失败 **')
                return
        except Exception as e:
            print('** get_following : %s **' % str(e))
            raise Exception(e)

    def get_start(self, user_token=None, updata=False):
        """ 爬虫启动 """

        if not user_token:
            crawl_user = self.db.session.query(ZhiHuUserInfo).filter_by(crawl_flag=None or False).first()
            crawl_user.crawl_flag = True
            self.db.session.commit()
            user_token = crawl_user.url_token
        try:
            self.get_user_info(user_token=user_token)
            self.get_following(user_token=user_token, updata=updata)
            self.get_followers(user_token=user_token, updata=updata)

            # 取一个没有爬过的用户
            crawl_user = self.db.session.query(ZhiHuUserInfo).filter_by(crawl_flag=None or False).first()

            crawl_user.crawl_flag = True
            self.db.session.commit()
            url_token = crawl_user.url_token

            # print('** 开始分析 : %s **' % url_token)
            self.get_start(user_token=url_token)
        except Exception as e:
            print('** get_start : %s **' % str(e))
