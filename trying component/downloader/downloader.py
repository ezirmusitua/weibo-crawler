#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Downloader decide use selenium or requests to download page according to method in Request
"""
import re
from gevent import monkey
monkey.patch_all()
import gevent
from gevent.queue import Queue
from weibo_crawler.queue_objects import Page
from weibo_crawler.downloader import NormalDownloader, SeleniumDownloader
from weibo_crawler.downloader import requests_download, selenium_download


class Downloader(object):
    """
    A singleton object
    """
    _requests_downloader = NormalDownloader()
    _selenium_downloader = SeleniumDownloader()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(Downloader, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, url_patterns=dict()):
        """
        May be need some initial work
        :param url_patterns: decide how to create Page accord to url-patterns
        :return: None
        """
        self.url_patterns  = url_patterns

    def _choose_parse_rule_by_url(self, url):
        """
        use url to decide use which parse_rule
        :param url: request url
        :return: parse rule
        """
        for key, value in self.url_patterns.items():
            if re.match(key, url):
                return value
        # return the default parse-rule
        return self.url_patterns['default']

    def _convert_and_send_to_page_queue(self, url_page_list, pages_queue):
        """
        convert {url:page-content} to Request object
        :return: None
        """
        # TODO: may be can use g\ent
        [pages_queue.put(
            Page(
                parse_rule=self._choose_parse_rule_by_url(url_page[0]),
                content=url_page[1]
            )
        ) for url_page in url_page_list]

    def _async_requests_download(self, tmp_requests_queue, url_page_list):
        """
        do requests download using gevent
        :param tmp_requests_queue: tmp requests queue from out
        :param url_page_list: url page list used to save tmp result
        :return: None
        """
        while not tmp_requests_queue.empty():
            greenlets, qsize = [], 5 if tmp_requests_queue.qsize() > 5 else tmp_requests_queue.qsize()
            [greenlets.append(gevent.spawn(
                requests_download(
                    downloader=self._requests_downloader,
                    requests_queue=tmp_requests_queue,
                    url_page_list=url_page_list
                ))) for i in xrange(qsize)]
            gevent.joinall(greenlets)

    def _linear_selenium_download(self, tmp_selenium_queue, url_page_list):
        """
        linear do selenium download
        :param tmp_selenium_queue: tmp selenium requests queue from out
        :param url_page_list: url page list use to save tmp result
        :return: None
        """
        while not tmp_selenium_queue.empty():
            selenium_download(
                downloader=self._selenium_downloader,
                requests_queue=tmp_selenium_queue,
                url_page_list=url_page_list
            )

    def download_and_convert(self, requests_queue, pages_queue):
        """
        Download page using requests or selenium downloader
        :param requests_queue: requests queue
        :param pages_queue: pages queue
        :return: None
        """
        tmp_requests_queue, tmp_selenium_queue, url_page_list = Queue(), Queue(), list()
        while not requests_queue.empty():
            request = requests_queue.get(block=True, timeout=3)
            if "SELENIUM" not in request.method:
                tmp_requests_queue.put(request)
            else:
                tmp_selenium_queue.put(request)
            if tmp_selenium_queue.qsize() == 5 or tmp_requests_queue.qsize() == 5:
                # TODO: 5 is the max tmp queue size
                break
        # do requests download
        self._async_requests_download(tmp_requests_queue=tmp_requests_queue, url_page_list=url_page_list)
        # do selenium download
        # TODO: in windows seem like can run this, try on linux
        # self._linear_selenium_download(tmp_selenium_queue=tmp_selenium_queue, url_page_list=url_page_list)
        self._convert_and_send_to_page_queue(url_page_list=url_page_list, pages_queue=pages_queue)

    def close_driver(self):
        """
        close the phantomjs driver in hand
        :return:
        """
        self._selenium_downloader.quit_driver()


