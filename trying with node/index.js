/**
 * A weibo crawler implemented by Node.js
 * author: Jferroal  
 */
var phantom = require("phantom");
var cookies = require("./cookies.js");
var async   = require("async");
var _ph, _page, _outObj;
var addCookies = function (page, cookies) {
    var count = 1;
    cookies.forEach(function (cookie) {
        page.addCookie(cookie);
        count += 1;
    });
};


var scrollToButtom = function (page) {
    console.log("here");
    var _page = page;
    return _page.evaluate(function () {
        document.body.scrollTop = document.body.scrollHeight;
        setTimeout(function() {
            console.log("load page done ... ");
        }, 3000);
    });
};
phantom.create([ "--ignore-ssl-errors=yes", "--load-images=no" ]).then(ph => {
    console.log("1");
    _ph = ph;
    return _ph.createPage();
}).then(page => {
    console.log("2");
    _page = page;
    addCookies(_page, cookies);
    return _page.open("http://weibo.com/p/aj/v6/mblog/mbloglist?\
                       ajwvr=6&domain=100206&refer_flag=0000015010_\
                       &from=feed&loc=nickname&is_all=1&pagebar=0&\
                       pl_name=Pl_Official_MyProfileFeed__28&\
                       id=1002061892522605&script_uri=/zijuejueren&\
                       feed_type=0&page=1&pre_page=1&domain_op=100206\
                       &__rnd=1461375668030");
}).then(status => {
    var f = function (a, b) {
        console.log(2);
    };
    return async.series({
        one: function(f){
            setTimeout(function(){
                f(null, 1);
            }, 200);
        },
        two: function(f){
            setTimeout(function(){
                f(null, 2);
            }, 100);
        }
    },
    function(err, results) {
        if (err) {
            console.log(err);
        } else {
            console.log(results);
        }
    });
    //return _page.property("content");
}).then(content => {
    console.log(content);
    _page.close();
    _ph.exit();
});