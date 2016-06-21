#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Saver, use to save file and create new Request
"""
from gevent import monkey
monkey.patch_all()
import re
import json
import codecs
import gevent
from gevent.queue import Queue
from weibo_crawler.queue_objects import create_request, ItemQueue


class Saver(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig          = super(Saver, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, save_rules=dict()):
        """
        initial work
        :param save_rules: decide how to deal with Item
        :return: None
        """
        self.save_rules = save_rules

    def _choose_save_rule(self, save_rule):
        """
        choose save_rule from save_rules accord to save_rule
        :param save_rule: save rule
        :return: None
        """
        return self.save_rules[save_rule]

    def _save_and_convert(self, items_queue, requests_queue):
        item = items_queue.get(block=True, timeout=3)
        save_rule = self._choose_save_rule(item.save_rule)
        data, urls = item.data, item.urls
        # TODO: more detail on saving
        # save
        for attrib in save_rule:
            if attrib == "url-patterns":
                continue
            save_data = dict()
            # TODO: maybe someday can change to support multi-file
            [save_data.setdefault(key, data[key]) for key in data if key in save_rule[attrib]['content']]
            # TODO: use random to create random filename
            import random
            with codecs.open(unicode(random.randint(1,256)) + save_rule[attrib]['filename'], mode="wb", encoding="utf-8") as wf:
                json.dump(save_data, wf)
        # convert
        url_patterns = save_rule['url-patterns']
        for url_pattern in url_patterns:
            [requests_queue.put(create_request(
                url=url,
                method=url_patterns[url_pattern]
            )) for url in urls if re.match(url_pattern, url)]

    def _save_and_convert_async(self, items_queue, requests_queue):
        greenlets = []
        [greenlets.append(
            gevent.spawn(
                self._save_and_convert,
                items_queue=items_queue,
                requests_queue=requests_queue
            )
        ) for i in range(5 if items_queue.qsize() > 5 else items_queue.qsize())]
        gevent.joinall(greenlets)

    def save_and_convert(self, items_queue, requests_queue):
        # can not use ItemQueue cause ItemQueue was singleton
        tmp_items_queue = Queue()
        # each round just parse 5 items
        while not items_queue.empty():
            if tmp_items_queue.qsize() < 5:
                tmp_items_queue.put(items_queue.get(block=True, timeout=3))
            else:
                break
        # save and convert async
        self._save_and_convert_async(items_queue=tmp_items_queue, requests_queue=requests_queue)
