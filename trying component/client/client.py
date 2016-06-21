#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Client for crawler
"""
from weibo_crawler.queue_objects import RequestQueue, PageQueue, ItemQueue, create_request
from weibo_crawler.downloader    import Downloader
from weibo_crawler.parser        import Parser
from weibo_crawler.saver         import Saver

class Client(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig          = super(Client, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance

    requests_queue = RequestQueue()
    pages_queue    = PageQueue()
    items_queue    = ItemQueue()
    crawl_count    = 0
    max_crawl      = 5

    def __init__(self, url_patterns=dict(), parse_rules=dict(), save_rules=dict()):
        self.downloader = Downloader(url_patterns=url_patterns)
        self.parser     = Parser(parse_rules=parse_rules)
        self.saver      = Saver(save_rules=save_rules)

    def update_url_patterns(self, url_patterns):
        self.downloader = Downloader(url_patterns=url_patterns)

    def update_parse_rules(self, parse_rules):
        self.parser = Parser(parse_rules=parse_rules)

    def update_save_rules(self, save_rules):
        self.saver = Saver(save_rules=save_rules)

    def init_requests_queue(self, requests_list):
        [self.requests_queue.put(create_request(
            url=request[0],
            method=request[1])) for request in requests_list]

    def run(self):
        while True:
            if self.crawl_count >= self.max_crawl or self.requests_queue.empty():
                print "Finish"
                break
            print "round : %d" % self.crawl_count
            self.downloader.download_and_convert(self.requests_queue, self.pages_queue)
            self.parser.parse_and_convert(self.pages_queue, self.items_queue)
            self.saver.save_and_convert(self.items_queue, self.requests_queue)

