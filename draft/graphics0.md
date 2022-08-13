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


### 导入 GPUImage 3

GPUImage 发展到第三代虽然支持 SPM 导入，但却无法正常 build，会提示无法打开获取 `defautl.metallib` 路径，出错的代码如下：

```swift
// ...
let frameworkBundle = Bundle(for: MetalRenderingDevice.self)
let metalLibraryPath = frameworkBundle.path(forResource: "default", ofType: "metallib")!
// ...
```

这个问题困扰了我好一会儿，刚开始以为是使用姿势的问题，例如初始化 `RenderView` 未传入必须参数，调整了几个参数后依旧不行。仔细对比 demo 后发现工程目录中都引入了 `GPUImage.xcodeproj`，产生一波后发现暂时没找到通过 SPM 引入 GPUImage 3 后如何便捷的引入工程中的方法。

我们需要做的是，download/clone 一份 GPUImage 3 源码，复制其中 framework 文件夹下内容到工程中，并在 `Build Phases` 中添加 GPUImage_mac framework 相关依赖。

![](./images/graphics/0/3.png)

![](./images/graphics/0/2.png)


### 切换图片 

在 GPUImage3 中切换输入源，需要重建所有相关对象，包括 `PictureInput`、`RenderView` 和各种 Filter 对象。若不重建，这些相关对象中关联的数据都是上一张图片。

清空数据后如果你使用的是非 SwiftUI 进行 UI 搭建，到此切换图片所需要注意的问题都被解决了，若你使用的是 SwiftUI 进行 UI 搭建，你会发现所有数据都重建了但 `RenderView` 中所关联的数据却依然无法被切换，刚开始一直以为还遗漏了什么数据未重建，反复盯了好几次调用栈后明确所有数据都重建完成。

此时问题就回到了 SwiftUI 这边，脑海里闪出了 AppKit/UIKit 视图暴露给 SwiftUI 后只关联了初始化时的第一次数据，但后续切换图片时并未“通知”到 SwiftUI 需要去刷新视图，而 SwiftUI 在视图刷新上又强依赖“状态”的变化，没办法，只好写出了如下十分愚蠢的代码：

```swift
// ...
@ObservedObject var imageManager = ImageManager.shared
// ..
if (imageManager.isUpdateRenderView) {
    GPUImageRenderView()
        .aspectRatio(ImageManager.shared.currentImageRatio,
                        contentMode: .fit)
} else {
    GPUImageRenderView()
        .aspectRatio(ImageManager.shared.currentImageRatio,
                        contentMode: .fit)
}
```

在需要刷新 SwiftUI 的地方，反复调用 `isUpdateRenderView.toggle()` 即可。

### SwiftUI 链式编程的坑

SwiftUI 链式编程十分美好，不需要开发者去关心如何组织 UI 上各种 set 关系，但仍需我们关注各种方法间的相互关系。如下图所示代码中 `.clipped()` 在 `.frame()` 之前会因为无法读取到当前组件的最终宽高而导致无法对内容进行正确的裁切。

```swift
Image(nsImage: ImageManager.shared.NSImageWithURL(imgUrl[urlIndex]))
    .resizable()
    .scaledToFill()
    .frame(width: 50, height: 50, alignment: .center)
    .clipped()
```

### 注意 Swift 的类型推断
当你的计算规则较长时，Swift 的类型推断就会出错，解决办法就是注意每一个变量的类型是否在计算规则过程中的一致性得到保证。

### SwiftUI 加大手势区域
在 `.frame` 后使用 `.contentShape()`（太骚了...