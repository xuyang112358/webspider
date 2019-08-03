import requests
import re
import random
import time
##############
from random_agent import get_agent


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

