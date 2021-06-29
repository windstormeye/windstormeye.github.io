---
title: Unity 工程导入 Android Studio 的关键步骤
date: 2020-12-19 21:08:37
tags:
- Unity
- Android
- 游戏开发
---

![](http://img.pjhubs.com/20201219215121.png)

## 前言
最近开始学习 AS 和 Unity 相关的工具链，去实现一些自己的想法。此篇文章意在修正目前网络上错误或滞后的步骤，减少痛苦。


## Unity
### 选择版本
Unity 官方推荐使用 Unity Hub 进行管理 Unity 版本，最开始我也不明白怎么写个游戏还需要处理多个不同版本的引擎呢？后来在实际操作中才发现，在应对不同的游戏开发需求时，我们需要输出的目标平台产物也不一样，而且有些 Unity 版本在不同平台上可能还会出现不同的差异（未验证），而且在我学习的这段时间中，最开始我的学习版本是 `2019.3.8f1` 这个版本，而到了现在我居然已经创建出了三个不同 Unity 版本的工程，而通过 Unity Hub 就可以较为便捷的切换成我们最终想要的 Unity 版本。

![](http://img.pjhubs.com/20201219211516.png)

在我目前的配置中，因为我仅输出移动平台，也就是 iOS 和 Android 两个平台的目标产物，因此在安装 Unity 版本时，只选择了这两个平台，如果你有其它需要的话，可以新建多个不同的 Unity 版本来做隔离。

### 输出产物
当我们想要输出目标平台对应产物时，Unity 默认是桌面平台，如果想要输出移动端平台的产物需要我们在运行 Unity 工程时选择「目标平台」为即将要输出产物的平台。

![](http://img.pjhubs.com/20201219211708.png)

当进入我们已经写好的游戏后，可以在 File -> Build Settings 中做目标产物的属性配置，如包名、系统版本号等。

![](http://img.pjhubs.com/截屏2020-12-19 下午9.19.49.png)

如果我们想要生成对应移动端平台的架构包时，需要注意判断下自己要输出的产物到底是什么架构，否则后续导入 AS 中后你会得到缺失 `libmain.so` 的报错。

![](http://img.pjhubs.com/截屏2020-12-19 下午9.22.31.png)

当这些关键性信息都确认后，我们可以通过 `Export` 来导出。稍微等待一段时间后，我们得到的产物包含一个可运行的 module 和一个核心游戏逻辑的 Module。

## Android Studio
### 导入
准备好一个已有的 AS 工程，通过 File -> New -> Import Module 来导入之前通过 Unity 输出的产物。

![](http://img.pjhubs.com/20201219212658.png)

这里的 `launcher` 没必要导入，这是 Unity 给我们生成的一个 demo app，可以直接通过 AS 导入整个工程，但因为我们已经有一个存在的 AS 工程了，所以可以把 `launcher` 的 `import` 勾取消。

![](http://img.pjhubs.com/截屏2020-12-19 下午9.28.15.png)

此时我们的 AS 工程目录中多了一个 `unityLibrary` 目录（如果你没有修改过名字的话），此时我们需要继续把 `unityLibrary` 给 app 添加依赖。

![](http://img.pjhubs.com/20201219213206.png)

在下图所示的依赖添加面板中点击 `+` 你会看到之前我们所添加的 `unityLibrary`，apply 即可，但因为我之前已经添加过，所以并没有在面板中看到。

![](http://img.pjhubs.com/截屏2020-12-19 下午9.32.57.png)

修改 `unityLibrary` 中的 `AndroidManifest.xml` 文件，注释掉其中 `<intent-filter>` 标签，否则当我们的 app 启动后将直接运行 unity 游戏主体而不是我们的 app 了。 

![](http://img.pjhubs.com/20201219213533.png)

### 运行
此时，我们已经完成了 unity 工程导入 AS 项目中的操作了，并且也可以在代码中引用到 unity 游戏主体类。

![](http://img.pjhubs.com/20201219213916.png)

运行工程！

app 完美的 build 通过且 install 到我们的设备上了，但当我们点击跳转到对应的 item 进入 unity 主体时却得到了 source ID 找不到问题。

```shell
    java.lang.RuntimeException: Unable to start activity ComponentInfo{com.example.myapplication/com.example.myapplication.UnityActivity}: android.content.res.Resources$NotFoundException: String resource ID #0x0
```

一番搜索，需要在 string.xml 中添加字符映射。

```xml
<string name="game_view_content_description">Game view</string>
```

![](http://img.pjhubs.com/20201219214439.png)

## 总结
写这篇文章的时候，我是第三次把 Unity 工程导入 AS 中，第一次因为遇到的问题太多，或者说没有很多的引导步骤，导致毫无头绪，第二次换了个心态，折腾了好久后发现终于搞定，等到这一次时，基本上就轻车熟路了，所有遇到的问题都有头绪。

总而言之，官方都没有提供一个很好的指南去教授给我们这些初学者，而这些事情在高阶开发者面前又先得如此轻易，再加上目前网络上相关问题的解答实在是版本太老，有些解决思路界面上都没有这个入口了。

（为什么这么简单的东西，你们抄来抄去还是没解决是怎么回事。。。