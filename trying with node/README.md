## 微博爬虫 -- 使用 Node.js 实现  
一个使用 Node.js 实现的微博爬虫  
### 目前进度  
1. 使用 Node.js + PhantomJS 实现抓取微博页面  

### 记录  
1. 使用 phantomjs-node 添加 cookie 必须通过 page 的 addCookie 方法  
```  
// 无法直接为 phantom 添加 cookie    
page.addCookie(cookie)  
```  
2. 目前的问题在于微博的动态加载问题，使用 page.evaluate 滑动到底部后如何等待等待页面加载是个问题  
3. 即使解决了页面加载的问题，如何让爬虫持续运作也是一个问题  
PS: 被异步回调打败了(:_<)  