#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
downloader use requests to download page
"""
from gevent import monkey
monkey.patch_all()
import requests
from weibo_crawler.queue_objects import Page


class NormalDownloader(object):
    session = requests.Session()

    def request(self, request):
        """
        do request according to request.method and convert response to Page
        :param request: request from requests_queue
        :return: a Page obj converted from response
        """
        if   request.method == 'HEAD':
            return request.url, self.session.head(url=request.url).content
        elif request.method == 'GET':
            return request.url, self.session.get(url=request.url).content
        elif request.method == 'DELETE':
            return request.url, self.session.delete(url=request.url).content
        elif request.method == 'PUT':
            return request.url, self.session.put(url=request.url, data=request.data).content
        elif request.method == 'POST':
            return request.url, self.session.post(url=request.url, data=request.data).content
        elif request.method == 'PATCH':
            return request.url, self.session.patch(url=request.url, data=request.data).content
        else:
            raise "UnKnown Method"


def requests_download(downloader, requests_queue, url_page_list):
    """
    use downloader to download page in requests_queue and store result into responses_queue
    :param downloader: NormalDownloader
    :param requests_queue: Request queue
    :param result: page content and url
    :return: None
    """
    request = requests_queue.get(block=True, timeout=3)
    try:
        url_page_list.append(downloader.request(request))
    except Exception as e:
        print e

