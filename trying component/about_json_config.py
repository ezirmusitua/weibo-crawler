"""
Detail about json config
"""


# url patterns
url_patterns = {
    "url-pattern-1": "parse-rule-1",
    "url-pattern-2": "parse-rule-2",
    "url-pattern-4": "parse-rule-3",
    "default"      : "default-rule"
}
"""
url patterns:
usage:
    use to choose a parse rule
howto:
    url-patterns is a attribute of downloader which is a dict
    While we use a download for target url, downloader will download the page at first,
    then, download will do re.match("url-pattern in url-patterns", target_url) to find the
    parse rule and create a Page object which .content=page-source and .parse_rule=parse_rule
"""


# parse rules
parse_rules = {
    "parse-rule-1": {
        "save-rule":"save-rule",
        "data": {
            "page-content-1": {
                "xpath": "xpath/for/page/content1"
            },
            "page-content-2": {
                "xpath": "xpath/for/page/content2"
            },
            "page-content-3": {
                "xpath": "xpath/for/page/content3"
            }
        },
        "urls": {
            "url-in-page-1": {
                "xpath": "xpath/for/url/in/page1",
                "method": "GET"
            },
            "url-in-page-2": {
                "xpath": "xpath/for/url/in/page2",
                 "method": "GET"
            },
            "url-in-page-3": {
                "xpath": "xpath/for/url/in/page3",
                "method": "GET"
            }
        }
    },
    "parse-rule-2": {
        "save-rule": "save-rule",
        "data": {
            "page-content...": "xpath/..."
        },
        "urls": {
            "urls-in-page...": "xpath/..."
        }
    }
}
"""
parse rules:
usage:
    1. About Extract: To Extract what in page using xpath
    2. About Save: Using data and urls in page that we need and save-rule to create Item object
howto:
    parse-rules is an attribute of parser which is a dict
    While parser get a Page object, at first it will got that object's parse-rule to find proper extract-
    strategy for the object.
    After parser got the extract-strategy, it will do the parse, and save data in the following way:
        {"page-content-1":["page-content-1-list"] ,"page-content-2":["page-content-2-list"],}
    And save the urls in the following way:
        {"url-in-page-1":["url-in-page-1-list"], "url-in-page-2":["url-in-page-2-list"],}
    Finally, parser will create a Item object and send it to items_queue:
        items_queue.put(Item(save_rule=save_rule, data=data, urls=urls))
"""


# save rules
save_rules = {
    "save-rule-1": {
        "item-1": {
            "content": "1-page-content-1 1-page-content-2",
            "format": "JSON",
            "filename": "xxx/yyy/zzz/%d" or "1-page-content-1",
            "onefile": "True" or "False" # bind with filename
        },
        "item-2": {
            "content": "2-page-content-1 2-page-content-2",
            "format": "JSON",
            "filename": "xxx/yyy/zzz/%d" or "2-page-content-1",
            "onefile": "True" or "False" # bind with filename
        },
        # this part use to create new Request objects
        # just like url-patterns in downloader, use re.match to decide
        # TODO: may be i can combine this with downloader, Just Think About It!
        "url-patterns": {
            "url-pattern-1": "method-1",
            "url-pattern-2": "method-2",
        }
    }
}
"""
save rules:
usage:
    1. About Saving: How to save (save what, format, filename, ...) data which is an attribute of Item
    2. About Request: Convert what url in urls(an attribute of Item) to Request object
howto:
    save-rules is an attribute of saver which is a dict
    While Saver get a Item object, at first it will got that object's save-rule to find proper save-
    strategy for the Item object.
    After saver got the save-strategy, it will do the save action in the save-strategy:
        combine content, decide format, save to specific file
    Finally, saver will create new Request object and send it to requests_queue:
        for url in urls:
            for url_pattern in url_paterns:
                if re.match(url-pattern, url):
                    requests_queue.put(create_request(url=url, method=method)))
"""
