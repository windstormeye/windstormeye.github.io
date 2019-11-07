---
title: DiDi（十一）
date: 2018-03-05 09:39:23
tags:
- iOS
- DiDi
- internship
---

## 2018-02-26
1. 小红点通知实现方案：
    * 给UITabBar做拓展；
    * 给UITabBarItem做拓展；
    * 使用系统提供的badge，要求系统最低为iOS 10。
    
    此处之前遇到了一个问题，小红点这块是我做的，但是当时没有考虑到系统版本要求，直接使用了iOS 10以后自带的tabBarItem.badge属性设置了小红点，这就导致了当用户为iOS 10以下系统时，GG。
    
    但是最后没有发现这个问题，手上没有iOS 10以下的设备，导致就成为了一个线上bug。同事的解决方案是给UITabBar做了分类，让我意外的是居然不是给UITabBarItem做分类，其实这样也行，但是让我更加意外的是，他并没有执行完所有的路径测试，导致当“我的审批”通知都结束后，并不能消除UITabBar上之前出现的小红点。

    我找出了原因，具体出错原因是因为同事居然写了两份功能代码，用UILabel渲染出了小红点，又用UIView再渲染了一次，不过UIView只做了backgroundView作用，给这个UIView做了tag标记，但让我感到非常奇怪的是，居然没有对UILabel做tag标记，导致最后for-in当前UITabBar.subviews时根本就没remove掉UILabel。最终我把无用的UIView删掉，把原先给UIView的tag赋值给了UILabel，遂解决。

2. 重温OC中的“_”和“self.”
    * 比如people：
    我们可以用_pe0ple和self.peole两种方式去访问people这个变量，而当使用实例变量也就是“_”的方式去访问people时，只是拿到people本身而已，如果我们通过self.people的方式去获取，则是通过getter方法去拿到这个变量。

    说的再简单一些，如果假设我们给people赋值为8，那么通过_people去访问，只能拿到8，但是如果我们通过self.people去获取变量，实际上是访问了

    ```ObjC
    - (NSInteger)getPeople {
        return _people
    }
    ```
    我们可以重写这个getter方法，想想看！这是一个我们可以自定义配置的方法！能做的事情就出来了！！！
    ```ObjC
    - (NSInteger)getPeople {
        _people = 10;
        return _people
    }
    ```
    emmm。总结来看，如果我们对这个变量毫无要求，完全可以通过“_”的方式去访问，如果我们对其有了二次定义的更多需求，比如对tableView的dataSource的setter方法中，数据源赋值过来了，可能会执行一次reload，此时我们就可以通过self.的方法使用这个变量，而引起其他变量的变化。

## 2018-02-27
1. 公司昨天下午给实习生配了新电脑，做iOS的是17款MacBook Pro 15，导致所有环境都需要自己去重新搭建，其中遇到了一个比较尴尬的问题，昨天进行`pod install`失败的原因找到了，是因为当执行pod时会比对本地git账户生成的SSH key与远程是否一致，昨天并未上传本机生成的SSH key，进行下载是权限出错。😓。

2. 关于cocoapods的一些详细内容，英语好的可以直接去[官网](https://cocoapods.org/)，中文翻译的[在这](https://www.jianshu.com/p/efb3e2b44623)

3. 关于动态库和静态库的一些[解释和区别](http://www.cocoachina.com/ios/20161012/17730.html)

4. 获取一个view中的内容，return回一张图片。思路：系统会维护一个CGContextRef的栈，UIGraphicsGetCurrentContext()会取出栈顶的context
    * 在drewRect方法中调用UIGraphicsGetCurrentContext()
    * 不用drewRect默认自带提供的上下文，自己造一个上下文。
```ObjC
// 自己造一个上下文
// 此处的size为传入view的大小
UIGraphicsBeginImageContextWithOptions(rect.size,YES,0);
// 获取上下文
CGContextRef context =UIGraphicsGetCurrentContext();
//然后在context上绘画。。。
// 画完后，获取这个上下文中绘制的内容，保存成UIImage
UIImage *temp = UIGraphicsGetImageFromCurrentImageContext();
// 关闭上下文
UIGraphicsEndImageContext();
```

5. 问题：
    分享完后的back回App，并未消失shareView。

6. DiDi学院公开课：
    * 最开始滴滴只有出租车，快车业务因为发展太快了，直接copy了一份代码
    * 一条业务线完成后，另外一条还未完成，修改了公共处代码，导致前一条失败
    * 平台型架构。微信、天猫、淘宝。
    * 各个业务线的团队成员要保证自身业务线的快速迭代，平台团队，要做一个支撑
    * 最初三步走：
        平台化——TheOne
        组件化——乘客端5.0，司机端5.0
        动态化——热修复，插件化，Hybrid


## 2018-02-28
1. 今天遇到了一个大问题，在某个时间段重新build工程后，发现Swarm提出了没有找到“语言服务”！当时都惊了，之前在Swarm里从未提出要求寻找对应的“语言服务”，这莫名的来了一出。刚开始还以为是Swarm上出了问题，先去找Swarm的开发团队负责人，尬聊了好一会儿，他一直以为是我这边配置少了什么东西，不过确实是，因为Swarm的断言截获了错误，弄了一会儿，发现这个问题貌似是“小笑脸”的版本号更新出错，就把这个问题丢给了AfantySDK的开发团队，人家说，“对，这是0.6.8版本的一个bug，我们稍后会打一个tag解决这个问题”，woc，当时我的心情！！！一个中午都在为这个事情脑热中，以为是自己的操作不当。


## 2018-02-29
1. 修改了UITabBar。主要是只通过tag的方式清除掉了一个View，但实际上Label才是重点。（周一只是看懂了同事写的逻辑，和review他之前写的所有代码。🙂）

2. 添加了Load菊花，为首页和发现页面的载入提升了用户体验。有一种想法，DiDi内部有一个ONEUIKit的统一UI组件，之前没发现这个问题，早知道就不用SVProgressHUD了。也就从今天开始，开始有了一种冲动，去阅读DiDi内部的这些组件，感觉写的非常不错。

3. cancelPreviousPerformRequestsWithTarget方法用于取消performSelector指定方法。

4. setNeedsDisplay和setNeedsLayout的[区别](https://www.jianshu.com/p/b6ade523974d)


## 2018-03-01
## 2018-03-02

这两天基本上都在对之前同事写的代码进行高层封装，JIRA上要求对分享相关组件暴露成API的方式，供今后走JSBridge做准备，所以完成了一行代码调起分享页面。😝。等等还有一些其它的优化。
