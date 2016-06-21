#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
test can cookies got from weibo_login are usable
"""
import codecs
import json
import unittest

import requests
from selenium.webdriver import Chrome
from weibo_crawler.utils.cookies import set_cookies_for_selenium, set_cookies_for_requests
from weibo_crawler.utils.cookies import save_wb_cookies_for_selenium, save_wb_cookies_for_requests

from weibo_crawler.utils.cookies.common import CHROME_DRIVER_PATH


class TestCookiesUtils(unittest.TestCase):
    def setUp(self):
        self.test_driver  = Chrome(executable_path=CHROME_DRIVER_PATH)
        self.test_session = requests.Session()
        self.test_url     = r"http://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=100206&" \
                            r"refer_flag=0000010005_&is_hot=1&pagebar=0&" \
                            r"pl_name=Pl_Official_MyProfileFeed__28&" \
                            r"id=1002061642591402&script_uri=/entpaparazzi&feed_type=0&page=1&pre_page=1&" \
                            r"domain_op=100206&__rnd=1458444020278"
        self.sel_cookies  = r"F:\Desktop\Graduation-Project\weibo_crawler\utils\cookies\selenium-cookies.json"
        self.req_cookies  = r"F:\Desktop\Graduation-Project\weibo_crawler\utils\cookies\requests-cookies.json"

    def test_set_selenium_cookie_and_usable(self):
        with codecs.open(self.sel_cookies, 'rb', 'utf-8') as rf:
            cookies = json.load(rf)
        set_cookies_for_selenium(self.test_driver, "http://weibo.com", cookies)
        self.test_driver.get(self.test_url)
        self.assertTrue(self.test_driver.page_source.find("W_nologin_logo") == -1)

    def test_set_requests_cookies_and_usable(self):
        with codecs.open(self.req_cookies, 'rb', 'utf-8') as rf:
            cookies = json.load(rf)
        set_cookies_for_requests(self.test_session, cookies)
        response = self.test_session.get(self.test_url)
        self.assertTrue(response.content.find("W_nologin_logo") == -1)
        pass

    def tearDown(self):
        self.test_driver.quit()
        pass


if __name__ == '__main__':
    unittest.main()