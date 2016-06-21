#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
uid container
Remove duplicate items
"""
import json
import codecs
import cPickle as pickle
from Queue import Queue
from pybloom import BloomFilter
from errors import *

class UidQueue():
    """
    Uid queue, include queue and bloom filter
    """
    def __init__(self, max_count=200000, error_rate=0.001):
        """
        Initialize
        @param max_count: capacity of bloom filter
        @param error_rate: error_rate of bloom filter
        @return: None
        """
        self.queue   = Queue()
        self.bloom   = BloomFilter(capacity=max_count, error_rate=error_rate)
        self.crawled = 0
    
    @staticmethod
    def _remove_duplicate(list_in):
        """
        remove duplicated item in list
        @param list_in: list
        @return: None
        """
        return list(set(list_in))
    
    def dump(self, path, encoding):
        """
        Dump data to file
        @param path: path prefix
        @param encoding: file encoding
        @return: None 
        """
        try:
            print "Saving ... "
            with codecs.open(path+'-queue.bak', 'wb', encoding) as wf:
                tmp = {'queue': list(set(list(self.queue.queue))), 'count': self.crawled}
                json.dump(tmp, wf)
            with codecs.open(path+'-bloom.bak', 'wb') as wf:
                self.bloom.tofile(wf)
        except Exception as e:
            print "Dump Uid Queue Failed"
            print e
    
    def restore(self, path, encoding):
        """
        Restore data from file
        @param path: path prefix
        @param encoding: file encoding
        @return: None 
        """
        try:
            with codecs.open(path+'-bloom.bak', 'rb') as rf:
                self.bloom.fromfile(rf)
            with codecs.open(path+'-queue.bak', 'rb', encoding) as rf:
                tmp = json.load(rf)
                [self.queue.put(uid) for uid in tmp['queue']]
                self.crawled = tmp['count']       
            # set encoding=utf-8 is wrong, only deal with ascii
            
        except Exception as e:
            print "Restore Uid Queue Failed: ", e
    
    def _put_all(self, list_in, block, timeout):
        """
        Put all item in list to queue while item not in bloom
        @param list_in: Item from
        @param block: Is block for put open
        @param timeout: Timeout of put
        @return: None
        """
        [self.queue.put(uid, block, timeout) for uid in list_in]
    
    def extend(self, container, block=True, timeout=3):
        """
        Extend uid Queue, remove duplicated and put all in container to queue
        @param container: Where items in
        @param block: Is block for put open
        @param timeout: Timeout of put
        @return: Error return WRONG_TYPE
        """
        # TODO: seem like can not remove duplicate using set
        tmp = []
        for uid in container:
            if uid not in self.bloom and uid not in self.queue.queue:
                tmp.append(uid)
        self._put_all(list_in=tmp, block=block, timeout=timeout)
        
    
    def get(self, block=True, timeout=3):
        """
        Get uid from queue, and add it into bloom filter 
        @param block: Is block for put open
        @param timeout: Timeout of put
        @return: uid
        """
        uid = self.queue.get(block=block, timeout=timeout)
        self.bloom.add(uid)
        self.crawled += 1
        return uid
    
    def __len__(self):
        """
        Length of uid queue
        """
        return self.queue.qsize()
    

    
        
        
    