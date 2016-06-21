#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Save content
"""
import json
import codecs

def save(filename, content):
    """
    Save to file
    @param filename: Where to save file
    @param content: Save what
    @return: None
    """
    # TODO: add clean work
    with codecs.open(filename, 'wb', 'utf-8') as wf:
        json.dump(content, wf);