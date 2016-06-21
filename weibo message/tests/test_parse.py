#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
sys.path.append('../components')
import re
import unittest
from components.parse import parse

class TestParse(unittest.TestCase):
    def setUp(self):
        self.pattern  = re.compile("\d+")
        self.content1 = "" 
        pass
    
    def tearDown(self):
        pass
    
    def test_parse(self):
        """
        1. content can not be json
        2. page has no data key
        """
        self.