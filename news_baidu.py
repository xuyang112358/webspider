import requests
from lxml import etree
from random_proxy import get_proxy
from random_agent import get_agent
import random

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













