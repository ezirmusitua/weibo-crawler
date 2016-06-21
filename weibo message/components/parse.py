#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Parser for page content
"""
import re
import sys
import json
from errors import *

def parse(content, items, pattern):
    """
    Parse page content and store to items
    @param content:Page content
    @param items: Store parsed content into it
    @param regex: re pattern
    @return: None
    """ 
    try:
        page = json.loads(content)['data']
    except Exception as e:
        print "Parse Exception: ", e
        uids, page = [], ""
    else:
        try:
            uids = re.findall(pattern, page)
        except Exception:
            print "error page", page
            sys.exit(-1)
    items['uids']    = list(set(uids))
    items['content'] = page
    
    
