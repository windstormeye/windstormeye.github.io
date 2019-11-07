---
title: Swift_构造器
date: 2018-08-15 23:13:40
tags:
- swift
---

## Swift 构造器
Swift 中的构造器（也可称为构造方法）与 OC 的不同以用一篇文章进行记录。在编写 Swift 构造器的过程中，我们要明确一个理念： **不管是类类型还是值类型，在构造器完成初始化过程后，实例的每个属性都必须要有值**。Swift 和 OC 一样都有指定构造器和便捷构造器之分，指定构造器是类的主要初始化器，在类的指定构造器中要保证将类中的所有属性都赋上了初始值，包括从父类继承的属性（如果有的话）并且要调用“合适”的父类（如果有的话）初始化器。一般情况下，每个类最少有一个指定构造器。便捷构造器可以没有，如果我们并不需要便捷的构造器。

### 自动化构造器
在 Swift 的类类型和值类型中的某些情况下，我们可以不显式写出初始化方法， Swift 会为我们生成默认的初始化构造方法，如果我们想要使用这个特性，就需要满足每个成员变量都必须有默认值。其实自动生成的默认构造器也是指定构造器的一种，如下所示：
```Swift
class Person {
    let gender: String = "women"
    let age: Int = 28
    var nationality: String?
}

struct Car {
    let width = 0.0
    let height: Double 
}

```

在结构体中，注意我们并没有给 height 设置默认值，此时 Swift 只会自动的帮我们生成 `init(height:)` 这个方法，具体使用如下所示：
```swift
struct Car {
    let width = 0.0
    let height: Double
}
class Person {
    let gender: String = "women"
    let age: Int = 28
    var nationality: String?
}

let p = Person.init()
let c = Car.init(height: 12.4)
```

### 初始化方法调用顺序
分别对 Swift 和 OC 写类的初始化方法，

```objc

@implementation Test
- (instancetype)init
{
    self = [super init];
    if (self) {
      
    }
    return self;
}
@end
```

```Swift
class Test: NSObject {
    override init() {
        
    }
}
```

从以上代码中我们可以看出，Swift 的初始化方法比 OC 多了一个 `overrinde` 关键字，而且 `init` 方法内部并没有返回 `self` ，也没有调用 `super` 的 `init` 方法，此时 cmd + B 进行编译没有任何问题。

分别给这两个类添加上相关属性，

```objc
@interface Test ()
@property (nonatomic, strong) NSString *singleDog;
@end
@implementation Test
- (instancetype)init {
    self = [super init];
    if (self) {
      	
    }
    return self;
}
@end
```

```Swift
class Test: NSObject {
    let singleDog: String
    
    override init() {
        
    }
}
```

此时，我们会发现 Xcode 已经给我们写的 Swift 类报了这个错 `Property 'self.singleDog' not initialized at implicitly generated super.init call` 直接指出了我们的错误，`singDog` 没有在暗中调用（其实就是 隐式调用 ） `super.init` 方法前进行初始化。此时我们明白了，Swift 的初始化方法并不是不需要调用父类初始化方法，而是我们目前的代码处在编译器自动帮我们调用父类初始化方法 `init` 的环境中（后文有需要显式调用的情况）。所以我们要把代码修改为：

```Swift
class Test: NSObject {
    let singleDog: String
    
    override init() {
        singleDog = "I am"
        // 可以不写，上文已说过当前环境符合编译器自动生成 super.init() 要求
        // super.init() 
    }
}
```

这样就 OK 了，但是如果我们需要去修改父类的属性，那就需要把代码修改为：

```Swift
class Test: NSObject {
    var singleDog: String
    
    override init() {
        singleDog = "I am"
    }
}

class BigTest: Test {
    let singleCat: String
    
    override init() {
        singleCat = "You are"
        super.init()
        singleDog = "She is"
    }
}
```

可以看出，如果我们要修改父类的属性，得先保证本类的所有属性已经初始化完成才能去修改父类属性，想一想也就明白啦！ Swift 中的构造器无返回值（而 OC 是返回 id 类型变量），它的主要作用是保证新实例在第一次使用前完成正确的初始化工作。可对 Swift 中类的初始化顺序做个总结：

1. 先初始化子类的成员变量（require）；
2. 调用父类的初始化方法（如果不需要修改父类成员变量，可无 2 和 3 ）；
3. 修改父类成员变量；

 需要注意的是，Swift 中如果你的成员变量是可选类型 `let aha: String?` 同样也可以不用对其进行初始化工作，因为编译器已经为其设置了一个默认值 `nil` ， Swift 中的 `nil` 代表一个可选值，是一个值类型，而 OC 中的 `nil` 代表的是一个空对象，指向不存在对象的指针，对对其发送消息。 **在 OC 中的构造方法中，先调用父类的构造方法，再正确初始化子类的成员变量；在 Swift 的构造方法中，先正确初始化子类成员变量，再调用父类构造方法。**

### 关键字
以上部分只是 Swift 中语法的小小变化，我们来看看具体的需求。一般来说，我们会在工程中继承 `UIView` 做自定义视图类，结合上文讨论的内容和以往 OC 的思路去写，就会又出现了问题，如下所示：

```Swift 
class PJFuckView: UIView {
    let title: String
    
    override init() {
        title = "2333"
        super.init()
    }
}
```

按照我们以往的思路可能会写出上述代码， cmd + B 编译一下，我们会得到 3 个 error 。分别为：
1. `Initializer does not override a designated initializer from its superclass`
2. `Must call a designated initializer of the superclass 'UIView'`
3. `'required' initializer 'init(coder:)' must be provided by subclass of 'UIView'`（提示让我们插入一段代码，下文说）

`Initializer does not override a designated initializer from its superclass` 错误告诉我们并没有去重写父类中的指定构造器，cmd + control 进父类 `UIView` 中可以看到，`UIView` 只提供了以下两种构造方法，而不是我们写的 `init` 方法，
```swift
public init(frame: CGRect)

public init?(coder aDecoder: NSCoder)
```

OK，那我们就重写我们需要的父类指定构造器吧！

```Swift
class PJFuckView: UIView {
    let title: String
    
    override init(frame: CGRect) {
        title = "2333"
        super.init()
    }
}
```

此时，再编译一下，我们已经解决了第一个问题。当然，第二个问题也随之可以解决，改为跟我们重写的父类指定构造器方法即可 `super.init(frame: frame)` ，或者也可以选择直接删掉，因为我们此时并未对父类的成员变量做其它的任何操作。

最后一个问题，因为 Xcode 提示我们插入一段代码，插入这段代码后就变成了：
```Swift
class PJFuckView: UIView {
    let title: String
    
    override init(frame: CGRect) {
        title = "2333"
        super.init(frame: frame)
    }
    
    required init?(coder aDecoder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
}
```

此时再编译一下，发现所有的 error 都解决了。那 Xcode 自动帮我们插入的这段代码是什么意思呢？可以注意到插入的这段代码前有一个 `required` 关键词，也就是我们必须要实现这个方法，但是注意了，插入的代码中有这么一句话 `fatalError("init(coder:) has not been implemented")` ， 也就是说当这个方法被执行的时候就会无条件停止在这并打印 `init(coder:) has not been implemented` 这句话 😑 （真是不懂为什么要自动生成这么一句话），那这个方法到底是个啥？

从字面意思上我们也可以看出来这跟 `NSCoding` 协议脱不了关系，cmd + control 点到 `UIView` 中也看到确实 `UIView` 继承了 `NSCoding` 协议。有趣的是 `UIViewController` 更加激进，只有以下这两种方法
```Swift
public init(nibName nibNameOrNil: String?, bundle nibBundleOrNil: Bundle?)

public init?(coder aDecoder: NSCoder)
```

通过 `UIView` 和 `UIViewController` 的初始化方法中根据我们以往的知识也就能分析得出来了，`UIView` 和 `UIViewController` Apple 现在主推使用 xib 或者 StoryBoard 的方式搭建界面，而这两个东西编译在 iPhone 上后存在于某个位置上（我猜是沙盒或者与之类似的东西中），Cocoa 使用我们以往常见的“编码”和“解码”（序列化和反序列化）的方式对其进行存储和读取。也就是说，当我们使用 xib 或者 Storyboard 进行界面的搭建时，将会调用这个方法，这分别是两条不同的类初始化路径。当我们没有在子类中写明任何指定构造器时，父类的必须构造器将会被自动继承，但如果在子类中写明了对应的指定构造器，那就要手动写明实现父类必须构造器，如果在子类中只定义了便捷构造器，父类的必须构造器也会自动继承。

所以，较为完整的、安全的初始化方法，可参考如下所示：
```Swift
class PJFuckView: UIView {
    let title: String
    
    override init(frame: CGRect) {
        title = "2333"
        super.init(frame: frame)
    }
    
    required init?(coder aDecoder: NSCoder) {
        title = "2333"
        super.init(coder: aDecoder)
    }
}
```

### 便捷构造器
有了指定构造器，跟 OC 中的一样，肯定也是要有便捷构造器的，只不过 OC 中并没有从编译器层面上向 Swift 一样对我们的构造器做出约束，这需要我们自己约束自己写出一套较好的 OC 风格指定构造器和便捷构造器。

在 Swift 中的便捷构造器也是一样的，需要在便捷构造器中显式的调用指定构造器，如下：
```Swift
class PJFuckView: UIView {
    var title: String
    
    override init(frame: CGRect) {
        title = "2333"
        super.init(frame: frame)
    }
    
    convenience init(titleString: String, frame: CGRect) {
        title = titleString
        self.init(frame: frame)
    }
    
    required init?(coder aDecoder: NSCoder) {
        title = "2333"
        super.init(coder: aDecoder)
    }
}
```

如上所示，我们写了一个便捷构造器，以便于外部能够直接通过该构造器直接初始化 Test 类，但是毫无疑问，我们又得到了一个 error `'self' used in property access 'title' before 'self.init' call` ，提示我们要在 `self.init` 之后才能对 `title` 进行操作。这是又是为什么呢？仔细一想，我们现在写的便捷构造器，如果我们在便捷构造器中对子类成员变量进行了修改，然后才去调用子类的指定构造器，如果在该指定构造器中做了对成员变量的初始化操作就会覆盖掉了我们便捷构造器中所给的值，得不偿失，所有这应该是编译器做的一个安全检查（我觉得语法层面上没问题），所以我们只需要把 `self.init` 和 `title` 的赋值操作做一个调换即可，如下所示：

```Swfit
class PJFuckView: UIView {
    var title: String
    
    override init(frame: CGRect) {
        title = "2333"
        super.init(frame: frame)
    }
    
    convenience init(titleString: String, frame: CGRect) {
        self.init(frame: frame)
        title = titleString
    }
    
    required init?(coder aDecoder: NSCoder) {
        title = "2333"
        super.init(coder: aDecoder)
    }
}
```

### 可失败初始化器
如果你有仔细观察的话，会发现其实之前 Xcode 给我们自动插入的那一段 `required` 指定构造器方法名后跟了个 `?` ，这个 `?` 就向我们表明了这是个可失败的构造器，也就是可以返回 nil 的初始化方法，会发现这其实就是我们之前在 OC 中的 `self = [super init] if (self) {} ` 要做的事情，但是 OC 中的这个“神奇”的写法会引起很多异议，因为虽然我们对其返回值 `self` 做了空判断，但是依然不知道是什么情况（只能列出几个大致情况，以后在说啦~）下才导致了其会返回 nil 。因此，在 Swift 中对其做了一个较好的处理，比如在[ Swift 官方文档](https://docs.swift.org/swift-book/LanguageGuide/Initialization.html)中所描述的：

```Swift
class Product {
    let name: String
    init?(name: String) {
        if name.isEmpty { return nil }
        self.name = name
    }
}

class CartItem: Product {
    let quantity: Int
    init?(name: String, quantity: Int) {
        if quantity < 1 { return nil }
        self.quantity = quantity
        super.init(name: name)
    }
}
```

从以上代码中可以看到，在 `CartItem` 的构造方法中对传入的参数 `quantity` 做了下限判断。具体的细节我就不展开啦，在文档中已经讲得非常清楚了。如果我们已经开始写 Swift 了，还会发现有出入的地方，一般如果我们没有对自定义的 `UIViewController` 写下任何构造器我们也能通过 `let vc = UIViewController()` 进行初始化，我没能在代码中翻到有关内容，不过在网上找到了一个解答：
```
UIViewController 的那个无参的构造器是从 UIKit 里面迁移过来的，也就是说这个无参的构造器实际上就是 Objective-C 的 UIViewController 的无参构造方法，因为UIKit 是 OC 写的，是 Objective-C bridge 过来的。
```

### 析构（反初始化）deinit
我觉得跟 OC 中的 dealloc 方法差不多，因为没怎么又用到这方面的东西，如果你的 app 是从 iOS 8 起开始支持，需要手动的移除通知观察者（iOS 9开始不需要），我也只达到了在在 dealloc 或者 deinit 方法中移除通知者这一层面，如果后续有遇到更多问题，再来分享。具体细节可参考[官方文档](https://docs.swift.org/swift-book/LanguageGuide/Deinitialization.html)


### 结束
以上就是这篇文章的主要内容，如果大家对指定构造器和便捷构造器的调用关系比较混乱的话，可以参考这句话进行记忆归纳：
```
指定构造器总是向上代理
便利构造器总是横向代理
```
当然，如果在日后的学习过程中，还有遇到关于 Swift 构造器的相关好玩的事情，会持续更新哒~

### 相关链接
强烈推荐大家阅读完鄙人的内容后，再去仔细品读[箫神的文章](http://yulingtianxia.com/blog/2014/06/24/initialization-in-swift/)