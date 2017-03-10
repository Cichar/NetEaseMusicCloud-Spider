from urllib.request import urlopen, Request

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    # 'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    }


def get_html(url=None, cookie=None):
    """
    
    :param cookie: None
    :param url: 待解析的代理网页 
    :return: 解析后的html结构
    
    """

    if cookie:
        headers['Cookie'] = cookie
    req = Request(url, headers=headers)
    response = urlopen(req)
    html = response.read().decode('utf-8', 'ignore')
    return html
