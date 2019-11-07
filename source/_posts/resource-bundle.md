---
title: 由修改资源引用方式产生的思考
date: 2019-09-16 22:41:39
tags:
- iOS
---

## 前言
前段时间 mentor 交给了我一个活，要跟主端对齐一个改进需求，把原先 pod 库里资源的引用方式由打入主工程 `mainBundle` 的方式改为我们自己维护。

之前我没做过这个事情，各方调研了一波后发现这个事情并不复杂，甚至还有些简单。但直到昨天（中秋前）居然还能分配到因为这个事情所导致的 crash，遂决定从头到尾梳理一遍。

我相信到今天，在上一波移动浪潮存活下来且存活得还算不错的互联网公司，手上所负责的产品都势必经历过 app 减包大小的事情。从之前的个人角度出发，做过一些个人开发作品，在这些作品中，可以说只关注到了功能层面，在保证了功能层面上的流畅后，才能有机会去关注到代码层面上的优化，最后才去考虑到与 app 相关的各种配套工具，如日志系统、崩溃统计、性能报告和 A/B 测试等。

我在前几天看的内部分享中，也确实验证了上述所说的流程，换句话说就是「过早的优化是魔鬼」。曾经甚至出现了我导入了一张大小为 4.6M 的资源图片到个人作品中，当初觉得这并没有什么奇怪的地方。时至今日，我慢慢的理解了其实这些优化的事情，有一部分是技术需求，但很大一部分是大家对产品的追求，都在力争用最少的精力完成最多的事情，用「最小」的 app 承载更多的业务。

主端缩减包大小这个事情据我所知已经开展了很长的一段时间。之前实习时，我因极力推崇 Swift，直接把原本只为 7m 的 app 涨为了 15.7m 的大小，当时还是 Swift 3.x +，每个使用 Swift 进行开发的 app 免不了会带上 `Swift runtime`，在我离开之前，Swift 化已达 70%。

原先的 pod 库里资源引用方式为：

```swift
s.resources = [
    'yourPod/Assets/YourAssets.xcassets',
]
```

现在要改成：

```swift      
s.resource_bundle = {
  'yourBundle' => [
    'yourPod/Assets/YourAssets.xcassets',
  ]
}
```

看上去确实挺简单的，加上修改关于各种图片资源引用方式，预估一个下午不到就可以完事。那么我们先来看看这么做的原因是什么？

## Apple 对资源做的优化
可以很明白的跟大家说，做这件事情是有依赖关系的。我从 iOS8 起开始接触 iOS 开发，在 iOS7 时已经推出基于 Asset Catalog 去管理 app 所使用的各种图片资源。在此之前，**据说**都是把所有图片丢到一个文件夹中，Apple 在推出 Asset Catalog 后，附带了一个从 app store 方面做的优化，如果我们在 app 中使用了 Asset Catalog 进行图片资源的管理，这些图片的资源可能有一、二和三倍图等等，不同的用户使用不同设备去下载 app 时，在 app store 这一侧可以根据此次下载的设备标识符，只给设备下发包含此种类型的图片资源，不会与早期开发 iOS app 那般直接把所有资源都下载了。

也就是说，如果拿 iPhone7 去下载一个 app，整个 app 里只包含了二倍图，其它的一倍图和三倍图都不在 app 里，并且此时在 app 包里的图片资源也是会被 Apple 所优化过的，在大小上会比原先整体上小一些。但会有一些特殊情况，如果想图片不被压缩且全设备都使用同一个图片资源，例如 Lottie 动画，如果就想在各种尺寸设备上保持一个清晰度的动画，那么只需要三倍图即可。

以上所说只是在图片资源这一层面上的优化，但实际上在 app store 根据用户设备下载 app 时所「抛弃」的文件种类和个数会更多一些。上述所说，app 里的资源必须采用 Asset Catalog 进行管理才能使用 App Thingning 方法所带来的包大小优化。


## CocoaPods 提供的资源管理方式
CocoaPods 在是一个构建工具，类似 android 中的 Gradle，Java 中的 Maven 等工具，其通过 Podfile 来编写规则，是一个**声明式构建工具**。在一个 Xcode 工程引入 Podfile 后，会生成对应构建的 Xcode Target，上文我们已经说明，目前 CocoaPods 有 `resources` 和 `resource_bundle` 两种方式对资源进行声明并引入，这两种资源引用方式的使用规则大家可以自行去 CocoaPods 官网查阅教程。

在之前的一段时间里，在 OC 工程中引入 Swift 后，Podfile 中会被「引导」加入 `use_framework!` ，最终生成的 Xcode 工程会据此来进行调整。

## 普通资源
### 关闭 `use_framework!`
这是 Podfile 的默认选项。当关闭/不使用 `use_framework!` 时，CocoaPods 会对主工程的 App Target 增加脚本来拷贝 Pods 中的资源，这些 Pod 库最终会被合并成一个单独的静态链接库的 Target。这种情况下，我们来看之前所描述的两种资源引用方式的差别。

使用 `resources` 字段。

```swift
s.resources = [
    'yourPod/Assets/YourAssets.xcassets',
]
```

该资源对应的参数是一个数组，在这个数组中我们可以写入想要被引入工程的所有资源的路径，且支持使用通配符进行描述。当我们在主工程目录下执行 `pod install` 时，CocoaPods 会在主工程对应的 App Target 中的 `Build Phases` 插入资源拷贝脚本。

![插入脚本](https://i.loli.net/2019/09/16/F4pblZ219hacite.png)

build 完成后，我们可以在模拟器上拿到该 ipa 包，解压后可以看到我们通过 `resources` 字段引入的各种资源都直接合并到了该 ipa 包的展开根路径中。

这么做有什么好处呢？简单快速，如果最开始我们是直接把所有资源放在一个文件夹下，然后再把这个文件夹放到主工程下，那这个文件夹是被 Xcode 默认加载到主工程的 main bundle 里的。所以，之前在代码中所使用的资源应用方式不需要任何改动，直接 build 过。

这么做有什么缺点？相信你也能看出来，因为是把所有的资源都直接打入 main bundle 中，所以无法避免资源重名问题，当出现两个资源重名时，将会被被系统随机选择一个进行展示，**注意，是所有资源。**Apple 其实在位于其主工程内的 PNG 图片资源会做一个压缩优化，但通过 CocoaPods 的这种合并方式，走的是自己的脚本合并，本质上与直接把文件放入 main bundle 中没有区别，无法触发 Xcode 的压缩优化。

使用 `resource_bundle` 字段

```swift      
s.resource_bundle = {
  'yourBundle' => [
    'yourPod/Assets/YourAssets.xcassets',
  ]
}
```

可以看的出来 `resource_bundle` 使用的是 k-v 进行管理，也就是说，我们可以在一个 Pod 库里使用多个 Bundle 对多个不同的资源进行分开管理。一般的配置规则是 `BundleName => [各种资源集合的数组]`，同样可以使用通配符进行配置。

通过这种做法，在 Podfile 完成配置修改后执行 `pod install` 后，会对这些通过 `resource_bundle` 声明的资源以 Key（bundleName）创建一个单独的 Bundle Target，然后把被索引的资源都打入其中，接着再通过 CocoaPods 的脚本拷贝到 main bundle 中。例如按照上述代码的设置`YourAssets.xcassets` 将会在 `yourBundle` 父文件夹中被找到。

这么做有什么好处？通过把资源打入不同的 bundle，直接解决掉了资源重名的问题（如果 bundleName 自己无聊到抄其它库也没办法），并且利用上了 Xcode 的压缩优化，因为是单独建立的 Target，使用 Xcode 原生的 Copy Bundle Resources 过程。

这么做有什么缺点？**必须要改动代码**。因为原先的资源现在的父目录从 main bundle 变为了各自维护的 bundle，不能再通过 main bundle 去获取资源。

我们想要去取一个资源或者图片，需要修改为下列形式：

```swift
let bundlePath = Bundle(for: YourClass.self).bundlePath + "/yourBundle.bundle"
let bundle = Bundle(path: bundlePath)

// 加载资源
let plistPath = bundle?.path(forResource: "yourPlist", ofType: "plist")
let image = UIImage(named: "yourImage", in: bundle, compatibleWith: nil)
```

但是这又会引入另外一个问题，如果我们的某些资源，如果 Lottie 动画要求高清，就是不能被压缩。这种情况可以给这个 Lottie 资源动画再封一个 bundle，在使用到的地方再多加上一层路径。

### 打开 `use_framework!`
在 Podfile 中打开/写入 `use_framework!` 后，我们的每个 Pod 库都单独建立了一个动态链接库 Target，每个库都会直接以 Framework 进行集成。因为 Framework 自身处理资源，其下的所有资源都会被拷贝到 Framework 文件夹中。

使用 `resources` 字段。打开 `use_framework!` 后，因为 Framework 可以承载资源，也就不存在资源重名的问题，但需要对原先的代码进行更改，因为资源不会再被合并到 main bundle 中。

```swift
let bundle = Bundle(for: YourClass.self)
let plistPath = bundle?.path(forResource: "yourPlist", ofType: "plist")
let image = UIImage(named: "yourImage", in: bundle, compatibleWith: nil)
```

使用 `resource_bundle` 字段。目录上多了一个 Framework 层的同时也多了一个 bundle 层，这点需要注意。

## Asset Catalog 
如果之前尤其解压过 .ipa 包，会发现根本没有 `.xcasset` 文件夹存在，取而代之的是 `Assets.car` 二进制文件，Xcode 在编译时产生。在工程中想要读取其中的图片资源，只能通过 UIKit 提供的方法，也即 `imageName:`。github 上有一些解开该文件的工具，但基本上 star 数高的我都用过了，都是残废品。

CocoadPods 并不会帮助我们创建 Asset Catalog，需要手动创建。

![创建 Asset Catalog](https://i.loli.net/2019/09/16/ReJocgsmHkT8B7Z.png)


使用 Asset Catalog 来管理资源，CocoaPods 两种资源引用方式又会出现什么不同呢？

### 关闭 `use_framework!`
使用 `resources` 字段。不同于之前普通资源的强行拷贝方式，Pod 库里此时的编译产物 `Assets.car` 无法直接到 main bundle 里了，因为这么做会覆盖掉主工程的 `Assets.car`。因此，Pod 会先把自身的 Asset Catalog 合并到主工程的 Asset Catalog 里。

这么做的优点？与之前所示的优点一致，因为是直接合并到主工程，所以也会出现重名问题，当出现重名问题后，普通资源出现重名问题是被替换掉，但 Asset Catalog 出现重名问题再使用时就会随机指定一个进行使用。想要避免这个问题，还得针对性的对 Asset Catalog 里的每个资源做前缀。

使用 `resource_bundles` 字段。如果我们的 Pod 库此时有多个资源 bundle，最终在编译时会把位于同一个 bundle 下的 Asset Catalog 进行合并。使用方法于指定 bundle 加载资源逻辑类似。


### 开启 `use_framework!`
使用 `resources` 字段。各个 Pod 库编译后的产物只会合并到 framework 这一层，使用方法与前文所描述的类似。使用 `resource_bundle`。在生成 bundle 的同时，编译后的产物也会合并到 framework 这一层。

## 后记
CocoaPods 对普通资源和 Asset Catalog 都支持两种不同的资源引用管理方式，当普通资源出现重名情况会被直接替换，但 Asset Catalog 会进行合并。**故 Pod 库自行管理资源时，应该使用 `resource_bundle`，以避免命名冲突，以使用 [App Thingning](https://help.apple.com/xcode/mac/current/#/devbbdc5ce4f)** ，且注意资源引用方式的方法修正。


