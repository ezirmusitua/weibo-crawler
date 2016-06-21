## 使用 Python 实现抓取 weibo 消息  
实现方法有两种：  
1. 使用 selenium + phantomjs 抓取，效率不好  
2. 使用 requests 抓取 ajax 请求(存在 ajax 就不可能直接抓页面了)  
第一种以前做过，虽然是 firefox(win10 phantomjs + selenium 报错)    
现在尝试第二种  
  
## requests 抓取 ajax 请求  
1. 必须是给 requests 设置 headers (直接设置 headers 还不用添加 cookie，好方便~)  
cookie 的获取可以直接通过 Chrome 拓展 Live Http Header 获取，复制下来改成 json 格式就好  
2. 分析 ajax 请求的 url  
大致会有一下三种 url，他们产生的 ajax 请求都是同类的  
```  
pre:  http://weibo.com/u/3217179555?refer_flag=0000010005_
ajax: http://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=100505&id=1005051449533345&page=2&__rnd=1461381272481

pre:  http://weibo.com/n/%E7%A7%81%E5%AE%B6%E9%87%8E%E5%8F%B2?from=feed&loc=at
ajax: http://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=100505&id=1005051449533345&page=2&__rnd=1461381272481

pre:  http://weibo.com/foxshuo?refer_flag=0000015010_&from=feed&loc=nickname
ajax: http://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=100505&id=1005051560906700&page=1&__rnd=1461381558313

pre:  http://weibo.com/u/5891170011?refer_flag=0000015010_&from=feed&loc=nickname
ajax: http://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=100505&id=1005055891170011&page=1&__rnd=1461382087925
```  
ajax 请求 url 最主要的参数(不可缺少)如上  
其中决定获取那个人的是有 id 决定  
id 的构成为 domain + uid  
因此如何获取 uid 就是持续抓取的关键  
PS: domain 好像是个人不同的，分析一下自己的就知道了  
3. 获取 uid  
最开始我还傻傻的在找上面三种类型的 url，以为可以得到什么方法获取 uid  
最后发现: 
```  
pattern = "[a-z]*uid=(\d+)"  
print set(re.findall(pattern, response.content))  
```  
这样就可以提取到页面中出现的相关 uid (名字不一定，一般是 pre + uid = 10位uid)  

4. 构造 ajax 请求 url  
构造 ajax url 的方法很简单的噻，看到上面的 url 了嘛，主要讲一下后面的参数：  
```  
ajwvr -- 一个固定的值，可能版本相关吧，不管他  
domain -- 这个是个人账号相关的值，建议用自己的账号看几个别人的微博就能知道了  
id -- 这是通过 domain + uid 构成的值，uid 的获取看上面  
page -- 自己看吧  
__rnd -- 就是 int(time.time() * 1000)  
```  
用 re 获取到 uid 后直接 format 就可以构造 url  

5. 使用 requests 抓取  
说一下单线程最简单的抓取：  
```  
session = requests.Session()
session.headers.update(headers)
content = session.get(url)  
```  
就是这么简单~  

## 问题记录  
1. headers 会过期  
2. 开 5 协程，间隔 0s~1s 会被封
3. 要选择合适的种子，不然抓不到 uid 就惨了

## 改进  
1. 保持 cookies 的有效性  
2. 自动切换代理
