#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Utils for crawler
"""
import os
import sys
import time
import json
import codecs
import random
import requests
from errors import *

def _load_headers(path):
    """
    load session from path
    @param path: path of headers.json
    @return: a headers dict
    """
    if os.path.isfile(path):
        with codecs.open(path, "rb", "utf-8") as rf:
            try:
                headers = json.load(rf)
            except Exception:
                return NOT_JSON_FILE
            else:
                return headers
    else:
        return NOT_VAILDATE_FILE

def set_headers(session, path):
    """
    set headers from path for session
    @param session: a requests.Session object
    @path path: path of headers.json
    @return: None
    """
    if not (hasattr(session, "headers")):
        print "Session has no attribute, check it!"
        return NO_ATTRIBUTE
    headers = _load_headers(path)
    session.headers.update(headers)


url_pattern = "http://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=100505&id=100505{uid}&page={page}&__rnd={now}"

def url_generator(uid, max_page_count=10):
    """
    use uid to generate max page count url generator
    @param uid: uid of weibo
    @param max_page_count: max count of page
    @return: a generator
    """
    for i in xrange(1, max_page_count):
        yield url_pattern.format(uid=uid, page=i, now=int(time.time() * 1000))
        
def sleep(min=0.01, max=0.55):
    """
    sleep a random number from min to max
    @param min: floor
    @param max: ceil
    @return: None
    """
    secs  = random.uniform(min, max)
    time.sleep(secs)

def set_proxies(session, path="./proxies.json"):
    """
    Random choice proxy and set for session
    @param session: Requests session
    @param path: path of proxies file
    @return: None
    """ 
    test_url = "http://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=100505&id=1005051708922835&page=4&__rnd=1461508446878"
    with codecs.open(path, 'rb', 'utf-8') as rf:
        proxies_list = json.load(rf)
        while True:
            proxies = random.choice(proxies_list)
            try:
                requests.get(test_url, proxies=proxies, timeout=10)
            except Exception as e:
                print "remove: ", proxies
                proxies_list.remove(proxies)
                continue 
            else:
                print "Set proxies: ", proxies
                session.proxies.update(proxies)
                break
    with codecs.open(path, 'wb', 'utf-8') as wf:
        json.dump(proxies_list, wf)