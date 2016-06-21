#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
login weibo by user and get utils
"""
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from common import CHROME_DRIVER_PATH

def weibo_login():
    """
    show login page and ask user to enter psd and usr to login
    :return: utils
    """
    driver = Chrome(executable_path=CHROME_DRIVER_PATH)
    driver.get("http://weibo.com")
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "W_nologin_logo"))
        )
    except Exception as e:
        print e
    else:
        print u"请在登陆页面上进行登陆操作, 之后再文件夹下寻找cookies文件"
        retcode = 1 if raw_input(u"登陆成功?(Y/N)") == 'Y' else 0
        return retcode, driver.get_cookies()
    finally:
        driver.quit()
