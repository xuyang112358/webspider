import requests
from lxml import etree
import os
import threading
import time
import random_agent

nMaxThread = 3
lock = threading.BoundedSemaphore(nMaxThread)


class MyThread(threading.Thread):
    def __init__(self, url, header, page):
        threading.Thread.__init__(self)
        self.url = url
        self.header = header
        self.page = page

    def run(self):

        try:
            # 访问网站
            response = requests.get(self.url, headers=self.header)
            data_w = response.content.decode('gbk')

            # 存储网站url
            pic_html = '%s.html' % (self.page)
            with open(pic_html, 'w', encoding='gbk') as f:
                f.write(data_w)

            # 爬取图片url
            html = etree.parse(pic_html, etree.HTMLParser())
            self.pic_url = html.xpath('//li/a[not(contains(@title,"日历"))]/img/@src')
            self.title = html.xpath('//li/a[not(contains(@title,"日历"))]/img/@alt')
            # 下载图片
            self.save_Pic()
        finally:
            lock.release()

    def save_Pic(self):

        # 创建图片保存目录
        savepath = "./page {page}'s photos".format(page=str(self.page))
        if not os.path.exists(savepath):
            os.makedirs(savepath)
        # 保存图片
        for i in range(len(self.pic_url)):
            pic = requests.get(self.pic_url[i], headers=self.header)
            with open(savepath + '/%s.jpg' % (str(self.title[i])), 'wb') as f:
                f.write(pic.content)


def main():
    # 抓取壁纸网站源码
    url = 'http://www.netbian.com/index_{page}.htm'
    header = random_agent.get_agent()
    num = input("请输入要爬取的页数：")
    #单独抓取第一页
    lock.acquire()
    end_url = 'http://www.netbian.com/index.htm'
    thread = MyThread(end_url, header, '1')
    thread.start()
    for page in range(2, int(num)+1):
        lock.acquire()
        end_url = url.format(page=str(page))
        thread = MyThread(end_url, header, str(page))
        thread.start()


if __name__ == '__main__':
    main()
