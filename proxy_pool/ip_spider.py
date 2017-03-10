from bs4 import BeautifulSoup
import re

from parse_html import get_html


class IpSpider:
    """
    
    通过爬取代理ip网站获取ip：port键值对
    
    """

    @staticmethod
    def get_proxy_ip_first():
        """ 
        
        西刺代理
        -------
        透明：'http://www.xicidaili.com/nt/1'
        
        """

        html = get_html(url='http://www.xicidaili.com/nt/1')

        # bs4解析表格
        soup = BeautifulSoup(html, 'html.parser')
        trs = soup.find_all(name='tr')
        for tr in trs[2:]:
            tds = tr.find_all('td')
            if tds[5].getText() == 'HTTP':
                ip, port = tds[1].getText(), tds[2].getText()
                print('{0}:{1}'.format(ip, port))

    @staticmethod
    def get_proxy_ip_second(ip_num=80):
        """
        
        66代理
        ---------
        代理：http://m.66ip.cn/mo.php?sxb=&tqsl={}&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=
        
        :return: 
        
        """

        html = get_html(url='http://m.66ip.cn/mo.php?sxb=&tqsl={}&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea='.format(ip_num))
        for ip_port in re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', html):
            print(ip_port)


if __name__ == '__main__':
    spider = IpSpider()
    spider.get_proxy_ip_first()
    #spider.get_proxy_ip_second()



