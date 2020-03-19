#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:Administrator
@file: 1_login_qcc.py
@time: 2020/03/{DAY}
"""
import selenium
from selenium import webdriver
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


def login():
    options = Options()
    # 不能隐藏浏览器，会被检测到，要求登入账号
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    # options.add_argument(
    #     '--user-agent="Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"')
    # driver = selenium.webdriver.Chrome(options=options)
    # 等待时间
    # driver.implicitly_wait(5)
    # driver.delete_all_cookies()


    # 实例化driver
    driver = webdriver.Chrome()
    # driver = webdriver.Firefox()
    # driver.maximize_window()
    time.sleep(3)
    driver.get('https://www.qcc.com')
    time.sleep(3)
    try:
        # 页面一直循环，直到 id="myDynamicElement" 出现
        print(1)
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "myDynamicElement"))
        )
    finally:


        # 去除介绍界面，进入登录界面
        driver.find_element_by_class_name("tep1").click()
        time.sleep(3)
        # driver.find_element_by_xpath('//div[@class="login-panel-head clearfix"]/div[2]').click()

        # 选择密码登录模式
        driver.find_element_by_id("normalLogin").click()
        time.sleep(5)

        # 输入帐号密码
        driver.find_element_by_id("nameNormal").send_keys("13536020881")
        time.sleep(3)
        driver.find_element_by_id("pwdNormal").send_keys("123456789")
        time.sleep(3)

        # 滑动条定位
        start = driver.find_element_by_xpath('//div[@id="nc_2__scale_text"]/span')
        # 长按拖拽
        action = ActionChains(driver)
        # 长按
        action.click_and_hold(start)
        # 拉动
        action.drag_and_drop_by_offset(start, 308, 0).perform()
        time.sleep(3)

        # 登录
        driver.find_element_by_xpath('//form[@id="user_login_normal"]/button').click()
        time.sleep(2)

        # 获取cookies
        cookies = {i["name"]:i["value"] for i in driver.get_cookies()}
        print(cookies)

        # 关闭浏览器
        # driver.quit()


if __name__ == '__main__':
    login()
