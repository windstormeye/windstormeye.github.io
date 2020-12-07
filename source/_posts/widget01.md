---
title: 从实际问题看 SwiftUI 和 Widget 编程
date: 2020-12-06 18:21:38
tags:
- iOS14
- Widget
- SwiftUI
---

![](http://img.pjhubs.com/20201207102254.png)

Widget 的实现依赖 SwiftUI，SwiftUI 部分的内容推荐大家自行学习，给出了一些质量较高的文章，可以配置 WWDC19/20 SwiftUI 相关 session 搭配食用。

## 参考资料
- 推荐看完 WWDC20 Widget Code-Along 三个环节
  - https://developer.apple.com/wwdc20/10034
  - https://developer.apple.com/wwdc20/10035
  - https://developer.apple.com/wwdc20/10036
- [TimelineProvider](https://developer.apple.com/documentation/widgetkit/timelineprovider)
- [小组件编程临摹课程](https://developer.apple.com/cn/news/?id=yv6so7ie)
- [当 Widget 遇到智能化](https://my.oschina.net/SwiftOldDriver/blog/4528390)

Demo 工程：[SwiftUIWidget](https://github.com/windstormeye/SwiftUIWidget)



## 前言
iOS14 的 Widget 和 iOS14 之前的 Widget 已经完成了统一，之前老样式的 Widget 只能通过在老版本上进行查看，后续仅支持 iOS14 目前的 Widget。只能使用 SwiftUI 进行开发。

## Widget 核心
- 快速、关联性、个性化
- 看一眼，就能够获取到重点内容
- 内容才是最重要的
  - 相册 Widget 注意到的话，会发现展示的照片总是某个时刻下最棒的那一张，而不是最新的。

Widget 不是 mini app，应该看作是把 app 的内容在主屏幕的映射关系。官方给出的数据，一般我们会在一天的时间里进入主屏幕超过 90 次，并在主屏幕上短暂停留。

## Widget 类型
Widget 有三个尺寸，但不强迫每个尺寸都实现，因为不是所有 app 都适合全尺寸 widget 展示，但推荐都实现（猜测就是要给用户最大自由度。

![](http://img.pjhubs.com/20201207102329.png)

- 不能滚动和不能添加开关等其它系统控件。
- 不支持视频和动图。
- 小组件并不是在主屏幕上实时展示的。
  - 系统的时钟 Widget 的事实刷新 UI 是个系统级 app 才能拥有的对待。
  - SwiftUI 中对 `Text` 组件新增了可以实时展示时间的 API。
    - `Text(Date(), style: .time)`
- 不要把小尺寸组件直接拉伸成中或者大尺寸小组件。
- Small 尺寸组件只能接受单次点击。
- 小组件内部按照 16pt 设定布局边距。
- 小组件内部有圆形素材，应该使用 11pt 边距。
- 小组件内部边界有圆角时要做得跟小组件本身的圆角半径同心。
  - 不同设备上的小组件本身圆角值不一样，不能直接写死圆角值。
  - SwiftUI 中提供了一个圆角容器。
- 字体官方推荐使用 SF 系列，可自定义。
- 不要放入 app logo 和 name。

## Widget 如何成组？
控制允许用户选择的小组件类型
```swift
@main
struct PJWidget: Widget {
    private let kind: String = "PJWidget"

    public var body: some WidgetConfiguration {
        StaticConfiguration(kind: kind, provider: Provider()) { entry in
            PJWidgetEntryView(entry: entry)
        }
        .configurationDisplayName("PJWidget")
        .description("2333")
        .supportedFamilies([.systemSmall, .systemMedium])
    }
}
```

在构建 `entryView` 时，根据当前选择的 `widgetFamily` 值来返回不同的样式。

```swift
struct PJWidgetEntryView: View {
    var entry: Provider.Entry
    @Environment(\.widgetFamily) var family

    @ViewBuilder
    var body: some View {
        switch family {
        case .systemSmall:
            PJAvatarView(entry.name)
        default:
            Text("PJHubs")
        }
    }
}
```

使用 Xcode Widget Extension 模版创建完后，会自动给默认 Widget 加上 `@main` 修饰符标记出当前 app Widget 的入口。

换句话说，此时我们进入到「Widget 搜索」，找到我们的 app，只会看到一个 Widget。

```swift
@main
struct SwiftUIWidgetDemo: Widget {
    let kind: String = "SwiftUIWidgetDemo"

    var body: some WidgetConfiguration {
        IntentConfiguration(kind: kind, intent: ConfigurationIntent.self, provider: Provider()) { entry in
            SwiftUIWidgetDemoEntryView(entry: entry)
        }
        .configurationDisplayName("西瓜作者-数据日报")
        .description("你的数据精简日报")
        .supportedFamilies([.systemSmall])
    }
}
```

![](http://img.pjhubs.com/20201207103211.png)

```swift
@main
struct Widgets: WidgetBundle {
    @WidgetBundleBuilder
    var body: some Widget {
        SwiftUIWidgetDemo()
        SwiftUIWidgeMediumDemo()
        SwiftUIWidgeMediumFansDemo()
    }
}
```

注意：最多只允许塞入五个 Widget 样式。

### Tips：What is `@main`？
说起 `@main` 大家可能会先想到之前的 `@UIApplicationMain` 这个修饰词，说到 `@UIApplicationMain` 可能又会想到 main.swift 或者 main.m 等等这些文件。总的来说，它们之间是存在某种神秘联系的！我们来写一个简单的 Swift 代码：

```swift
class demoSwift {
    class func test() {
        print("world!")
    }
}
demoSwift.test()
```

此时使用 `swiftc demo.swift` 后会得到一个可执行文件，看上去 Swift 的语法让新上手的同学令人感到愉快，不会再有类 C 系那种必须写一系列又臭又长的 main 函数初始化流程，但本质上真的不用写了吗？
我们来看看中间代码。

```shell
# 查看生成的中间代码
swiftc demo.swift -emit-sil
```

```swift
sil_stage canonical

import Builtin
import Swift
import SwiftShims

class demoSwift {
  class func test()
  @objc deinit
  init()
}

// main
sil @main : $@convention(c) (Int32, UnsafeMutablePointer<Optional<UnsafeMutablePointer<Int8>>>) -> Int32 {
bb0(%0 : $Int32, %1 : $UnsafeMutablePointer<Optional<UnsafeMutablePointer<Int8>>>):
  %2 = metatype $@thick demoSwift.Type            // user: %4
  // function_ref static demoSwift.test()
  %3 = function_ref @$s4demo0A5SwiftC4testyyFZ : $@convention(method) (@thick demoSwift.Type) -> () // user: %4
  %4 = apply %3(%2) : $@convention(method) (@thick demoSwift.Type) -> ()
  %5 = integer_literal $Builtin.Int32, 0          // user: %6
  %6 = struct $Int32 (%5 : $Builtin.Int32)        // user: %7
  return %6 : $Int32                              // id: %7
} // end sil function 'main'

// ... 以下省略
```

可以看到，所谓的对新人友好都是假的，全都是编译期间 `swiftc` 做的自动化插入，自动给我们的方法插入了与之前类似的流程，如果我们需要多文件编译依赖，要有一个 main.swift 作为入口文件进行索引其他文件进行编译。
`@UIApplicationMain` 出现后，我们不再需要 main.swift 文件来做入口切割，可通过自定义类并加上该标记即可，这个好处在 Swift 5.3 中正式推广到语言层面，我们仅需使用 `@main` 即可标记出 Swift 文件的入口，不再是 Cocoa 特性，进而替代掉了 `@UIApplicationMain`。


## Widget 用户如何配置数据？
Widget 提供了用户可配置数据源的方式，可以通过此类方式来绕过 Widget 成组后最大上限五个的限制。提供两种配置方式

- StaticConfiguration。用户不可自定义数据源，参考头条 Widget。
![](http://img.pjhubs.com/20201207103106.png)
- IntentCOnfiguration。允许用户选择配置，参考下图。
![](http://img.pjhubs.com/20201207103610.png)

其中 IntentConfiguration 可提供给用户有限的“自由”，自行选择对应 Widget 下需要展示的数据源。利用了基于 Intents.framework 框架实现，并可以直接复用 SiriKit 的功能来达到 Widget 的智能化（后文再叙）。

配置 IntentConfiguration 的步骤如下：
- 创建对应的 IntentConfiguration 文件。

![](http://img.pjhubs.com/20201207103329.png)

- 新增用户可配置的数据类型

![](http://img.pjhubs.com/20201207103355.png)

- 配置新增数据类型相关信息

![](http://img.pjhubs.com/20201207103420.png)

- 在对应类型的 Widget 中判断数据视图

```swift
struct SwiftUIWidgetDemoMediumEntryView : View {
    var entry: Provider.Entry

    @ViewBuilder
    var body: some View {
        switch entry.configuration.countType {
        case .money:
            // 此处需传入数据源
            MediumWidgetFansView()
        default:
            // 此处需传入数据源
            MediumWidgetView()
        }
    }
}
```

### Tips: What is `@ViewBuilder`
[从实际问题看 SwiftUI 和 Combine 编程](http://pjhubs.com/2019/11/09/swiftUIandCombine01/) 已说明，可以前往了解。

## Widget 如何跳转到对应的页面？
### 预览视图

```swift
struct Provider: IntentTimelineProvider {
    // NOTE: 小组件占位视图，第一次添加或 loading 状态中的视图
    func placeholder(in context: Context) -> SimpleEntry {
        SimpleEntry(date: Date(), count: 0, image: nil, configuration: ConfigurationIntent())
    }

    // NOTE: 第一次添加或小组件第一次被展示时调用
    func getSnapshot(for configuration: ConfigurationIntent, in context: Context, completion: @escaping (SimpleEntry) -> ()) {
        let entry = SimpleEntry(date: Date(), count: 0, image: nil, configuration: configuration)
        completion(entry)
    }
                
    func getTimeline(for configuration: ConfigurationIntent, in context: Context, completion: @escaping (Timeline<Entry>) -> ()) {
        // ...
        let timeline = Timeline(entries: entries, policy: .atEnd)
        completion(timeline)
    }
}
```

placeholder方法中返回 widget 在初始化 loading 过程中的占位 UI。
  - 每一个 widget 都必须提供。
  - 默认内容展示。
  - 没有任何用户相关数据。
  - 当系统无法显示你的小组件数据时会出现。
  - 无法被告知什么时候应该展示占位图。这是系统行为，系统需要的时候就会要求展示，例如用户更换了 widget 尺寸等。
![](http://img.pjhubs.com/20201207103745.png)

这个视图是系统行为，只要我们使用的是标准 SwiftUI 组件，会自动根据组件类型，如 `Image`、`Text` 结合我们自定义的颜色和背景来自动完成占位图的设置，如果我们不想要的系统自定义的话，也可以在方法中自行返回自定义的占位组件。

注意点：在构建 `PlaceHolderView` 时，Session 中所给的 `isPlaceHoler` 通过属性的方式去做已经不行了，得通过以下方式来进行（如果我们需要预览的话）：
```swift
PJWidgetEntryView(entry: SimpleEntry(date: Date())).redacted(reason: .placeholder)
```

### 跳转
Widget 的目的非常简单，目前在 Widget 上所做的事情，全都是为了引导用户可以轻松的点击小组件和通过 deepLink 跳转到我们的 app 中。而从 Widget 跳转到 app 中针对不同类型的 Widget 有共有两种跳转方式。

- `.widgetURL`
  - 三种类型的小组件均可使用该方式进行跳转。
    ```swift
    struct SmallWidgetView: View {
        var body: some View {
            VStack(alignment:.leading) {
            Text("PJHubs")
            }
            .widgetURL(URL(string: "urlschema://pjhubsWidgetURL"))
        }
    }
    ```

- `Link`
  - 只有 Medium 和 Large 类型的小组件可以使用该方式进行跳转。
  - Small 类型小组件编译没问题，点击后无回调。
    ```swift
    struct MediumWidgetView: View {
        var body: some View {
            Link(destination:URL(string: "urlschema://pjhubsLink")!) {
                VStack(alignment:.leading) {
                    Text("PJHubs")
                }
            }
        }
    }
    ```

- SceneDelegate.m 中的内容为：
  - 可以直接复用以往主工程通过消息通知 push 的逻辑流程来打开 widget 上挂载的 schema。
```swift
#import "SceneDelegate.h"
#import "WidgetURLViewController.h"
#import "LinkViewController.h"

@implementation SceneDelegate

- (void)scene:(UIScene *)scene openURLContexts:(NSSet<UIOpenURLContext *> *)URLContexts {
    if (URLContexts.allObjects.count != 0) {
        UIOpenURLContext *urlContext = URLContexts.allObjects.firstObject;
        NSURL *url = urlContext.URL;
        if ([url.absoluteString isEqualToString:@"urlschema://pjhubsWidgetURL"]) {
            [self.window.rootViewController presentViewController:[WidgetURLViewController new] animated:YES completion:nil];
        }
        
        if ([url.absoluteString isEqualToString:@"urlschema://pjhubsLink"]) {
            [self.window.rootViewController presentViewController:[LinkViewController new] animated:YES completion:nil];
        }
    }
    
}

@end
```

### 注意点
- 调试 Widget Deep Link 跳转时需要切换到 app target 下进行调试，一直在用 Widget target 调，发现断点一直走不进去，才猛的想起来，我在 widget target 里能断在 app target 里才奇了怪了。
- 更新 widget 的内容后，需要 build 一遍 widget target，然后再回到 app target 走 app 生命周期相关方法。

### Tips: 如果 OC View 想要被使用在 SwiftUI 中。
- 首先创建或确定要被引入 SwiftUI 中的 OC 视图，下文以 OCView 替代。

```Objective-C
#import "OCView.h"

@implementation OCView

- (instancetype)initWithFrame:(CGRect)frame {
    if (self = [super initWithFrame:frame]) {
        [self initView];
    }
    return self;
}

- (void)initView {
    self.backgroundColor = [UIColor whiteColor];
    
    UILabel *textLabel = [[UILabel alloc] init];
    textLabel.text = @"这是 OC View";
    textLabel.font = [UIFont systemFontOfSize:30];
    [textLabel sizeToFit];
    textLabel.frame = CGRectMake((self.frame.size.width - textLabel.frame.size.width)/2, (self.frame.size.height - textLabel.frame.size.height)/2, textLabel.frame.size.width, textLabel.frame.size.height);
    [self addSubview:textLabel];
}

@end
```

- 创建一个 OCWidgetView.swift 文件，用于封装 SwiftUI 视图。

```swift
import Foundation
import SwiftUI


struct OCWidgetView: UIViewRepresentable {
    func makeUIView(context: Context) -> OCView {
        return OCView()
    }
    
    func updateUIView(_ uiView: OCView, context: Context) {
        
    }
}
```

SwiftUI 中提供了 `Coordinator` 这个理念来作为 `OCView` 可能存在的各种 delegate 相关回调事件，在 SwiftUI 中同样可以进行使用，在此不做展开。

此时就可以在 SwiftUI 中引入 OCWidgetView 了！

```swift
struct MediumWidgetFansView: View {
    var body: some View {
        VStack(alignment:.leading) {
            OCWidgetView()
        }
    }
}
```

Widget 的 UI 部分只能使用 SwiftUI 框架下的 UI 组件，不能使用任何 UIKit 相关的组件，就算用 SwiftUI 包一层也不行（UIViewRepresentable），强行使用的话，会在 Widget 视图上得到一个黄色背景红叉：
![](http://img.pjhubs.com/20201207104139.png)


## Widget 如何更新数据？
### 刷新时机
#### Timeline 刷新
Widget 需要通过 Timeline 来进行数据刷新，但其刷新的时机由系统控制，但有时我们设置了刷新间隔时间也不一定会在该时间点进行刷新。

如果我们完全依赖 Widget 自身的数据更新策略，每次间隔 1s 刷新数据，每次更新时拉取 5 个数据，设置 Timeline policy为 `.atEnd`，也即当 timeline 中的数据用完后立即拉取下一条数据，则最短也许要 1min 时间才能拉取下一条 timeline（自测）。

- `atEnd`: 拉取到最后一个数据后重新拉取。
- `atAfter`: 在指定时间后以一定时间间隔拉取数据。
- `never`：该 timeline 不需要刷新。

不是都需要一次在 timeline 中构造好多个数据实体，可以一次返回一个，刷新间隔设置为 1min（或其它时间），这样比较适合对数据实时性要求较高的产品。系统并不少按照我们所规定的那样执行逻辑，系统考虑的因素用官方的话语来说，要结合耗电量等等问题综合给到不同 Widget 的刷新时机和此时，但总的来说，经常被查看的 widget 会获得更多的刷新机会。

#### 主动刷新
如果我们想要在 app 内主动同步 widget 上所展示的消息，或在当前时刻必须刷新，如“开言英语” Widget 用户登录前后的 UI 表现不同等，在这种需求背景下，我们可以使用 WidgetKit 的 WidgetCenter API 来完成。

![](http://img.pjhubs.com/20201207104248.png)

`WidgetCenter.shared.reloadAllTimelines()`。`reloadAllTimelines` 方法会重新 load 所属 app 内的所有已配置的 Widget，重新拉取 Timeline。

需要注意的是，WidgetKit 为 Swift Only，想要在 OC 工程中使用该方法刷新 Widget Timeline 得通过 Swift 包一层，且要求 app 处于活跃状态。

```swift
import WidgetKit

@objcMembers class PJWidgetCenter: NSObject {
    class func reloadWidgetTimeline() {
        WidgetCenter.shared.reloadAllTimelines();
        WidgetCenter.shared.reloadTimelines(ofKind: "What kind of widget?")
    }
}
```

支持所有 widget 刷新或某一个 widget。

```swift
#import "ViewController.h"
#import "SwiftUIWidget-Swift.h"

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    [PJWidgetCenter reloadWidgetTimeline];
}
```

数据来源
`getTimeline` 方法支持异步操作，我们如果需要动态的走网络请求拉取构造 timeline 数据，可以直接丢出一个异步回调。

```swift
struct Provider: IntentTimelineProvider {

    // ...
    func getTimeline(for configuration: ConfigurationIntent, in context: Context, completion: @escaping (Timeline<Entry>) -> ()) {
        networkHandler {
            let timeline = Timeline(entries: $0, policy: .atEnd)
            completion(timeline)
        }
    }

    func networkHandler(completion: @escaping ([SimpleEntry]) -> Void) {
        URLSession.shared.dataTask(with: URL(string: "http://pjhubs.com")!) { (data, response, error) in
            let originalDict = try? JSONSerialization.jsonObject(with: data!, options: JSONSerialization.ReadingOptions.allowFragments) as? NSDictionary
            print(originalDict as Any)
            completion([SimpleEntry(date: Date(), count: 1234, image: UIImage(named: "avatar")!, configuration: ConfigurationIntent())])
        }.resume()
    }
}
```

注意请求间隔、Timeline 更新时间和数据转换等问题。

### 数据共享
以在 Widget 展示用户头像举例，在以往的开发经历中，我们都不希望有同步操作阻塞主线程从而造成 app 卡顿，故在 Widget 中我们也会自然而然的在“图片展示”这一环节中套用异步请求资源的思路去做，但这在 Widget 中是不被允许的，我们需要转变一个思路。

以下这种把图片资源延后到 UI 层的做法可以拉取成功，但不会被加载。
```swift
struct SmallWidgetView: View {
    @State var networkImage: UIImage?

    var body: some View {
        VStack(alignment:.leading) {
            HStack {
                Image(uiImage: self.networkImage ?? UIImage(named: "avatar")!)
                    // ...
                    .onAppear(perform: getNetworkImage)                
            }       
           // ...
        }
        // ...
    }

    func getNetworkImage() {
        URLSession.shared.dataTask(with: URL(string: "https://tu.sioe.cn/gj/qiege/image.jpg")!) { (data, _, _) in
            self.networkImage = UIImage(data: data!)
        }.resume()
    }
}
```

解决这一问题目前有三种方法但都是一种思路，核心就是把图片的加载过程从异步转化为同步，这个同步的过程可以是在 `getTimeline` 初始化时间线时，也可以是在构造 Widget UI 层逻辑时。
- UserDefault
- FileManager
- CoreData

以下为在 getTimeline 初始化时间线时的事例：

```swift
struct SmallWidgetView: View {
    var uiImage: UIImage?

    var body: some View {
        VStack(alignment:.leading) {
            HStack {
                Image(uiImage: uiImage ?? UIImage(named: "avatar")!)
                    // ...
            }       
           // ...
        }
        // ...
    }   
}
```

```swift
struct Provider: IntentTimelineProvider {
    // ...
    func getTimeline(for configuration: ConfigurationIntent, in context: Context, completion: @escaping (Timeline<Entry>) -> ()) {
        var entries: [SimpleEntry] = []
        let currentDate = Date()
        for hourOffset in 0 ..< 3 {
            let entryDate = Calendar.current.date(byAdding: .second, value: hourOffset, to: currentDate)!
            // NOTE: 在处理 timeline 时就把资源加载好
            var image: UIImage? = nil
            if let imageData = try? Data(contentsOf: URL(string: "https://tu.sioe.cn/gj/qiege/image.jpg")!) {
                image = UIImage(data: imageData)
            }
            let entry = SimpleEntry(date: entryDate, count: Int.random(in: 0...100), image: image, configuration: configuration)
            entries.append(entry)
        }

        let timeline = Timeline(entries: entries, policy: .atEnd)
        completion(timeline)
    }
}
```

Widget 在最初放出的 beta 版本中是可以支持图片资源的异步回调的，但后来又改成了目前的这种只能通过同步的方式进行资源获取。

如果出现不同类型的 widget 需要复用图片资源，可以使用系统内轻量级 cache 方法（如：`NSCache`等）来完成在 A 类型 Widget 下已经加载完成的图片资源，后续用户再手动添加 B 类型 Widget 后可以加速 Widget 渲染。

当我们需要从 app target 传递数据到 widget target 时，可以组成 App Groups，通过 `UserDefualt` 来完成数据传递，注意两个 target 都需要增加 app groups。
![](http://img.pjhubs.com/20201207104639.png)

在 app target 中设置测试代码，10s 后刷新 widget 的显示内容，以此来模拟真实 app 中主工程触发某个网络事件，等待延时后同步数据给 Widget。

App target
```objc
#import "ViewController.h"
#import "SwiftUIWidget-Swift.h"

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];

    dispatch_after(dispatch_time(DISPATCH_TIME_NOW, (int64_t)(10 * NSEC_PER_SEC)), dispatch_get_main_queue(), ^{
        [PJWidgetCenter reloadWidgetTimeline];
    });
}
@end
```

Swift 处理过程（非必需）
```swift
import WidgetKit
import Foundation

@objcMembers class PJWidgetCenter: NSObject {
    class func reloadWidgetTimeline() {
        if let userDefaults = UserDefaults(suiteName: "group.com.pjhubs.swiftuiwidge") {
            userDefaults.setValue("2333", forKey: "integer")
        }
        WidgetCenter.shared.reloadAllTimelines();
    }
}
```

Widget
```swift
struct Provider: IntentTimelineProvider {
    @AppStorage("integer", store: UserDefaults(suiteName: "group.com.pjhubs.swiftuiwidge"))
    var intString: String = ""

    //...        
    func getTimeline(for configuration: ConfigurationIntent, in context: Context, completion: @escaping (Timeline<Entry>) -> ()) {
        var entries: [SimpleEntry] = []
        let currentDate = Date()
        for hourOffset in 0 ..< 5 {
            let entryDate = Calendar.current.date(byAdding: .second, value: hourOffset, to: currentDate)!
            // ...
            let entry = SimpleEntry(date: entryDate, count: Int(intString)!, image: image, configuration: configuration)
            entries.append(entry)
        }
        let timeline = Timeline(entries: entries, policy: .atEnd)
        completion(timeline)
    }
}
```

## Widge 如何在「智能堆叠」中提高展示？
**推荐看完 [为小组件添加智能和配置](https://developer.apple.com/videos/play/wwdc2020/10194/)**

基于 iOS12 引入的 Intent.framework，目前有两种提高 Widget 在智能堆叠中展示的办法。
- 用户行为捐赠（系统推断）
- 数据源评分展示（评估函数判分）

### 用户行为捐赠
WWDC20 Session - 为小组件添加智能和配置视频截图。

![](http://img.pjhubs.com/20201207104926.png)

我们可以把一些自定义的关键组合信息构造出一个 intent 捐赠给系统，通过 Intent.framework，系统不但可以把这些信息传递给我们 app widget 还可以传递到 spotlight 等其它依赖 Intent 的场景从而减少进入特定场景/app 的步骤。

转换成我们的产品视角，当作者每天都在 14 点查看自己的视频播放量这一个指标数据，可以在作者进入到指标页面时，通过构造 Intent 实例进行捐赠给系统，当累计到一定次数（不定）后，系统会在每天用户 14 点前后解锁进入主屏时，在「智能堆叠」Widget 中自动翻滚到我们加入其中的 Widget 并展示出对应的播放量 Widget。

![](http://img.pjhubs.com/20201207104957.png)

### 数据源评分展示
如果我们想要在特定时间主动突出小组件在智能堆叠上的展示机会，可以使用「数据源评分展示」策略，在构造 Timeline 时可以给不同的数据实体塞入不同的评分，从而达到在不同时间节点或特定时间节点下的突出展示。

转换成我们的产品视角，当作者新发布了一个视频，可能想要在未来的一天、两天甚至一周内关注视频本身的播放量这一指标，我们可以通过固定分数和持续时间来达到提升展示，从而关闭其它数据源更新时的

```swift
struct Provider: IntentTimelineProvider {

    // ...
    func getTimeline(for configuration: ConfigurationIntent, in context: Context, completion: @escaping (Timeline<Entry>) -> ()) {
        // ...
        for hourOffset in 0 ..< 3 {
           // ...
            if (hourOffset == 1) {
                let revelance = TimelineEntryRelevance(score: 2000, duration: 60);
                let entry = SimpleEntry(date: entryDate, count: 2000, image: image, configuration: configuration, relevance: revelance)
                entries.append(entry)
            } else {
                let revelance = TimelineEntryRelevance(score: 10, duration: 0);
                let entry = SimpleEntry(date: entryDate, count: Int(intString)!, image: image, configuration: configuration, relevance: revelance)
                entries.append(entry)
            }
        }

        let timeline = Timeline(entries: entries, policy: .atEnd)
        completion(timeline)
    }
}
```

需要注意的是，我们给在第二分钟时要展现的数据分数 Relevance 分数设置为 2000，其它数据的分数设置为 10 分，此时运行 Widget 并等待到第二分钟，智能堆叠的 Widget 并不会一定翻转到我们的 Widget 上，但 Widget 上的数据是确确实实被更新了的，同时也说明了系统并不会一定认为当前数据比同一个 Widget 下的其它数据评分高，就一定为在智能堆叠上必须展示我们的 Widget，只是说在智能堆叠执行翻转时，我们的 Widget 会获得比其它 Widget 可能会获得更高的展示机会。

并且该评分也仅仅只是和当前 Widget 内的数据源做的对比。

![](http://img.pjhubs.com/20201207105108.png)

