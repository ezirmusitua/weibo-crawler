#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
class PageQueue defined a queue object that send page to Parser
"""
from singleton_queue import SingletonQueue


class Page(object):
    def __init__(self, content, parse_rule):
        """
        create a Page instance
        :param content: page content comes from Downloader
        :param parse_rule: decide use which parse-rule in Parser
        :return: None
        """
        self.content    = content
        self.parse_rule = parse_rule


class PageQueue(SingletonQueue):
    _queue_type = "Page"
