#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
downloader use to download page which got content by AJAX
"""
import time
from selenium.webdriver import PhantomJS
from weibo_crawler.queue_objects import Page
from weibo_crawler.downloader.common import PHANTOMJS_DRIVER_PATH
SCROLL_MAX_HEIGHT = 99999


class SeleniumDownloader(object):
    """
    selenium downloader didn't use gevent, it is linear
    """
    driver = PhantomJS(executable_path=PHANTOMJS_DRIVER_PATH)
    # This signal use to tell downloader could not be using now
    # TODO: i should add a test for it, but not now
    is_running = True

    def request(self, request):
        """
        use selenium to get entire page source of request-page
        :param request: request from requests_queue
        :return: None
        """
        self.driver.get(request.url)
        while True:
            pre_page = self.driver.page_source
            # TODO: here with key error
            self.driver.execute_script("scroll(0, {0})".format(SCROLL_MAX_HEIGHT))
            # wait for page load
            # TODO: add global static variable
            time.sleep(1)
            aft_page = self.driver.page_source
            if pre_page == aft_page:
                break
        url_page = (request.url, self.driver.page_source)
        # TODO: driver can not be closed or quit ,would raise error
        # It seem like a window+python2.7 error
        # TODO: test source in linux
        # close current window
        self.driver.close()
        return url_page

    def quit_driver(self):
        try:
            self.driver.quit()
        except WindowsError as e:
            print e

def selenium_download(downloader, requests_queue, url_page_list):
    """
    use selenium to get entire page content and put into a PageQueue
    :param downloader: a SeleniumDownloader
    :param requests_queue:
    :param pages_queue:
    :return:
    """
    request = requests_queue.get(block=True, timeout=3)
    url_page_list.append(downloader.request(request))
