---
title: 为已有的 SwiftUI 代码适配 Apple Watch（〇）
date: 2019-12-07 22:09:34
tags:
- iOS
- Swift
- WatchOS
- SwiftUI
- Combine
---

![](https://i.loli.net/2019/12/08/2SwpGhrAkTCLmZv.png)

> SwiftUI 在 WWDC19 上以其达到了真正跨 Apple 自家生态所有的平台的特性而震撼了当时坐在台下的我。

## 前言
我们都知道「跨平台」是一个面向用户开发「亘古难题」，并且也是当下最火的话题，从 RN 到 Weex 再到 Flutter 已经坐实了，从工程师到决策层都在追求降低单位人力成本，提高人效。

而在 Apple 这个大平台上，一直与业界的主流意识错位。自从封禁 `JSPatch` 后，各大互联网公司内部一直在「偷摸」着研究给自家 app 使用的 `hotPatch` 技术，以至于居然在不断推动着某些现在的异常火爆的某 ter 框架前进。

因此，从 WWDC19 后我内心就埋下了一个种子。SwiftUI 真的是 Apple 提交给开发者的解决跨自家平台的最佳答卷么？入了 Apple Watch Series 5 并且好好的把玩一番后，我发现 Apple 的野心很大，这一次他真的做到了。
 
## Apple Watch 
Apple Watch 第一代发布时，我刚高考完，当时的我并不是 Apple 的受众，只是学长在力推我买 mac 而踏入这个圈子。当我在新生讲座上亲眼看到面前侃侃而谈的学长的左手上真的戴了一块 Apple Watch 时，我的内心被稍微的触动了一下。

后续我开始关注每年的 WWDC，开始「挑灯夜战」每一场开发者大会，不知为何，发现自己已经默认是一个 Apple 生态圈中的一员，会非常热心的参与到有关 Apple 的事情当中。

从此，每年的 WWDC 上我都发现了一个我认为并不是主角的主角——watchOS。我对 Apple watch 的概念一直都是「慢且鸡肋」，但只要出现有关 Apple Watch 的消息我都会下意识的去看一眼。

一直都有在时不时的搜集一些有关 Apple watch 的消息，比如一些在 watchOS 上新奇好玩的 app，因为这个东西对于我来说是一个非常非常新鲜的平台，并且之前根本没有使用过，我不知道这个平台上的产品应该具备哪些必须具备的属性，哪些功能点是共通且已经沉淀下来的，询问了身边的几个同学后，大家给我的回复也都是比如记账、睡眠记录等偏「记录」的答案，我总觉得不太对劲，但当我再继续问到“为什么非得需要一个 Apple Watch 呢？”，他们的回到也很让我感到意外——“一旦有了，就不会离开”。

后来，我仔细一下，我觉得除了少数几个大头被 Apple 点名表扬外，在 Apple Watch 这个平台上各大厂对其的认识都不够，至少我厂目前对其的认识我觉得是不够的，或许说咨询类 app 确实比较难搞定？

说了这么多，主要是在描述我对这个平台的困惑，因为这是第一个 Apple 让我如此纠结的平台，如此不知道如何去下手的平台。关于真正适合在这个平台上的最佳应用模式是怎么样的，我还在探索，但目前我摸索到的是在 Apple Watch 这个平台上，真的不适合做太多耗时操作。

## 实践
我的题目是「如何为已有的 SwiftUI 代码适配 Apple Watch」，前提要求必须是 `SwiftUI` 代码，之前的做法并没有抹平平台差异性，很多东西重复造轮子比较难受，在此不做展开。

我使用之前已经适配过主机手柄的「能否关个灯」游戏进行说明。该小游戏主要使用了 `SwiftUI`、`Combine` 和 `GameController` 这三个 Framework。

为已有的 iOS app 支持 watchOS App 只需要在 Xcode 中添加一个新的 `targer` 即可，因为这部分内容 Apple 也提供了较为的详细的文档说明，我只做适配过程的必须步骤。

### target
在 Xcode 中新建 `target` 时，可以选择 `watch app for ios app` 或者 `watch app`。后者直接新建一个独立的 `watch app` 是 iOS13 和 watchOS 6 之后新增的特性，watchOS 6 允许 watch app 脱离 iPhone 而独立存在，但据我目前观察所看，支持该特性的 app 寥寥无几。

思考了一下，该游戏只是原先版本的平行拓展，并没有单独给 watchOS 平台增加某些独有的特性，因此我也并不准备支持其成为一个独立的 `watch app`。

### notification & complication
`notification` 的支持与我们之前的经验是一样的，不太相同的地方是 `complication`，这个东西就是在表盘上的入口。

![支付宝付款码在表盘上的入口](https://i.loli.net/2019/12/08/ZFtWgMDAU9HNmdQ.png)

个人觉得 `complication` 会是一个非常值得研究的东西，它并不仅仅只是一个快捷入口那么简单，不过目前我们的这个游戏暂未涉及到，先不考虑。

### target membership
最开始我的想法是这样的，既然 Apple 已经表明了 `SwiftUI` 的跨端特性，我下意识的认为只需要对需要编入 `watch app extension` 即可，但却发生了以下问题：

#### 问题一
创建好我们需要的 `target` 后，想跑一下默认自带的 `hello, world` 模版代码，但却遇到了这个问题：

`The run destination PJHubs is not valid for Running the scheme 'watchapp'.`

解决方案也非常的简单的粗暴：重启 Xcode 即可解决。

#### 问题二
`GameController` Apple Watch 不支持。好吧，其实这是我的锅，然后使用了提示的这个宏定义写了一些规避代码。

```swift
#if !os(watchOS)
#else
#endif
```

#### 问题三
什么！居然连 `UIScreen` 也不支持。好吧，其实这也是我的锅，`UIKit` 并不能在 `watchOS` 上使用，在 `watchOS` 上得使用 `watchKit`。

其实这也说明了，**通用的 UI 组件一定不能引入平台差异性**。

#### 问题四
太慢了！！！

为什么编译一次 `SwiftUI` 代码一次都 Xcode 11.2.1 了还这么慢！！！在适配的过程中差点直接劝退，因为真的太慢太慢太慢了，再加上经常性的代码渲染失败、代码提示消失等等问题，开发体验真的是巨差！！！

没想到的是，居然都到了 watchOS 6 了，都还需要必须连接 iPhone，并且先把 watch app 编译到 iPhone 上，再从 iPhone 上重新安装到 apple watch 上。

艹！

### 工程结构
工程结构比较简单，就是一个正常的 target 工程结构。

![代码结构](https://i.loli.net/2019/12/08/X2RBDo41irf5yHY.png)

## 总结
稍微修改一下，我原先的工程就可以直接在 `watchOS` 上跑起来了。我又仔细的思考了一下，原来我之前遇到的这些问题都是因为我把 UI 组件强行限定了运行平台，如果后续再把 UI 组件封装得更好一些，可以直接编译到 macOS 平台上。

在我的游戏逻辑管理类 `GameManager` 中，除了把 `GameController` 的逻辑去掉外，也并不需要做任何其他的操作，这两点点确实让我感到惊讶。

最终我还是把跑在 `iOS` 和 `watchOS` 两个平台上的所有源码都分开了，因为 `watchOS` 上的空间真的有限，很多东西都要重新思考是不是用户真的需要。

后来，我突然感悟到，为什么我们非得要写一套代码，多端运行呢？其实 Apple 已经做的很好了，能够在 UI 层上直接抹掉大部分的平台差异性，剩下的逻辑部分也确实不应该做过多的操作，Apple 的这次操作我很喜欢。

## 下一步
下一步我会继续尝试性的使用更多的 watch app，并且是真的日常去使用，就目前周末使用的这一两天来说，正是入手的好时机，可以把我之前想做的一些事情，想做一些工具都开始付诸于行动。

关于这个我适配的这个游戏你可以在 [github](https://github.com/windstormeye/SwiftGame) 上找到源码，可以在[我的小专栏《Swift 游戏开发》](https://xiaozhuanlan.com/pjhubs-swift-game)上找到游戏讲解。

Apple Watch 是一个如果你没有狠下心去购买就不会去购买的产品，一旦你购买了就一定会离不开它的产品，我也很期待自己能够在 apple watch 这个平台上玩出些什么～