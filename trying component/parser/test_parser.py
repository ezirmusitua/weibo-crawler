#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
test parser
"""
import codecs
import unittest
from weibo_crawler.queue_objects import Page, PageQueue, Item, ItemQueue
from weibo_crawler.parser import Parser
TEST_FILE_DIR = r"F:\Desktop\Graduation-Project\weibo_crawler\parser\hn.test"

class TestParser(unittest.TestCase):
    def setUp(self):
        self.parse_rules = {
            "hn":{
                "save_rule":"hacker-news",
                "data" : {
                    "title":{
                        "xpath":"//table[@id=\"hnmain\"]//td[@class=\"title\"]/a/text()",
                    },
                    "hrefs":{
                        "xpath":"//table[@id=\"hnmain\"]//td[@class=\"title\"]/a/@href",
                    }
                },
                "urls": {
                }
            }
        }
        self.parser = Parser(parse_rules=self.parse_rules)

    def test_is_parser_singleton(self):
        parser_1 = Parser(parse_rules=self.parse_rules)
        self.assertTrue(parser_1 is self.parser)

    def test_can_choose_right_rule(self):
        parse_rule = self.parser._choose_parse_rule("hn")
        self.assertTrue("save_rule" in parse_rule)
        self.assertTrue("data" in parse_rule)
        self.assertTrue("title" in parse_rule["data"])
        self.assertTrue("hrefs" in parse_rule["data"])

    def test_can_parse_page_properly(self):
        pages_queue        = PageQueue()
        with codecs.open(filename=TEST_FILE_DIR, mode="rb", encoding="utf-8")as rf:
            pages_queue.put(
                Page(content=rf.read(), parse_rule="hn")
            )
        save_data_urls_list = list()
        self.parser._extract(pages_queue=pages_queue, save_data_urls_list=save_data_urls_list)
        self.assertTrue(len(save_data_urls_list) == 1)
        self.assertTrue(len(save_data_urls_list[0][1]['title']))

    def test_can_parse_page_async(self):
        pages_queue        = PageQueue()
        tag_data_urls_list = list()
        for i in range(1, 6):
            with codecs.open(filename=TEST_FILE_DIR+str(i), mode="rb", encoding="utf-8")as rf:
                pages_queue.put(
                    Page(content=rf.read(), parse_rule="hn")
                )
        self.parser._extract_async(pages_queue=pages_queue, save_data_urls_list=tag_data_urls_list)
        self.assertTrue(len(tag_data_urls_list) == 5)
        self.assertTrue(len(tag_data_urls_list[0][1]['title']))

    def test_can_convert_to_item_properly(self):
        pages_queue        = PageQueue()
        save_data_urls_list = list()
        items_queue        = ItemQueue()
        for i in range(1, 6):
            with codecs.open(filename=TEST_FILE_DIR+str(i), mode="rb", encoding="utf-8")as rf:
                pages_queue.put(
                    Page(content=rf.read(), parse_rule="hn")
                )
        self.parser._extract_async(pages_queue=pages_queue, save_data_urls_list=save_data_urls_list)
        self.parser._convert_to_item(save_data_urls_list=save_data_urls_list, items_queue=items_queue)
        self.assertTrue(items_queue.qsize() == 5)
        self.assertTrue(isinstance(items_queue.get(), Item))

    def test_can_parse_and_convert_properly(self):
        pages_queue = PageQueue()
        items_queue = ItemQueue()
        for i in range(1, 7):
            with codecs.open(filename=TEST_FILE_DIR+str(i), mode="rb", encoding="utf-8")as rf:
                pages_queue.put(
                    Page(content=rf.read(), parse_rule="hn")
                )
        self.parser.parse_and_convert(pages_queue, items_queue)
        self.assertTrue(items_queue.qsize() == 5)
        self.assertTrue(isinstance(items_queue.get(), Item))

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()