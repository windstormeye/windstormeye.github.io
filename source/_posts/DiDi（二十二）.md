---
title: DiDi（二十二）
date: 2018-05-14 22:35:30
tags:

- DiDi
- iOS
---

## 2018-05-14

今天总算把首页的数据缓存全部搞定了，遇到了几个小问题，其中最有趣的是，当我在对数据进行归档存储时居然也把`UIImage`对象数组也用`JSONSerialization`做了序列化为`Data`，当时知道自己犯了这个错误后，焕然大悟的差点给了自己个耳光。hhhh。

接着就来了一个跨越今天大部分时间的`Cookie`问题，因为在“我”页面上的三个功能Cell都要求外网可访问，之前是服务端直接把`Cookie`直接中在`bigdata`这个二级域名下，但是要求公网可访问后就要求在`dididata`这个二级域名下，但是这个二级域名因为不是自己部门可以控制的，没法直接用。因此有两种方法可以解决，要么以拼接URL的方式进行传递所需认证信息，要么就在客户端自己种`Cookie`，在经过一番讨论，直接否决掉了把认证信息拼接在URL上的做法，这种直接暴露在公网上的信息这么搞不太妥。

在我一番的骚操作后，Cookie是种下去了，但是出现了一个尴尬的事情，种下的`Cookie`相关web页面并没有得到相应，我看了leader给我发的`Cookie`“种植指南”，仔仔细细对比了一番发现是完全正确的啊，几个人再讨论了一次后，发现了居然还是我端上的锅，我直接set`Cookie`就完了，但是于`Cookie`相关的属性，比如`Path`、`timeout`等都没加上。

再重新经过我的一番操作后，发现想要正确的加上`Cookie`还是有点可以玩的地方，而且通过`UIWebView`和`WKWebView`设置的`Cookie`居然从概念上也不一样，有人这么告诉我的`WKWebView`设置`Cookie`并不能跟服务器产生交互（没记错的话），下面是完整的给`WKWebView`设置`Cookie`的相关代码：

首先是`setCookie`方法，
```Swift
private func setCookie() {
    var ticketCookieProperties = [AnyHashable: Any]()
    ticketCookieProperties[HTTPCookiePropertyKey.domain]    = "Your hostname"
    ticketCookieProperties[HTTPCookiePropertyKey.name]      = "Your Cookie.name"
    ticketCookieProperties[HTTPCookiePropertyKey.value]     = "Your Cookie.value"
    ticketCookieProperties[HTTPCookiePropertyKey.path]      = "/"
    ticketCookieProperties[HTTPCookiePropertyKey.expires]   = Date().addingTimeInterval(3600)
    let ticketCookie = HTTPCookie.init(properties: ticketCookieProperties as! [HTTPCookiePropertyKey : Any] )
    HTTPCookieStorage.shared.setCookie(ticketCookie!)
    
    var usernameCookieProperties = [AnyHashable: Any]()
    usernameCookieProperties[HTTPCookiePropertyKey.domain]    = "Your hostname"
    usernameCookieProperties[HTTPCookiePropertyKey.name]      = "Your Cookie.name"
    usernameCookieProperties[HTTPCookiePropertyKey.value]     = "Your Cookie.value"
    usernameCookieProperties[HTTPCookiePropertyKey.path]      = "/"
    usernameCookieProperties[HTTPCookiePropertyKey.expires]   = Date().addingTimeInterval(3600)
    let usernameCookie = HTTPCookie.init(properties: usernameCookieProperties as! [HTTPCookiePropertyKey : Any] )
    HTTPCookieStorage.shared.setCookie(usernameCookie!)
}
```

接着是`readCurrentCookie`方法，把之前设置全局`Cookie`取出来，
```Swift
private func readCurrentCookie() -> String {
    let cookieJar = HTTPCookieStorage.shared
    var cookieString = ""
    for cookie: HTTPCookie in cookieJar.cookies! as Array {
        cookieString = cookieString + "\(cookie.name)=\(cookie.value);"
    }
    return cookieString
}
```

最后是给当前的`WKWebView`的request添加`Cookie`，
```Swift
var request = URLRequest.init(url: URL(string: requestURL!)!)
// 注入公网所需Cookie
request.addValue(readCurrentCookie(), forHTTPHeaderField: "Cookie")
webView?.load(request)
```

## 2018-05-15

今天搞完了“发现页”和“消息页”的数据缓存，昨天临下班之前遇到了一个问题，“发现”页VC和“消息页”VC居然收不到网络状态改变的通知，而首页居然能够十分良好的运行，纠结、思考加调试一波操作后猛的发现，我的tabBarController是在Appdelegate中进行初始化的，而且默认选择了`selectedIndex = 1`，也就是说，运行起App后，只有首页被成功load的，而tabBarController下的其它VC添加监听网络状态通知的代码居然都是在`viewDidLoad`方法中进行添加的，这样就又造成生命周期错乱的问题。

首页之所以能够完美的接收到对应的通知，那是因为该通知代码放在了首页的`viewDidLoad`方法下，而且首页会被Appdelegate默认加载，而首页加载完之后，其它VC是不做页面初始化的，因为用户并没有进入该界面，也就无从让视图DidLoad的。因此，最终的做法是，重载对应VC的`init`方法，在其中写上监听网络状态的代码，而不是在`viewDidLoad`中，而在`init`方法中，我们只能设置网络状态标记，而不能直接去初始化页面，因为初始化页面的所需相关内容等均为初始化，而当用户最终点击进入该页面后，在对应VC的`requestData`方法中，判断当前网络状态标记是否为无网络标记，如果是就`loadCacheData`即可。

通过以上的操作，这就又让我想起了之前在社团实验室中有位同学的QQ退出后还能收到推送，说明QQ在用户退出QQ后并没有对当前用户登录设备进行注销，`deviceToken`一直保存在表中，除非把App删掉的，再装一次即可。因为这样会触发APNS把之前注册的`deviceToken`删除。

因为明天就要提测这一个超大版本的迭代，间隔了快两个月才发版，做了不少的Swift代码替换，也重构和删除了不少之前遗留下来的垃圾代码，自己总算是把这个看上去四不像的App改善得有模有样了。


## 2018-05-18

今天提测的第一天，但是感觉好像QA没啥动静，梳理了一番这段时间中做的东西，写了点小总结，后续又刷了一遍众大佬的blog，受益匪浅，需要学习的东西还有很多。

### 1.4.0开发总结

从1.3.1到1.4.0两个版本之间总共间隔了整整两个月，严格来说实际上中间应该是隔了一个1.3.5的版本，上的是多语言和哈勃代驾数据，但是哈勃团队迟迟审核不过，再加上三月份Android的同学都回学校了，就剩我一个人孤零零的苦逼着，所以就把所有需求延续到了1.4.0。

1.4.0从开始4月28号到昨天提测，共三周左右，不过好在中间来了个iOS实习同学，分担了一些工作，也让我能够更加专注于核心需求的开发，分给他“国际化服务”的模块，具体的作用就是切换国内和美东数据接口，上午review他的代码，一眼看过去是真的舒服，比之前的同学好太多了，这点值得称赞！不过现在还欠缺的同学跟我当时来的差不多，对整个业务流程和模式都不太熟悉，不过也没怎么见他问，有可能人家已经掌握了吧。原本还打算想跟他进行结对，不过我左右两边的工位都被占了，非常遗憾。😔。

先梳理一下1.4.0的需求：（应该没有触发保密协议😑）
* 1、 手动Push功能优化。大概的意思就是说，要根据从友盟后台提交公共push消息的参数做识别并跳转，比如判断某一个key跳转webView or VC。洋洋洒洒的给PM写了非常详细的后台参数填写文档，希望到时PM千万别填错了，要不然push出来的内容非常奇怪。

* 234都是Web需求，跟端无关。

* 5、对接哈勃。哈勃从一二个月前就开始对接到现在。基本上没啥问题了，给我感觉哈勃团队也是一个神一般的存在，各自问题考虑得非常周到，非常强，有时间也会去钻研一波哈勃的相关代码哒~

* 6、报表列表中透出数据最后更新时间字段。后台说跟不上了，需要牵扯到的内容太多，而且有些报表没法拿到实时修改时间，遂delay。

* 7、动态页的刷新机制。就是给消息页加个下拉刷新、上拉加载。但是之前做的接口有问题，后来跟后端开发沟通后才发现，消息页每次只加载一次，而且在端上没有做任何二次刷新机制，如果你要刷新消息页的数据，或者现在给你推送了一个消息，你知道kill掉App然后再进来，个人感觉应该是之前的RD忘了加上了。而且最奇怪的地方不在这里，接口没做分页，而且一拉就拉回来100条数据，先不说这时间耗费了，但是是拉回数据后给tableView进行reloadData重新渲染的体验也很GG哇。但是在这其中居然发现了请求中有个参数叫“lastMessageId”，给的是当前tableView第一条数据的“msgId”，第一条数据默认为当前数据源中的最大“msgId”，这就很奇怪了，也就说如果当前后台给你发了新数据，你要下拉刷新一次，然后滑到最后才能找到它。emmm。总之最后调整回来了，多加了action字段作为刷新或加载识别。

* 8、断网或弱网环境下缓存和前端优化。后边讲

* 9、我的审批和我的申请外网可访问。这块虽然是只需要替换个二级域名就行，但是这也让我学到了点东西，搞懂了在iOS中如何重放Cookie，花了差不多一天的时间才搞懂，不亏，而且按照我最初的想法去做有个超大坑，不过这个坑应该是我没理解好设置Cookie的相关做法吧。详细见此：https://github.com/windstormeye/iOS-Course/blob/master/%E8%AF%AD%E8%A8%80/Swift%E6%B3%A8%E6%84%8F%E7%82%B9.md    第八点

* 10、国际化策略。这块内容丢给了新来的实习生做，试试他的水。😜

* 11、12是后端的需求，略过。

* 13、新增了一个埋点。用于统计消息页中的没条消息的pv和uv

* 14、在首页中增加新H5策略。首页的headerView在我来之前是写死在本地的，不过到了1.4.0开始要求真正的动态上下线，而且还要可调换入口顺序。这么搞就不能用之前的方法，只能全部推倒重来，这块内容是正常的重构开发，没有多大的特殊，原本想用UIStackView的，UIStackView限制在了iOS 9以上，而滴滴数据App的target在iOS 8，记得去年年末看一次用户分布，只有区区的7个iOS 8用户，而且居然还有两个iPod用户，我坚信其中有个iPod是我，剩下的6个用户当时我觉得不用管也行啊，但是被PM强烈拒绝了，本来用户就没多少，这还少了几个。emmm，现在也不多，不到1300。刚开始我还嫌弃用户太少，但是我现在一点不嫌弃了，正是因为用户量不大，我可以自己“偷偷”的做一些改进和实验，而不让其他人知道，而且就算真的出现了线上bug，也不用连夜修复，hhhhh。

* 15、截屏打开upload接口，需要测试。emmm这个需求是之前被另外一个实习生脑抽了关上了，可能当时他跟我一样觉得这个接口并没有啥用吧。



在1.4.0的所有需求中，我觉得最有趣的就是网络状态监测和数据缓存了，可以说这是我之前从未接触过的知识，刚好有了这么个机会不但可以学习还可以直接把学习后的成果运用到实际中，double kill~

我们先来说说看在iOS中如何做网络状态监测，这块内容在之前写的实习日记中也有说明，苹果爸爸给我们贴心的提供了`Reachbility`这个库可以使用，但是这其中有个超大坑，去查了一波资料，网上都是各种骂苹果爸爸的，因为它不是真的Reach，所以导致了GitHub上有个比较火的库叫`RealReachbility`🤣。

不过现在慢慢想起来，其实苹果爸爸做的没错啊，人家这个库提供的是判断你本机的本地连接是否reach，而不是判断你网络是否可达，如果你要确定自己的网络是否可达，应该再加上苹果爸爸提供了另外一套库，结合使用类似`ping`的思想去完成，我原本是想直接使用
`RealReachbility`的，但却无意中发现了滴滴的一个内部工具`ONEReachbility`，使用起来非常简单，有时间我们来剖析下它。

另外一个让我得到比较大的成长是数据缓存这个需求，之前就一直想找个时间好好搞搞数据缓存，在之前的面试中也一直被问到，现在总算是一路顺下来了。在iOS中进行数据缓存的方法就有好几种，比如归解档、Core Data/sqlite、plist等，这三种方式基本上也是目前市面上使用最广的数据缓存方案，尤其是CoreData/sqlite，不过也正是因为CoreData/sqlite太火了，才导致了很多团队对其不满意，因此出现了更加好用的第三方库，比如`Reaml`、`FMDB`以及神秘的`WXDB`，尤其是这个`WXDB`，不知道是在QCon还是ArchSummit上听到了微信开发团队说要开源`WXDB`，当时记得性能吊打目前市面上的移动端数据库，但是一直没有消息，估计是好东西想自己留着吧，emmm。


仔细分析了一下需求文档，发现需要做缓存的入口才五个左右，在这种情况下引入Core Data有点大题小做了，而且缓存的数据之间没有一丁点的联系，就是存储的数据缓存而已，让用户在网络情况不佳时载入缓存数据即可。

因此，最后我采取的做法是直接上归解档，实际上就是利用`NSFileManager`文件。

<img src="https://i.loli.net/2018/05/18/5afe6285a199f.png" width = "80%" height = "80%" align=center />

关于结合`NSFileManager`去做文件缓存网上也有非常多详细的资料啦，就不在此展开了。


以上两个需求可以说是较好的打开了我对数据缓存认知的这个大门吧，后续肯定还会做更多的缓存需求，而且看了1.5.0 PRD，又让我心头一震，做的东西慢慢的在变得完善起来，也在慢慢的考验自己对整个App的架构有没有一个好的理解。

加油吧，骚年~💪

