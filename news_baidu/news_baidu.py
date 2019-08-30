import requests
from lxml import etree
import random
import re

def get_proxy(page):
    # 从快代理抓取网页信息
    base_url = 'https://www.kuaidaili.com/free/inha/{pages}/'
    proxies = []

    for page in range(1,page):
        url = base_url.format(pages=str(page))
        # 获取随机agent
        header = get_agent()
        response = requests.get(url, headers=header)
        data = response.content.decode()
        # 解析出网页中的ip和端口数据
        # <td data-title="IP">60.191.57.78</td>
        para1 = re.compile('"IP">(.+)</td>')
        finaip = re.findall(para1, data)
        para2 = re.compile('"PORT">(.+)</td>')
        finaport = re.findall(para2, data)

        for ip, port in zip(finaip, finaport):
            proxy = {}
            fina_url = 'http://' + ip + ':' + port
            proxy['http'] = fina_url
            print(fina_url)
            #验证url是否能用
            test_url = 'https://www.baidu.com/'
            header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
            }
            response = requests.get(test_url, headers=header, proxies=proxy)
            if (response.status_code != 200):
                continue
            ###############
            proxies.append(proxy)
    # 返回代理数组
    return proxies

def get_agent():
    user_agent_list = [
        {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'},
        {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'},
        {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},
        {'User-Agent':'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50'}
    ]

    usr = random.choice(user_agent_list)
    return usr

if __name__ == '__main__':

    header = get_agent()
    proxies = get_proxy(2)
    proxy = random.choice(proxies)
    url = 'https://news.baidu.com/'

    response = requests.get(url,headers=header,proxies=proxy)
    data = response.content.decode('utf8')
    #存取信息
    with open('news_baidu.html','w',encoding='utf8') as fw:
        fw.write(data)

    html = etree.parse('./news_baidu.html',etree.HTMLParser())
    result = html.xpath('//a[@target="_blank"]/text()')

    i=1
    for data in result:
        if data!='\r\n':
            print(str(i)+':'+data)
            i+=1













