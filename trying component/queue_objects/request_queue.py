#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
class RequestQueue defined an request queue that Downloader get request object
"""
from singleton_queue import SingletonQueue


class Request(object):
    def __init__(self, url, method, **kwargs):
        """
        Initialize a Request Object
        :param url: target need to download,
                    Downloader will use to match url-pattern to decide how to create Page
        :param method: method name, Download will use to decide use requests or selenium
        :param kwargs: see from http://docs.python-requests.org/zh_CN/latest/api.html
        :return: None
        """
        self.url    = url
        self.method = method
        if "params" in kwargs:
            self.params = kwargs["params"]
        if "headers" in kwargs:
            self.headers = kwargs["headers"]
        if "cookies" in kwargs:
            self.cookies = kwargs["cookies"]
        if "files" in kwargs:
            self.files = kwargs["files"]
        if "auth" in kwargs:
            self.auth = kwargs["auth"]
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
        if "allow_redirects" in kwargs:
            self.allow_redirects = kwargs["allow_redirects"]
        if "proxies" in kwargs:
            self.proxies = kwargs["proxies"]
        if "verify" in kwargs:
            self.verify = kwargs["verify"]
        if "stream" in kwargs:
            self.stream = kwargs["stream"]
        if "cert" in kwargs:
            self.params = kwargs["cert"]


class GetDataRequest(Request):
    def __init__(self, url, method, **kwargs):
        """
        method use to get data, like:
            HEAD, GET, DELETE
        :param url: see Request
        :param method: see Request
        :param kwargs: see Request
        :return: None
        """
        super(GetDataRequest, self).__init__(url=url, method=method, **kwargs)


class SendDataRequest(Request):
    def __init__(self, url, method, data, **kwargs):
        """
        method that need to send data, like:
            PUT, POST, PATCH
        :param url: see Request
        :param method: see Request
        :param data: data use to send
        :param kwargs: see Request
        :return: None
        """
        super(SendDataRequest, self).__init__(url=url, method=method, **kwargs)
        self.data = data


class SeleniumRequest(GetDataRequest):
    """
    Just like Simple Get Data Request
    """


def create_request(url, method, data=None):
    """
    Request Factory
    :param url: target url
    :param method: using method
    :param data: send data if need
    :return: An Request instance
    """
    if "GET" or "HEAD" or "DELETE" in method:
        return GetDataRequest(url=url, method=method)
    if "PUT" or "POST" or "PATCH" in method:
        return SendDataRequest(url=url, method=method, data=data)
    if "SELENIUM" in method:
        return SeleniumRequest(url=url, method=method)


class RequestQueue(SingletonQueue):
    _queue_type = "Request"
