#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
test can saver run properly
"""
import unittest
from weibo_crawler.saver import Saver
from weibo_crawler.queue_objects import ItemQueue, Item, RequestQueue, create_request


class TestSaver(unittest.TestCase):
    def setUp(self):
        self.save_rules = {
            "hn":{
                "article-list": {
                    "content": "titles hrefs",
                    "filename": "test.json",
                    "format": "JSON",
                    "onefile": "True"
                },
                "url-patterns": {
                    "http://www.baidu.com":"GET"
                }
            }
        }
        self.saver = Saver(save_rules=self.save_rules)

    def test_can_choose_right_save_rule(self):
        save_rule = self.saver._choose_save_rule("hn")
        self.assertTrue("article-list" in save_rule)
        self.assertTrue("url-patterns" in save_rule)


    def test_can_save_and_convert_async(self):
        items_queue = ItemQueue()
        requests_queue = RequestQueue()
        [items_queue.put(Item(
            data={"titles":["abc", "def"], "hrefs":["http://www.baidu.com", "http://www.qq.com"]},
            urls=["http://www.baidu.com"],
            save_rule="hn"
        )) for i in range(5)]
        self.saver._save_and_convert_async(items_queue=items_queue, requests_queue=requests_queue)
        self.assertTrue(requests_queue.qsize() == 5)

    def test_can_save_run_properly(self):
        items_queue = ItemQueue()
        requests_queue = RequestQueue()
        [items_queue.put(Item(
            data=["hello", "world"],
            urls=["http://www.baidu.com"],
            save_rule="hn"
        )) for i in range(7)]
        self.saver.save_and_convert(items_queue=items_queue, requests_queue=requests_queue)
        self.assertTrue(requests_queue.qsize() == 5)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()