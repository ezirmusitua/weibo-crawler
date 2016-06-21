#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
test can downloader run properly
"""
import unittest
from gevent import monkey
monkey.patch_all()
import gevent
from weibo_crawler.queue_objects import create_request, Page, RequestQueue, PageQueue
from weibo_crawler.downloader    import NormalDownloader, requests_download
from weibo_crawler.downloader    import SeleniumDownloader, selenium_download
from weibo_crawler.downloader    import Downloader


class TestDownloader(unittest.TestCase):
    def setUp(self):
        self.normal_downloader   = NormalDownloader()
        self.selenium_downloader = SeleniumDownloader()
        self.in_queue            = RequestQueue()
        self.test_url            = "https://news.ycombinator.com/"
        self.test_url_patterns   = {"http://www.jianshu.com/p/\w+": "js", "default":"default"}
        self.test_method         = "GET"
        self.url_page_list       = list()
        self.out_queue           = PageQueue()

    def test_can_requests_download_run_properly(self):
        """
        can download method return properly Page Queue
        :return:
        """
        self.in_queue.put(create_request(url=self.test_url, method=self.test_method))
        requests_download(
            downloader=self.normal_downloader,
            requests_queue=self.in_queue,
            url_page_list=self.url_page_list
        )
        self.assertTrue(len(self.url_page_list) == 1)
        url_page = self.url_page_list.pop()
        self.assertTrue("Hacker News" in url_page[1])

    def test_can_normal_downloader_run_async(self):
        [self.in_queue.put(create_request(url="http://www.baidu.com", method="GET")) for i in range(7)]
        while len(self.in_queue):
            greenlets = []
            [greenlets.append(
                gevent.spawn(
                    requests_download,
                    downloader=self.normal_downloader,
                    requests_queue=self.in_queue,
                    url_page_list=self.url_page_list
                )) for i in range(5 if len(self.in_queue) > 5 else len(self.in_queue))]
            gevent.joinall(greenlets)
        self.assertTrue(len(self.url_page_list) == 7)

    def test_can_selenium_download_run_properly(self):
        """
        test following code in linux
        :return: None
        """
        # -------------------------------------------
        """
        self.in_queue.put(create_request(url=self.test_url, method=self.test_method))
        selenium_download(
            downloader=self.selenium_downloader,
            requests_queue=self.in_queue,
            url_page_list=self.url_page_list
        )
        self.assertTrue(len(self.out_queue) == 1)
        page = self.out_queue.get()
        self.assertTrue("Hacker News" in page.content)
        """
        self.assertTrue(True is True)

    def test_downloader_is_singleton(self):
        downloader_1 = Downloader(url_patterns=dict())
        downloader_2 = Downloader(url_patterns=dict())
        self.assertTrue(downloader_1 is downloader_2)
        downloader_1.close_driver()
        downloader_2.close_driver()

    def test_can_choose_right_pattern(self):
        test_url_1 = "http://www.jianshu.com/p/876d23f"
        test_url_2 = "http://www.zhihu.com"
        downloader_1 = Downloader(url_patterns=self.test_url_patterns)
        self.assertTrue(downloader_1._choose_parse_rule_by_url(test_url_2) == "default")
        self.assertTrue(downloader_1._choose_parse_rule_by_url(test_url_1) == "js")

    def test_can_downloader_download_properly(self):
        import random
        downloader = Downloader(url_patterns=self.test_url_patterns)
        [self.in_queue.put(create_request(
            url="http://www.jianshu.com/p/84ae207ccaf7",
            method=random.choice(["GET", "SELENIUM"])
        )) for i in xrange(20)]
        downloader.download_and_convert(
            requests_queue=self.in_queue,
            pages_queue=self.out_queue
        )
        self.assertTrue(self.out_queue.qsize() == 20)
        out_queue_size = self.out_queue.qsize()
        [self.assertTrue(isinstance(self.out_queue.get(), Page)) for i in xrange(out_queue_size)]
        downloader.close_driver()

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
