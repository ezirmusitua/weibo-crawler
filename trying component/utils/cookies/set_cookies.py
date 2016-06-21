#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
set utils for selenium or requests
"""

import time
import requests
from common import WAIT_FOR_LOADED


def set_cookies_for_selenium(driver, host, cookies):
    """
    set utils for selenium webdriver
    :param driver: webdriver instance
    :param host: utils of specific site
    :param cookies: utils list
    :return: None
    """
    # we need to open host at first in order to set utils for selenium webdriver
    driver.get(host)
    # wait for page loaded
    time.sleep(WAIT_FOR_LOADED)
    for cookie in cookies:
        driver.add_cookie(cookie)


def set_cookies_for_requests(session, cookies):
    """
    add utils to session's cookie-jar
    :param session: session instance
    :param cookies: utils of specific site
    :return: None
    """
    requests.utils.add_dict_to_cookiejar(session.cookies, cookies)

