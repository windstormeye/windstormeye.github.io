---
title: 如何为你的 iOS App/游戏快速适配主机手柄？
date: 2019-11-30 22:49:41
tags:
- Swift
- 游戏开发
---

![](https://i.loli.net/2019/12/01/rfnc9byUWjSxLNs.png)

> iOS 13 支持主机手柄连接了！！！需要注意的是，并不是手柄去支持 iOS 13，而是 Apple 终于允许自家平台「发现」手柄了......

## 前言
在 WWDC19 上，apple 正式对外宣称 iOS，macOS，tvOS 三大平台正式支持接入遵守 **MFi** 协议的手柄进行操作，接入方式为「蓝牙」。

因此，我们可以推测出今后在 Apple 生态圈中游戏发布在以上三个平台时都会一定去考虑对手柄的支持。仔细观察目前在 Apple 生态圈中的游戏，尤其是 iOS 上的游戏，或者说是移动平台上的游戏，几乎都逃不掉左边一个虚拟滚轮，右边三四个虚拟按键。

可以说，这些虚拟操作都是在模拟最初手柄对用户已经养成的习惯，这些习惯既然是从实体手柄时代遗传下来的，并且在 iOS 13 之前 Apple 并不允许接入其他手柄，那现在已经允许接入的前提下，我们为何不顺势而为呢？

还有一种说法，部分游戏会故意通过虚拟按键位置的排布来消减玩家的游戏体验，以降低玩家完成某个要求的速度和质量，这就是 QWERTY 的现代玩法。

## 选择合适的手柄
我已经有了 Switch，想当然的再入一个 NS Pro Controller，但幸亏事先做了调查，发现 NS Pro Controller 和 joy-Controller 均不支持连接，个人猜测老任并没有为其手柄申请 MFi 认证。

因此，只能回落到 PS4 还是 Xbox 的手柄选择上。在最终下单前，也做一番调查，发现大家基本上一窝蜂的倒向 Xbox 手柄手感比 PS4 强太多，本来我也打算确实是选择 Xbox，后来发现 Apple 官网上的广告宣传是 PS4，而且 B 站上众多 up 主也都基于 PS4 进行测评，想想最终还是选择了 PS4 手柄。

到现在总共玩了大概三个小时不到，发现手柄和设备的连接非常稳当，个人认为无延迟，但 PS4 手柄还真出现了网友所说玩久了左手大拇指会疼，因为经常会使用半个大拇指去「搓」滑杆。

但看到 PS4 手柄的颜值也就忍了，如果你也想买一个手柄且不是颜值党，可以考虑选择 Xbox。

## 适配主机手柄
### 手柄的差异
apple 的官方文档中推荐我们的 app/游戏（下文统一使用 app）**一定不能只支持手柄**，其实也就是说，手柄只是一个提升体验的工具，而不是一个必须品，只要 apple 不下死命令，我们能够通过手柄体会到的游戏就会越往后拖。

PS4 和 Xbox 的手柄可以理解为是两种风格，如下图所示：

![](https://i.loli.net/2019/11/30/DFCq1OlPiLx4Sgy.png)

PS4 和 Xbox 手柄的 ABXY 分别使用不同的风格进行标识。但如果你有使用过这两个手柄，一定能够知道大部分的手柄都是基于「位置等量」的，也就是说，PS4 上的 `X` 会被「位置等量」到 Xbox 上的 `A`，二者对于开发者来说都是一样的功能。

这一点同样被 Apple 所保留，但我们在使用时 Apple 并不会给我们识别出当前在 `A` 这个位置上到底是 `X` 还是 `A`，Apple 只有 `A`。

### 键冲突
Apple 会自动协助我们在某个「固定时间」内保留最终的按键状态，而不是反复发送按键回调。

### UI
这部分 Apple 要求得比较多，简单来说，要么全部统一，在 UI 上也做「位置等量」的标识，要不然就得通过连接设备的标识符来针对性的返回不同的 UI 资源。

## 接入
了解了以上主机手柄适配的前置内容，接下来就可以正式进入到手柄适配部分。我在适配的过程中，彻底被 Apple 的简洁所折服了！我以为对主机手柄各种硬件的调用过程会类似于 `Photos` 这种看似不应该那么复杂的却非常复杂的框架一样复杂，但简洁得令人感到惊讶。

对主机手柄接入的所有工作只需要 `GameController` 即可完成，而且该框架与平台无关，也就是说，只要我们封装好一次对外暴露的主机手柄操作管理类，可以完全做到三平台全通吃！

### 第一步：注册通知
第一步，我们得先注册对手柄连接/取消连接的事件通知。

```swift
import GameController

class GameController {
    
    init() {
        NotificationCenter.default.addObserver(self, selector: .didConnect, name: .GCControllerDidConnect, object: nil)
        NotificationCenter.default.addObserver(self, selector: .didConnect, name: .GCControllerDidDisconnect, object: nil)
    }
}
```

### 第二步
在通知的回调方法中完成对事件的筛选和处理。

```swift
extension GameController {
    @objc fileprivate func gameControllerDidConnect() {
        for controller in GCController.controllers() {
            if controller.extendedGamepad != nil {
                setupControllerControls(controller: controller)
            }
        }
    }
    
    @objc fileprivate func gameControllerDidDisconnect() {
        
    }
    
    func setupControllerControls(controller: GCController) {
        controller.extendedGamepad?.valueChangedHandler = {
            (gamepad: GCExtendedGamepad, element: GCControllerElement) in
            self.controllerInput(gamePad: gamepad, element: element)
        }
    }
    
    private func controllerInput(gamePad: GCExtendedGamepad, element: GCControllerElement) {
      
    }
}
```

### 第三步
在 `controllerInput` 中处理手柄的 `valueChangedHandler` 回调事件。`valueChangedHandler` 这个方法需要我们在接收到手柄的连接通知时，传递给手柄控制对象一个回调方法，后续当手柄发生按键事件时，将通过我们传入的回调进行调用。

因此，我们在 `controllerInput` 方法中处理手柄被按下时的各种事件值的改变处理。

```swift
extension GameController {
    @objc fileprivate func gameControllerDidConnect() {
        for controller in GCController.controllers() {
            if controller.extendedGamepad != nil {
                setupControllerControls(controller: controller)
            }
        }
    }
    
    @objc fileprivate func gameControllerDidDisconnect() {
        
    }
    
    func setupControllerControls(controller: GCController) {
        controller.extendedGamepad?.valueChangedHandler = {
            (gamepad: GCExtendedGamepad, element: GCControllerElement) in
            self.controllerInput(gamePad: gamepad, element: element)
        }
    }
    
    private func controllerInput(gamePad: GCExtendedGamepad, element: GCControllerElement) {
        if (gamePad.leftThumbstick == element) {
            if (gamePad.leftThumbstick.yAxis.value != 0 && !movingY && !movingX) {
                movingY = true
                isSelectY?(gamePad.leftThumbstick.yAxis.value > 0)
                return
            } else if (gamePad.leftThumbstick.yAxis.value == 0) {
                movingY = false
            }
            
            if (gamePad.leftThumbstick.xAxis.value != 0 && !movingX && !movingY) {
                isSelectX?(gamePad.leftThumbstick.xAxis.value > 0)
                movingX = true
                return
            } else if (gamePad.leftThumbstick.xAxis.value == 0) {
                movingX = false
            }
        }
        if (gamePad.buttonA == element) {
            if (gamePad.buttonA.value != 0) {
                isTapButtonA?()
            }
        }

        // ...
}
```

`valueChangedHandler` 回调只是当数值发生变化时的回调，我们还需要手动处理例如手柄摇杆上从按住到归位的单次计数，当然，我做这个是为了适配我的游戏，这部分还没来得及完善，如果你想持续的监听到摇杆的持续按住事件，完全可以把数值对外暴露，通过系数倍乘的方式来达到例如对赛车的油门控制等好玩的事情。

对外，可以通过注册的回调进行传递单次按键事件。

```swift
class GameController {
    
    var movingX = false
    var movingY = false
    
    var isSelectX: ((Bool) -> ())?
    var isSelectY: ((Bool) -> ())?
    var isTapButtonA: (() -> ())?

    //...
}

// ...
```



## 总结
我确实没想到对手柄的第一步适配工作居然不到 80 行代码搞定了。手柄是一个玩家的武器，同时也是一个标志，希望大家都能够正视在自己的游戏中支持手柄操作，提供更好的游戏体验。

如果你对我的第一个适配手柄的游戏「能否关个灯」感兴趣，可以在 github 上找到这个项目，如果你想跟我一起通过 Swift 进行游戏开发，可以在小专栏上找到《Swift 游戏开发》进行。

github 地址：[Swift 游戏开发](https://github.com/windstormeye/SwiftGame)

小专栏地址：[Swift 游戏开发](https://xiaozhuanlan.com/pjhubs-swift-game)


## 参考链接

* [https://developer.apple.com/videos/play/wwdc2019/616/](https://developer.apple.com/videos/play/wwdc2019/616/)
* [https://medium.com/@samdubois18/adding-controller-support-to-your-ios-app-a9b8308ce0b4](https://medium.com/@samdubois18/adding-controller-support-to-your-ios-app-a9b8308ce0b4)