import requests
from lxml import etree
import os
# 抓取壁纸网站源码
url = 'http://www.netbian.com/'
header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}
response = requests.get(url,headers=header)
data_w = response.content.decode('gbk')
with open('simple_crawl_picture.html','w',encoding='gbk') as f:
    f.write(data_w)
# 抓取图片url
html = etree.parse('simple_crawl_picture.html',etree.HTMLParser())
pic_url = html.xpath('//li/a[not(contains(@title,"日历"))]/img/@src')
# 创建图片保存目录
savepath = "./photo"
if not os.path.exists(savepath):
    os.makedirs(savepath)
# 保存图片
i=1
for single_pic in pic_url:
    pic = requests.get(single_pic,headers=header)
    with open(savepath+'/%d.jpg'%i,'wb') as f:
        f.write(pic.content)
        i+=1



