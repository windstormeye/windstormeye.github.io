---
title: iOS14 - Widget 
date: 2020-11-09 13:06:38
tags:
- iOS
- Widget
---

快速、关联性、个性化

快速看一眼小组件，就能够达到最大价值

内容才是最大重点

小组件不是 mini app
* 应该看作是把 app 的内容投射到主屏幕上

智能叠放
* 可以通过 Siri 快捷指令来帮助系统定位何时该展示你的 widget
* 系统还提供了 widgetKit API 来协助展示。

widget 有三个尺寸，但不强迫每个尺寸都实现，因为不是所有 app 都适合全尺寸 widget 展示，但推荐都实现（猜测就是要给用户最大自由度。

widgwt 支持内容配置，详情参考系统天气 widget。

只能使用 SwiftUI 进行开发。

官方给出的数据，一般我们会在一天的时间里进入主屏幕超过 90 次，并在主屏幕上短暂停留。

widget 更新数据依赖时间线。

widget：
* Configuration
    * StaticConfiguration。app 提供的默认配置。
    * IntentCOnfiguration。允许用户选择配置。
* PlaceHolder。widget 在初始化 loading 过程中的占位 UI。
    * 每一个 widget 都必须提供。
    * 默认内容展示。
    * 没有任何用户相关数据。
    * 当系统无法显示你的小组件数据时会出现。
    * 无法被告知什么时候应该展示占位图。这是系统行为，系统需要的时候就会要求展示，例如用户更换了 widget 尺寸等。
* supportedFamilies
    * 可以填入当前 Widget 支持的小组件类型
* 创建 StatelessUI（无状态 UI
* 不能滚动和不能添加开关等其它系统控件。
* 不支持视频和动图。
* 都是为了引导用户可以轻松的点击小组件和通过 deepLink 跳转到我们的 app 中。
* 通过 widgetURL 与 app 内容关联起来。

snapshot

timeline

reloadPolicy

System reloads
* 经常被查看的 widget 会获得更多的刷新机会

当用户主动修改或 app 收到通知修改了内容，可以通过 WidgetCenter API 来刷新 widget。

小组件并不是在主屏幕上实时展示的。

Intent frameworks
* 可以看 Siri 相关的 session。


小组件智能化：
* TimelineEntryRelevance
    * score
    * duration
    * 其实这有点像评估函数的说法。



个人化、信息化和关联化。

photo widget 总是拿出最棒的照片，而不是最新的照片。

不要把小尺寸组件直接拉伸成中或者大尺寸小组件。

小尺寸组件只能接受单次点击。

* 小组件内部按照 16pt 设定布局边距。
* 小组件内部有圆形素材，应该使用 11pt 边距。
* 小组件内部边界有圆角时要做得跟小组件本身的圆角半径同心。
    * 不同设备上的小组件本身圆角值不一样，不能直接写死圆角值。
    * SwiftUI 中提供了一个圆角容器。
* 字体官方推荐使用 SF 系列，可自定义。
* 不要放入 app logo 和 name。


WidgetKit 配置由 SiriKit 驱动。

Widget 的 deepLink 是 SwiftUI 提供的新 API。

### 如何控制允许用户选择的小组件类型？
* supportedFamilies
    * 可以填入当前 Widget 支持的小组件类型

    ```swift
    @main
    struct EmojiRangerWidget: Widget {
        private let kind: String = "EmojiRangerWidget"

        public var body: some WidgetConfiguration {
            StaticConfiguration(kind: kind, provider: Provider()) { entry in
                EmojiRangerWidgetEntryView(entry: entry)
            }
            .configurationDisplayName("Ranger Detail")
            .description("See your favorite ranger.")
            .supportedFamilies([.systemSmall, .systemMedium])
        }
    }
    ```

    * 在构建 `entryView` 时，根据当前选择的 `widgetFamily` 来返回不同的样式。

    ```swift
    struct EmojiRangerWidgetEntryView: View {
        var entry: Provider.Entry

        @Environment(\.widgetFamily) var family
        
        @ViewBuilder
        var body: some View {
            switch family {
            case .systemSmall:
                AvatarView(entry.character)
            default:
                ZStack {
                    HStack(alignment: .top) {
                        AvatarView(entry.character)
                            .foregroundColor(.white)
                        Text(entry.character.bio)
                            .padding()
                            .foregroundColor(.white)
                    }
                }
                .background(Color.gameBackground)
            }
        }
    }
    ```

* 在构建 PlaceHolderView 时，Session 中所给的 isPlaceHoler 通过属性的方式去做已经不行了，得通过以下方式来进行：

```swift
EmojiRangerWidgetEntryView(entry: SimpleEntry(date: Date(), character: .panda)).redacted(reason: .placeholder)
```

* 当小组件位于堆叠视图中，可以使用 relevance 来提示系统提高小组件优先级的具体时间。
    * 类似于写一个评估函数，来对比两个时间点下当前 widget 是否要被展示出来。


### 小组件如何支持 linkAPI
* 也即 deepLink
    * 在构建 entryView 的视图上添加 `.widgetURL()`，并传入 url 即可。
* 需要注意的是，传入的 url 是单独经过处理的。
* 打开哪个 URL 需要在 ContentView 中进行匹配处理。
    ```swift
    struct ContentView: View {
    
    @State var pandaActive: Bool = false
    @State var spoutyActive: Bool = false
    @State var eggheadActive: Bool = false
    
    var body: some View {
        NavigationView {
            List {
                NavigationLink(
                    destination: DetailView(character: .panda), isActive: $pandaActive) {
                    TableRow(character: .panda)
                }
                NavigationLink(
                    destination: DetailView(character: .spouty), isActive: $spoutyActive) {
                    TableRow(character: .spouty)
                }
                NavigationLink(
                    destination: DetailView(character: .egghead), isActive: $eggheadActive) {
                    TableRow(character: .egghead)
                }
            }
            .onAppear {
                if let character = CharacterDetail.getLastSelectedCharacter() {
                    print("Last character selection: \(character)")
                }
            }
            .navigationBarTitle("Your Characters")
            .onOpenURL(perform: { (url) in
                self.pandaActive = url == CharacterDetail.panda.url
                self.spoutyActive = url == CharacterDetail.spouty.url
                self.eggheadActive = url == CharacterDetail.egghead.url
            })
        }
    }
}
    ```