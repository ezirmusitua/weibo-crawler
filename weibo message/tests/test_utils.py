#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
sys.path.append('../components')
import re
import unittest

from errors import *
from utils import _load_headers, set_headers  
from utils import url_generator
from utils import sleep

class Session1(object):
    headers = dict()

class Session2(object):
    headers = list()

class Session3(object):
    header  = dict()


class TestHeaders(unittest.TestCase):
    def setUp(self):
        self.right_headers    = r'resources/headers.json'
        self.un_exist_headers = r'resources/un_exist.json'
        self.not_json_headers = r'resources/not_json.json'
        self.headers          = {u"hello": u"world"}
        self.url_pattern      = "http:\/\/weibo.com\/p\/aj\/v6\/mblog\/mbloglist\?ajwvr=6&domain=100505&id=1005055891170011&page=\d+&__rnd=\d+"                            
        self.uid              = "5891170011"
        
    def tearDown(self):
        pass
    
    def test_load_header(self):
        """
        1. exist and json: return dict
        2. not exist: return NO_HEADERS_FILE
        3. not json: return HEADER_FILE_IS_NOT_JSON
        """  
        self.assertIsInstance(_load_headers(path=self.right_headers), 
                              dict, "Return wrong type")
        self.assertTrue(_load_headers(path=self.un_exist_headers) == NO_HEADERS_FILE, 
                        "File un-exist")
        self.assertTrue(_load_headers(path=self.not_json_headers) == NOT_JSON_FILE, 
                        "Not a json file")
    
    def test_set_header(self):
        """
        1. update headers
        1. session has no headers
        2. headers should set for a dict
        """
        self.assertEqual(set_headers(Session3(), self.right_headers), NO_ATTRIBUTE, 
                         "No headers attribute")
        self.assertEqual(set_headers(Session2(), self.right_headers), WRONG_TYPE, 
                         "Wrong type (not dict)")
        tmp = Session1()
        set_headers(tmp, self.right_headers)
        self.assertTrue(tmp.headers['hello'] == self.headers['hello'], 
                         "Error result")
    
    def test_url_generator(self):
        """
        return value should match url pattern
        """
        for url in url_generator(self.uid):
            res = re.match(self.url_pattern, url)
            self.assertTrue(res)
        
         
