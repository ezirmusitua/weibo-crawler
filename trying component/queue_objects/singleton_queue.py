#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Parent of *_queue
"""
from gevent import monkey
monkey.patch_all()
from gevent.queue import Queue


class SingletonQueue(Queue):
    """
    A singleton Queue Object
    """
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(SingletonQueue, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance

