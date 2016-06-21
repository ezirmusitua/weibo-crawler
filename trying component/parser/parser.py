#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Parser use to extract items from page content
"""
from gevent import monkey
monkey.patch_all()
import gevent
from gevent.queue import Queue
from lxml.html import soupparser as lxml_parser
from weibo_crawler.queue_objects import Item


class Parser(object):
    """
    A singleton class
    """
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(Parser, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, parse_rules=dict()):
        """
        initial work
        :param parse_rules: decide how to page using different rules
        :return: None
        """
        self.parse_rules = parse_rules

    def _choose_parse_rule(self, parse_rule):
        """
        using parse_rule to get rule from parse-rules
        :param parse_rule :use to choose from parse-rules
        :return: a dict about how to parse page and convert to Item
        """
        return self.parse_rules[parse_rule]

    def _extract(self, pages_queue, save_data_urls_list):
        page = pages_queue.get(block=True, timeout=3)
        page_dom = lxml_parser.fromstring(page.content)
        parse_rule = self._choose_parse_rule(parse_rule=page.parse_rule)
        # TODO: should i do judgement for un-exist 'data' or 'urls'
        save_rule, data_xpath, urls_xpath = parse_rule['save_rule'], parse_rule['data'], parse_rule['urls']
        data, urls = dict(), dict()
        for item in data_xpath:
            data[item] = page_dom.xpath(data_xpath[item]['xpath'])
        for url in urls_xpath:
            urls['url'] = {page_dom.xpath(urls_xpath[url]['xpath']):urls_xpath[url]['method']}
        save_data_urls_list.append((save_rule, data, urls))

    def _convert_to_item(self, save_data_urls_list, items_queue):
        [items_queue.put(Item(
            save_rule=save_data_urls[0],
            data=save_data_urls[1],
            urls=save_data_urls[2]
        )) for save_data_urls in save_data_urls_list]

    def _extract_async(self, pages_queue, save_data_urls_list):
        while not pages_queue.empty():
            greenlets, qsize = [], 5 if pages_queue.qsize() > 5 else pages_queue.qsize()
            [greenlets.append(
                gevent.spawn(
                    self._extract,
                    pages_queue=pages_queue,
                    save_data_urls_list=save_data_urls_list
                )
            ) for i in range(qsize)]
            gevent.joinall(greenlets)

    def parse_and_convert(self, pages_queue, items_queue):
        """
        parse page and create Item and send to items queue
        :param pages_queue: pages queue use to get Page
        :param items_queue: items queue use to receive Item
        :return: None
        """
        tmp_pages_queue ,save_data_urls_list = Queue(), []
        # each round just parse 5 pages
        while not pages_queue.empty():
            if tmp_pages_queue.qsize() < 5:
                tmp_pages_queue.put(pages_queue.get(block=True, timeout=3))
            else:
                break
        # TODO: i should find out should parse page using gevent
        # extract
        self._extract_async(pages_queue=tmp_pages_queue, save_data_urls_list=save_data_urls_list)
        # convert
        self._convert_to_item(save_data_urls_list=save_data_urls_list, items_queue=items_queue)
