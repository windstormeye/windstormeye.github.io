---
title: PhotosKit开发总结（一）
date: 2018-12-21 15:29:32
tags:
- iOS
- Swift
---

> 这个组件做的实在是太久了，最近终于从一大堆事儿中慢慢的恢复过来了，继续肝！

## 前言

这次的组件开发换了个思路继续精进，也还是 `MVC` 的模式，前段时间自己非常纠结到底哪种模式才是“最佳”设计模式？翻阅了大量资料，后来在[这篇文章](https://www.jianshu.com/p/33c7e2f3a613)中得到了“救赎”，让我真正的从回归到从实际问题出发，而不是一昧的为了“用”而用，尤其是在昨天的迭代总结会上，android 同学“夸夸其谈”的列出了许多所谓的“优化点”，某些“优化点”在我看来却是十分的可笑，本来以为来了个大佬，现在看来却是个“大佬”。

从 11 月末开始就着手准备开发这一新组件，但因为刚好与三方、新版本迭代期、期末课设等各种因素导致组件开发一再延后。该组件利用了 `PhotosKit` 框架，完成了从系统相册读取并自定义相册的功能，设计稿如下；

![设计稿](https://i.loli.net/2018/12/21/5c1c9bade7ff8.png)


## 思考
一开始看到设计图后，感觉并没有多少东西需要去做，玩好 `PhotosKit` 即可，经过了一段时间后，再三确认后，最终的产品效果是要对齐 `Instagram` 里的“照片浏览器”体验一致，截图如下所示：

![Instagram 照片浏览器截图](https://i.loli.net/2018/12/21/5c1c9d27849a2.png)

接着我就去玩了 `Instagram`，越玩越感觉这是个“大坑”，如果要做到 100% 的交互相似，估计做完直接丢出去开源又会拉到一波 star，对 `Instagram` 的”照片浏览器“分析如下：

* 可以简单的进行上下拆分。上部分为”选中视图“，可以直接套 `UIImageView`，下部分为“浏览视图”，可用 `UICollectionView`；
* 当”浏览视图“进行“上滑”操作时，无论滑动多么快速都不会触发“选中视图”的连带“上滑”操作；
* 当用户从“浏览视图”的范围滑动到“选中视图”中时，也就是手指触摸区域到达“选中视图”区域，将触发“选中视图”的连带“上滑”操作。
* 当“选中视图”已经到顶时，用户从“浏览视图”进行”下拉“操作，直接触发“选中视图”的连带“下拉”操作。

以上是目前总结出 `Instagram` 的“照片浏览器”四大要点，后续的开发工作也围绕着这四点进行。


## 需求拆分
在**思考**环节明确了该组件的开发难点后，开始对需求进行拆分，细致工作量。前几天还冒出了一个“笑话”，组件都快开发完了，自己却不放心，多嘴再去沟通了一遍，发现原来最终的效果和目前所实现的差距有些大，不得不又反工重来。

经过一番调研，设定的耗时为：2天，包括前后端联调。整理出的需求大致如下：

Feature | UI | Power
--- | --- | --- 
浏览相册 | `UITableView` | 0.5
浏览相册照片 | `UICollectionView` | 1
交互 | - | 1


## 实现
一开始在数据源的获取上就跪了，之前在读取系统相册资源这方面需求仅仅只是“获取”这一方面，并没有对交互有太多的要求，也就一直没有精进，这回需要对相册做一个自定义就跪在数据源的获取上了，构思后，觉得有必要拉出一层 `DataManager`，虽然只是从系统中拉数据，但为了“高内聚、低耦合”的理念，应该降低“调用方”的使用成本。

挑出了一部分 `PhotosKit` 框架核心知识点列举如下：

* `PHObject`：`Photos` 的资源集合和集合列表的抽象父类；
* `PHAssetCollection`：一个相册；
* `PHCollectionList`：一个包含多个相册的集合；
* `PHFetchResult`：
  * 作为 `PHAsset`(Live Photo)、`PHCollection`、`PHAssetCollection`、`PHCollectionList` 相关方法的返回结果对象；
  * 内容可动态加载，并不是直接把某个相册中的内容直接全部遍历出来，而是当需要一部分内容后才会去照片库中获取，这可以在处理大量结果时提供一个最佳性能；
  * 默认**线程安全**；
  * 缓存规则个人看法是利用了 `LRU`，但实际上是不是这么一回事有待考证。

### 读取所有所需相册
加了个关键词——“所需”，`PhotosKit` 框架提供了一套十分完整的获取不同类型相册 API，在 `PJAlbumDataManager` 中，我是这么做的：
```Swift
/// 获取所有相册
private func allAlbumCollection() -> [PHAssetCollection] {
    var collections = [PHAssetCollection]()
    let smartAlbums = PHAssetCollection.fetchAssetCollections(with: .smartAlbum,
                                                              subtype: .any,
                                                              options: nil) as! PHFetchResult<PHCollection>
    let userAlbums = PHCollectionList.fetchTopLevelUserCollections(with: nil)
    
    for album in [smartAlbums, userAlbums] {
        for s_i in 0..<album.count {
            let collection = album[s_i] as! PHAssetCollection
            let types: [PHAssetCollectionSubtype] = [.albumRegular, // 用户自己创建的相册
                                                      .smartAlbumPanoramas, // 全景
                                                      .smartAlbumScreenshots, // 屏幕截图
                                                      .smartAlbumUserLibrary, // 相机胶卷
                                                      .smartAlbumRecentlyAdded] // 最近添加
            if types.contains(collection.assetCollectionSubtype) {
                collections.append(collection)
            }
        }
    }
    return collections
}
```

从上文中列出来的核心知识点，明确了 `PHAssetCollection` 相当于是一个相册，我们需要拿到由相机拍摄的照片集 `.smartAlbum` 和用户自己创建的照片集 `fetchTopLevelUserCollections`，注意，这包括了“获取相册权限”的应用自行创建的相册。

而 `album` 是 `PHAssetResult<PHAssetCollection>` 类型，且因未实现 `Sequence` 协议，而无法进行遍历，而采取了一个简单的做法，至于比较优雅的做法暂未实现。

### 获取相册封面
通过以上方法，我们就拿到了当前用户设备中的所有所需相册集合。那如何获取一个相册的封面以及其所包含的照片数呢？经过一番研究后发现 `PHAssetCollection` 中提供了获取并未提供“封面”这个属性，同时也没有提供单独的 API 去获取一个相册封面，但是通过一个比较尴尬的方法，即通过获取相册中的所有照片 API 去锁定第一张照片，直接作为封面 😅，`PJAlbumDataManager` 中的实现如下：
```Swift
/// 获取所有相册封面及照片数
func getAlbumCovers(complateHandler: @escaping (_ coverPhotos: [Photo], _ albumPhotosCounts: [Int]) -> Void) {
    let albumCollections = albums
    var photos = [Photo]()
    var photosCount = [Int]()
    // 获取单张照片资源是异步过程，需要等待所有相册的封面图片一起 append 完后再统一通过逃逸闭包进行返回
    var c_index = 0
    for collection in albumCollections {
        let assets = albumPHAssets(collection)
        // 有些系统自带相册类型如果用户没有进行照片归类则会导致取到的相片数为0
        guard assets.count != 0 else {
            c_index += 1
            continue
        }
        
        photosCount.append(assets.count)
        
        var photo = Photo()
        photo.photoTitle = collection.localizedTitle
        convertPHAssetToUIImage(asset: assets[0],
                                size: CGSize(width: 150, height: 150),
                                mode: .fastFormat) { (photoImage) in
                                    photo.photoImage = photoImage
                                    photos.append(photo)
                                    c_index += 1
            
                                    if c_index == albumCollections.count - 1 {
                                        complateHandler(photos, photosCount)
                                    }
        }
    }
}
```

同样在上文中我们也说明了，一张张的照片是 `PHAsset` 资源对象，而 `PHAsset` 是从 `PHAssetCollection` 取出的，并且取出的资源集合类型中不需要包含视频且按照时间“由近到远”对集合进行排序。在 iOS 中对集合进行检索最佳做法是通过**“谓词”**进行限制，`PJAlbumDataManager` 实现 `albumPHAssets` 方法如下所示：
```Swift
/// 当前相册的所有 PJAsset
private func albumPHAssets(_ collection: PHAssetCollection) -> PHFetchResult<PHAsset> {
    let options = PHFetchOptions()
    options.predicate = NSPredicate(format: "mediaType = %d", PHAssetMediaType.image.rawValue)
    options.sortDescriptors = [NSSortDescriptor(key: "creationDate", ascending: false)]
    let fetchResult = PHAsset.fetchAssets(in: collection, options: options)
    return fetchResult
}
```

一个相册中的所有 `PHAsset` 资源是全都拿到了，但是 `PHAsset` 资源却无法直接与 `UIKit` 进行协作，还需要对 `PHAsset` 对象转为 `UIImage` 对象，`PJAlbumDataManager` 中是这么做的：
```Swift
/// PHAsset 转 UIImage
func convertPHAssetToUIImage(asset: PHAsset,
                                      size: CGSize,
                                      mode: PHImageRequestOptionsDeliveryMode,
                                      complateHandler: @escaping (_ photo: UIImage?) -> Void) {
    let coverSize = size
    let options = PHImageRequestOptions()
    options.isSynchronous = false
    options.deliveryMode = mode
    options.isNetworkAccessAllowed = true
    PHImageManager.default().requestImage(for: asset,
                                          targetSize: coverSize,
                                          contentMode: .default,
                                          options: options) { result, info in
                                            guard result != nil else { return complateHandler(nil) }
                                            complateHandler(result)
    }
}
```

在 `requestImage` 方法中，我们可以对最终要生成 `UIImage` 对象做一些额外的设置，例如“目标尺寸”、“是否异步操作”等。需要注意的是，如果开启了“异步操作”，要记得处理好全部 `PHAsset` 资源集合的异步获取时间节点，否则一张照片都拿不到。

#### UI 搭建
显示所有相册的封面及其照片数，上文解决了数据来源后，剩下的事情就正常操作 `UITableView` 即可，完工截图如下所示：

![选择相册 截图](https://i.loli.net/2018/12/21/5c1cc242ba1c8.png)


### 获取一个相册下的所有照片
这部分思路已经上节中描述过了，把“只取第一张的照片”限制条件放开即可，`PJAlbumDataManager` 的实现如下：
```Swift
/// 获取某一相册的所有照片
func getAlbumPhotos(albumCollection: PHAssetCollection,
                    complateHandler: @escaping (([Photo], PHFetchResult<PHAsset>) -> Void)) {
    let assets = albumPHAssets(albumCollection)
    var photos = [Photo]()

    for a_index in 0..<assets.count {
        var photo = Photo()
        convertPHAssetToUIImage(asset: assets[a_index],
                                size: CGSize(width: 150, height: 150),
                                mode: .highQualityFormat) { (photoImage) in
                                    photo.photoImage = photoImage
                                    photo.photoTitle = albumCollection.localizedTitle ?? ""
                                    photos.append(photo)
            
                                    if a_index == assets.count - 1 {
                                        complateHandler(photos, assets)
                                    }
        }
    }
}
```

#### UI 搭建
在相册详情的 UI 搭建中，主要涉及到有 `UICollectionView` 和 `UIImageView` 两者，但在交互上需要满足上文所说的这三点：
* 当”浏览视图“进行“上滑”操作时，无论滑动多么快速都不会触发“选中视图”的连带“上滑”操作；
* 当用户从“浏览视图”的范围滑动到“选中视图”中时，也就是手指触摸区域到达“选中视图”区域，将触发“选中视图”的连带“上滑”操作。
* 当“选中视图”已经到顶时，用户从“浏览视图”进行”下拉“操作，直接触发“选中视图”的连带“下拉”操作。

这三点中实现难度相对较高的为第二点，需要利用 `hitTest` 或 `point(inside)` 进行实现，这部分放到下篇文章中结合前后端交互一块进行分享。目前实现的部分效果截图如下：

![相册详情 截图](https://i.loli.net/2018/12/21/5c1cc74f41c52.png)


## 优化点
* 相册读取因为采用的是“计算属性”，并不会对已经读取过的数据结果进行缓存，应采用 `lazy`；
* 交互细节需要继续完善。