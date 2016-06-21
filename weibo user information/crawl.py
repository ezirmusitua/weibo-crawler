import time
import json
import codecs
import requests

OUTPUT = "./out/"

with codecs.open("result.json", "rb", "utf-8") as rf:
    USER_DATA = json.load(rf)
    print "Load user data done"

UIDS = USER_DATA.keys()
print "Load uids done"

OUTPUTS = {}

SESSION = requests.Session()

with codecs.open("headers.json", "rb", "utf-8") as rf:
    SESSION.headers = json.load(rf)

URL_PATTERN = "http://weibo.com/p/100505{uid}/info?mod=pedit_more"

def crawl(session, uids):
    for uid in uids:
        try:
            response = session.get(URL_PATTERN.format(uid=uid), timeout=10)
        except Exception as e:
            print e
        else:
            print "Response: ", response
            with codecs.open(OUTPUT + uid, 'wb', 'utf-8') as wf:
                json.dump(response.content, wf)
            OUTPUTS[uid] = response.content
            time.sleep(3)

if __name__ == '__main__':
    crawl(SESSION, UIDS)