import requests
from urllib.parse import urlencode
from requests import codes
import os     #路径
from hashlib import md5    #摘要算法（哈希）
from multiprocessing.pool import Pool
import re
import re,string
from auto_cookie import get_cookie_from_network


proxy = {
    'http':'117.90.137.72:9000'
}
def get_page(offset):   #获取网页json文本
    params = {
        'aid':'24',
        'app_name':'web_search',
        'offset': offset,
        'format': 'json',
        'keyword': '街拍图片',
        'autoload': 'true',
        'count': '20',
        'en_qc': '1',
        'cur_tab ': '1',
        'from': 'search_tab',
        'pd': 'synthesis'
    }
    base_url = 'https://www.toutiao.com/api/search/content/?'
    url = base_url + urlencode(params)
    headers={
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'referer': 'https://www.toutiao.com/',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    }
    try:
        response = requests.get(url=url,headers=headers,proxies=proxy,cookies=get_cookie_from_network())
        if 200  == response.status_code:
            print('访问成功')
            return response.json()
    except requests.ConnectionError:
        return print('访问失败')

def get_images(json):   #获取图片来源
    print(json)     #观察data键里是否有值
    if json.get('data'):
        for item in json.get('data'):
            title = item.get('title')
            images = item.get('image_list')
            print(images)
            if images == None:
                continue
            for image in images:
                yield {
                    'title': title,
                    'image': image.get('url')
                }
    else:
        print('data里没有值')

def save_image(item):   #图片写入
    s = item.get('title')
    image = item.get('image')
    title = re.sub('[%s]' % re.escape(string.punctuation), '', s)
    if not os.path.exists(title):
        os.mkdir(title)
    try:
        response = requests.get(image)
        if response.status_code == 200:
            pic_path = '{file}\{pic}.jpg'.format(file=title,pic=md5(response.content).hexdigest())
            if not os.path.exists(pic_path):
                with open(pic_path, 'wb') as f:
                    f.write(response.content)
            else:
                print('图片已存在')
    except requests.ConnectionError:
        print('图片下载失败')

def main(offset):
    json = get_page(offset)
    for item in get_images(json):
        save_image(item)



if __name__ == '__main__':
    pool = Pool()     #pool=Pool(5)创建拥有5个进程数量的进程池,默认计算机能力范围
    groups = ([x * 20 for x in range(1, 6)])     #列表解析
    pool.map(main, groups)
    pool.close()    #关闭进程池，不再接受新的进程
    pool.join()     #主进程阻塞等待子进程的退出
