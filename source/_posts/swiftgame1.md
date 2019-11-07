---
title: Swift 游戏开发之「能否关个灯」（〇）
date: 2019-09-02 23:13:06
tags:
- iOS
- Swift
- SwiftUI
- 游戏开发
---

![]( https://images.xiaozhuanlan.com/photo/2019/22c830968d31df2249696119aa63d2db.png)

## 前言
第一个游戏我们将基于 `SwiftUI` 来完成。主要想验证的问题有两点：

* `SwiftUI/UIKit` 这种我们日常接触到的 UI 框架是否能够做游戏？
* 如何建立起游戏开发的思维？

《能否关个灯》是我在大一时去「中国科学技术馆」做志愿者时发现的一个小游戏。结合当时「绿色环保」的理念，这个小游戏火得不行，排了好久的队才到我，半个多小时后，我几乎每次都是差一个「灯」就通关了，但每次都不行。

![馆内的关灯游戏（图片来源网络）](https://i.loli.net/2019/08/28/uirfLIYsGXho29J.jpg)

为了避嫌，我把这个游戏改为了《能否关个灯》。这个小游戏的规则非常简单，开始游戏后，会「随机」点亮一些灯，接着我们就可以开始玩了，想办法去关掉这些灯，需要注意的是**每一盏灯的开关会连带其附近的灯进行开关**，如下图所示：

![逻辑示意图](https://i.loli.net/2019/08/28/VSyxD6wMk5P2YGs.png)

## 逻辑梳理
从上述内容我们可以把逻辑先写出来：
* 每一盏灯的开关会影响其 **「上下左右」** 灯的状态（取反）；
* 灯只有「开」和「关」两种状态；
* 胜利的条件是：关掉所有灯；

逻辑梳理完了，看上去不足以称为一个「游戏」，我们来把这个逻辑给补充完整，让它看起来像个游戏：

* 加入计时器。记录每把游戏经历过的时间；
* 加入关卡难度配置。可以调整为 4x4、5x5 或其它难度；
* 加入灯的随机过程。让每次游戏开局时灯的状态可控；
* 加入历史记录功能。

在这里解释一下什么是「灯的随机过程」。游戏的开局已经给定了一些灯的状态，而且作为一个游戏，它一定是可以把灯全部灭掉的，但如果我们不是按照开始「亮灯」的顺序去逆序的「灭灯」，是一定没法把所有灯都灭掉的。

因此，这个游戏的核心逻辑我们也就理解了，是围绕 **「亮灯」的顺序去逆序出「灭灯」的顺序**，比较考验玩家的想象能力。在这个游戏中，我们需要做的事情有：

- [ ] 灯状态的互斥
- [ ] 灯的随机过程
- [ ] 游戏关卡难度配置
- [ ] 计时器
- [ ] 历史记录
- [ ] UI 美化

## 游戏框架搭建
打开 Xcode11（ >= beta 7），新建一个 iOS 工程，并勾选 SwiftUI。SwiftUI 的语法细节在此不做展开，你可以参考我的这两篇文章 [SwiftUI 如何实现更多菜单？](http://pjhubs.com/2019/08/06/swiftui01/)与[SwiftUI 怎么和 CoreData 结合？](http://pjhubs.com/2019/08/12/swiftui02/)来查看更多关于 SwiftUI 的基础内容。

### 构建灯的模型
对于一个「灯」来说，抽象其模型目前我们只需要一个状态值 `status` 即可，用于记录该灯的开关状态，且默认值为 `false`，也就是「熄灭」状态。

```swift
struct Light {
    /// 开关状态
    var status = false
}
```

### 游戏布局
我们先默认设置游戏尺寸为 3x3 大小的九宫格，我们可以先快速的搭建出布局框架：

```swift
import SwiftUI

struct ContentView: View {
    
    var lights = [
        [Light(), Light(), Light()],
        [Light(), Light(), Light()],
        [Light(), Light(), Light()],
    ]
    
    var body: some View {
        ForEach(0..<lights.count) { rowindex in
            HStack {
                ForEach(0..<self.lights[rowindex].count) { columnIndex in
                    Circle()
                        .foregroundColor(.gray)
                }
            }
        }
    }
}
```

此时运行工程是下图这个样子的。

![第一个布局](https://i.loli.net/2019/08/29/zvFyG8PgVa3B1UA.png)

虽然，我们什么间距都没有设置，各个圆形之间间距是 Apple 根据其人机交互指南自动设置一个默认值，并且 `SwiftUI` 如果我们什么布局都不写的前提下是**居中布局**的。我们可以利用 `SwiftUI` 的优秀布局能力把游戏主布局变为这样：

```swift
import SwiftUI

struct ContentView: View {
    
    var lights = [
        [Light(), Light(status: true), Light()],
        [Light(), Light(), Light()],
        [Light(), Light(), Light()],
    ]
    
    /// 圆形图案之间的间距
    private let innerSpacing = 30
    
    var body: some View {
        ForEach(0..<lights.count) { rowindex in
            HStack(spacing: 20) {
                ForEach(0..<self.lights[rowindex].count) { columnIndex in
                    Circle()
                        .foregroundColor(self.lights[rowindex][columnIndex].status ? .yellow : .gray)
                        .opacity(self.lights[rowindex][columnIndex].status ? 0.8 : 0.5)
                        .frame(width: UIScreen.main.bounds.width / 5,
                               height: UIScreen.main.bounds.width / 5)
                        .shadow(color: .yellow, radius: self.lights[rowindex][columnIndex].status ? 10 : 0)
                }
            }
                .padding(EdgeInsets(top: 0, leading: 0, bottom: 20, trailing: 0))
        }
    }
}
```

利用了 `Light` 模型中的 `status` 状态值去控制了每个「灯」（圆形）的颜色和透明度，以显得我们真的把「灯」给点亮了，调整了一下「灯」和「灯」之间的间距，让它们显得不那么拥挤，同时为了表现出真的「点亮」了灯，使用阴影来表示出灯的「光晕」，并把数据源 `lights` 中的一个模型的 `status` 值设置为了 `true`。此时运行工程，你会发现我们游戏的主布局完成了：

![第二个布局](https://i.loli.net/2019/08/29/AWE4GLDVvltSz21.png)

### 修改灯的状态
完成了布局后，我们需要去修改「灯」的状态。之前，我们已经通过 `lights` 这个变量去作为管控布局中「灯」的模型，我们需要对这些模型进行处理即可。还要给「灯」加上「点亮」操作，相当于需要给每个「灯」添加上触摸手势，并在触摸手势的回调处理事件中，维护与之相关的状态变化。

```swift
import SwiftUI

struct ContentView: View {
    
    var lights = [
        [Light(), Light(status: true), Light()],
        [Light(), Light(), Light()],
        [Light(), Light(), Light()],
    ]
    
    /// 圆形图案之间的间距
    private let innerSpacing = 30
    
    var body: some View {
        ForEach(0..<lights.count) { row in
            HStack(spacing: 20) {
                ForEach(0..<self.lights[row].count) { column in
                    Circle()
                        .foregroundColor(self.lights[row][column].status ? .yellow : .gray)
                        .opacity(self.lights[row][column].status ? 0.8 : 0.5)
                        .frame(width: UIScreen.main.bounds.width / 5,
                               height: UIScreen.main.bounds.width / 5)
                        .shadow(color: .yellow, radius: self.lights[row][column].status ? 10 : 0)
                        .onTapGesture {
                            self.updateLightStatus(column: column, row: row)
                    }
                }
            }
                .padding(EdgeInsets(top: 0, leading: 0, bottom: 20, trailing: 0))
        }
    }
    
    /// 修改灯状态
    func updateLightStatus(column: Int, row: Int) {
        // 对「灯」状态进行取反
        lights[row][column].status.toggle()
    }
}
```

开开心心的写出上述的状态修改代码，但 Xcode 报了 `Cannot assign to property: 'self' is immutable` 的错误，这是因为 `SwiftUI` 在执行 DSL 解析还原成视图节点树时，不允许有「未知状态」或者「动态状态」，`SwiftUI` 需要明确的知道此时需要渲染的视图到底是什么。我们现在直接对这个数据源进行了修改，想要通过这个数据源的变化去触发 `SwiftUI` 的状态刷新，需要借用 `@Stata` 状态去修饰 `lights` 变量，在 SwiftUI 内部 `lights` 会被自动转换为相对应的 setter 和 getter 方法，对 `lights` 进行修改时会触发 `View` 的刷新，`body` 会被再次调用，渲染引擎会找出布局上与 `lights` 相关的改变部分，并执行刷新。修改我们的代码：

```swift
struct ContentView: View {
    
    // 加上 `@State`
    @State var lights = [
        [Light(), Light(status: true), Light()],
        [Light(), Light(), Light()],
        [Light(), Light(), Light()],
    ]

    // ...
}
```

此时运行工程，会发现我们已经可以完美的把「灯」给点亮啦～

![给「灯」加上状态修改](https://i.loli.net/2019/08/29/uRP1j4dXfYHFico.gif)

### 灯状态的互斥
完成了「灯」的交互后，我们需要对其进行「状态互斥」的工作。回顾前文所描述的游戏逻辑，再看这张图，

![逻辑示意图](https://i.loli.net/2019/08/28/VSyxD6wMk5P2YGs.png)

我们需要完成的逻辑是，当中间的「灯」被「点击」后，与之相关「上下左右」的四个「灯」和它自己的状态需要取反。修改之前更新灯状态的方法 `updateLightStatus` 为：

```swift
// ...

/// 修改灯状态
func updateLightStatus(column: Int, row: Int) {
    lights[row][column].status.toggle()
    
    // 上
    let top = row - 1
    if !(top < 0) {
        lights[top][column].status.toggle()
    }
    // 下
    let bottom = row + 1
    if !(bottom > lights.count - 1) {
        lights[bottom][column].status.toggle()
    }
    // 左
    let left = column - 1
    if !(left < 0) {
        lights[row][left].status.toggle()
    }
    // 右
    let right = column + 1
    if !(right > lights.count - 1) {
        lights[row][right].status.toggle()
    }
}

// ...
```

运行工程，我们可以和这个游戏开始愉快的玩耍了～

![灯状态的互斥](https://i.loli.net/2019/08/29/NVOJsquKvpidC98.gif)

### 灯的随机过程
现在游戏的雏形已经具备，但目前非常死板，每次开局都是第一行中间的灯被点亮，我们需要加上游戏开始时的随机开局。从我们目前掌握的源码带来看，需要对数据源 `lights` 下手。游戏初始化时的状态数据来源于 `lights` 中所记录的模型状态，我们需要对这里边的模型状态值在初始化时进行随机过程。所以可以对 `Light` 模型进行如下修改：

```swift
struct Light {
    /// 开关状态
    var status = Bool.random()
}
```

通过 `Bool.random()` 让模型初始化时都生成不一样的 `Bool` 值，这样每次运行工程时，生成的布局都不一样，达到了我们的目的！

![灯的随机过程](https://i.loli.net/2019/08/29/PUQoC3epYujR7fb.png)

## 后记
至此，我们已经完成的需求有：

- [x] 灯状态的互斥
- [x] 灯的随机过程
- [ ] 游戏关卡难度配置
- [ ] 计时器
- [ ] 历史记录
- [ ] UI 美化

万事开头难，实际上我们已经把这个游戏的核心部分给完成了，在下一篇文章中，我们将继续完成剩下的 case，赶快试试看你能不能把所有的灯都熄灭吧～


GitHub 地址：[https://github.com/windstormeye/SwiftGame]( https://github.com/windstormeye/SwiftGame)

来源：我的小专栏《 Swift 游戏开发》：[https://xiaozhuanlan.com/pjhubs-swift-game]( https://xiaozhuanlan.com/pjhubs-swift-game)