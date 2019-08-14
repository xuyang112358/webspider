from selenium import webdriver
import json
import time
import os
from urllib.parse import urlencode
import re


def get_cookie_from_network():
    url = 'https://sso.toutiao.com/'
    driver = webdriver.Chrome()
    driver.get(url)
    driver.find_element_by_xpath('//*[@id="login-type-account"]').click()  # 切换账号密码登录
    driver.find_element_by_xpath('//*[@id="user-name"]').send_keys('???????')  # 改成你的账号
    driver.find_element_by_xpath('//*[@id="password"]').send_keys('??????????')  # 改成你的密码
    driver.find_element_by_xpath('//*[@id="bytedance-login-submit"]').click()  # 点击登录
    time.sleep(10)  #此处需要改成自动识别验证码
    if not os.path.exists('cookies'):
        os.mkdir('cookies')
    # 获得 cookie信息
    cookie_list = driver.get_cookies()
    driver.close()
    cookie_dict = {}
    for cookie in cookie_list:
        f = open('cookies\\'+cookie['name'] + '.json', 'w')
        json.dump(cookie, f)
        f.close()
        cookie_dict[cookie['name']] = cookie['value']

    return cookie_dict


