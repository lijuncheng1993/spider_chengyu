#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:Administrator
@file: 2_spider_qcc.py
@time: 2020/03/{DAY}
"""
from selenium import webdriver
import time
import json
import re
from lxml import etree
import requests
from selenium.webdriver import ActionChains


def run():
    selector = etree.HTML(res)
    urls = re.findall(r'<a onclick="utLoginInterceptor.*? href="(.*?)" target="_blank" class="ma_h1"', res,
                      re.S)  # 匹配url
    try:
        print('识别出滑动界面')
        url_fail = re.findall("<script>window.location.href='(.*?)';</script>", res, re.S)
        url_fail=url_fail[0]
        # driver.maximize_window()
        time.sleep(3)
        driver.get(url_fail)
        time.sleep(2)
        print('开始滑动')
        # 滑动条定位
        start = driver.find_element_by_xpath('//div[@id="nc_1__scale_text"]/span')
        # 长按拖拽
        action = ActionChains(driver)
        # 长按
        action.click_and_hold(start).perform()
        # 拉动
        action.drag_and_drop_by_offset(start, 400, 0).perform()
        time.sleep(3)

    except Exception as e:
        for url in urls:
            url_new = 'https://www.qcc.com/' + url
            print(url_new)

        print('*' * 100)


def getHTML(url_new):
    print(333)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
    response = requests.get(url_new, headers=headers)
    if response.status_code == 200:
        return response.text
    return None


def ParsePage(text):
    print('采集信息')
    selector = etree.HTML(text)  # 构造了一个XPath解析对象并对HTML文本进行自动修正。
    Enterprise_name = selector.xpath('normalize-space(//div[@class="row title jk-tip"]/h1/text())')  # 匹配企业名称
    Representative_person = selector.xpath('normalize-space(//div[@class="bpen"]/a/h2/text())')  # 匹配法定代表人
    Status = selector.xpath('normalize-space(//*[@id="Cominfo"]/table/tr[1]/td[4]/text())')  # 匹配经营状态
    Build_date = selector.xpath('normalize-space(//*[@id="Cominfo"]/table/tr[1]/td[6]/text())')  # 匹配成立日期
    Registered_mon = selector.xpath('normalize-space(//*[@id="Cominfo"]/table/tr[2]/td[2]/text())')  # 注册资本
    Total_mon = selector.xpath('normalize-space(//*[@id="Cominfo"]/table/tr[2]/td[4]/text())')  # 实缴资本
    Com_num = selector.xpath('normalize-space(//*[@id="Cominfo"]/table/tr[3]/td[6]/text())')  # 匹配工商注册号
    Taxpayer_num = selector.xpath('normalize-space(//*[@id="Cominfo"]/table/tr[4]/td[2]/text())')  # 匹配纳税人识别号
    Registered_address = selector.xpath('normalize-space(//*[@id="Cominfo"]/table/tr[8]/td[2]/text())')  # 匹配企业地址
    Business_scope = selector.xpath('normalize-space(//*[@id="Cominfo"]/table/tr[9]/td[2]/text())')  # 匹配经营范围

    # Enterprise_name = selector.xpath('//div[@class="clear"]/div[@class=""]/h1/text()')  # 匹配企业名称
    # Representative_person = selector.xpath('//div[@class="bpen"]/a/h2/text()')  # 匹配法定代表人
    # Chairman = selector.xpath('//*[@id="kcbBase"]/table/tr[1]/td[4]/text()')  # 匹配董事长
    # Build_date = selector.xpath('//*[@id="kcbBase"]/table/tr[2]/td[2]/text()')  # 匹配成立日期
    # Registered_address = selector.xpath('//*[@id="kcbBase"]/table/tr[3]/td[2]/text()')  # 匹配注册地址
    # Business_scope = selector.xpath('//*[@id="kcbBase"]/table/tr[4]/td[2]/text()')  # 匹配经营范围

    data = [Enterprise_name, Representative_person, Status, Build_date, Registered_mon, Total_mon, Com_num,
            Taxpayer_num,
            Registered_address, Business_scope]
    # print(data)
    saveFile(data)


def saveFile(data):
    print('上传信息')
    with open(r'QCC.json', 'a', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False) + '\n\n')


if __name__ == '__main__':

    # 打开企查查登录网页
    driver = webdriver.Chrome()
    url = "https://www.qcc.com/search?key={}"
    proxy = {
        'http': '221.6.32.206:41816',
        'http1': '221.6.32.206:41816'
    }

    headers = {"Accept": "application/json, text/javascript",
               "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
               "Cookie": "cy=1; cye=shanghai; _lxsdk_cuid=16ca41d3344c8-050eb4ac8f1741-4d045769-1fa400-16ca41d3345c8; _lxsdk=16ca41d3344c8-050eb4ac8f1741-4d045769-1fa400-16ca41d3345c8; _hc.v=38ae2e43-608f-1198-11ff-38a36dc160a4.1566121473; _lxsdk_s=16ce7f63e0d-91a-867-5a%7C%7C20; s_ViewType=10"
               }

    option = webdriver.ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_argument('--disable-infobars')  # 禁用浏览器正在被自动化程序控制的提示
    # option.add_argument(
    #     '--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"')
    # driver = webdriver.Chrome(options=option)

    # from fake_useragent import UserAgent
    # ua = UserAgent()
    # headers = {'User-Agent': ua.random}
    # print(headers)
    for name in ['华为', '欧特', '美的', '苹果']:
        urls = url.format(name)
        # driver.get(urls)
        # print(urls)
        res = requests.get(urls, headers=headers).content.decode()
        print(res)
        print('*' * 100)
        # # 加载时间
        time.sleep(5)
        run()
