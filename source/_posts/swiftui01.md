---
title: SwiftUI 怎么实现一个「更多菜单」？
date: 2019-08-06 10:36:02
tags:
- SwiftUI
- Swift
- iOS
- Masq
---

![在 WWDC 现场与 SwiftUI](https://i.loli.net/2019/08/06/6qJADoNfY8Wlt3E.png)

## 前言
最近新起了一个 side project，用于承载 WWDC19 里公布的内容，会用上以下技术栈：

1. `SwiftUI` 做所有的表现层。
2. `Alamofire` + `SwiftyJSON` 做所有的网络层交互，原本想再上一个 `Moya`，想了想，这个产品网络层比较简单，没必要为了上而上。
3. SPM 管理所有三方依赖，就目前使用情况来看，比 pod 体验持平，会继续使用。
4. 还是使用 MVC，但是此次的 MVC 只是简单的「模块划分」而已，workflow 和 dataflow 都尽可能的跟着 `SwiftUI` 官方推荐做法来。
5. 使用 `Core Data` + `FileManager` 管理所有数据缓存。
6. 使用 `SF Symbols` 做所有的 icon。
7. 因为另外一个侧重点在 dark mode，所以使用 Group 设置 light mode 和 dark mode 两种模式，直接预览。

在完成了一些前期的工作后，最近在空闲时间发力实现项目中的「更多菜单」。「更多菜单」在 github 上搜索关键词 `contextMenu`/`menu`，再限制语言，会出来一堆基于 `UIKit` 的实现，如果我们想要基于 `SwiftUI` 实现一个符合 `SwiftUI` 风格的「更多菜单」要怎么实现呢？

## `UIKit` 会怎么做？
在使用 `SwiftUI` 实现「更多菜单」之前，先看看使用 `UIKit` 怎么实现。因为 `UIKit` 我们都相对熟悉，大多数 API 也都知道，就不放实现细节了。

1. 有两种实现方式。如果是全屏「更多菜单」，可能会基于 `CATransition` 做一个「更多菜单」`ViewController` 动画过渡出现，或者是基于 `UIWindow` 切换 `keyWindow` 动画过渡出现，这是在**做一个容器**。

2. 容器有了，内部我们可以基于 `UITableView` 或者 `For` 循环遍历创建模拟出一个「列表」视图出来，然后可以用闭包的方式接收 `ViewModel` 的数据源配置传递，再通过闭包的方式把「更多菜单」中的点击事件传递出去。

3. 创建出容器内部的「更多菜单」后，调整调整布局约束，获取屏幕宽高之类的位置操作，最后再封装一个好用的 API，暴露给业务调用方，丢给 QA 等着反馈继续调整就可以了。封装好的调用方式可能会如下所示（这是我自定义的一个选择器组件

    ```swift
    PJPickerView.showPickerView(viewModel: {
        $0.dataArray = [["PJHubs", "PJ", "皮筋"], ["培钧", "阿钧"]]
        $0.titleString = "选择你的昵称"
    }) {
        print("选择的昵称是：\($0)")
        print("选择的索引为：\($1.section)\($1.row)")
    }
    ```

但是这种 `UIKit` 的思路直接套在 `SwiftUI` 上能「跑」得起来了吗？

## `SwiftUI` 应该怎么做？
在说 `SwiftUI` 应该怎么去实现一个「更多菜单」时，先假设我们都已经熟悉了 `SwiftUI` 的基本语法，都跟着 Apple 官方的 [SwiftUI Tutorials](https://developer.apple.com/tutorials/swiftui/creating-and-combining-views) 摸索过一遍了。

如果你跟我一样也是一个从 `UIKit` 过来的选手，那么我们还会去这么思考：

1. 创建一个容器。
2. 创建容器里的「列表」视图。
3. 通过一个状态变量去控制「更多菜单」的显示和隐藏。
4. 暴露出一个闭包告诉「更多菜单」依赖的父视图点击了哪个选项。

这看上去思路都是正确的。在我的一番实践下来，确实是这个思路没错，可见 Apple 并没有抛弃在 `UIKit` 里养成的思维习惯，但是，正准备上手做时，发现了一些奇怪的地方......

### 如何创建一个容器？
从 `UIKit` 切换到 `SwiftUI` 后，我们会发现 `View` 不再是 `UIView`，你甚至都无法创建一个 `Array<View>` 这么个视图集合，但是在 `SwiftUI` 中却一切都是 `View`（除了那几个基本的主视图，如 `Text`， `Image`，`Color` 等。

我们兴致勃勃的用 `VStack` 和 `HStack`，可能会再加上一个 `ForEach` 根据传入的数据源，创建出了一个如下「更多菜单」的列表：

![快速的写完了「更多菜单」的原型](https://i.loli.net/2019/08/06/rdmeJKvlc5NSa84.png)

当我们想要把这个「更多菜单」的原型放在首页列表的导航栏上时，出现了一个问题，当我们把菜单原型直接加到写好的列表上时，它被全屏覆盖了！

![出现了一个问题](https://i.loli.net/2019/08/06/vVAxhG4QOy815rz.gif)

思考了一下，`SwiftUI` 中的 `View` 不是 `UIView`，这点非常重要，而且要牢记在心！当我们通过一个状态变量去控制菜单的显示和隐藏时，我们加进去的是一个 `View`，当它隐藏时，`SwiftUI` 只会渲染原先的列表；当它出现时，触发了 `SwiftUI` 的 `diff` 算法，重新渲染应该渲染的部分。

那就算重新渲染，为什么会把原先的已经渲染出来的列表「弄没了」呢？我翻了一圈没有找到解答的资料，以下内容为猜测：

首先我们需要明确 `SwiftUI` 是「声明式」布局，当需要返回一个整体的 `View` 给 `body` 时，我们却返回了「一堆」`View`，也就是菜单和列表。此时菜单 `View` 和列表 `View` 并不是一个集合体，也就是我们返回了两个 View，但如果我们把这个代码铺开来看，在 `Swift 5.1` 中当只有一个需要返回的值时，`return` 可以省略。

但外部我们却只返回了一个 `NavigationView`，满足了省略 `return` 的要求，但 `NavigationView` 内部的 `content` 内容集合因为**缺失布局**导致列表虽执行了 DSL，但转换成绘制信息时，丢失了绘制列表的数据。这也就说明了，为什么我们在给 `SwiftUI` 断点的时候停下了，但却在 Xcode 的 `Debug View Hierarchy` 中未看到对应的视图层级。

知道问题出在哪了以后，加上一个 `VStack`，算是解决了这一个问题。

![修复了一个问题](https://i.loli.net/2019/08/06/gHSemD2EYN1ip63.gif)

但实际上我们会发现菜单和列表混在一个同一个层级上，回想使用 `UIKit` 实现菜单时，正如上文说的，我们会使用 `UIViewController` 或者 `UIWindow` 把菜单和父视图在**纵坐标**上进行隔离，在 `SwiftUI` 中也是一样的，所以我们需要用上 `ZStack`。

![使用了 ZStack 还是不行？](https://i.loli.net/2019/08/06/xZ8kiqLSHCuRE9l.gif)

可以发现使用了 `ZStack` 后还是不行，再换回用 `UIKit` 的思路去想，我们在使用 `UIKit` 去完成菜单时，是不是会去做切换视图层级的操作？那在 `SwiftUI` 中怎么切换视图层级呢？

很遗憾，在 `SwiftUI` 中不能切换视图层级，只能通过一个状态变量值去控制某个视图的显示和隐藏，但是 `SwiftUI` 只是一个 DSL，最终还是会被翻译成渲染节点树的么，那么可以推测出菜单绝对是被列表给遮挡了。

![只是被遮盖了](https://i.loli.net/2019/08/06/zhEXmFgZRAdtuCw.png)

因此只需要把菜单添加在列表下面即可。

![修复完成](https://i.loli.net/2019/08/06/Kvbl64s1h5cZ9in.gif)


### 调整列表约束
我们需要把列表调整到左上角，并加上箭头。到这一步，我们已经把原型给实现出来了，需要对库进行一个封装，包装成一个 `MenuView` 供外部调用。

如果我们直接给 `VStack` 设置 `frame` 是没有效果的，因为 `VStack` 没有「几何边界」，那么我们应该使用 `GeometryReader` 来包一层菜单视图，并设置 `GeometryReader` 的 `frame` 即可。

也就是说，菜单现在的容器由 `VStack` 变为了 `GeometryReader`，此时我们再去看 `Debug View Hierarchy`，会发现菜单和列表都出现在了同一个视图上，我们只需要把菜单的容器变为透明，然后给 `GeometryReader` 添加点击事件来控制菜单的显示和隐藏即可。

但这里需要注意的是，在 `SwiftUI` 中，如果你给一个 `View` 的背景色为 `clear`，那这个 `View` 就不会被渲染出来了，因此要控制透明度为 `0.01`。

其实到现在如果把工程 `build` 起来一看，从 UI 上看效果差不多，如果是纯文本菜单的话，基本上这一环节的内容就结束了，但因为我还还想用上 `SF Symbols`，所以做了一个「左图右字」的菜单。

让我感到惊讶的是，`SF Symbols` 居然不是规整的正方形图标，直接不做任何处理丢到菜单上会发现每一行的图和字都有了一些偏移。如果你直接调用 `.resizable()`、`.frame` 和 `.scaledToFill()` 等方法，会发现图标又变形了。

还是那句话“计算机科学领域的任何问题都可以通过增加一个间接的中间层来解决”，`Image` 和 `Text` 套在一个 `HStack` 里会出现上述问题，那就给 `Image` 再套一个 `HStack` 就好了，对 `Image` 进行约束限制。

这是我已经封装好的菜单 cell 组件（可以 `ForEach` 直接弄完：

```swift
struct MASSquareMenuCell<Content: View>: View {
    var itemName: String
    var itemImageName: String
    var content: () -> Content
    
    var body: some View {
        NavigationLink(destination: content()) {
            HStack {
                // 限定 `Image`
                HStack {
                    Image(systemName: itemImageName)
                        .imageScale(.medium)
                        .foregroundColor(.white)
                        .padding(EdgeInsets(top: 0, leading: 10, bottom: 0, trailing: 20))
                }
                    .frame(width: 50)

                Text(itemName)

                Spacer()
            }
                .foregroundColor(.white)
                .padding(EdgeInsets(top: 5, leading: 5, bottom: 5, trailing: 5))
                .frame(width: 130)
        }
    }
}
```

### 数据源设置
布局约束设置好了，就剩下塞数据了。因为 `SwiftUI` 所用的开发流程和我之前的开发流程差别挺大的，尤其是数据流这一块，看了 github 上几个项目后才明白大概是怎么回事。

跟 mentor 讨论了一下关于类似这种菜单组件是做成一个 UI 组件还是业务组件，最后得出的结论是还得看业务具体的需求，如果做的就是一个存粹的 UI 组件，那每一个菜单项的点击都要暴露给管理其生命周期的拥有者，如果这个组件做的事情比较封闭，留给业务调用方自定义的操作并不多，而且也确实是做到了一行代码或者比较简单的配置就可以接入，那做成纯业务组件也未尝不可。

首先说明，我之前在其它的 side project 中也有实现过类似的「更多菜单」，但是当时因为 `UIKit` 和实习公司代码风格的影响，我养成了一个不管是什么组件，总之外部表现出是 UI 组件，那就一股脑的全都是 UI 组件。但 `SwiftUI` 所推崇的开发模式引发了我对上的思考。

![与 mentor 讨论的草稿](https://i.loli.net/2019/08/06/XEHLi42sY3woUVc.png)

最终经过我的一番整理后，同时也遵循「过早的优化是魔鬼」的原则，杂糅了业务和 UI 两种组件模式，确定了菜单上的每一个选项点击都是要通过 `NavigationLink` 进行跳转，然后我需要暴露一个闭包让调用方填入菜单中的每个选项的视图。

刚开始我的想法非常简单，还是按照 `UIkit` 的那一套思想，新建一个菜单数据源中间件，调用方可以动态的增删菜单中的选项，这种模式没有错，但问题 `SwiftUI` 不支持这么做。

菜单选项中的 `itemName` 和 `itemImageName` 左图右字的配置选项很容易思考出结果，但 `itemView` 难道是继承 `View` 吗？很明显不行，因为 `View` 是一个协议，那如果我继承 `View` 实现一个类或者结构体呢？别忘了，实现 `View` 协议你需要把 `body` 属性也声明好了，但动态增删选项的目的就是要动态不同的 `View` 内容呀～

换回去 `UIkit` 的想法，如果我们想要实现一个菜单数据源模型，可能会这么写：

```swift
struct MenuModel {
    var itemName: String
    var itemImageName: String
    var itemView: UIView
}
```

我们已经显式的指明 `itemView` 的类型为 `UIView` 了，在 `SwiftUI` 中，要达到这个效果其实也是一样，既然我们不能规避不声明 `View` 的 `body` 属性，那就去实现它好了，完整的菜单代码如下所示：

```swift
//
//  MASSquareMenuView.swift
//  masq
//
//  Created by 翁培钧 on 2019/8/2.
//  Copyright © 2019 PJHubs. All rights reserved.
//

import SwiftUI

struct MASSquareMenuCell<Content: View>: View {
    var itemName: String
    var itemImageName: String
    var content: () -> Content
    
    var body: some View {
        NavigationLink(destination: content()) {
            HStack {
                // 限定 `Image`
                HStack {
                    Image(systemName: itemImageName)
                        .imageScale(.medium)
                        .foregroundColor(.white)
                        .padding(EdgeInsets(top: 0, leading: 10, bottom: 0, trailing: 20))
                }
                    .frame(width: 50)

                Text(itemName)

                Spacer()
            }
                .foregroundColor(.white)
                .padding(EdgeInsets(top: 5, leading: 5, bottom: 5, trailing: 5))
                .frame(width: 130)
        }
    }
}

struct MASSquareMenuView<Content: View>: View {
    
    @Binding var isShowMenu: Bool
    var content: () -> Content
    
    
    var body: some View {
        GeometryReader { _ in
            // 顶部箭头
            Image(systemName: "triangle.fill")
                .padding(EdgeInsets(top: 5, leading: 25, bottom: 0, trailing: 0))
            
            VStack(alignment: .leading) {
                self.content()
            }
                .background(Color.black)
                .cornerRadius(5)
                .padding(EdgeInsets(top: 10, leading: 10, bottom: 0, trailing: 0))
            
            Spacer()
        }
            .background(Color.white.opacity(0.01))
            .frame(minWidth: UIScreen.main.bounds.width, minHeight: UIScreen.main.bounds.height)
            .onTapGesture {
                self.isShowMenu.toggle()
            }
    }
}
```

大家可以参考 `VStack` 的声明实现，看看它是怎么实现接收多 `View` 参数的～实际上从代码中可以看出使用了 `@ViewBuilder`，而 `@ViewBuilder` 是 `@_functionBuilder` 关键字修饰的结构体，这部分细节可以看喵神的[这篇文章](https://onevcat.com/2019/06/swift-ui-firstlook/)。

而我们只需要按照下图的方式进行调用，就可以优雅的完成菜单数据源填入了。

![优雅的「更多菜单」API](https://i.loli.net/2019/08/06/yc1326XVlZIQow4.png)

## 后记
还是那句话，这是我用于承载 WWDC19 新推出的各种 framework 的 side project，对很多东西的认识也在不断的发展中，从 beta1 到 beta5 我几乎看了 github 上**公开**的与 `SwiftUI` 有关的 60% 的 repo，大家都在改 Apple 的官方 demo，而且有一些类似与「更多菜单」的实际问题并没有人去解决，大部分都在做各种「TODO-list」的变种。

这个项目还没写完，甚至才刚开始，在一些点子的实现上因为 `SwiftUI` 太新了，我想了解或者类似的需求都没有可以借鉴的地方，只能说顶住了很多自己给自己的压力。

## 参考资料
[SwiftUI 的一些初步探索 (一)](https://onevcat.com/2019/06/swift-ui-firstlook/)
[SwiftUI 的一些初步探索 (二)](https://onevcat.com/2019/06/swift-ui-firstlook-2/)
[Custom view won't use state variable update provided through binding, but debug watch shows changes](https://stackoverflow.com/questions/57022388/custom-view-wont-use-state-variable-update-provided-through-binding-but-debug)
[hite/YanxuanHD](https://github.com/hite/YanxuanHD)
[Fucking SwiftUI](https://fuckingswiftui.com)
[SwiftUI 数据流](https://xiaozhuanlan.com/topic/0528764139)
[How do I create a multiline TextField in SwiftUI?](https://stackoverflow.com/questions/56471973/how-do-i-create-a-multiline-textfield-in-swiftui/56549250#56549250)
[SwiftUI 背后那些事儿](https://mp.weixin.qq.com/s/ciiauLB__o-cXXfKn7lL1Q)
[SWIFTUI BY EXAMPLE](https://www.hackingwithswift.com/quick-start/swiftui)

项目地址：[Masq iOS 客户端](https://github.com/windstormeye/Masq-iOS)