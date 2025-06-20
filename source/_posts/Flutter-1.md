---
title: Flutter 初探
date: 2019-01-11 20:39:11
tags:
- Flutter
- 跨平台
---

>原本是准备利用寒假较为充裕的时间好好研究 Flutter ，但最近组里开了一个“跨端技术研讨会”，整场会议下来体验不佳。会议主讲同学没有把技术研究透彻就召开会议，在某些问题的描述上运用了一些模糊的推断词语，导致有些小情绪（时间又很长）。会后大家对讲述的内容都不是特别满意，并且缺失了 iOS 原生与 Flutter 的对比这重要的一环，遂把对 Flutter 以及其它跨平台技术的整体研究推上日程。此篇文章为 Flutter 系列的第一篇，主要是初识 Flutter 的上手体验总结。

## 前言

研究一门新技术，不管利用任何手段去探索和实践，我的底线是必须亲手把 demo 写出来，不管看了几篇、几十篇质量有多么高的文章都抵不上动手实践，因为别人所经历过的事情我们没法全盘去经历，双方在对待一件事情的态度上会带入自己以往的经验，但务必保证事必躬亲，唯一无二。就算技术预研时间十分紧凑，也必须遵循“单一变量”原则。

17 年在“蜗牛睡眠”暑期实习时，我做了一个自己在面试前毫无准备的新方向——游戏开发。面试时一点都没有透露出我进来后是要做游戏开发相关的事情，全盘在讨论 iOS 开发内容。正式入职后，我和另外一个小伙伴利用了一个星期的时间分别对 `Unity` 和 `Cocos2d-X` 攻关了产品的核心难点，从语言、社区支持、上手难度、相关类库、定制化难易等几个方面根据产出的 demo 做了对比，最后选择了 `Cocos2d-X` 完成了接下来两个多月的产品开发。

在技术预研环节中，我们并未相信各自社区对各自平台的优劣描述，因为当时全网都在倒向 `Unity` 更适合游戏开发这一边，如果只是通过所看到的资料就盲目进行开发工作，那么这个产品的开发进度将会更加延后。

这是我对技术预研阶段的认识，始终坚持这几点：
* 验证 demo 一定要写；
* 当全网都在疯狂吐槽一门技术时，那么它一定有个很大的优势；
* 当全网都在说一门技术好的时候，大家都快来用它，那么它一定有一个致命的缺点；
* 要针对产品的核心难点做验证 demo，而不是直接拿别人的成果作为自己预研阶段的产出；
* 性能相关的研究一定要使用部分真实或相似需求进行切入，否则无法正确预估正式接入后的成本；

以上是在技术预研阶段自己所坚持的一些点。去年年初开始学习 `React-Native` 和微信小程序当时最火的两个跨端技术，当时即将步入考试周，但每天晚上回宿舍后还有将近一个多小时的空闲时间，遂把两个跨端开发技术进行了快速入门学习，以下是当时输出的几篇文章：

* [小程序初探](http://pjhubs.com/2018/01/08/小程序初探/)
* [小程序初探（二）](http://pjhubs.com/2018/01/13/小程序初探（二）/)
* [React-Native记〇](http://pjhubs.com/2018/01/14/React-Native记〇/)
* [React-Native记（一）](http://pjhubs.com/2018/01/19/React-Native记（一）/)

在开始学习这两门技术时，已经上线了基于原生开发的 [iBistu 4.0](https://itunes.apple.com/cn/app/ibistu/id606795996?mt=8) iOS 客户端。在保证 UI 、数据源和操作逻辑不变的情况下，对两门技术做了一期验证，后续因为时间关系（过年回家）未继续开展。

正是因为通过了自己的手撸完验证 demo 并且对比产生总结，在面对新技术时有了一个较为浅显的把握，让接下来做更深入的研究时有了很大的保障，不会像当时给我上软件工程课的老师那般冒出“微信小程序出来啦！那些做 App 的都要死啦！......”等可笑之语。

所以我想表达的是，承认前辈们在技术方面的经验非常丰富，对新技术也能看个七七八八，但具体研究得有多么透彻也只有自己才知道。做任何事情都得首先对得起自己，尤其对待技术，是就是，不是就不是，计算机没有感情，它并不懂得自行推断。


## 环境配置
根据 `flutter` [中文官网](https://flutterchina.club)上所引导的步骤进行配置，中途可以根据 `flutter doctor` 命令进行检查相关依赖是否配置完成。

### 设备
* iOS: iPhone 7, iOS 12.1.2
* Android: meizu 15, Andriod 7.1.1

### 遇到的问题
* 在环境配置中，官方推荐使用 `Andriod Studio` 进行开发，因为体验是最好的，当然同时也支持 `VS Code` 和 `IntelliJ`。因为开发机“常年”连接公司内网，导致无法在 `Andriod Studio` 中下载 `Dart` 和 `Flutter` 插件，尝试好几次，网上的资料都翻遍了，突然灵光一闪！我特么这是在内网啊！切回外网后，一切顺畅......

## 初体验
Flutter 官方上说的优势之一为“热重载”，新建 flutter 测试项目分别运行在 iOS 和 Andriod 两台测试设备上，iOS 的热重载只要每次 `cmd + s` 即可，但 Andriod 需要执行两次（非必现），看第一次打印出来的信息提示已经完成 `hot reload`，但设备上什么都没出现，必须执行第二次 `cmd + s` 操作后，才能看到真正的 `hot reload` 的效果。

![左：iPhone 7，右：meizu 15](https://i.loli.net/2019/01/10/5c36f04c618e7.jpg)

flutter 官网上对于“热重载”是这么描述的：

> 通过将更新后的源代码文件注入正在运行的 `Dart` 虚拟机（VM）中来实现热重载。在虚拟机使用新的的字段和函数更新类后，`Flutter` 框架会自动重新构建 `widget` 树，以便您快速查看更改的效果。

所以对于在 meizu 15 上需要执行两次保存操作才能触发“热重载”后的效果展示，我的推测是，在第一次执行保存操作时要么没有把新更新后的代码注入进 `Dart` 虚拟机中，要么就是注入了但未触发重新自动构建 `widget` 树。

### 渲染
Flutter 的一大特点，基于 [`Skia`](https://skia.org/index_zh) 框架直接进行 UI 的绘制，在 iOS 和 Android 上都脱离了系统 UI 库，先不讨论具体性能如何，但这种做法相当于至少在 UI 渲染这一层 Google 已经在 iOS 和 Android 两个平台上自己都控制了，可能会受限一些系统 API，但也可以做一些原生不支持的事情。

![Flutter 在 iOS 上的视图层级](https://i.loli.net/2019/01/10/5c37187ca736f.png)

### 差异点
* 入口的 Main 函数入口使用了 `=>` 语法糖，官方说是“这是 `Dart` 中单行函数或方法的简写”：

```Dart
void main() => runApp(new MyApp());

// 我的推测：上下两者相等，论简洁性，确实是好看一丢丢
void main() { runApp(new MyApp()) }
```

* 每一个 `Widget` 都会有一个 `build()` 方法，用于描述如何根据其他较低级别的 `widget` 来显示自己。我的理解就是 `initView` 方法；

* 在 `Dart` 中“万物”（包括布局）都是 `Widget`，这点就类似与 `Objective-C` 中的“万物”都是 `NSObject`；
* `Scaffold Widget` 是 `Material library` 中的一个 `Widget`，提供了 `Material` 风格的基本组件。
* Flutter 中并没有类似 iOS 中的 `UITableViewCell`，直接在 `ListView Widget` 中构建了 `cell`，正是因为没有 `cell` 的概念，所以原本每个 `cell` 之间的“分割线”也需要手动使用 `Divider Widget` 进行索引模拟。推荐一篇关于 `Scaffold Widget` 的[内容介绍](http://flutter.link/2018/03/20/Scaffold/)

* Flutter 的 `Widget` 分为 `StatefulWidget（有状态）` 和 `StatelessWidget（无状态）` 两种，这跟在 iOS 中只要是继承了 `UIResponder` 就具备与用户产生交互进行状态的改变不一样。在 flutter 中如果我们需要实现设计要这个组件是否需要有状态的改变。

### 一些简单操作
* **格式化代码**：`Dart` 疯狂嵌套的代码风格已经被吐槽烂了，好在可以在写完代码后，利用 `Android Studio` 中提供的 `Dart` 格式化代码工具：选择任何一个 `Dart` 代码文件，右键选择“Reformat Code with dartfmt”，代码格式立马变得好看了许多。

### 总结
经过这次对 Flutter 的初体验，对其惊叹的地方有：
* 真的做到了一套代码可以“无脑”运行在 iOS 和 Android 两个平台上，使用 `Andriod Studio` 编写完主体代码后，完全不需要做任何平台差异化设置，直接选择不同平台设备直接运行即可，在加上真的脱离了 `JS Core` 的“热重载”技术，在 iOS 上的开发体验非常流畅和方便！
* 在 iOS 上真的抛弃了 `UIKit` 的所有内容，全都基于 `Skia` 自己渲染，这点跟 `Texture` 在 UI 渲染上有异曲同工之处。
* `Dart` 这门语言本身有着与 `JSX` 类似的代码风格痕迹，尤其是对 `Widget` 做属性的定义时，但从整体上来看因为前身是准备要替代 `JS`，所以在很多地方也有 `JS` 痕迹，在一些细节上又透露着 `Java` 的微小细节，所以从语言本身的上手难度不算大，并没有在语法层面上做出太多的革新。
* 强烈推荐使用 `Android Studio` 进行开发！！！
* 创建 Flutter 工程下的 iOS 平台工程居然主体基于 `Swift`，这点让我十分意外！

目前来看不满意的地方只有一个：
在 iOS 上的长列表滑动卡顿十分严重！！！在快速滑动下，估计只有两三帧，而且每一个 `ListTitle Widget` 上只放了一个 `Text Widget` 啊！太辣眼睛了......[视频在此](https://www.bilibili.com/video/av40402669/)，对 Flutter 抱有所谓“高性能”的同学可以死心了。

## 后记
Flutter 的这一系列的文章引起了当时与会同学的一些“讨论”，当你看到本文时已不是最初版本，这对于从来不修改原文的我来说无疑是一个重大的打击，同时也因为这个事情，让我对 Android 开发的研究也提上了日程，不想再以“我是写 iOS 的......”来规避掉核心问题，真的再也受不了了。