#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Downloader of crawler
use to download page and do parse and save operation
"""
import re
from requests.exceptions import ProxyError, ConnectionError, Timeout
from components.utils import set_proxies
from errors import *
def download(session, uid_queue, url_generator, parse, save, sleep):
    """
    Get uid from uid queue and use url generator to create url for download
    After downloaded, parse and save content, sleep for a specific time
    @param session: session use to get page
    @param uid_queue: get uid from this, would block
    @param url_generator: use to create a url generator using uid
    @param parse: parse function
    @param save: save function
    @sleep sleep: AAC, sleep function
    @return: None
    """
    uid_pattern = re.compile("[a-z]*uid=(\d{10})")
    try:
        uid = uid_queue.get()
    except Exception:
        return QUEUE_EMPTY
    item_count = 0
    items      = dict()
    for url in url_generator(uid, 20):
        # download
        try:
            #print "request {uid}: {page}".format(uid=uid, page=item_count)
            content = session.get(url, timeout=10).content
            #print "request {uid}: {page} done".format(uid=uid, page=item_count)
        except (ProxyError, ConnectionError, Timeout, ) as e:
            print "Requests exception (PE, CE, TO): ", e
            # set_proxies(session)
            continue
        except Exception as e:
            print "Requests exception: ", e
            continue
        
        # parse
        # print "url:%s -- content:%s" %(url, content)
        if u'你们太快了!慢点!' in content or u'加载过于频繁' in content or u"File not found." in content:
            set_proxies(session)
        if u"Authentication Required" in content: 
            print "Need New Header"
            sys.exit(-1);
        
        parse(content=content, items=items, pattern=uid_pattern)
        
        # extend uid queue
        uid_queue.extend(items['uids'])
        
        # save to file
        filename = "result/" + str(uid) + "-" + str(item_count)+".json"
        save(filename=filename, content=items['content'])
        
        # sleep for random time
        sleep()
        item_count += 1
        
        
    