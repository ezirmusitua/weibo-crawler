#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Define a singleton Download Pool Object
"""
# TODO: I can not use pool now !
from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool
# TODO: POOL MAX SIZE
POOL_MAX_SIZE = 10

class DownloadPool(Pool):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(DownloadPool, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance

download_pool = DownloadPool(size=POOL_MAX_SIZE)