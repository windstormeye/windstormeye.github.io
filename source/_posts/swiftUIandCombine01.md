---
title: 从实际问题看 SwiftUI 和 Combine 编程
date: 2019-11-09 13:31:39
tags:
- SwiftUI
- Combine
- 响应式
---

## 0x00 | 前言
假设大家已对 Swift 语法有基本了解，并且已经上手体验过。虽在工作中可能并不会立即介入 SwiftUI 和 Combine，但通过对这两个框架的学习和使用可以从侧面给我们提供一个优化的思路，从以往「流程化」和「命令式」的编程思维中转变出来，提升开发效率。

此次分享在于快速对 SwiftUI 和 Combine 框架有一个基本认识，通过一个常规业务 demo 来验证 SwiftUI 和 Combine 提升效率的可能性，分享我在学习 SwiftUI 和 Combine 遇到问题和值得开心的地方。

## 0x01 | SwiftUI
### 1. SwiftUI 是什么？
- ~~指令式编程~~ 响应式编程。
- 基于 `UIKit`、`Core Graphics`、`Core Text` 等系统框架封装了完整而优美的 DSL。
- Combine 响应式编程框架和函数式编程思想直接驱动了 SwiftUI 中的数据流向。

![](https://i.loli.net/2019/11/09/GPgBCqTURvI8uor.png)

- 提供了一套通用的语法和基础数据类型，抹平 Apple 自家平台差异性，降低同生态跨端难度。
- 抛弃 `ViewController` 概念。
- 在 API 层面上，有 RAC 链式调用的影子和 Combine 的强依赖实现。

### 2. Combine 是什么？
- SwiftUI 中处理数据的本体，响应式框架。
- 提供给 SwiftUI 中与数据源双向绑定的能力。
- 数据流式处理「链式」调用。与 SwiftUI 的「链式」组织 UI 不同，SwiftUI 是通过链式调用构造出一个确定的单一对象（语法糖），但 Combine 的每一次链式调用都会生成一个新的源数据。

## 0x02 | 实现一个 Context Menu

![Context Menu](https://i.loli.net/2019/11/09/GgvzAkcDW4LtMjm.png)

### 容器

### 菜单容器
「更多菜单」是一个几乎所有 App 里都会去实现的一个组件，其承担了非主业务，但又十分重要的二级工具类业务入口。如果通过常规的 `UIKit` 的思路去做，大致的实现思路是这样的：

1. 创建一个 `UIWindow` 或 `UIViewController`，作为菜单视图的容器；
2. 通过 `UITableView` 或循环组件的方式创建出具体的菜单视图；
3. 视图关系建立及菜单点击事件跳转逻辑回调完善。

如果只想用 SwiftUI 去实现的化，在 SwiftUI 万物皆 `View`，没有 `ViewController` 的概念，所以这里的容器就回落到了 `View` 身上。包装一个视图容器，可能会是这样的：·

```swift
struct MASSquareMenuView: View {
    
    var body: some View {
        GeometryReader { _ in
            // ......
        }
            .frame(minWidth: UIScreen.main.bounds.width, 
                   minHeight: UIScreen.main.bounds.height)
    }
}
```

`MASSquareMenuView` 充当了底层的 `ViewController` 角色。`View` 实际上是个结构体。如果 `body` 里返回不确定的类型，DSL 解析会失败，例如同时返回两个 `View`，通过 `if-else` 判断来返回不同的 `View`，这种情况会被拒绝执行。如果我们就是想通过一个标识位去判断当前要返回的到底是什么视图，需要使用 `@State` 关键词修饰的一个变量去操作。

#### 菜单 Cell 容器
```swift
struct MASSquareHostView: View {
    
    var body: some View {
        NavigationView {
            // ...
            
            ZStack {
                MASSquareMenuView {
                    // ......
                }
            }
            
            // ...
        }
    }
}
```

#### 链式调用
「链式调用的过程」被称为是 `SwiftUI` 中 `View` 的 `modifier`，每个 `modifier` 的调用结束后，返回给下一个 `modifier` 有两种情况：第一种情况只是对 `View`（如 `Text`）的 `font` 等与布局无关的方法，返回给下一个 `modifier` 相同类型的 `View`；第二种情况对 `View` 的布局产生了修改，如调用了 `padding` 等方法，返回给下一个链式调用的 `modifier` 是一个重新包装过的全新 `View`。

其实我觉得这跟之前用的链式调用库从概念上是一样的道理，有些链式方法的调用必须是依赖于某些方法的先执行，比如自定义 `Image` 这个标签的大小，必须先设置 `resizeable` 才能设置 `frame`，否则失效。

### 数据源
SwiftUI 的 API 设计哲学，强迫我去思考对外公开的组件所提供的定制化功能，之前跟 mentor 讨论过，类似这种 `ContextMenu` 是封装成一个 UI 组件还是一个业务组件，最后决定还是把这个菜单组件做成一个 UI 组件。

「更多菜单」的数据源经过调整，最终写出了一个基本符合 SwiftUI 风格的 API，基本符合是因为多了一个烦人的 `Group`，之前已经说过，SwiftUI 不接受多个视图返回，如果确实要返回多个视图的「组合视图」，需要手动对这些视图使用 `Group` 包装成一个 `View` 进行返回。

引发一个新的问题，怎么接收一组 `View`，通过对一个组件传递一串 `View` 来完全自定义菜单组件里的内容，使用 `UIKit` 的话我可能会这么做：

```swift
PJPickerView.showPickerView(viewModel: {
    $0.titleString = "感情状态"
    $0.pickerType = .custom
    $0.dataArray = [["单身", "约会中", "已婚"]]
}) { [weak self] finalString in
    if let `self` = self {
        self.loveTextField.text = finalString
    }
}
```

![](https://i.loli.net/2019/11/10/Ii59dkpazWt7BTV.png)

但在 SwiftUI 中，因目前版本（beta 7）受限于不支持返回不确定的内容，因此，我的设计为：

```swift
MASSquareMenuView(isShowMenu: self.$showingMenuView) {
    Group {
        MASSquareMenuCell(itemName: "笔记", 
                          itemImageName: "square.and.pencil") {
            FirstView()
        }
        MASSquareMenuCell(itemName: "广场", 
                          itemImageName: "burst") {
            SecondView()
        }

        // ...
    }
}
```

其中 `itemName` 和 `itemImageName` 均可通过 `ForEach` 来完成，目前还没找到一个可以完成动态跳转的比较好的方式。

#### 拆解
如何把多个子 `View` 通过以上类似这种相对优雅的方式进行视图组合？我的这种封装方法思想来源于 `List` 系统组件的使用方式：

```swift
 List {
    // PJPostView(post: post)

    ForEach(posts) { post in
        PJPostView(post: post)
    }
}
```

先来看 `List` 这个系统组件的定义：

```swift
@available(iOS 13.0, OSX 10.15, tvOS 13.0, watchOS 6.0, *)
public struct List<SelectionValue, Content> : View where SelectionValue : Hashable, Content : View {

    @available(watchOS, unavailable)
    public init(selection: Binding<Set<SelectionValue>>?, @ViewBuilder content: () -> Content)

    @available(watchOS, unavailable)
    public init(selection: Binding<SelectionValue?>?, @ViewBuilder content: () -> Content)

    public var body: some View { get }
    public typealias Body = some View
}
```

发现有一个全新的关键词 `@ViewBuilder`，要求被 `@ViewBuilder` 修饰的 `content` 闭包返回的是个 `Content`。`Content` 的定义如下：

```swift
@available(iOS 13.0, OSX 10.15, tvOS 13.0, watchOS 6.0, *)
public protocol ViewModifier {

    associatedtype Body : View

    func body(content: Self.Content) -> Self.Body

    typealias Content
}
```

也就是说，`content` 里的可以被「包含」的对象，只要是 `View` 类型即可，这一点很完美，但 `@ViewBuilder` 是什么？文档中的定义为：

```swift
@available(iOS 13.0, OSX 10.15, tvOS 13.0, watchOS 6.0, *)
@_functionBuilder public struct ViewBuilder {

    /// Builds an empty view from an block containing no statements, `{ }`.
    public static func buildBlock() -> EmptyView

    /// Passes a single view written as a child view (e..g, `{ Text("Hello") }`) through
    /// unmodified.
    public static func buildBlock<Content>(_ content: Content) -> Content where Content : View
}
```

终于看出了点端倪，通过 `@ViewBubilder` 修饰的 `View` 可以接收多个组合视图，从官方文档中，我们可以得知最多同时单个组件可承载的最大子组件数为 10 个。如果超过 10 个子组件，官方推荐的做法是再抽象进行封装成一个新的组件。

![](https://i.loli.net/2019/11/11/A2eRycMEl4bsQdp.png)

大致的菜单 Cell 实现细节为：

```swift
struct MASSquareMenuView<Content: View>: View {
    
    @Binding var isShowMenu: Bool
    var content: () -> Content
    
    var body: some View {
        GeometryReader { _ in
            VStack(alignment: .leading) {
                self.content()
            }
            
            // ......
        }
    }
}
```

对这个 `MunuView` 初始化的时候，不给 `init` 方法，补齐 `content`，并且因为在 Swift 5.x 中最后一个闭包可省略，这就出现了之前的 API 格式。在封装 SwiftUI 组件的适合，可以不用一开始就着手封装，而是先「一锅端」，最好再利用 Xcode 11 提供的快捷操作，直接把位于一个上下文中的组件进行「一键抽离」。


## 0x03 | Combine 与 CoreData
这里引入 `CoreData` 的意义只是能够给了一个相对稳定的数据来源，目前暂时还未结合网络请求进行验证。

这个例子想要完成的事情有：

* 在「弹出框」中输入文本内容；
* 在「首页」展示输入的所有内容；
* 提供检索；
* `CloudKit` 备份。

![首页](https://i.loli.net/2019/11/11/AoV2g1SCbeRB9lk.png)

![输入](https://i.loli.net/2019/11/11/zVZH9XC46SOGfQ8.png)

实话实说，完成这整套无缝的逻辑下来，花了不少时间。主要的时间耗费在理解和适应 SwiftUI 与 Combine 之间的联合关系，经常在思考如何合理有效的组织各个数据源去控制组件的交互。其中一定要死死握住的就是「单一数据源」，把能够引发某个组件产生某种行为的源头限制在同一个数据对象本身。

其中，最为常用的三个状态修饰符为：

* `@State`；
* `@Binding`；
* `@ObservedObject`。

在这个例子中的使用方式为：

```swift
@State private var showingSheet = false

@Binding var text: String

@ObservedObject var aritcleManager = AritcleManager()
```

使用 `@State` 来修饰 `showingSheet` 变量作为控制「输入框」是否弹出的标识位，使用 `@Binding` 来修饰 `text` 从「弹出框」中**引用**出用户输入的内容，使用 `@ObservedObject` 修饰 `aritcleManager` 对象，其作为连接首页数据交互的中枢。

`@State` 的作用本质上非常像「自动合成」了被修饰变量的 `setter` 和 `getter` 方法，我们如果直接使用 `didSet`/`willSet` 监听方法，也确实能够完成 `@State` 做的事情，这部分事情之前也确实有人做过。在 SwiftUI 中每当去触发一个 `@State` 修饰变量的 `setter` 方法时，`body` 属性都会根据新值跑一遍 diff，找出需要被刷新的视图，并生成新的视图进行刷新。

`AritcleManager` 作为首页数据处理的中枢，其承担了「输入」和「搜索」两个任务，而为了保证单一数据源的理念，引入了 `@Published` 修饰其内部持有的真正数据源 `articles`，每当 `articles` 发生改变时，都向外部订阅者发布通知。

```swift
class AritcleManager: NSObject, ObservableObject {
    // 写法 1
    var objectWillChange: ObservableObjectPublisher = ObservableObjectPublisher()
    // 写法 2
    @Published var articles: [Article] = []
}
```

与 CoreData 的交互使用了 `NSFetchedResultsController` 来进行，这部分可以替换成网络交互部分的方法：

```swift
// MARK: NSFetchedResultsControllerDelegate
extension AritcleManager: NSFetchedResultsControllerDelegate {
    
    func controllerDidChangeContent(_ controller: NSFetchedResultsController<NSFetchRequestResult>) {
        articles = controller.fetchedObjects as! [Article]
        // 写法 2 可省略，不需要主动触发发布
        objectWillChange.send()
    }
}
```

在「首页」中的初始化和交互操作为：

```swift
struct MASSquareHostView: View {
    
    @ObservedObject var aritcleManager = AritcleManager()
    
    var body: some View {
        NavigationView {
            MASSquareListView(articles: self.$aritcleManager.articles,
                              showingSheet: self.$showingSheet) {
                                self.aritcleManager.articles[$0].delete()
            }
        }
    }
}
```

从写法 1 发现了一个奇怪的地方（写法 2 可暂时理解为是写法 1 的语法糖）， `ObservableObjectPublisher` 是怎么做到「自动监听」的呢？来看看其定义：

```swift
@available(iOS 13.0, OSX 10.15, tvOS 13.0, watchOS 6.0, *)
final public class ObservableObjectPublisher : Publisher {

    public typealias Output = Void

    public typealias Failure = Never

    public init()

    final public func receive<S>(subscriber: S) where S : Subscriber, S.Failure == ObservableObjectPublisher.Failure, S.Input == ObservableObjectPublisher.Output

    final public func send()
}
```

其中 `ObservableObjectPublisher` 是继承自 `Publisher` 类，而 `Publisher` 是 Combine 中三大支柱之一，具体定义为：

```swift
@available(OSX 10.15, iOS 13.0, tvOS 13.0, watchOS 6.0, *)
public protocol Publisher {

    associatedtype Output

    associatedtype Failure : Error

    func receive<S>(subscriber: S) where S : Subscriber, Self.Failure == S.Failure, Self.Output == S.Input
}
```

### Combine 中的三大支柱

* `Publisher`，负责发布事件；
* `Operator`，负责转换事件和数据；
* `Subscribe`，负责订阅事件。

这三者都是协议，且都是 `@propertyWrapper` 的具体应用。

#### Publisher
`Publisher` 最主要的工作其实有两个:发布新的事件及其数据，以及准备好被 `Subscriber` 订阅。`Output` 及 `Failure` 定义了某个 `Publisher` 所发布的值的类型，以及可能产生的错误 的类型。

`Publisher` 可以发布三种事件：

1. 类型为 `Output` 的新值:这代表事件流中出现了新的值；
2. 类型为 `Failure` 的错误:这代表事件流中发生了问题，事件流到此终止；
3. 完成事件：表示事件流中所有的元素都已经发布结束，事件流到此终止。

`Publisher` 的这三种事件不是必须的，也就是说，`Publisher` 可能只发一个或者一个都不发，也有可能一直在发，永远不会停止，这就是**无限事件流**，还有可能通过发出 `failure` 或者 `finished` 的事件表明不会再发出新的事件，这是**有限事件流**。

![Apple 提供了满足几乎所有场景的 Publiser](https://i.loli.net/2019/11/12/9P1pQS7YdGgLurH.png)

#### Operator

每个 `Operator` 的行为模式都一样：它们使用上游 `Publisher` 所发布的数据作为输入，以此产生的新的数据，然后自身成为新的 `Publisher`，并将这些新的数据作为输出，发布给下游，这样相当于得到了一个响应式的 `Publisher` 链条。

当链条最上端的 `Publisher` 发布某个事件后，链条中的各个 `Operator` 对事件和数据进行处理。在链条的末端我们希望最终能得到可以直接驱动 UI 状态的事件和数据。这样，终端的消费者可以直接使用这些准备好的数据。

## 总结
问题一：其不适合直接使用在当前「树形操作流」的工程里，用户对 App 的操作以目前的情况来看是一种「树形结构」，但 SwiftUI 与 Combine 的强依赖，导致了必须写大量的兼容代码去兼容 Combine 的开发哲学，但 Combine 自身的「线性开发模型」与现在的模型是冲突且难以兼容的。所以，问题不仅仅只是在对系统版本的依赖上这么简单而已。

问题二：目前 SwiftUI 并不具备多行文本组件，只能通过 `UITextView` 包一层，包完了以后在模拟器上一跑就卡死，只能走真机。换句话说，如果是从零开始想要搞一个大事情，全部基于 SwiftUI 去 UI 表现层上的内容，几乎不可能，非常非常痛苦。

这两个问题在我看来都是可解的，尤其是问题二，正是因为其能够完美的无缝兼容 `UIKit`，在接入成本上可以忽略不计，反而是问题一带来的影响会更大，虽然 Combine 与现在 Rx 等一套有异曲同工之处，但对已有业务的改造成本不小，比如埋点，可能会需要从以往的跟随视图的变化变为跟随数据流。

SwiftUI 与 SB 和 xib 一样，我认为其只是个 UI 表现层，且可以认为是用于布局等最上层的操作，对待其应该使用 SB 和 xib 的思路去使用。

## 参考链接
### demo

[Masq](https://github.com/windstormeye/Masq-iOS)

[能否关个灯](https://github.com/windstormeye/SwiftGame)

### 相关内容
[SwiftUI Tutorials](https://developer.apple.com/tutorials/swiftui/)

[SwiftUI 的一些初步探索 (一)](https://onevcat.com/2019/06/swift-ui-firstlook/)

[SwiftUI 的一些初步探索 (二)](https://onevcat.com/2019/06/swift-ui-firstlook-2/)

[SwiftUI 与 Combine 编程](https://objccn.io/products/swift-ui)

[历时五天用 SwiftUI 做了一款 APP，阿里工程师如何做的？](https://mp.weixin.qq.com/s/QgDSuTFjwFlXzhksfgmkIQ)

[SwiftUI 怎么实现一个「更多菜单」？](http://pjhubs.com/2019/08/06/swiftui01/)

[SwiftUI 怎么和 Core Data 结合？](http://pjhubs.com/2019/08/12/swiftui02/)


### 开源库
[CombineX](https://github.com/cx-org/CombineX)

[MovieSwiftUI](https://github.com/Dimillian/MovieSwiftUI)


