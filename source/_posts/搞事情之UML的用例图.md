---
title: 搞事情之 UML 的用例图
date: 2019-01-05 20:28:22
tags:
- UML
- 搞事情系列
---
> 搞事情系列文章主要是为了继续延续自己的 “T” 字形战略所做，同时也代表着毕设相关内容的学习总结。本文章是 `UML` 部分的第一篇，主要是加强对面向对象相关技术的认识，尤其这反反复复记了好几次，每次用到都要搜索一番的用例图！

## 面向对象技术概述
面向对象的基本建模原则：抽象、封装、继承和分类。

面向对象的基本软件工程：OOA（面向对象的分析）、OOD（面向对象的设计）、OOP（面向对象的编程）和OOSM（面向对象的软件维护）

对象的概念是：对问题域中某个实体的抽象；类的概念是：对具有项目属性和行为的一个或多个对象的描述

属性的定义：描述对象静态特征的数据项；服务的定义：描述对象的动态特征（行为）的一个操作序列。

类的定义要包括：名称、属性和操作三要素。

面向对象呈现设计的三大特性：封装、继承和多态。

面向对象的系统分析要确立 3 个系统模型是对象模型、功能模型和动态模型。

## 用例图
### 参与者
**参与者**是指系统以外的、需要使用系统或与系统交互的外部实体，包括**人、设备、外部系统**等。

### 用例
用例是对一个活动者使用系统的一项功能时所进行的交互过程的一个文字描述序列。可以说，软件开发的过程是**用例驱动**的。

用例是对系统行为的动态描述，属于 UML 的动态建模部分。UML 中的建模机制包括**静态建模**和**动态建模**两部分，其中静态建模机制包括类图、对象图、构件图和部署图；动态建模机制包括用例图、顺序图、协作图、状态图和活动图。

理论上可以把一个软件系统的所有用例都画出来，但实际开发过程中，进行用例分析时只需把那些**重要的、交互过程复杂的用例**找出来。不要试图把所有的需求都以用例的方式表示出来。需求有两种基本形式：功能性需求和非功能性需求。用例描述的只是功能性方面的需求，那些难以用 UML 表示的需求很多是非功能性需求。

#### 泛化关系
官方解释：泛化代表一般的与特殊的关系，在用例之间的泛化关系中，子用例继承了父用例的行为和含义，子用例也可以增加新的行为和含义或覆盖父用例中的行为和含义。

PJ 的解释：子类和父类的关系。

![用例图——泛化关系](https://i.loli.net/2019/01/01/5c2b5f04f3e3a.png)

#### 包含关系
官方解释：包含关系指的是两个用例之间的关系，其中一个用例（基本用例）的行为包含了另一个用例（包含用例）的行为。

PJ 的解释：把某一个功能进行重用。

【例 1】银行的 ATM 系统中，有“存款”、“取款”、“账户余额查询”和“转账”四个用例，都要求用户必须登录了 ATM 机。也就是说，它们都包含了用户登录系统的行为。因此，用户登录系统的行为是这些用例中相同的动作，可以将它提取出来，单独的作为一个包含用例。

“存款”、“取款”、“查询用户余额”和“转账”是基本用例，“登录”是包含用例，如下图所示：

![银行 ATM 系统中用例之间的包含关系](https://i.loli.net/2019/01/01/5c2b61c637949.png)

由于将共同的用户登录系统行为提取出来，“存款”、“取款”、“查询用户余额”和“转账”四个基本用例都不再含有用户登录系统的行为。

【例 2】网上购物系统，当注册会员在线购物时，网上购物系统需要对顾客的信用卡进行检查，检查输入的信用卡号是否有效，信用卡是否有足够的资金进行支付。

![网上购物系统中用例之间的包含关系](https://i.loli.net/2019/01/01/5c2b65c9f225d.png)

上图中有没有必要将检查信用的行为提取出来，单独构成一个用例（作为包含用例），当信用检查的行为只发生在“在线购物”活动中时，可以不用提取出来。当信用检查的行为还发生在其它活动中时，应该提取出来，以便实现软件重用。

#### 拓展关系
官方解释：在拓展关系中，对于拓展用例的执行有更多的规则限制，基本用例必须声明若干个“拓展点”，而拓展用例只能在这些拓展点上增加新的行为和含义。

PJ 的解释：基本用例在满足一定条件后可进行选择执行拓展用例。

【例 3】图书借阅系统。当读者还书时，如果借书时间超期，则需要缴纳一定的滞纳金，作为罚款。

![图书借阅系统中还书时用例之间的拓展关系](https://i.loli.net/2019/01/01/5c2b69e8c68e5.png)

#### 综合
【例 4】 网上购物系统，当注册会员浏览网站时，他可能临时决定购买商品，当他决定购买商品后，就必须将商品放进购物车，然后下订单。

![客户网站购物的用例图（一）](https://i.loli.net/2019/01/01/5c2b6c1e44ed8.png)

如果网上购物系统的需求改为了：注册会员即可以直接在线购物，又可以浏览商品后临时决定在线购物，则可以改为下图所示：

![客户网站购物的用例图（二）](https://i.loli.net/2019/01/01/5c2b6d2106196.png)

### 用例描述
> 没有描述的用例就像是一本书的目录，人们只知道该目录的标题，但并不知道该目录的具体内容是什么，仅用图形符号表示的用例本身并不能提供该用例所具备的全部信息，必须通过文本的方式描述该用例的完整功能。实际上，用例的描述才是用例的主要部分，是后续的交互图分析和类图分析必不可少的部分。

用例描述了参与者和软件系统进行交互时，系统所执行的一系列动作序列，因此这些动作序列应该包含正常使用的各种动作序列（主事件流），而且还包含对非正常使用时软件系统的动作序列（子事件流）。

【例 1】 在银行 ATM 系统的 ATM 机上“取款”用例一个简单用例描述可以采取如下格式

描述项 | 说明
--- | ---
用例名称 | 取款。
用例描述 | 在储户账户有足够金额的情况下，为储户提供现金，并从储户账户中减去所取金额。
参与者 | 储户。
前置条件 | 储户正确登录系统。
后置条件 | 储户账户余额被调整。
主事件流 | （1）储户在主界面选择“取款”选项，**开始用例**（这个词的出现很重要）。（2）ATM 机提示储户输入欲取金额。（3）储户输入欲取金额。（4）ATM 确认该储户账户是否有足够的金额。如果金额不够，则执行子事件流 `b` 。**如果与主机连接有问题，则执行异常事件流 `e`**。（5）ATM 机从储户帐号中减去所取金额。（6）ATM 机向储户提供要取的现金。（7）ATM 机打印取款凭证。（8）进入主界面。ATM 机提供以下选项：存款、取款、查询和转账。**用例结束**（这个词的出现同样很重要）。
子事件流 `b` | b1. 提示储户余额不够。b2. 返回主界面，等待储户重新选择选项。
异常事件流 `e` | e1. 提示储户主机连接不上。e2. 系统自动关闭，退出储户银行卡，用例结束。

一个复杂用例主要体现在基本操作流程和可选操作流程的步骤和分之过多，此时，可以采用“场景（或称脚本）”的技术来描述用例，而不是用大量的分之和附属流来描述用例。

### 用例建模
用例模型主要应用在需求分析时使用。

#### 步骤
* 找出**系统外部**的参与者和外部系统，确定系统的边界和范围；
* 确定每一个参与者所期望的系统行为，参与者对系统的基本业务需求；
* 把这些**系统行为作为基本用例**；
* 区分用例的优先级；
* 细化用例。使用泛化、包含、拓展等关系进行处理；
* 编写每个用例的用例描述；
* 绘制用例图；
* 编写项目词汇表。

#### 确定系统边界
系统边界是指系统与系统之间的界限。系统可以认为是一系列的相互作用的元素形成的具有特定功能的有机整体。不属于这个有机整体的部分可以认为是**外部系统**。因此系统边界定义了**油谁或什么参与者来使用系统**，系统能够为参与者提供什么特定服务。**系统边界决定了参与者**。

【例 1】在一个仅为交易客户提供买卖基金的基金交易系统中，**参与者**为交易客户，交易客户能够操作的系统功能有买入基金和卖出基金。因此，系统有两个用例：买入基金和卖出基金。

进一步分析发现，基金的品种应该存在与该系统中，否则交易客户无法进行基金的买卖。但系统已存的两个用例都不能完成基金品种的管理，所以可以确认基金品种的管理应该在别的系统中完成。

所以，我们需要开发这个系统，仅存在两个用例：买入基金、卖出基金。

![仅完成基金买卖的“基金交易系统”的系统边界](https://i.loli.net/2019/01/04/5c2f81bb9cd84.png)

【例 2】对例 1 做个调整。在一个既提供基金买卖又提供基金品种录入的基金交易系统中，交易客户，能够进行基金的买入和卖出。因为还需要对基金品种进行管理（录入、修改、删除和查询），由基金公司员工进行操作。所以该系统的参与者有交易客户和基金公司员工。系统边界可以改为下图所示：

![拓展了基金品种管理的“基金交易系统”的系统边界](https://i.loli.net/2019/01/05/5c309b74d8f8d.png)

#### 如何确定参与者
* 谁将使用系统的主要功能？
* 谁将需要系统的支持来完成她们的日常工作？
* 谁将必须维护、管理和确保系统正常工作？
* 谁将给系统提供信息、使用信息和维护信息？
* 系统需要处理哪些硬件设备？
* 系统使用外部资源吗？
* 系统需要与其他系统交互吗？ 
* 谁对系统产生的结果感兴趣？

需要注意的问题：
* 只要是参与者，对于子系统而言都是外部的；
* 参与者直接与系统进行交互；
* 参与者指的与系统直接交互时所扮演的角色，而不是特定的人或事物。比如，不是 PJ 与教务系统产生交互而是学生与教务系统产生交互；


#### 如何确定用例
识别用例可以从列出的参与者列表中从头开始寻找，考虑每个参与者如何使用系统，需要系统提供什么样的服务。

* 参与者要向系统请求什么功能？
* 每个参与者的特定任务是什么？
* 参与者需要读取、创建、撤销、修改和存储系统的某些信息吗？
* 参与者是否有需要通知系统的事件？系统是否有需要通知参与者的事件？
* 这些事件代表了哪些功能？
* 系统需要哪些输入输出功能？
* 是否所有的功能需求都被用例使用了？

需要注意以下问题：
* 每个用例至少有一个参与者；
* 每个参与者至少一个用例；
* 如果存在没有参与者的用例，再三检查后，还是没有参与者，可以考虑把该用例并入其他用例中；
* 如果存在没有用例的参与者，再三检查后，该参与者还是没有用例，可以考虑该参与者是如何与系统产生交互的，或由该参与者确定一个新的用例，或实际上该参与者本身就是多余的。

#### 项目词汇表
这什么鬼，没见过，没听说过......

### 其他问题
#### 需求应该有层次的组织
系统的高层需求一版用不超过 12 个左右的用例进行表示，在其下的层次中，用例的数量不应超过当前用例的 5～10 倍。可以将用例划分为**业务用例**、**系统用例**和**组件用例**等。

#### 不要从用例直接推导设计
用例应该描述参与者使用系统所遵循的顺序，但用例绝不说明系统内部采用什么步骤来响应参与者的刺激。

### 用例包

#### 用例模型的调整
如果两个用例总是以同样的顺序被激活，可能需要将它们合并为一个用例。

#### 不要过于详细
在进行用例描述时还没有考虑系统的设计方案，那么也不会涉及用户界面。
