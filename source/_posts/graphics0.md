---
title: 基于 GPUImage 3 做一个修图工具
date: 2022-08-02 23:24:56
tags:
---


![](./images/graphics/0/0.png)

## SwiftUI

### 页面布局
写一个 macOS app 最重要的就是 UI 布局约束可变以及区域划分，这些内容我因为之前只接触过 iOS 以及一丢丢的 iPadOS 开发经验，被先入为主的带入了做一个内容区域可变化的 app 是非常困难的。谁知在经历过一发 Qt 的历练后，目前还没遇到使用 QML 无法实现的 UI 组件，而且目前基于 QML 所实现的 UI 组件过程也是十分美好的，几乎也没遇到多少棘手的问题。

对于 app 内 UI 区域可变在 QML 中使用 [`SplitView`](https://doc.qt.io/qt-6/qml-qtquick-controls2-splitview.html) 即可完成，在 SwiftUI 中我也同样思维的产生了直接敲下 `Split` 关键词，等待 Xcode 代码提示给到我惊喜，没想到这个惊喜还真有，SwiftUI 中的可变视图分割可使用 `VSplitView` 或 `HSplitView` 即可完成，虽然分开了这里和 QML 通过 property 方式区分不同，SwiftUI 采用不同的组件来划分水平和垂直 UI 划分，这两种做法我个人是比较喜欢 QML 更多一些，非必要不新增实体嘛。

![](./images/graphics/0/1.png)

```swift
struct ContentView: View {
    var body: some View {
        GeometryReader { geo in
            HSplitView {
                ImageBrowserView()
                        .frame(minWidth: geo.size.width * 0.5, idealWidth: geo.size.width * 0.8, maxWidth: geo.size.width * 0.8, minHeight: geo.size.height, idealHeight: geo.size.height, maxHeight: geo.size.height, alignment: .leading)
                

                
                AdjustColorView()
                        .frame(minWidth: geo.size.width * 0.2, idealWidth: geo.size.width * 0.2, maxWidth: geo.size.width * 0.5, minHeight: geo.size.height, idealHeight: geo.size.height, maxHeight: geo.size.height, alignment: .trailing)
            }
        }
    }
}
```

以上就是划分出上图所示红蓝区域的 SwiftUI 代码，这里引入了之前理解不到位的 `GeometryReader`，之所以要引入这个组件是因为我想要对 `SplitView` 划分出的 UI 红蓝两个区域做最大和最小 width 做限制，需要读取到父视图的 size，`GeometryReader` 组件做的就是读取当前组件的 size，macOS 的窗体大小如果不手动限制大小，会自动根据窗体中内容自动拓展大小。

而我们在 PhotoPApp 中通过 `.frame` 同样限制了最大最小和最适合的 size。

```swift
@main
struct PhotoPApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView().frame(minWidth: 680, idealWidth: 680, maxWidth: .infinity, minHeight: 400, idealHeight: 400, maxHeight: .infinity, alignment: .center)
        }
    }
}
```

### 打开文件管理器

```swift
Button("select File") {
    let panel = NSOpenPanel()
    panel.allowsMultipleSelection = false
    panel.canChooseDirectories = false
    if panel.runModal() == .OK {
        self.fileName = panel.url?.path ?? ""
    }
}
```

### 展示用户选择的图片

SwiftUI 的 `Image` 只是一个 UI 容器，自带了展示了沙盒内图片的能力，如果我们想要展示用户所选择的图片，需要使用 `Image(nsImage:)` 这个方法，塞入一个 `NSImage` 对象即可。

### 图片重设大小
使用 `.resizable` 方法。