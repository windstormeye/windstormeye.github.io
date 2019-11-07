---
title: 【翻译】iOS 视图的编程指导（一）
date: 2019-05-27 18:56:26
tags:
---

> 本翻译不是意译也不是直译，因为意译杂糅太多个人理解有时会曲解原文，直译太硬，英文思路直译成中文相当怪异。为保证原意，尽可能的直译下进行意译。

[原文地址](https://developer.apple.com/library/content/documentation/WindowsViews/Conceptual/ViewPG_iPhoneOS/Introduction/Introduction.html)

# iOS中的视图编程指导

在iOS中，我们会使用多个 `window` 和多个 `View` 在屏幕上展示你的应用程序内容。`Window` 本身不会包涵任何的可见内容，但提供了一个基础容器给我们应用程序中的 `view` 使用。`View` 定义了一部分你想要填入 `window` 中的内容。举个例子，你可以有用于显示图片、文本、形状或者以上内容的组合 `view`，甚至你还可以使用 `view` 去组织和管理其它 `view`。

## 概览

每一个应用程序至少拥有一个 `window` 和 `view` 去展示它的内容。`UIKit` 框架和其它系统框架预先定义了一些 `view` 供你去展示你的内容。这些 `view` 涵盖了简单的 `button` 和文本 `lable` 甚至是复杂的 `view`，比如 `table view`、`picker view` 和 `scroll view`。在这些预先定义好的 `view` 中如果没有提供你想要的 `view`，你可以自定义 `view` 并自己管理绘制和事件处理。

### `view` 管理你的应用程序可视内容

一个 `view` 是 `UIView` 类（或者它的一个子类）的实例并管理了一个应用程序 `window` 中的矩形区域。`view` 能够进行内容的绘制，处理多点触控事件和管理该 `views` 中子视图的约束。在一个矩形 `view` 区域中绘图会涉及到使用图像技术，比如 `Core Graphics`、`OpenGL ES` 或者 `UIKit` 去绘制形状、图片和文本。`view` 能够直接响应手势识别或触摸事件。在 `view` 的视图层级中，父视图负责其子视图的位置和大小，且还能动态的完成。父视图的这个动态修改的能力能够让你的 `view` 去适应条件的改变，比如说界面旋转和动画。

你可以认为 `view` 是构建你的用户界面中的一个砖块。你会经常的使用一系列的 `view` 去构建一个等级视图去展示内容，而不是只使用一个 `view`。每一个在等级视图中的 `view` 都表现了用户界面中的一部分，并且通常是用于优化一个具体的内容类型，例如，`UIKit` 有很多个用于优化图像、文本和其它类型内容的 `view`。

> 相关章节：[View and Window Architecture](https://developer.apple.com/library/archive/documentation/WindowsViews/Conceptual/ViewPG_iPhoneOS/WindowsandViews/WindowsandViews.html#//apple_ref/doc/uid/TP40009503-CH2-SW1)，[Views](https://developer.apple.com/library/archive/documentation/WindowsViews/Conceptual/ViewPG_iPhoneOS/CreatingViews/CreatingViews.html#//apple_ref/doc/uid/TP40009503-CH5-SW1)


### 配合 `window` 显示你的 `view`
`window` 是 `UIWindow` 类的实例且能够处理全部呈现在应用程序用户界面上的内容。`window` 使用 `view`（及其视图控制器）来管理视图层级的交互和改变。在大部分的时候，你的应用程序 `window` 并不会发生改变。`window` 创建之后，它不会发生改变，只有通过它显示` view` 才会发生改变。每一个应用程序都至少拥有一个 `window` 在设备的主屏幕上去显示这个应用程序的用户界面。如果有外部显示设备连接到了这个设备，应用程序能够很好的在这个外部显示设备上创建第二个 `window` 去呈现内容。

> 相关章节：[Windows](https://developer.apple.com/library/archive/documentation/WindowsViews/Conceptual/ViewPG_iPhoneOS/CreatingWindows/CreatingWindows.html#//apple_ref/doc/uid/TP40009503-CH4-SW1)

### 动画提供了用户可见界面改变的反馈
动画提供了关于用户可见视图层级改变的反馈。系统定义了呈现模态视图（或单一视图）和位于不同组合视图之间的标准过渡动画。但是，`view` 的许多属性可以进行动画。例如，可以通过动画改变 `view` 的透明度，在屏幕中的位置，大小，背景颜色或者其它的属性。如果你直接使用底层的 `Core Animation` 层对象，你能够作出很多不错的动画。

> 相关章节：[Animations](https://developer.apple.com/library/archive/documentation/WindowsViews/Conceptual/ViewPG_iPhoneOS/AnimatingViews/AnimatingViews.html#//apple_ref/doc/uid/TP40009503-CH6-SW1)

### `Interface Builder` 扮演的角色

`Interface Builder` 是一个图形构造和配置你的应用程序 `window` 和 `view` 的工具。使用`Interface Builder` 能够把 `view` 集中在 `nib` 文件中进行处理，`nib` 是一个存储了你可以自由操控版本的 `view` 或其它对象资源的文件，当你在 `runtime` 中加载一个 `nib` 文件时，你可以使用你的代码去操纵这些位于真实对象中的 `view`。

当你不得不去进行创建应用程序界面的工作时，使用 `Interface Builder` 会变得非常简单 。因为在 iOS 中已经整合进了对 `Interface Builder` 和 `nib` 的支持，只需要一点时间就可以把你应用程序的设计工作合并到 `nib` 中。

关于如何使用 `Interface Builder` 的其它信息，可查看 [Interface Builder User Guide](https://developer.apple.com/library/archive/documentation/DeveloperTools/Conceptual/IB_UserGuide/Introduction/Introduction.html#//apple_ref/doc/uid/TP40005344)。关于如何使用 `view controller` 管理包涵这些 `view` 的 `nib` 文件，可查看 [View Controller Programming Guide for iOS](https://developer.apple.com/library/content/featuredarticles/ViewControllerPGforiPhoneOS/index.html#//apple_ref/doc/uid/TP40007457) 中的创建自定义视图控制器部分。

#### 查看更多
因为视图是非常复杂和灵活的对象，在一个文档中完全讲解是很困难的。但是，下面的这些文档能够很好的帮助你去学习关于如何管理视图交互和用户界面的内容。
* 视图控制器是管理应用中的视图很重要的一部分。视图控制器控制着在其单一视图层级之中的所有视图，并协助这些视图在屏幕上的显示。查看 [View Controller Programming Guide for iOS](https://developer.apple.com/library/archive/featuredarticles/ViewControllerPGforiPhoneOS/index.html#//apple_ref/doc/uid/TP40007457) 来获得更多关于视图控制器的内容以及它运行规则的信息。
* 视图是应用的手势和触摸事件的关键接收者。查看 [Event Handling Guide for iOS]() 来获得更多关于如何使用手势识别器和处理触摸事件。
* 自定义视图必须要使用可信赖的绘制技术去渲染其内容。查看 [Drawing and Printing Guide for iOS](https://developer.apple.com/library/archive/documentation/2DDrawing/Conceptual/DrawingPrintingiOS/Introduction/Introduction.html#//apple_ref/doc/uid/TP40010156) 来获得更多关于使用这些技术去绘制你的视图内容。
* 在一些标准视图动画无法满足的部分，你可以使用核心动画库 `Core Animation`。查看 [Core Animation Programming Guide](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/CoreAnimation_guide/Introduction/Introduction.html#//apple_ref/doc/uid/TP40004514) 来获得更多关于使用核心动画库 `Core Animation` 实现动画的内容。

### `view` 和 `window` 的结构
`view` 和 `window` 展示应用程序用户界面和处理界面上的交互。`UIKit` 和其它系统框架提供了一些只需要做一点修改或完全不修改就可以使用的 `view`。你还可以自定义视图去展示标准视图不允许的位置内容。

### 视图结构的基础知识
我们想要通过可视化完成的事情大多都是基于 `view` 对象的，也就是 `UIView` 类的实例。`view` 对象在屏幕上定义了一个矩形区域，该区域能够绘制并和响应触摸事件。`view` 能够作为其它 `view` 的父容器，管理它们的位置和大小。`UIView` 类本身管理了这些工作的大部分，但我们也可以根据需要自定义视图之间的默认行为。

`view` 与 `Core Animation` 层共同处理内容的渲染和动画。每一个 `view` 都拥有一个 `layer` 对象（通常是 `CALayer` 的实例），它负责 `view` 的渲染内容和与 `view` 相关的动画。我们大多数情况下的操作应该通过 `UIView` 提供的接口进行，但在某些需要对渲染或动画行为进行更多的控制时，我们可以替换为对 `layer` 进行操作。

为了便于我们理解 `view` 和 `layer` 的关系，下面这个例子可以提供帮助。图 1-1 展示了来自于 [ViewTransitions](https://developer.apple.com/library/archive/samplecode/ViewTransitions/Introduction/Intro.html#//apple_ref/doc/uid/DTS40007411) 这个简单应用的视图结构和它与底层 `Core Animation` 层的关系。这个应用程序的视图包括一个 `window`（本质上是个 `UIView`），它是一个继承于 `UIView` 类且作为 `view` 容器的对象，一个图像 `view`，一个用于显示按钮的 `toolbar` 以及一个 `bar button item`（它不是 `view`，但其内部有一个可共使用的 `view`）。（实际上 [ViewTransitions](https://developer.apple.com/library/archive/samplecode/ViewTransitions/Introduction/Intro.html#//apple_ref/doc/uid/DTS40007411) 这个简单应用还包括了一个用于实现变换的图像 `view`，但为了保证简单，在图 1-1 中并没有描述出来）。每个 `view` 都有与之匹配的 `layer` 对象，可以通过 `view` 的 `layer` 属性来访问它。（因为 `bar buttom item` 不是 `view`，所以你不能直接访问它的 `layer`）`layer` 层对象的背后是 `Core Animation` 渲染对象，并且最终用于管理硬件缓冲区中显示在屏幕上的实际字节。

![图 1-1 简单应用中的视图结构](https://developer.apple.com/library/archive/documentation/WindowsViews/Conceptual/ViewPG_iPhoneOS/Art/view-layer-store.jpg)

使用 `Core Animation` `layer` 对象对性能提升有很大的帮助。要尽可能的少调用视图对象的绘制部分代码，当这部分代码被调用时，其结果会被 `Core Animation` 进行缓存，并在未来进行多次重用。在需要更新视图时重用渲染出内容的会消耗大量的绘制周期。在动画中重用这部分缓存的内容是非常重要的，因为这些内容是可被操控的。使用这些缓存的内容会比创建新内容成本小很多。

### `view` 的视图层级以及管理子视图
除了提供自身显示的内容，`view` 还可以作为其它 `view` 的容器。当一个 `view` 包含了另外一个 `view`，父子关系就在其之中建立了。在这个父子关系中，子视图通常被称为 `subView` 父视图被称为 `superView`。这种关系类型的创建对应用程序的可视化内容和行为都造成了影响。

看上去子视图中的内容会遮挡其父视图的部分或全部内容，当子视图是非透明时，则其所占据的区域将会完全遮挡父视图。如果子视图是部分透明的，则父子视图中的内容会先进行融合再显示于屏幕上。每个 `superView` 都一个存储 `subView` 的数组，数组中元素的位置会影响每个 `subview` 的可见性。 当同为一个 `superView` 的两个 `subView` 互相重叠在了一起，最后添加进 `superView` 中的（或移动到 `subView` 数组最后的） `subView` 将会显示在在上面。

`superView` 与 `subView` 的关系还影响到了一系列的视图行为。改变一个父视图的大小时会波及到其子视图的大小和位置。当改变父视图的大小时，我们可以适当的通过一些配置方法来重新设置每个子视图大小。例如隐藏父视图，修改父视图的透明度或者对父视图的坐标系统做数学变换（3D）等这些事件同样会影响子视图。

对视图层级的排布还意味着应用程序如何响应各种事件。当一个特殊的视图发生了触摸，系统立即将这个触摸信息发送给这个视图进行处理。但是如果该视图没有对这个事件进行单独处理，则系统将会把该事件对象传递给父视图。如果父视图同样没有处理这个事件，系统将会把该事件继续传递给父视图，在整个响应链上以此类推。

更多关于如何创建视图层级的内容，可查看 [Creating and Managing a View Hierarchy](https://developer.apple.com/library/archive/documentation/WindowsViews/Conceptual/ViewPG_iPhoneOS/CreatingViews/CreatingViews.html#//apple_ref/doc/uid/TP40009503-CH5-SW47)。

## 视图绘制周期
`UIView` 类使用了“按需变化”的绘制模型去展示内容。当视图第一次呈现在屏幕上时，系统要求其进行内容绘制。系统对渲染内容进行快照捕获并且使用该快照作为该视图的视觉呈现。如果你从未对视图内容进行修改，执行视图内容绘制的代码将不会再执行。对视图进行的大多数操作会重复使用快照图片替代。如果你对内容进行了修改，需要通知系统视图已经修改。视图将会重复进行绘制视图内容的过程，并捕获新的图像内容为快照。

当你的视图内容修改时，你不必立即重绘这些修改的内容。相反，你可以使用 `setNeedsDisplay` 或 `setNeedsDisplayInRect` 方法使视图内容失效。这些方法将会告诉系统视图的内容已经修改，并且需要在下个时机中进行重绘。系统将会等待到当前 `runloop` 结束后才进行初始化任何的绘图操作。这个延迟给你一个机会去使多个视图内容失效，从视图层级中添加或者移除视图，隐藏视图，调整视图大小以及调整视图位置。你对视图进行所有修改都会在同一时间进行调整。

> 注意：修改视图的几何形状并不会自动触发系统对视图内容的重绘。视图的 `contentMode` 属性决定了如何解释视图的几何形状修改。大多数 `contentMode` 在延伸和重定位已经存在快照的边界，而不是创建一个新的快照。获取更多 `contentMode` 是怎么影响你的视图绘制周期的，可以查看 [Content Modes](https://developer.apple.com/library/archive/documentation/WindowsViews/Conceptual/ViewPG_iPhoneOS/WindowsandViews/WindowsandViews.html#//apple_ref/doc/uid/TP40009503-CH2-SW2)。

当渲染视图内容时，实际的绘制过程的变化会依赖于视图及其配置。系统视图一般通过实现私有绘图方法来完成视图内容的渲染。这些相同的系统视图经常会暴露出接口供我们配置视图的实际外观。自定义 `UIView` 类型的子类，通常你要针对你的视图去重载 `drawRect:` 方法去绘制你视图的内容。这还有一些其它方法提供完成内容的绘制，例如直接设置底层的内容，但是重载 `drawRect` 方法是目前最常用的方法。 

获取更多关于如何绘制自定义视图的内容，可见 [ Implementing Your Drawing Code](https://developer.apple.com/library/archive/documentation/WindowsViews/Conceptual/ViewPG_iPhoneOS/CreatingViews/CreatingViews.html#//apple_ref/doc/uid/TP40009503-CH5-SW3)

### 内容模式（`content modes`）
每个视图都有一个内容模式，其控制了如何根据视图的几何尺寸发生变化时回收视图内容，以及是否回收视图内容。当视图第一次显示时，按照流程绘制其内容并捕获其内容于底层位图中。接下来改变视图几何尺寸并不会导致位图的重新创建。反而，`contentMode` 属性目的在于位图是否缩放以进行适配新的界限，还是仅简单的贴在一个视图的角或者边上。

视图的内容模式在你做以下操作时生效：
* 改变视图的 `frame` 或 `bounds` 矩形区域的宽或高。
* 赋值带有缩放功能的 transform 变换给视图的 `transform` 属性。

默认情况下大多数视图的 `contentMode` 属性是 `UIViewContentModeScaleToFill`，它能够让视图内容缩放适配至新的 frame 大小。图 1-2 展示了一些可用的内容模式结果。从图中可以看到，不是所有的内容模式都会完全充满视图界限，并且有一些还会导致视图内容的失真。

![Figure 1-2  Content mode comparisons](https://developer.apple.com/library/archive/documentation/WindowsViews/Conceptual/ViewPG_iPhoneOS/Art/scale_aspect.jpg)

内容模式对于视图回收非常适合，但如果你特别想在缩放或者重设尺寸操作时自定义视图重绘它，还可以使用 `UIViewContentModeRedraw` 该内容模式。给视图模式设置为该值能够当几何尺寸改变时强制让系统调用 `drawRect:` 方法。一般情况下，应该尽可能的避免在任何时候使用该值，除非你非常确定你不会使用标志系统视图。

查看更多关于可用的内容模型内容，可看 [UIView Class Reference](https://developer.apple.com/documentation/uikit/uiview)。

### 可伸缩的视图
你可以指定视图的一部分作为可伸缩区域，以至于当视图改变其大小时只修改了可伸缩区域。通常会在按钮或者其它视图中使用可伸缩区域，其中视图的部分区域定义了一个可重复模式。视图中指定的可伸缩区域允许在单独一个轴或者两个轴上进行伸缩。需要注意的是，当对两个轴进行伸缩，对视图的边来说还要定义一个重复模式避免任何变形。图 1-3 清晰的展示了失真是怎么在视图中展示出来的。来自原图中每一个像素点的颜色重复的通过一致的排列充满了大图。

![Figure 1-3  Stretching the background of a button](https://developer.apple.com/library/archive/documentation/WindowsViews/Conceptual/ViewPG_iPhoneOS/Art/button_scale.jpg)

使用 `contentStretch` 属性指定视图的可伸缩区域。这个属性接受一个矩形区域，该值是 0.0 到 1.0 范围内的标准值。当伸缩视图时，系统将会对视图当前的 bounds 值和缩放值与该标准值进行乘积，以达到确定对视图一个像素或多个像素的伸缩。使用标准值能够降低当视图界限改变时更新 `contentStretch` 属性值的次数。

视图的内容模式还扮演了如何使用视图的伸缩区域决定者的角色。当内容模式导致内容区域的缩放时才会使用可伸缩的区域。这意味着可伸缩视图只支持 `UIViewContentModeScaleToFill`、`UIViewContentModeScaleAspectFit` 和 `UIViewContentModeScaleAspectFill` 内容模式。如果你指定了内容模式对内容进行了贴边或贴角（因此实际上导致内容并不能缩放），该视图将会忽略可伸缩区域。

> 注意：指定背景视图时，建议创建可伸缩的 `UIImage` 对象时使用 `contentStretch` 属性。可伸缩视图可以在 Core Animation Layer 中完全处理，其通常提供更好的性能。

### 内置动画支持
每一个视图后都有一个层对象的好处之一是你可以对与视图相关的更改进行动画化。动画是向用户传递信息交流的有效方法，在设计应用程时应该一直思考这个问题。许多 `UIView` 的属性都是可动画化的，也就是说支持半自动的从一个值到另外一个值。提高这些其中一个可动画化属性的性能，我们只需要做：

1. 告诉 UIKit 你想要一个高性能动画。
2. 改变属性值。

你可以对 `UIView` 对象中执行动画的属性如下：

* `frame` -- 使用这个属性能够对视图位置和大小的改变进行动画变化。
* `bounds` -- 使用这个属性能对视图大小的改变进行动画变化。
* `center` -- 使用这个属性能对视图位置的改变进行动画变化。
* `transform` -- 使用这个属性能够对视图选择和缩放。
* `alpha` -- 使用这个属性能够修改视图进行透明度的。
* `backgroundColor` -- 使用这个属性能够修改视图的背景颜色。
* `contentStrech` -- 使用这个属性能够修改视图的中心延伸。

从一组视图变换到另外一组视图是动画非常重要的一点。通常情况下会使用视图控制器通过动画去管理用户界面各部分中主要修改的部分。举个例子，展示从高级别到低级别视图的过渡信息，通常情况下会使用导航控制器管理每一个成功显示的视图数据。甚至你还可以创建两个视图集合之间的动画过渡来替代视图控制器。在使用标准控制器动画达不到你想要的结果时，可以通过这个方法做到。

除了使用 UIKit 进行动画的创建外，还可以使用 Core Animation layer 完成。下降到图层级别能够对动画的时间和属性进行更多的控制。

查看更多关于如果提升基于视图的动画性能可看 [Animations](https://developer.apple.com/library/archive/documentation/WindowsViews/Conceptual/ViewPG_iPhoneOS/AnimatingViews/AnimatingViews.html#//apple_ref/doc/uid/TP40009503-CH6-SW1)。查看更多关于如何使用 Core Animation 创建动画可看[Core Animation Programming Guide](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/CoreAnimation_guide/Introduction/Introduction.html#//apple_ref/doc/uid/TP40004514) 和 [Core Animation Cookbook.](https://developer.apple.com/library/archive/documentation/GraphicsImaging/Conceptual/CoreAnimation_Cookbook/Introduction/Introduction.html#//apple_ref/doc/uid/TP40005406)。
