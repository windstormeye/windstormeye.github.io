---
title: 如何实现一个手帐 app
date: 2019-08-25 22:30:39
tags:
- iOS 
- Swift
- side project
---

> 前段时间对手帐类 app 的实现细节非常感兴趣，遂萌生了想自己实现一个最小化的可行性产品。当然啦～既然是 MVP 模式下的产品，所以只实现了「功能」，但是在一些自己特别想要去「抄袭」的地方也下了一点功夫去追求 UI 的表现。

## 前言
小时候，我是一个手抄报爱好者，四年级的时候班里组织了一个手抄报比赛，老师要求每位同学利用周末的时间做一份手抄报进行评比，主题自选。到现在我印象还非常深刻的是，我想了一个中午都不知道要选什么主题，在白纸上画了一些东西后又全都擦掉了，弄脏了好几张纸，最后画出了一个地球，思路就慢慢打开了。

到了周一交给老师的时候，我不敢第一个交，我排在了队伍的最后。老师接到我的手抄报后，居然说：“来来来，你们来看看什么叫手抄报”，我当时的心率达到了极高点，脸又红又烫，站在老师身边站也不是走也不是，尴尬的笑着，但内心却极度自豪。

到了初中，班主任也让大家利用周末的时间去做了一个手抄报，因为在小学的时候有了一点经验，再加上到了初中那会儿基本上使用计算机来辅助完成各种任务也都铺开了，我就寻思着能不能再做些创新。当时柯达传出了倒闭的消息，这相当于是一代人的记忆吧～有时候我会跑到老房子里翻到各种胶卷，在阳光的照射下看着映射出的反色图像。

结合这个事件，我就想到了利用「胶卷」风格的来阐述对保护鸟类的主题，从网上下载了一些各种鸟类的图片，自己加工一下，终于把手抄报做好了交给老师。当交给老师的那一刻，老师愉悦的笑了，并拿着我的手抄报在讲台上给同学们展示，“大家看下，做的还不错吧～嗯，挺好看！”。

高考完的那个暑假，《南国都市报》组织了一次中小学生手抄报大赛，当时我用堂弟的身份参加这个大赛，拿了三等奖，奖品是一张创新书店 500 元的购书卡。

以上就是我对手抄报或者说类似于手帐的这种手工画的经历了，我特别喜欢这种讲述一个故事的方式，可以很好的把我想要表达的东西通过一些文字、图片和画的方式展现出来。

所以，当出现了手帐类 app 时，我迅速的下载进行使用，使用过程中确实达到了自己当初通过组织一些元素和文字来讲述一件事的初衷。前段时间突发奇想，如果我能自己做一个手帐，顺便去探究实现一个手帐 app 中需要注意的问题，那该多好啊！

## 设计
首先，我把 App Store 中「手帐」关键词下的搜索排名前 10 的 app 都进行了一番使用，总结出了一些手帐 app 通用点：

* 添加文字。可旋转、放大缩小、旋转字体；
* 添加照片。可旋转翻转、放大缩小、并具备简单或者辅助的图像修饰工具；
* 添加贴纸。使用一些绘制好的贴纸，操作与「添加照片」差不多；
* 模版。提供一套模版，用户可以在这个模版规定好的区域进行内容添加；
* 提供无限长或宽的画布。

基本上这些手帐 app 的共性功能就是这么多了，因为本着 MVP 的思路去做这个项目，所以也就没有做到高保真的设计，直接抄了一个比较简洁的手帐 app 设计。

![体验过的手帐 app 集合（部分）](https://i.loli.net/2019/08/25/3KNSrIBkvH8MTsn.png)


## 技术栈
确定好了自己要实现的大概需要做的功能点后，就需要开始去选择技术栈，因为要做的毕竟是 MVP 产品而不是 demo，我对 demo 的理解是「实现某个功能点」，对 MVP 产品的理解是「某个阶段下的完整可用的产品」，MVP 模式下出来的东西细节出现一些问题不用太过于苛责，但整体的逻辑上一定是要完整的，不完整的逻辑可以没有，但是一旦有了就要是完整的，覆盖的逻辑路径也可以不是 100%，但主逻辑一定要全覆盖。

### 客户端
iOS app 的开发技术点如下：

* 纯原生 Swift 开发；
* 网络请求 => `Alamofire`，一些简单的数据直接走 `NSFileManager` 进行文件持久化管理；
* UI 组件全都基于 `UIKit` 去做；社会化分享走系统分享，不集成其它 SDK；
* 模块上提供「贴纸」、「画笔」、「照片」和「文字」。做的过程中发现其实「照片」和「文字」本质上来说也是贴纸，省了不少事。

![客户端架构](https://i.loli.net/2019/08/25/yzYlOgC8U65JWTE.png)

### 服务端
其实我对自己每新开一个 side project 都有一个硬性要求，做完后要对自己的技术水平有增长，其实「增长」这个东西很玄学，怎么定义「增长」对吧？我给自己找到了一个最简单的思路：用新的东西去完成它！

因此在服务端上我就直接无脑的选择了 `Vapor` 进行，通过 Swift 去写服务端这是我之前一直想做但找不到时机去做的事情，借此机会就上车了。至于为什么不是选 `Perfect`，其实我个人没有去动手实践过，只是听大佬们说 `Vapor` 的 API 风格比较 `Swifty` 一些。

![服务端架构](https://i.loli.net/2019/08/25/7eMWqmfviEyFJno.png)

在第一期的 MVP 中对服务端的依赖不大，所以目前的架构比较简单，达到能用即可就完事了～关于 `Vapor` 的一些使用细节，可以在我的[这篇文章](http://pjhubs.com/2019/05/03/vapor01/)中进行查看，本文将不再细述 `Vapor` 使用细节。

## 实现
### 手势
对于手帐来说，最核心的一个就是**「贴纸」**。如何把贴纸从存储中拉出来放到画布上，这一步解决了，后续大部分内容也都解决了。

首先，我们需要明确一点，在这个项目中，「画布」本身也是个 `UIView`，把「贴纸」添加到画布上，实质上就是把 `UIImageView` 给 `addSubview` 到 `UIView` 上。其次，手帐中追求的是对素材的控制，可旋转放大是基本操作，而且前文也说过了，我们几乎可以把「照片」和「文字」都认为是对「贴纸」的继承，所以这就抽离出了「贴纸」本身是所以可提供交互组件的基类。

手帐类 app 对贴纸进行多手势操作的流畅性是决定用户留存率很大的一个因素。因此，我们再抽离一下手帐「贴纸」，把基础手势操作都移到更高一层的父类中去，贴纸中留下业务逻辑。手势操作核心代码逻辑如下：

```swift
// pinchGesture 缩放手势
// 缩放的方法（文件私有）。  gesture手势 ：UI缩放手势识别器
@objc
fileprivate func pinchImage(gesture: UIPinchGestureRecognizer) {
    //  当前手势 状态   改变中
    if gesture.state == .changed {
        // 当前矩阵2D变换  缩放通过（手势缩放的参数）
        transform = transform.scaledBy(x: gesture.scale, y: gesture.scale)
        // 要复原到1（原尺寸），不要叠加放大
        gesture.scale = 1
    }
}

// rotateGesture 旋转手势
// 旋转的方法（文件私有）。  gesture手势 ：UI旋转手势识别器
@objc
fileprivate func rotateImage(gesture: UIRotationGestureRecognizer) {
    if gesture.state == .changed {
        transform = transform.rotated(by: gesture.rotation)
        // 0为弧度制（要跟角度转换）
        gesture.rotation = 0
    }
}

// panGesture 拖拽/平移手势
// 平移的方法（文件私有）。  gesture手势 ：UI平移手势识别器
@objc
fileprivate func panImage(gesture: UIPanGestureRecognizer) {
    if gesture.state == .changed {
        // 坐标转换至父视图坐标
        let gesturePosition = gesture.translation(in: superview)
        // 用移动距离与原位置坐标计算。 gesturePosition.x 已经带正负了
        center = CGPoint(x: center.x + gesturePosition.x, y: center.y + gesturePosition.y)
        // .zero 为 CGPoint(x: 0, y: 0)的简写， 位置坐标回0
        gesture.setTranslation(.zero, in: superview)
    }
}

// 双击动作（UI点击手势识别器）
@objc
fileprivate func doubleTapGesture(tap: UITapGestureRecognizer) {
    // 状态 双击结束后
    if tap.state == .ended {
        // 翻转 90度
        let ratation = CGFloat(Double.pi / 2.0)
        // 变换   旋转角度 = 之前的旋转角度 + 旋转
        transform = CGAffineTransform(rotationAngle: previousRotation + ratation)
        previousRotation += ratation
    }
}
```

实现的效果下图所示：


![对贴纸增加的手势操作](https://i.loli.net/2019/08/25/z46HEpLlrIqYhNW.gif)


使用 `UICollectionView` 作为贴纸容器，通过闭包把点击事件对应索引映射的 icon 图片实例化为贴纸对象传递给父视图：

```swift
collectionView.cellSelected = { cellIndex in
    let stickerImage = UIImage(named: collectionView.iconTitle + "\(cellIndex)")
    let sticker = UNStickerView()
    sticker.width = 100
    sticker.height = 100
    sticker.imgViewModel = UNStickerView.ImageStickerViewModel(image: stickerImage!)
    self.sticker?(sticker)
}
```

在父视图中通过实现闭包接收贴纸对象，这样就完成了**「贴纸」到「画布」**的全流程。

```swift
stickerComponentView.sticker = {
    $0.viewDelegate = self
    // 父视图居中
    $0.center = self.view.center
    $0.tag = self.stickerTag
    self.stickerTag += 1
    self.view.addSubview($0)
    // 添加到贴纸集合中
    self.stickerViews.append($0)
}
```

### 「照片」和「文字」
手帐编辑页面的底部工具栏之前没做好设计，按道理来说，应该直接上一个 `UITabBar` 即可完事，但最终也使用了 `UICollectionView` 完成。读取设备照片操作比较简单，不需要自定义相册，所以通过系统的 `UIImagePicker` 完成，对自定义相册感兴趣的同学可以看我的[这篇文章](http://pjhubs.com/2018/12/21/PhotosKit开发总结（一）/)。顶部工具栏的代码细节如下所示：

```swift
// 底部的点击事件
collectionView.cellSelected = { cellIndex in
switch cellIndex {
    // 背景
    case 0:
        self.stickerComponentView.isHidden = true
        
        brushView.isHidden = true
        self.bgImageView.image = brushView.drawImage()
        
        self.present(self.colorBottomView, animated: true, completion: nil)
    // 贴纸
    case 1:
        brushView.isHidden = true
        self.bgImageView.image = brushView.drawImage()
        
        self.stickerComponentView.isHidden = false
        UIView.animate(withDuration: 0.25, animations: {
            self.stickerComponentView.bottom = self.bottomCollectionView!.y
        })
    // 文字
    case 2:
        self.stickerComponentView.isHidden = true
        
        brushView.isHidden = true
        self.bgImageView.image = brushView.drawImage()
        
        let vc = UNTextViewController()
        self.present(vc, animated: true, completion: nil)
        vc.complateHandler = { viewModel in
            let stickerLabel = UNStickerView(frame: CGRect(x: 150, y: 150, width: 100, height: 100))
            self.view.addSubview(stickerLabel)
            stickerLabel.textViewModel = viewModel
            self.stickerViews.append(stickerLabel)
        }
    // 照片
    case 3:
        self.stickerComponentView.isHidden = true
        
        brushView.isHidden = true
        self.bgImageView.image = brushView.drawImage()
        
        self.imagePicker.delegate = self
        self.imagePicker.sourceType = .photoLibrary
        self.imagePicker.allowsEditing = true
        self.present(self.imagePicker, animated: true, completion: nil)
    // 画笔
    case 4:
        self.stickerComponentView.isHidden = true
        
        brushView.isHidden = false
        self.bgImageView.image = nil
        self.view.bringSubviewToFront(brushView)
    default: break
}
```

底部工具栏的每一个模块都是一个 `UIView`，这部分做的也不太好，最佳的做法应该是基于 `UIWindow` 或者 `UIViewController` 做一个「工具容器」作为各个模块 UI 内容元素的容器，通过这种做法就可以免去在底部工具栏的点击事件回调中写这么多的视图显示/隐藏的状态代码。

关注「照片」部分的代码块，实现 `UIImagePickerControllerDelegate` 协议后的方法为：

```swift
extension UNContentViewController: UIImagePickerControllerDelegate {
    /// 从图片选择器中获取选择到的图片
    func imagePickerController(_ picker: UIImagePickerController,
                               didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey : Any]) {
        // 获取到编辑后的图片
        let image = info[UIImagePickerController.InfoKey.editedImage] as? UIImage
        if image != nil {
            let wh = image!.size.width / image!.size.height
            // 初始化贴纸
            let sticker = UNStickerView(frame: CGRect(x: 150, y: 150, width: 100, height: 100 * wh))
            // 添加视图
            self.view.addSubview(sticker)
            sticker.imgViewModel = UNStickerView.ImageStickerViewModel(image: image!)
            // 添加到贴纸集合中
            self.stickerViews.append(sticker)
    
            picker.dismiss(animated: true, completion: nil)
        }
    }
}
```

### 文字
文字模块暴露给父视图也是一个实例化后的贴纸对象，不过在文字 VC 里需要对文字进行颜色、字体和字号的选择。做完了才发现其实因为贴纸是可以通过手势进行放大和缩小的，没必要做字号的选择......

![文字模块功能全览](https://i.loli.net/2019/08/25/wHC1Y6ih7B59tp2.png)

其中比较费劲的是对文字颜色的选择，刚开始我想的直接上 RGB 调色就算了，后来想到如果直接通过 RGB 有三个通道，调起色来非常的难受。想到之前在做[《疯狂弹球》](https://github.com/windstormeye/cocos)这个游戏时使用的 HSB 颜色模式，做一个圆盘颜色选择器，后来在思考实现细节的过程中了这么 EF 写的这个库 [EFColorPicker](https://github.com/EFPrefix/EFColorPicker)，非常好用，改了改 UI 后直接拿来用了，感谢 EF ！

「气泡视图」的本身是个 `UIViewController`，但是需要对其几个属性进行设置。其实现流程比较流程化，比较好的做法是封装一下，把这些模版化的代码变成一个「气泡视图」类供业务方使用，但因为时间关系就一直在 copy，核心代码如下：

```swift
/// 文字大小气泡
private var sizeBottomView: UNBottomSizeViewController {
    get {
        let sizePopover = UNBottomSizeViewController()
        sizePopover.size = self.textView.font?.pointSize
        sizePopover.preferredContentSize = CGSize(width: 200, height: 100)
        sizePopover.modalPresentationStyle = .popover
        
        let sizePopoverPVC = sizePopover.popoverPresentationController
        sizePopoverPVC?.sourceView = self.bottomCollectionView
        sizePopoverPVC?.sourceRect = CGRect(x: bottomCollectionView!.cellCenterXs[1], y: 0, width: 0, height: 0)
        sizePopoverPVC?.permittedArrowDirections = .down
        sizePopoverPVC?.delegate = self
        sizePopoverPVC?.backgroundColor = .white
        
        sizePopover.sizeChange = { size in
            self.textView.font = UIFont(name: self.textView.font!.familyName, size: size)
        }
        
        return sizePopover
    }
}
```

在需要弹出该气泡视图的地方通过 `present` 即可调用：

```swift
collectionView.cellSelected = { cellIndex in
    switch cellIndex {
    case 0: self.present(self.fontBottomView,
                            animated: true,
                            completion: nil)
    case 1: self.present(self.sizeBottomView,
                            animated: true,
                            completion: nil)
    case 2: self.present(self.colorBottomView,
                            animated: true,
                            completion: nil)
    default: break
    }
}
```

### 画笔
之前在滴滴实习时，写过一个关于[画笔的组件](https://github.com/windstormeye/PJImageEditViewController)（居然已经两年前了...），但是这个画笔是基于 `drawRect:` 方法去做的，对于内存十分不友好，一直画下去，内存就会一直涨，这回采用了 `CAShapeLayer` 重写了一个，效果还不错。

![画笔](https://i.loli.net/2019/08/25/ZtiYND6UJ2TrL9B.png)

关于画笔的撤回之前基于 `drawRect:` 的方式去做就会非常简单，每一次的撤回相当于重绘一次，把被撤回的线从绘制点数组中 `remove` 掉就好了，但基于 `CAShapeLayer` 实现不太一样，因为其每一笔都是直接生成在 `layer` 中了，如果需要撤回就得把当前重新生成 `layer`。

所以最后我的做法是每画一笔都去生成一张图片保存到数组中，当执行撤回操作时，就把撤回数组中的最后一个元素替换当前正在的绘制画布内容，并从撤回数组中移除这个元素。

有了撤回，那也要把重做给上了。重做的就是防止撤回，做法跟撤回类似。再创建一个重做数组，把每次从撤回数组中移除掉的图片都 `append` 到重做数组中即可。以下为撤回重做的核心代码：

```swift
// undo 撤回
@objc
private func undo() {
    // undoDatas 可撤回集合 数量
    guard undoDatas.count != 0 else { return }
    
    // 如果是撤回集合中只有 1 个数据，则说明撤回后为空
    if undoDatas.count == 1 {
        // 重做 redo  append 添加
        redoDatas.append(undoDatas.last!)
        // 撤回 undo 清空
        undoDatas.removeLast()
        // 清空图片视图
        bgView.image = nil
    } else {
        // 把 3 给 redo
        redoDatas.append(undoDatas.last!)
        // 从 undo 移除 3. 还剩 2 1
        undoDatas.removeLast()
        // 清空图片视图
        bgView.image = nil
        // 把 2 给图片视图
        bgView.image = UIImage(data: undoDatas.last!)
    }
}

// redo 重做
@objc
private func redo() {
    if redoDatas.count > 0 {
        // 先赋值，再移除（redo的last给图片视图）
        bgView.image = UIImage(data: redoDatas.last!)
        // redo的last 给 undo撤回数组
        undoDatas.append(redoDatas.last!)
        // 从redo重做 移除last
        redoDatas.removeLast()
    }
}
```

关于橡皮的思路我是这么考虑的。按照现实生活中情况，使用橡皮时是把已经写在纸上的笔迹给擦除，换到项目中来看，其实橡皮也是一种画笔只不过是**没有颜色**的画笔罢了，并且可以有两种思路：

* 笔迹直接加在 `contentLayer` 上，此时需要对橡皮做一个 `mask`，把橡皮笔迹的路径和底图做一个 `mask`，这样橡皮笔迹留下的内容就是底图的内容了；
* 笔迹加在另外一个 `layer` 上。这种情况可以直接给橡皮设置成该 `layer` 的背景色，相当于 `clearColor`。

第二种做法我没试过，但是第一种做法是非常 OK 的。

## 总结
以上就是手帐 app 的最小可行性产品了，当然还有很多细节都没有展开，比如服务端部分的代码思路。因为服务端还是围绕产品出发，设计上也不太好，是我第一次使用  `Vapor` 进行开发，只发挥出了 `Vapor` 的 10% 功力。目前服务端完成的需求有：

* 用户的登录注册和鉴权；
* 手帐及手帐本的创建、删除和修改；
* 贴纸的创建、删除和修改。

如果不想与服务端进行交互，可以直接该对应按钮的点击事件为你想要展示的类，并注释掉对应的服务端代码即可。


项目地址：
* [Unicorn-iOS](https://github.com/windstormeye/Unicorn-iOS)
* [Unicorn-Server](https://github.com/windstormeye/Unicorn-Server)

## 参考链接
* [WHStoryMaker](https://github.com/whbalzac/WHStoryMaker)
* [LyEditImageView](https://github.com/Thanatos-L/LyEditImageView)
* [phimpme-iOS](https://github.com/jogendra/phimpme-iOS)
* [TouchDraw](https://github.com/dehli/TouchDraw)