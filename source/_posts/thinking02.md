---
title: 再见了滴滴，再见了字节跳动
date: 2019-06-24 13:30:46
tags:
- 面试
- 滴滴
- 字节跳动
---

> 今天办完了在滴滴的离职手续，校招入职也停止了。回过头去看，有很多想要去表达的东西。

## 在滴滴发生的一些有趣的事情
我负责的是一个大数据可视化内部工具产品 iOS 客户端和前端。其实在滴滴的日子里我是在一个舒适圈当中，很多人都说在舒适圈里呆久了会“咸鱼”，但是我个人觉得吧，“咸鱼”久了能够发觉自己到底适合什么，现在应该去做什么。

### 产品 Swift 化
其实我还挺感谢这段时间的，有时间让我能够把一个纯 `Objective-C` 的工程全部迁移到 `Swift` 上，截止到今天已经前迁移了 `85%`，正是因为这个经历让我接下来做的所有的东西都在尽可能的使用 `Swift` 进行。

### 有趣的人
#### 实习生同学
没记错的话，我应该伴随四波实习生了。有些实习生同学到现在跟我都是很好的朋友，他们后来大部分都去了 BAT 和 TMD，如果大家需要内推的话，我可以帮忙联系一波哈哈哈～

我很少去问大家离职的原因，但隐约也能够看得出来。一部分同学是外地过来实习，然后做了一个跳板。其实这种做法我不排斥，但是这种做法背后带来的影响真的很难受。曾经有一个后来去了百度的同学，距离正式离职还有两周的时间，新版本需求来了居然跟我说他不做了，要离职了......甚至还有上午来签到，中午去面试，下午赶回来签退，晚上回去写需求的「奇葩」，然后 PM 各种找不到人。

滴滴是我实习的第三家公司，原本我有萌生回校考研的想法。但是后来见识到了一些研究生同学的「实力」后劝退我了，也慢慢想了很多，如果后续我感到比较累了，应该会去申请读研究生吧。

#### 淘宝大哥
去年组里来了一个从淘宝出来的大哥，据说拥有 10 年移动开发经验。刚开始我特别佩服，但是在接下来的沟通中我发现了他有有一些地方的思考和实践完全匹配不上 10 年经验，所以也在慢慢的跟他在心底里较劲。大哥想在产品里推 `weex`，我学了一遍 `weex`，做了一个 [todo-list demo](https://github.com/windstormeye/WeexPractices)，发现并没有什么优势，而且与 RN 同样是做了一个 DSL 再转换成 native 代码，但是可以基于「精简版」 `vue` 进行开发的体验符合滴滴基础架构强依赖 `vue` 的优势。

后来 `flutter` 1.0 发布了，大哥又说要 all in `flutter`，其实我到这个时间节点上已经很厌烦了，之前已经在上一个版本中不经过团队决定擅自引入 `weex`，这已经给了后续开发维护和包大小（虽然并没有多大）挖了坑。现在又要 all in 到 `fullter`，这很明显是一个屁股决定脑子的想法。在组里当时还聚集了一波前端、客户端和后端的同学开了个研讨会，本以为大哥已经使用 `flutter` 做了一些 demo，验证了一些产品差异性问题，但整个会议下来通篇都是引用其它资料，会议结束后我非常恼火。

因此我接下来用了一周的时间完成了 `flutter` 的调研，产出[三篇调研文章](http://pjhubs.com/2019/01/17/flutter-3/)，得出了「`flutter` 现阶段不错，但不能直接拉入使用，没有意义」，在人员允许的情况下做技术创新可以的决定。很明显，大哥又直接在下一个版本中上了 `flutter` 模块，到这里我已经忍无可忍了。上 `weex` 和 `flutter` 都是他一个人的决定，而且还在催着我赶紧上，我说「我不能上」，还给我黑人问号。

还有一些其它的事情，让我觉得他的 10 年移动开发经验有种「怪怪的」味道。

#### 前端小哥
在回校写毕设之前我都在为负责产品写对外服务的版本，说白了就是把一些核心页面转为 `H5`，套壳发布。这段时间其实我还好，基本上学习了 `vue` 的全套脚手架，也熟悉了一些前端开发中的问题。

这一切都是一个前端小哥在带着我。刚开始我觉得他很好，对待问题有钻研的态度，也很愿意分享自己的知识。但是直到后来我突然发现他的状态好像发生了变化，遇到了几个需求时，跟我说：“如果产品没催你，你就别管了”。那时我心底里开始有了不对劲的感觉，感觉大家都是在围绕 PM 去打转，而不是围绕如何做好产品这件事去思考。不过也有可能是因为这个产品并不是核心。

### 工作环境
我一直都很喜欢滴滴的工作环境，甚至去参观了一些其它国内外公司后都觉得滴滴的工作环境直接秒杀，而且滴滴是有人文素养的，我觉得应该没有多少家公司能够专门安排健身教练们每周三下午去每一个办公区「拉起」每位同学起立进行工位健身吧？而且滴滴还有「全员运动健身计划」，每个办公区都有配了自家健身房，也推荐大家去健身，我从去年八月份开始到今年五一，增重了 10 斤，体形都出来了！

滴滴的食堂我不能说价格有多实惠（其实就是贵），但是应该算我了解到的各大公司食堂「好味道」 top2 了吧。

### 团队氛围
团队氛围应该是直接劝退我的一大最主要的因素吧。可以很坦诚的说，我没有感受到团队需要我的感觉，很多时候我都在思考到底是我的问题还是团队的问题。

从确定要留在滴滴开始到现在，在遇到一些问题时我给自己开脱的借口是一直都是**「滴滴有让我足够自由的时间去做我想做的事情」**，确实也让我有足够的时间去做了我想做事情，但是这个团队氛围让我一直摸不着头脑，不过很有可能我在的是一个后端主导的部门，但是我在前端同学里也不受到看重，感觉我一直处在一种「游离」的状态，我看上去属于这个团队，但是这个团队里却没有我的位置。

其实如果后续能够一直留在这个团队里我也无所谓，因为时间很自由，我可以兼顾生活、工作和兴趣。在快速完成需求后，剩下的时间都是我的了，不会有说盲目加班的到特定时间的情况出现。但是到了五月份末时，公司层面的 HR 给我打了一个电话，沟通我入职后转岗的事情，我感觉到了苗头不对。沟通了一段时间，最终确定我居然要去「国际化支付」后端团队，一脸懵逼。

其实转岗到后端我也 OK，甚至也已经做好了准备，但是仔细一下：“我现在做的事情都没摸透呢，为啥这么着急转岗”。转岗我个人认为是要在目前的领域里已经相当熟悉了，遇到了一些情况能够提出很好的解决方案，而且我以后也有转岗到后端的准备，但是近期没有这么快。

### 后记
现在回过头去看，有很多个时间节点都已经帮我决定要离开，但是我一直在拿「时间自由」这个借口来安慰自己，因为「时间」自由这件事让我得到了很多，可以很坦然的说——不是因为钱。


## 字节跳动呐！！！
跟字节跳动扯上关系应该是去年年初，当时已经有字节跳动的 HR 通过 github 找到我的联系方式，邀请我去面试，但是当时我在滴滴的成长还是比较平稳上升的，不快也不慢，整体氛围我都很喜欢。甚至后续都字节跳动的技术 leader 都加了微信邀请我去面试，在最后时刻我都鸽掉了，因为我能够明确知道我肯定能进字节跳动，但我还是很舍不得滴滴的氛围。中间还有快手、天猫的同学也通过 github 联系到我，但每次都是在最后的时刻因为滴滴的氛围全部放弃。

没记错的话，字节跳动总共给我发了七次面试邀请。在最后一次面试邀请时，我接受了，因为我感受到了老天在帮我做一个决定。而且在拿到 `WWDC19 Scholarship` ，逛一圈硅谷后，我也认为自己应该出去看看了。下面是几轮面试过程中靠着印象回忆起的一些问题。

### 一面
一面是个小哥哥，人很 nice，进门后给了一个满满的微笑，把我的心理防御直接击破，状态回来了。

* **自我介绍**。顺着自我介绍说了好久，这点很重要，一个好的自我介绍，突出重点后基本上都在围绕自我介绍展开了。
* **WWDC Scholarship 做的是什么**。顺着这个给自己挖了坑，被面试官认为我很会做 UI。问了一道我之前没考虑过的问题：当一个 `UIButton` 使用 `UIView` 动画从 `(100, 100)` 到 `(200, 200)` 坐标的过程中，如果用户点击此时的 `UIButton` 会不会触发点击事件。
	- 刚开始很快的说了“不会”。但是想了一下后，又改口说了“会”。实际上是不会，这涉及到了三种 `layer` 类型的理解，[可见这篇文章](https://jackwzx.github.io/2017/11/12/iOS-iOSCALayer的presentLayer那点事/)。
	- 在移动的过程当中，输出该按钮的 `frame`，结果会是多少？这个我答出来了，是移动结束后的 `frame`。 解释同上。

* **给你一个 `A` 和 `B` 视图，如何找到它们的最近父视图**。我一开始直接就套用「二叉树最近父节点」问题的思路去想，但中途小哥哥一直在给我提示，不用把它想得那么难，这是一个很实际问题。到最后我才明白，其实只需要递归出 `A` 视图的 `superview` 和 `B` 视图的 `superview`，再用 `Set` 搞一搞就行了。
* **无限循环轮播图的实现**。常规问题，但是我扯太多了，提出了几个解决思路，可以只用三个 `UIButton` 实现。
* **自定义转场动画**。直接打开 `Vary` app，告诉面试官是怎么实现的。
* 中间应该有问到一些**计算机基础问题**，被我看出来了，然后叫停，再打开之前基于 `Cocos2dx` 做的一个游戏，涉及到了资源争抢、多线程、性能优化、多节点渲染的问题。直接过
* **滴滴带给你什么成长**
* ......
	
还有一些问题想不起来了，一个小时多一点。中途我有好几个问题都还在思考中，面试官就跟我说：“其实你回答不出来也没关系，这就是个概念问题”，我懵了，还能这样面试？好吧，那就索性说不了解好了。面试官面带笑容的出去，我觉得一面评价应该还行。
	
### 二面
去了趟洗手间，二面面试官太严肃了。~~跟一面简直就是天壤之别，面试氛围尬得我不行，有几次氛围太压抑都想直接跟面试官摊牌：“你是不想面了还是怎么着？”。~~（HR 小姐姐建议删除）

刚开始前两个问题我没看出来什么问题，但是越到后边我就感觉有点「怪异」，二面面试官应该不是做 iOS 的。到后边我发现了他打开了我的[PJ 的 iOS 开发日常](https://github.com/windstormeye/iOS-Course) repo，每一个问题都是我的 repo 里记录的问题，然后让我在白板上画图写思路写核心代码。总之二面给我感觉就是在验证你的水平，repo 里的东西是不是都是你写的，都是你的个人成果。

* MRC 和 ARC 的不同
* NSString
* 内存划分
* __weak
* 响应链
* https
* 你和其他同学有什么不同
* ......

有些问题也想不起来了，都是 repo 里的内容，没啥压力，唯一的压力就是我都没见过二面面试官的牙齿。二面大概四十分钟不到，结束后大概 12:30。带我去吃饭，也问了我 `WWDC19 Scholarship` 做的是什么，我在滴滴的一些情况，整个饭局也很尴尬，但是字节跳动的饭菜，比滴滴食堂差远了。

![午饭](https://i.loli.net/2019/06/24/5d107c72e463879448.jpeg)

### 三面
等了大概有十分钟左右，leader 来了。我们之前已经在微信上聊过了，所以整场下来就跟朋友聊天似的。告诉我他要问我三个环节，第一个是算法问题；第二个是设计模式；第三个是个人规划。我听到着基本上就断定稳了。

* 聊了 WWDC。你最喜欢 WWDC 哪个环节之类的问题。
* 给定一个无符号整型 32 位数组，请把所有 0 后置，请写出完整代码。简单到怀疑，刚开始以为有坑，问了一些细节问题。
* 题目同上，要求为用户可以指定后置的数字。封装了一下。
* 题目同上，要求用户可以指定后置的判断条件，比如二进制下第一位为 0 的数后置或能够被 2 整除的数后置等规则。其实还好，封装了一个 `Closure` 暴露给调用方，自己填写比对规则。
* 尽可能的优化时间、空间复杂度。我只能把时间复杂度优化到 O(1)，空间复杂度搞不定。
* `tableView` 多 `type` 优化。就是要设计一个好用的工厂。我用了配置文件，初步要求达到了。
* 游戏和 `Vary` 又帮了我，一些强弱引用的问题看到实际的产品中解决了问题就不再追问了。
- 个人意愿，聊了很多。

### HR 面
HR 在微信上跟我说三面面试官反映都不错，她就不面了，我：“？？？”

### 后记
其实我感觉这次字节跳动的面试挺玄乎的，感觉就像朋友聊天侃大山似的，有些问题我都还没怎么思考就直接摊牌跟我说这些概念问题不懂也没关系。也没有遇到上来先“啪”的来一套算法题的情况。

其实我感觉是 leader 和其它同学都知道「我」，不管是从其它社区或者 github 上都了解到了「我」到底有没有实力，再加上有滴滴这么长时间的实习加成，其实说白了还是 `WWDC19 Scholarship` 好使，大中华区被 Apple 选中的优秀学生开发者就 27 个，今年还是最多的一年，都被 Apple 选中了还挑什么是吧～


## 我的想法
很多同学都在问我：“你不是不喜欢加班吗？”

其实这个问题的成立是放在做的事情不讨厌的前提下，如果说负责的事情已经提不起什么兴趣了，就算一天只工作两小时也觉得这两个小时过得很浑浑噩噩。

还有同学问我是不是头条给的薪资高。其实说实话，还真不是，头条的 HR 在沟通入职详情时直接问了我：“你认为自己是一个什么样的水平，SP 还是 SSP？”，我直接说：“我都无所谓，重点要看做的产品是什么”，你看，像我这样的人怎么可能赚大钱 2333。

其实我真不想离开滴滴，今天去办离职时，感觉进入办公区就跟回家似的，状态都回来了。但是这个地方已经不属于我了呀～整个团队除了之前带我的导师，没有任何一个人起身告别，好吧，那就这样吧。

其实我也没什么其它的想法，存粹就是未来入职滴滴后要做的事情我不喜欢，既然不喜欢那就去一个能够提起我兴趣，看重我的团队，更何况也可以借此机会改变一下自己的工作习惯，去感受一下大小周的快感（放屁！

![持续了四个小时的面试](https://i.loli.net/2019/06/24/5d10844d4b5aa16116.jpg)

## 多说两句
给大家提个建议，在读别人的文章时，请不要带上自己的个人情绪，如果你真的要带上情绪，请带上跟作者当时写此篇文章一样的情绪，如果你把握不好，没法跟作者保持一样的情绪，那，咱能别带着情绪读文章么？

而且，我的博客不是「硬」的，它很「软」，你看了我的博客就相当于在跟我聊天，我的博客是一个我的「活生生」替身，它是有「生命」的，它表达了当时我所处环境里人和物对我产生的影响，我把它记录了下来。

这是一件很难得的事情，同时这也是我为什么一直不开 RSS 不开评论的一大原因，避免了一小撮「极端同学」拿着自己的经验去评判别人。你要记住，你只是你，你并不是我，我经历过的东西你没经历过，你经历过的我也没经历过，你的经验对于任何人来说只是具备「参考」价值，OK？