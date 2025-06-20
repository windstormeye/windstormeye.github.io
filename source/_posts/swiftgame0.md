---
title: Swift 游戏开发 - 序言
date: 2019-08-29 22:42:37
tags:
- Swift
- iOS
- 游戏开发
---

![]( https://images.xiaozhuanlan.com/photo/2019/4305214109ad56a7bbc8ed9e66c2bbf6.png)

## 前言
哈喽～大家好呀！我是 PJHubs，一名开源爱好者，正在努力成为全栈工程师，喜欢诗和远方。

我是 WWDC19 大中华区学生奖学金的获得者，之前在滴滴负责一个大数据可视化产品的 iOS 和 Web 端开发工作，现在在字节跳动负责今日头条和西瓜视频的 iOS 客户端相关内容，业余时间参与维护 Vary app （曾冲进 App Store 效率榜前 20 ），其它时间会做遵循「最小化可行性产品」的模式做一些好玩的产品。 你可以来我的博客看看我最近都在做些什么：[pjhubs.com]( http://pjhubs.com)。

说到为什么要开这个专栏，我是这么想的，我需要一个「地方」去激励我持续输出，最开始我特别喜欢在知乎上答题，并且几乎每天都会沉浸在其中，但久而久之，我发现知乎的风气不对，转而投身于自己的博客中，并且一直输出到现在。

后来，我发现需要跟一些同学进行更多的交流，会把我的博客文章分发到例如掘金等技术社区中，但经过一段较长的时间后，我发现还是没能有一个长期激励我的地方去做耕耘。我曾经也有想过直接在 gitbook 上写书，但是写了三章后又发现内容越写越多，根本坚持不下去；也试过在 B 站通过视频的方式去讲解一些东西，后来发现录一集视频需要花费的时间太长，以至于正反馈不足又放弃了；目前唯一还在坚持的是在网易云音乐上的电台《 PJHubs 》，录一期播客前后最长不超过两个小时的时间，在空闲时间里可以快速的完成。

现在博客写得多了，我想再通过一个比较激进的策略去让自己写出一个系列的文章。我对计算机的定义是「工具」，所以很多时候我并不会一股脑的扎入浩瀚的技术浪潮中，但是我会通过做一个个遵循「最小化可行性产品」的模式去做一些好玩的产品，通过这些小产品来反向激励自己去学习实现某个想法中应该学习的知识。通过这个模式，我在完成 [PLook]( https://github.com/windstormeye/Peek) 这个产品中花费了将近两周的时间刷完了 OpenCV3 这本书，入门了计算机视觉。

## 关于这个专栏
我自认为从小学到初中其中的四年的时间中，没有人比我更喜欢玩游戏啦。当初为了和小伙伴比赛谁能点亮更多的 QQ 图标，我玩遍了当时市面上所有的腾讯系游戏，（我的第一款网游是《 QQ 华夏》）以及发展到后面的盛大系、完美系，跑跑卡丁车我开到了黑手套，直到现在我还会偶尔的刷一刷《暗黑 3 》。应该没有同学比我还沉迷 4399 和 3366 小游戏了吧……噢，还有《摩尔庄园》和《赛尔号》。

我在大二的暑假实习中，做了一段时间游戏开发，当初使用的是 `Cocos2dx` 这个框架，`Objective-C` 与 `C++` 进行混编，但因为当时国内对游戏版号的收紧，导致这个游戏在最后关头不了了之。

通过这个实习，打开了我对游戏开发的大门，以至于到现在我都有在时不时的写一些好玩的小游戏。从 ARKit 出来后，我对游戏开发的兴趣达到了最高点，并一直在筹划使用纯原生的方式在 Apple 平台上做一些好玩的小游戏。

所以，通过这个专栏，我将与你一起在 Apple 的生态圈里使用 Swift 做一些好玩有趣的小游戏，同时也算「逼迫」我能够回忆起童年的欢乐吧～

## 准备搞什么事情？
我现在对这个专栏的规划还没有那么清晰，但是可以保证的是会涵盖以下技术栈：

* UIKit
* SwiftUI
* SpriteKit
* SceneKit
* ARKit

还可以确定的是我会尽量只使用 Xcode + Swift 完成，因为我也想最大化 Apple 自家的游戏开发能力。目前确定的游戏主题有：

* 能否关个灯？
* 黎锦拼图；
* win98 扫雷；
* 人工智障的井字棋；
* 疯狂弹一弹；
* 躲避球；
* 见缝插针；
* ……

以上这些小游戏我同样会基于「最小化可行性产品」的模式去实现，UI 上大家就不要太追求啦～我尽量保证符合 Apple 的人机交互指南。

## 后记
这个专栏会比我在博客以及其它平台中**优先发布一个星期**。主要我没想到有比小专栏更好能够激励我的地方（有更好的麻烦告诉我啦～），如果直接在博客里每篇文章的最后都放上一个二维码，我会觉得我在「卖文为生」，所以，如果你也想激励我继续输出，欢迎订阅我的小专栏。

关于定价的问题，最开始我实际上是想直接免费或者象征性的收 1 元，但仔细一想，那为什么不直接通过博客去写呢？最后的这个定价主要是让我有一个使命感，你们订阅了这个专栏，我也会认真的对待这件事，而不会一时的兴奋导致最后渐渐消失。

小专栏地址：[https://xiaozhuanlan.com/pjhubs-swift-game]( https://xiaozhuanlan.com/pjhubs-swift-game)

github 地址：[https://github.com/windstormeye/SwiftGame]( https://github.com/windstormeye/SwiftGame)