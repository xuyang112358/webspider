from selenium import webdriver
import json
import time
import os

# 破解验证码用
from urllib.parse import urlencode
import re
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

def get_cookie_from_network():
    url = 'https://sso.toutiao.com/'
    driver = webdriver.Chrome()
    driver.get(url)
    driver.find_element_by_xpath('//*[@id="login-type-account"]').click()  # 切换账号密码登录
    driver.find_element_by_xpath('//*[@id="user-name"]').send_keys('****')  # 改成你的账号
    driver.find_element_by_xpath('//*[@id="password"]').send_keys('****')  # 改成你的密码
    driver.find_element_by_xpath('//*[@id="bytedance-login-submit"]').click()  # 点击登录
    #手动滑动验证码
    time.sleep(10)

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


