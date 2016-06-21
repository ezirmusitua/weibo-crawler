#!/usr/bin/env python
# -*- coding:utf-8 -*-

from weibo_crawler.client import Client

client = Client()
url_patterns = {"https://news.ycombinator.com/news\?p=\d+":"hn"}
parse_rules  = {
    "hn":{
        "tag":"hacker-news",
        "attribs" : {
            "title":{
                "xpath":"//table[@id=\"hnmain\"]//td[@class=\"title\"]/a/text()",
                "usage":"SAVE",
            },
            "hrefs":{
                "xpath":"//table[@id=\"hnmain\"]//td[@class=\"title\"]/a/@href",
                "usage":"SAVE",
            },
            "next-page":{
                "xpath":"//*[@id=\"hnmain\"]/tbody/tr[3]/td/table/tbody/tr[92]/td[2]/a/@href",
                "usage":"SAVE",
                "method":"GET"
            }
        }
    }
}
save_rules   = {
    "hacker-news":{
        "filename":"test.json",
        "save_type":"JSON"
    }
}
client.update_url_patterns(url_patterns=url_patterns)
client.update_parse_rules(parse_rules=parse_rules)
client.update_save_rules(save_rules=save_rules)
requests_list = [("https://news.ycombinator.com/news?p=1", "GET")]
client.init_requests_queue(requests_list=requests_list)
client.run()

