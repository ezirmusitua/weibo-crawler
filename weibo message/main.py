#!/usr/bin/env python  
# -*- coding: utf-8 -*-
"""
Client of crawler
"""
from gevent import monkey;monkey.patch_all()
import os
import sys
import json
import codecs
import cPickle as pickle
import gevent
import requests
from components.utils import sleep
from components.utils import set_headers, set_proxies
from components.utils import url_generator
from components.save import save
from components.parse import parse
from components.download import download
from components.uid_queue import UidQueue

# Add search path
sys.path.append('.')

class Client(object):
    """
    Crawler Client
    """
    def __init__(self):
        self.uid_queue = UidQueue()
        self.session   = requests.Session()
    
    def _get_crawled_count(self):
        """
        return the crawled count of uid queue
        """
        return self.uid_queue.crawled
    
    def _async_download(self):
        """
        use gevent to download async
        @return: None
        """
        gevent.joinall([
            gevent.spawn(download, 
                         session=self.session, 
                         uid_queue=self.uid_queue, 
                         url_generator=url_generator, 
                         parse=parse, 
                         save=save, 
                         sleep=sleep)
                for i in range(5)
        ])
        
    def _dump(self, filename="./state/backup", encoding='utf-8'):
        """
        back up state
        @param path: back up file path
        @param encoding: encoding of file
        @return: None
        """
        self.uid_queue.dump(filename, encoding)
    
    def restore(self, path="./state/backup", encoding='utf-8'):
        """
        restore form back up file
        @param path: back up file path
        @param encoding: encoding of file
        @return: None
        """
        self.uid_queue.restore(path, encoding)
        
    def set_uids_from_list(self, list_in):
        """
        use list_in to initialize te uid queue
        @param list_in: a list contain uids
        @return: None
        """
        self.uid_queue.extend(list_in)
        
    def set_uids_from_pickle(self, uid_queue):
        """
        use uid_queue which load from pickle to set uid queue
        @param uid_queue: uid queue load from pickle file
        @return: None
        """
        self.uid_queue = uid_queue
        
    def set_headers(self, path='./headers.json'):
        """
        set headers for session headers
        @param path: path of headers
        @return: None
        """
        set_headers(self.session, path)
        
    def stop(self, bak_count, stop_count):
        """
        Judge stop or back up
        @param bak_count: when to backup
        @param stop_count: when to stop
        @return: None
        """
        if (self._get_crawled_count() % bak_count) == 0:
            print "Backing up start ... "
            self._dump()
            set_proxies(self.session)
            print "Backing up done ... "
        if (self._get_crawled_count() >= stop_count):
            print "Stoping ... "
            sys.exit(1)
        if (len(self.uid_queue) == 0):
            print "Empty uid queue ... "
            sys.exit(1)
            
    def start(self, max_count=5):
        """
        start the main loop
        @param max_count: how many coroutine at same time
        @return: None
        """
        while 1:
            print "current uid count: ", len(self.uid_queue)
            self._async_download()
            self.stop(bak_count=25, stop_count=200000)
            
            
if __name__ == '__main__':
    client = Client()
    
    if not os.path.isfile('./state/backup-bloom.bak'):
        list_in   = [ "3031539307", "5897703569", "5882243586", "2398816207", "1980953575"]
        client.set_uids_from_list(list_in)
    else:
        print "Load from back up ..."   
        client.restore()
    
    client.set_headers()
    # TODO: imporve proxies
    set_proxies(client.session)
    
    print "Start download ... "
    client.start()