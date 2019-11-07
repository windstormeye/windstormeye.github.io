---
title: DiDi（十九）
date: 2018-04-23 21:34:07
tags:
- iOS
- DiDi
---

## 2018-04-23

今天早上做完了实验才去的公司，修复了点击push消息打开webView时只能从首页进入的bug，原因是因为之前从tabBarController选择navigationController时直接写死了0，正确的做法应该是拿到当前`tabBarController.selectIndex`，接着又完善了在全部报表部分需要的调整修改的视图。

睡了一觉，起来后居然萌生了想要翻译苹果官方文档的冲动，开始着手翻译[Views Programming Guide for iOS](https://developer.apple.com/library/content/documentation/WindowsViews/Conceptual/ViewPG_iPhoneOS/Introduction/Introduction.html)，算是给三战四级找个练手的地方吧（谁让我英语就是这么差🙄）。

最后搞定了使用cocoapods进行组件化的第一步，详见[我的iOS开发之路](https://github.com/windstormeye/iOS-Course)


## 2018-04-24

今天本来是要接待新iOS开发同学的，一直在疯狂补相关的开发文档，补完了弄来弄去居然没等来人🙄。我有种预感，他应该不会来了。

邻近中午的时候完成了一个巨大的壮举！！！（对于我自己来说），我居然真的能够靠一己之力完成一个GitHub超过100star的项目！！！刚好一星期，真是人生中的第一次！！！随后继续完成我的翻译工作，感觉通过翻译官方文档的这种行为真的能弥补自己的很多不足🙄。

下午的时候又开了一个新坑！！！把现在的滴滴数据App用Swift替换，慢慢替换吧，感觉每天都做一些的话，至少得一个月。😔。

## 2018-04-26

今天有一个好消息一个坏消息。

**好消息**：成功的把“多语言”设置模块完全迁移到了Swift上，这是一块儿相对小的模块迁移，还算是平滑的迁移完成了，达到了练手的目的。现在是各完成一份OC和Swift的多语言转换模块，给我感觉Swift版本的更赞一些。hhhh，下次有时间找个机会开源出来，😝。还有`segementView`Swift版本，把之前OC的版本不管从功能上、视觉上、使用上都做了优化，但是某些还不够Swifty，还是有些OC的味道在里边，慢慢做吧，给自己定下的期限是一个月，也就是五月份底，那个时候应该能够替换到70%以上（按模块算）。

好了坏消息来了。在Swift中使用cocoapods，需要使用`use_frameworks!`，但问题就出在这，使用`use_frameworks!`会让Swift的第三方库以动态链接库的方式进行集成，但正是因为这样导致了集成其它的第三方库出现了问题，原本集成好好的库居然被报找不到。细节我就不展开了，给大家一个链接自瞅瞅吧[https://segmentfault.com/a/1190000007076865](https://segmentfault.com/a/1190000007076865)

最后我的解决方案是不使用cocoapods去集成Swift需要用用到的库，改用Carthage。给大家个使用文档[https://blog.csdn.net/Mazy_ma/article/details/70185547](https://blog.csdn.net/Mazy_ma/article/details/70185547)

在集成的过程中，还出现了这篇博客中所阐述的问题[https://blog.csdn.net/asdf_2012/article/details/50800791](https://blog.csdn.net/asdf_2012/article/details/50800791)

最后build通过后，推上git，Jenkins构建，等了一会，没想到居然构建失败了。看了Jenkins报告，好吧，刚通过Carthage集成link进去的SwiftJSON没找到😂。突然焕然大悟，这肯定找不到啊。我是通过Carthage在本地链接到工程中，Jenkins上哪知道我link了啥啊。问了Jenkins的同学，还确实是Jenkins只对Cocoapods做了配置，后边再仔细一想，确实应该只对cocoapods做配置，这工具确实很方便。

那最后怎么办了呢？我下班跑路了，刚才又翻到了一遍博客[https://www.jianshu.com/p/d0dc92d9a31b](https://www.jianshu.com/p/d0dc92d9a31b)，虽然跟这篇博客中的表述的内容不太一样，是直接连库都找不到，报红了。不管怎么说，今天至少迁移到Swift上还是比较顺利，明天再继续苦逼吧。😔


## 2018-04-27

emmm，今天被Swift的`!`和`?`虐惨了。如果没有强制解包，居然特么字符串中能给我带上`Optional`，彻底无语了。🙄，这种主打类型安全语言写起来真是难受得不行，基本上我每写一行代码，都会提示我补全`!`或者`?`，虽然我非常清楚这么做确实是Swift主打所谓的类型安全，但是感觉!!!和???比我的代码行数还多。

不过从OC转到Swift有一块我非常喜欢。首先，文件的数量大大减少了；其次代码变得非常简洁，看上去一点都不啰嗦；最后，Swift的某些特性让编码过程变得十分有趣，可以说是动不动就高潮。😂

不过！！！今天我的Xcode崩了三次，代码配色没了不下十次，代码补全几乎随机出现卡顿，跟OC完全没得比，还有一点非常难受，不过我估计是因为跟OC混编的原因，在桥接文件中添加新的内容，每次都得要`command + shift + B`重新生成Swift转换才能找到OC中对应的类和方法，真是迷。

今天尝试把一个入口迁移到Swift上，今天可以说是完成了10%吧。整体还算不错，Swift对界面的编写友好度比OC好起码10倍！不得不说，慢慢的爱上了它，这波迁移值！
