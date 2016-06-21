#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Test can Queue Object run properly
"""
import unittest
from weibo_crawler.queue_objects import SingletonQueue
from weibo_crawler.queue_objects import RequestQueue
from weibo_crawler.queue_objects import ItemQueue
from weibo_crawler.queue_objects import PageQueue


class TestQueueObject(unittest.TestCase):
    def setUp(self):
        pass

    def test_singleton_queue_is_singleton(self):
        """
        test is SingletonQueue actually singleton
        :return: None
        """
        instance_1 = SingletonQueue()
        instance_1.test_code = 1
        instance_2 = SingletonQueue()
        self.assertTrue(instance_1 is instance_2)

    def test_subclass_is_different_and_singleton(self):
        """
        test Sub-Class of SingletonQueue is different from SingletonQueue but singleton too
        :return: None
        """
        # singleton
        item_instance_1 = ItemQueue()
        item_instance_2 = ItemQueue()
        self.assertTrue(item_instance_2 is item_instance_1)
        page_instance_1 = PageQueue()
        page_instance_2 = PageQueue()
        self.assertTrue(page_instance_1 is page_instance_2)
        request_instance_1 = RequestQueue()
        request_instance_2 = RequestQueue()
        self.assertTrue(request_instance_1 is request_instance_2)
        # different
        self.assertTrue(request_instance_1 is not SingletonQueue())
        self.assertTrue(request_instance_1 is not page_instance_1)
        self.assertTrue(request_instance_1 is not item_instance_1)
        self.assertTrue(page_instance_1    is not item_instance_1)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
