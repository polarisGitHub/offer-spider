# -*- coding: utf-8 -*-

import time
import json
import requests
from selenium import webdriver
from pymongo import MongoClient

# 只能爬63页，按分类来
catalog = {
    "移动互联网": "https://www.lagou.com/gongsi/252-0-24.json",
    "电子商务": "https://www.lagou.com/gongsi/252-0-25.json",
    "金融": "https://www.lagou.com/gongsi/252-0-33.json",
    "企业服务": "https://www.lagou.com/gongsi/252-0-27.json",
    "教育": "https://www.lagou.com/gongsi/252-0-29.json",
    "文化娱乐": "https://www.lagou.com/gongsi/252-0-45.json",
    "游戏": "https://www.lagou.com/gongsi/252-0-31.json",
    "O2O": "https://www.lagou.com/gongsi/252-0-28.json",
    "硬件": "https://www.lagou.com/gongsi/252-0-47.json"
}

# 去除 chrome正受到自动测试软件的控制
option = webdriver.ChromeOptions()
option.add_argument('disable-infobars')

# 获取cookie
browser = webdriver.Chrome()
browser.get("https://www.lagou.com/")
cookies = list(map(lambda c: c["name"] + "=" + c["value"], browser.get_cookies()))
cookie = "; ".join(cookies)
browser.close()

header = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://www.lagou.com",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,mt;q=0.6",
    "Referer": "https://www.lagou.com/gongsi/252-0-0",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36",
    "X-Anit-Forge-Code": "0",
    "X-Anit-Forge-Token": "None",
    "Cookie": cookie
}
form = {
    "first": "false",
    "pn": 1,
    "sortField": 0,
    "havemark": 0
}

client = MongoClient('localhost', 27017)
db = client['lagou']
collection = db['company']

for key in catalog:
    for i in range(1, 64):
        form["pn"] = i
        r = requests.post(catalog[key], headers=header, data=form)
        print(key, "pn", i, r.text)
        data = json.loads(r.text)
        result = data["result"]
        if result:
            collection.insert(result)
        else:
            break
        time.sleep(2)

client.close()
