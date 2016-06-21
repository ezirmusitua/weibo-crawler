#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
save utils as json file accord to selenium or requests
"""
import json
import codecs
from common import COOKIES_PATH


def save_wb_cookies_for_selenium(cookies,
                                     filename=COOKIES_PATH + "selenium-utils.json"):
    """
    save weibo utils use for selenium webdriver , save at a json file
    :param cookies: site's cookie
    :param filename: json filename
    :return: None
    """
    cookies_before_clean = cookies
    cookies_after_clean  = []
    for cookie in cookies_before_clean:
        if '.weibo.com' == cookie['domain']:
            cookies_after_clean.append(cookie)
        else:
            continue
    with codecs.open(filename, 'wb', 'utf-8') as cwf:
        json.dump(cookies_after_clean, cwf)


def save_wb_cookies_for_requests(cookies,
                              filename=COOKIES_PATH + "requests-utils.json"):
    """
    save weibo utils for requests, save at a json file
    :param cookies: utils of the site
    :param filename: json filename
    :return: None
    """
    cookies_before_clean = cookies
    cookies_after_clean  = dict()
    for cookie in cookies_before_clean:
        cookies_after_clean[cookie['name']] = cookie['value']
    with codecs.open(filename, 'wb', 'utf-8') as cwf:
        json.dump(cookies_after_clean, cwf)

