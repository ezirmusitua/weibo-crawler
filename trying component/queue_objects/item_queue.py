#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
ItemQueue defined a queue that Saver use to get object
"""
from singleton_queue import SingletonQueue


class Item(object):
    def __init__(self, data, urls, save_rule):
        """
        create a Item object
        :param data: the data would save to disk
        :param urls: the urls use to create new Request
        :param save_rule: decide use which save_rule in Saver
        :return: None
        """
        self.data      = data
        self.urls      = urls
        self.save_rule = save_rule


class ItemQueue(SingletonQueue):
    _queue_type = "Item"
