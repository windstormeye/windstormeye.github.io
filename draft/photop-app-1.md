---
title: 《PhotoP 开发日志 03》- 基础体验完善
date: 2022-11-27 19:08:57
tags:
- 作品
- 感想
- 开发日志
- App
- 产品思考
- macOS
---

## 应用商店搜不到
PhotoP 这个名字被其他 app 作为关键词占用了，目前直接搜索 PhotoP 需要往下滑好几行才能看到，实在是失大策了。

## Appearance 适配
超！居然忘了 light mode 的适配，自己一直在使用 dark mode，导致根本就没想起来要适配 light mode，偶然间切换了一次 light mode 后，app 整个 UI 太辣眼睛了，立马抓紧适配。

## 快捷键支持
SwiftUI 虽好用但绑太多东西在固定框架下了，就一个快捷键而言它必须依赖组件本身带有 Control Modifier 的修饰，假设你使用了 Image 组件，给 Image 添加了 OnTapGesture 事件，但因为 Image 本身并不具备 Control Modifier 的实现，通过 `.keyboardShortcut()` 无法响应快捷键。

不过仔细想想也是，对于 Image 来说我们给它添加上的 OnTapGesture 只是额外的手势修饰符，其本身并不具备响应快捷键能力。


## 善用 Spacer() 
当你想完成类似以下布局时，但没有很好的办法按照 Apple 官方交互文档做间距时，切记你正在使用的是 SwiftUI，Apple 有史以来最智能的 UI 框架，仅需在关键的位置放上 `Spacer()` 标签，即可自动完成最佳间距控制和布局。

![](../images/app/photop/1.1/0.png)


## 修改光标样式
如果你想要在某些时刻修改光标样式，Apple 提供了一份完整的在不同系统下支持的光标样式[集合文档](https://developer.apple.com/documentation/appkit/nscursor)，非常完善。

如果我们想要在 SwiftUI 中修改光标样式，可以在 `onHover` 方法中这么做：

```swift
.onHover { isInside in
    if isInside {
        NSCursor.resizeLeftRight.push()
    } else {
        NSCursor.pop()
    }
}
```

## 右键菜单
本来打算抱着在 Qt 中写 QML 的那套古老思想，想着自行监听用户按下鼠标右键后自行弹出对应的自定义菜单，最后才发现仅需一个 `.contextMenu` modifier 即可完成，太爽了。

## Menu
周日正常是一个浏览信息的日子，从各种信息中翻到了一个台湾的小姐姐讲 SwiftUI，看了开头两集发现小姐姐在介绍如何使用 Xcode 自带的 Snippets 帮助学习 SwiftUI 组件和布局方式，我也跟着点开看了看，之前完全忽略了这个入口。

就这么一看，发现了好几个通过 SwiftUI 提供的组件大大降低了原先通过 AppKit 那冗长的调用逻辑，更惊喜的是发现了 `Menu` 这个组件，原来自己寻找许久的菜单样式在这里！！！经过一番改造后，剔除了原先通过 `.popup` 方式唤出的菜单给改造好了，最终变得更符合 macOS 平台的 UI 规范，但这个向下的箭头一直无法去除，最后用了一个非常骚的操作规避掉了

```swift
Menu()
    .opacity(0.09)
```

我也不想写这种逻辑，但就是没有办法了 =。=

