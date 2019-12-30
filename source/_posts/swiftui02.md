---
title: 
date: 2019-08-12 23:42:58
tags:
- SwiftUI
- Swift
- iOS
- Core Data
- Masq
---

> 最近新起了一个 side project，用于承载 WWDC19 里公布的内容。这篇文章主要讲述了 `SwiftUI` 和 `Core Data` 怎么结合，以及自己遇到的问题和思考的第〇篇。

## 前言
`Core Data` 是一个令人又爱又恨的东西，爱它因为系统原生支持，可以和 Xcode 完美的结合，恨它因为在会在一些极端的情况下导致不可预测的问题，比如初始化时不可避免的时间消耗，各种主线程依赖操作等。据我所知，西瓜视频和今日头条原先强依赖 `Core Data`，但因为「某些性能」问题，均已全部撤出。

既然已经有了赤裸裸的教训，为什么我还要执意上 `Core Data` 呢？刚才也说了，因为「某些性能」问题才导致了这两款 app 下掉 `Core Data`，但一般的 side project 可以不用考虑这些问题，再加上 WWDC19 中与 `Core Data` 相关的 session 有四场，明星光环足够了！

## `Core Data` 的封装使用

### 创建模型
首先来看完成图，

![Masq](https://i.loli.net/2019/08/12/Ez6RuUqclbD7Gsm.png)

这是一个非常简单的列表，在 `UIKit` 中我们只需要 `UITableView` 一顿操作即可完事，代码不过区区几十行，用 `SwiftUI` 封装好的话，主列表只需要不到十行即可完成，如下所示：

```swift
struct MASSquareListView : View {

    @State var articleManage = AritcleManager()
    @State var squareListViewModel: MASSquareListViewModel
    
    var body: some View {
        List(self.articleManage.articles, id: \.createdAt) { article in
            MASSquareNormalCellView(article: article)
                .padding(EdgeInsets(top: 5, leading: 5, bottom: 5, trailing: 5))
        }
    }
}
```

现在假设我们的列表已经做好了，现在先来思考列表上需要输入的数据，再来一张图进行解析：

![UI 分析](https://i.loli.net/2019/08/13/AKqPsekZ9iGzFfI.png)

每一个 Cell 里所需要输入的数据有「头像」、「创建时间」和「内容」，在这一篇文章中我们只考虑存粹和 `Core Data` 进行交互的**第一步**，如何让 `Core Data` 的推上 `CloudKit` 或自己的服务器上后续的文章中再展开。

![Core Data 官方组成图](https://docs-assets.developer.apple.com/published/8fc7c1ecbc/35317515-fd0c-418f-862d-d81efd29ed29.png)

从图中可以看出，我们的 Model 属于 `NSManagerObjectModel`，可以按照[这篇文章](https://developer.apple.com/documentation/coredata/creating_a_core_data_model) 所描述的如何创建 `.xcdatamodeld` 文件。

创建完成后，我们可以根据之前的分析的 UI 组成把实体属性定义为如下图所示：

![实体定义](https://i.loli.net/2019/08/13/v9duc4xbne2E7DV.png)

* `avatarColor`： 头像分成为了「颜色」和「图片」两个部分，每一张图片都是 带透明通道的 `png` 类型图片。用户可使用的颜色只能是 app 里被定义好的几种；
* `avatarImage`：如上；
* `content`：内容，该字段在服务端原本是长文本，此处用 `String` 保持一致；
* `createdAt`：创建时间；
* `type`：考虑到后续每一条推文都有可能是不同的形态，比如带不带 `flag` 或 `link`；
* `uid`：该条推文所需的用户 ID。该字段在此篇文章中所讲述的内容是多余字段，你可以不用加上，之前是考虑到了后续的工作，后续再加也无妨。

我们可以选择让 `Core Data` 自动生成与模型相匹配的代码也可以自己写。通过阅读 「objc 中国」的 [Core Data](https://objccn.io/products/core-data/) 书籍，了解原来自己写匹配的模型代码不会有太多的工作，而且还能加深对模型生成的理解过程（之前为了省事都是让 `Core Data` 自动生成，完成的模型代码如下：

```swift
final class Article: NSManagedObject {
    @NSManaged var content: String
    @NSManaged var type: Int16
    @NSManaged var uid: Int32
    @NSManaged var avatarImage: Int16
    @NSManaged var avatarColor: Int16
    @NSManaged internal var createdAt: Date
}
```

模型代码写好后，再去 `.xcdatamodeld` 文件对应的实体上选择刚写好的模型类和取消 `Core Data` 自动生成代码的选项即可：

![配置好对应的选项](https://i.loli.net/2019/08/13/FjlZJvBqt5PEh2S.png)

这一部分实际上我们做的是定义被存储的实体结构，换句话说，通过上述操作去描述你要存储的数据。

### 创建一个 `Core Data` 存储结构
在这个环节中，之前我的做法都是在 `AppDelegate` 中按照 Xcode 的生成模版创建的存储器，以完成需求为导向，导致后续再继续接入存储其它实体时，代码质量比较粗糙，经过一番学习后，调整了方向。

来看一张 「objc 中国」上的 `Core Data` 的存储结构图：


![Core Data 存储结构图](https://objccn.io/images/issues/issue-4/stack-complex.png)

图中已经把我们可以怎么做说的非常明白了，可以有多个实体，通过 `context` 去管理各个实体的操作，`context` 再通过协调器跟存储器产生交互，与底层数据库产生交互。这张图实际上与后续我们要把数据推上 `CloudKit` 的过程非常类似，但本篇文章中我们将使用「objc 中国」的这张图的方式去完成：

![](https://objccn.io/images/issues/issue-4/stack-simple.png)

通过一个 `context` 去管理多个实体，且只有一个存储管理器。为了方便后续调用数据管理方法的便利，而且存储器不需要重复创建，我拉出了一个单例去管理：

```swift
class MASCoreData {
    static let shared = MASCoreData()
    var persistentContainer: NSPersistentContainer!
    /// 创建一个存储容器
    class func createMASDataModel(completion: @escaping () -> ()) {
        // 名字要与 `.xcdatamodeleld` 文件名一致
        let container = NSPersistentContainer(name: "MASDataModel")
        
        container.loadPersistentStores { (_, err) in
            guard err == nil else { fatalError("Failed to load store: \(err!)") }
            DispatchQueue.main.async {
                self.shared.persistentContainer = container
                completion()
            }
        }
    }
}
```

在初始化时，我们可以这么用：

```swift
func scene(_ scene: UIScene,
            willConnectTo session: UISceneSession,
            options connectionOptions: UIScene.ConnectionOptions) {
    
    //TODO: 这么做有些粗暴，不能数据库创建失败就页面白屏，本篇文章只考虑需求实现，剩下内容后续文章讲解
    MASCoreData.createMASDataModel {
        if let windowScene = scene as? UIWindowScene {
            
            let window = UIWindow(windowScene: windowScene)
            window.rootViewController = UIHostingController(rootView:
                MASSquareHostView()
                    .environmentObject(MASSquareListViewModel())
            )
            
            self.window = window
            window.makeKeyAndVisible()
        }
    }
}
```

代码中的 `environmentObject` 是上一篇文章中需要控制菜单的显示和隐藏所加，在这篇文章中可以不用管。通过以上方法，我们就在 app 初始化时，就创建好了一个可用的存储器。

### 数据交互
模型有了，存储器有了，那就要开始做增删改查了。实际上对 `Core Data` 的增删改查实现，已经有了众多的文章去讲解，在此不做展开。以我之前做 `Core Data` 数据查询来看，之前我是这么写的：

```swift
func allxxxModels() -> [PJxxxModel] {
    var finalModels = [PJModel]()
    let fetchRequest = NSFetchRequest<xxxModel>(entityName: "xxxModel")
    do {
        let fetchedObjects = try context?.fetch(fetchRequest).reversed()
        guard fetchedObjects != nil else { return []}
        // 做一些数据读取出来的操作 ......
       
        print("查询成功")
        return finalModels
    }
    catch {
        print("查询失败：\(error)")
        return []
    }
}
```

其实一眼看上去也还好，我之前也觉得很好，但是当我写了三四个实体后，发现每个新建实体的查询方法都需要去复制之前写好的查询方法，改改参数就用了，当时觉得有些不太对劲的地方，因为重复的工作一直在做，现在会怎么做呢？

首先分析出每次创建一个 `NSFetchRequest` 都必须要硬编码进实体名字，并且还需要创建多个中间实体对象和真正对象模型的中间代码，因为存入 `Core Data` 的数据字段全部依赖 API 模型字段是肯定不行的，所以几乎在每一个视图查询方法里都写了大量的兼容代码，很是难看。

最后在这个项目里，又遇到了同样的问题。第二个问题基本无解，就是得要写两个模型，否则你的 `Core Data` 模型字段就会变得「无比巨大」，所以还是写了两个 model 分别针对 `Core Data` 和 API 模型。

对于第一个问题，可以通过协议的方式去解决：

```swift
protocol Managed: class, NSFetchRequestResult {
    static var entityName: String { get }
    static var defaultSortDescriptors: [NSSortDescriptor] { get }
}

extension Managed {
    static var defaultSortDescriptors: [NSSortDescriptor] {
        return []
    }

    static var sortedFetchRequest: NSFetchRequest<Self> {
        let request = NSFetchRequest<Self>(entityName: entityName)
        request.sortDescriptors = defaultSortDescriptors
        return request
    }
}

extension Managed where Self: NSManagedObject {
    static var entityName: String { return entity().name!  }
}
```

通过以上方式，只要 `NSManagedObject` 类型的对象遵循了 `Managed` 协议可以可以通过 `entityName` 属性获取到实体名字，而不需要硬编码字符串去做识别了。按照 UI 图中所展示的内容，基本上也都是按推文的创建时间倒序排序，所以为了不用在每个 `NSFetchRequest` 中都写 `sortDescriptors` 也给了一个默认实现，查询数据时只需要通过调用 `sortedFetchRequest` 属性即可配置完毕。

现在什么都配置好了，就差把数据切上列表进行展示了。如果是按照我之前的写法，通过 `allxxxModels()` 方法的返回值拿到的数据后，得手动的同步 `UITableView` 做 `reloadData()`，但现在我们使用的可是 `SwiftUI` 啊～如果还用之前 `UIKit` 的方法肯定是不符合 `SwiftUI` 的 workflow。

如果你关注过 `SwiftUI` 那对 `@State`、`@BindingObject` 和 `@EnvironmentObject` 肯定不陌生，这几个修饰词的定义我是从组件的角度出发去看的，当然还可以有其它的一些使用思路。三个属性在我的使用过程中我是这么定义的：

* `@State`：组件内数据或状态的传递；
* `@BindingObject`：跨组件间的数据传递；
* `@EnvironmentObject`：跨组件间的数据传递。从名字上看出，也可以设置一些不可变的环境值，后续会尝试用在用户管理部分。

如果要做到符合 `SwiftUI` 官方推荐的数据流处理方式，我们需要定义一个遵守 `ObservableObject` 协议的类，通过这个类去做数据的发送：

```swift
class AritcleManager: NSObject, ObservableObject {

    @Published var articles = [Article]() 
}
```

~~注意，这是我从 SwiftUI beta4 迁移到 beta5 的代码，使用 beta5 之前的版本都跑不起来。其中特别扎眼的是 @Published var willChange = PassthroughSubject<Void, Never>() 这行代码，在 beta5 之前，这行代码会这么写 var willChange = PassthroughSubject<Void, Never>()。~~

~~其中 <Void, Never> 的解释是，第一个参数表示此次通知抛出去的数据是什么，Void 表示全部抛出去，有些文章中写的本类名，本质上是一个意思。第二个参数表示此次抛出通知时的错误定义，如果遇到错误了，要抛出什么类型的错误，Never 代表不处理错误。这点其实不好，应该根据实际上会遇到的问题抛出异常，后续文章会继续完善。~~

~~其实代码中已经说的很明白了，当我们修改 articles 时，触发 willSet 方法调用 send() 方法触发通知的发送，接着我们在其它地方通过 @BindObject 去监听这个通知即可：~~

在最新的 beta5 中，我们只需要 `@Publisher` 修饰需要监听数据变化的变量即可，Combine 会在数据发生变化时自动调用 `send()` 方法对外进行广播，不再需要我们手动调用，当然之前的方式也依然可以继续使用。

```swift
struct MASSquareListView : View {
    // 在内部实例化即可，因为只有该 `View` 使用到
    @State var articleManage = AritcleManager()
    @State var squareListViewModel: MASSquareListViewModel
    
    var body: some View {
        List(self.articleManage.articles, id: \.createdAt) { article in
            MASSquareNormalCellView(article: article)
                .padding(EdgeInsets(top: 5, leading: 5, bottom: 5, trailing: 5))
        }
    }
}
```

所以如果我们直接按照之前的做法，通过 `NSFetchRequest` 拿到的数据后，在更新 `articles` 的值也能完成需求，这也是我之前的做法，但总不能一个实现直接套在多个项目中对吧，那这样也太没劲了，因此为了更好切合 `Core Data` 的使用方式，我们用上 `NSFetchedResultsController` 来管理数据。

使用 `NSFetchedResultsController` 来管理数据，我们可以不用理会 `Core Data` 数据**增删改查**的变化，只需要关注 `NSFetchedResultsController` 的代理方法，其中我的实现是：

```swift
extension AritcleManager: NSFetchedResultsControllerDelegate {
    func controllerDidChangeContent(_ controller: NSFetchedResultsController<NSFetchRequestResult>) {
        articles = controller.fetchedObjects as! [Article]
    }
}
```

我并没有把所有的方法都实现完，如果我们是使用传统的 `UITableView` 去实现，可能会需要再把剩下的几个代理方法实现完。在此，我的个人推荐做法是，如果你的实体需要处理「某些事情」，那每一个实体最好都做一个 `manager` 去对 `NSFetchedResultsControllerDelegate` 协议做实现，因为很有可能每一个实体在 `NSFetchedResultsControllerDelegate` 协议中的各个代理方法需要关注的点都不一样，不能一巴掌拍死，什么都抽象。

通过 `NSFetchedResultsController` 实现数据的改动监听后，在实例化 `AritcleManager` 时，要做补上一些配置工作：

```swift
class AritcleManager: NSObject, ObservableObject {
    
    @Published var willChange = PassthroughSubject<Void, Never>()
    
    var articles = [Article]() {
        willSet {
            willChange.send()
        }
    }
    fileprivate var fetchedResultsController: NSFetchedResultsController<Article>
    
    override init() {

        let request = Article.sortedFetchRequest
        request.fetchBatchSize = 20
        request.returnsObjectsAsFaults = false
        self.fetchedResultsController = NSFetchedResultsController(fetchRequest: request, managedObjectContext: MASCoreData.shared.persistentContainer.viewContext, sectionNameKeyPath: nil, cacheName: nil)
        
        super.init()
        
        fetchedResultsController.delegate = self
        
        // 执行方法后，立即返回
        try! fetchedResultsController.performFetch()
        articles = fetchedResultsController.fetchedObjects!
    }
}
```

通过以上代码的操作，我们就完成当 `Core Data` 中的 `Article` 实体数据发生改动时，会直接把改动发送到外部所有监听者。

我们现在来看看如何插入一条数据。我之前会这么做：

```swift
func addxxxModel(models: [xxxModel]) -> Bool{
    
    for model in models {
        let entity = NSEntityDescription.insertNewObject(forEntityName: "xxxModel", into: context!) as! xxxModel
        
        // 做一些插入前的最后准备工作
    }
    do {
        try context?.save()
        print("保存成功")
        return true
    } catch {
        print("不能保存：\(error)")
        return false
    }
}
```

可以看出插入数据时还是得依赖 `context` 去做管理，按照我们之前的想法，通过 `NSFetchedResultsController` 去监听的数据的改变是为了达到不需要每次都通过 `context` 调用 `fetch` 方法拉取最新的数据，但插入数据的一定得是「手动」完成的，必须是要显示调用。

因此，我们可以对这种「重复性」操作进行封装，不用再像我之前那样为每一个实体都写一个插入方法：

```swift
extension NSManagedObjectContext {
    func insertObject<T: NSManagedObject>() -> T where T: Managed {
        guard let obj = NSEntityDescription.insertNewObject(forEntityName: T.entityName, into: self) as? T else { fatalError("error object type") }
        return obj
    }
}
```

使用泛型限定方法内返回对象的调用方是 `NSManagedObject` 类型，使用 `where` 限定调用方必须遵循 `Managed` 协议。所以，我们可以对 `Article` 的 `Core Data` 模型修改为：

```swift
final class Article: NSManagedObject {
    @NSManaged var content: String
    @NSManaged var type: Int16
    @NSManaged var uid: Int32
    @NSManaged var avatarImage: Int16
    @NSManaged var avatarColor: Int16
    @NSManaged internal var createdAt: Date
    
    static func insert(viewModel: Article.ViewModel) -> Article {
        
        let context = MASCoreData.shared.persistentContainer.viewContext
        
        let p_article: Article = context.insertObject()
        p_article.content = viewModel.content
        p_article.avatarColor = Int16(viewModel.avatarColor)
        p_article.avatarImage = Int16(viewModel.avatarImage)
        p_article.type = Int16(viewModel.type)
        p_article.uid = Int32(2015011206)
        p_article.createdAt = Date()
        
        return p_article
    }
}
```

## 后记
你会发现到这里，我们实际上并没有对 `SwiftUI` 与 `Core Data` 做其它的上下文依赖工作，这是因为我们使用了 `NSFetchedResultsController` 去动态监听的 `Article` 实体的数据改动，然后通过 `@Publisher` 修饰的对象调用 `send()` 方法发送更新后的数据。

在这篇文章中使用的 `Combine` 主要体现在 `Core Data` 的数据获取和更新不需要主动的告知 UI。当然，如果你硬是要说这些事情并不需要的 `Combine` 去支持也是可以的，因为基于 `Notification` 确实也可以做到。关于 `Combine` 更细节的内容将会随着本项目的进展进行完善。

**注意：本篇文章中的部分内容因为项目在持续进展，部分内容实现会不太符合最终或目前常规做法。**

## 参考资料
[Core Data](https://objccn.io/products/core-data/)

项目地址：[Masq iOS 客户端](https://github.com/windstormeye/Masq-iOS)