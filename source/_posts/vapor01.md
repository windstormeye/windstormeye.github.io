---
title: 搞事情之 Vapor 初探
date: 2019-05-03 17:11:00
tags:
---

> 搞事情系列文章主要是为了继续延续自己的 “T” 字形战略所做，同时也代表着毕设相关内容的学习总结。本文是 `Vapor` 部分的第一篇，主要记录了第一次上手 `Swift` 最火的服务端框架 `Vapor` 所遇到的问题、思考和总结。

## 前言
从 `SwiftNIO` 开源后，之前对 `Swift Server Side` 完全不关心的我再也按耐不住了！尤其是还看到了[这篇文章](https://medium.com/@rymcol/benchmarks-for-the-top-server-side-swift-frameworks-vs-node-js-24460cfe0beb)，我相信这个文章肯定大部分同学都浏览过，看完后我也十分的激动，难道使用 `Swift` 统一前后端开发的日子就要到了吗？直到最近在毕设的“压迫”下，我才认认真真的学习使用 `Swift` 开发服务端。目前在 github 上 star 最多的是 `Vapor`，其次是 `Perfect`。

为什么选择 `Vapor`？
* 在 `2018 @Swift` 大会上虾神对 `Swift Serve Side` 做了一个 lightning talk，对 `Vapor` 十分赞扬；
* 陆陆续续看了网上的一些资料，发现大家对 `Vapor` 关注度也更高一些；
* `Vapor` 在语法和相关 `API` 的设计上会更加 `Swifty` 一些；
* github 上的所有 `Swift Sever Side` 框架中它的 `star` 是最多。

但是，在刚开始时估计是学校的网太破了，导致生成 `Xcode` 模版文件时真的是巨慢！！！有一次等了二十分钟，还失败了！中途切回了 `Perfect`，然后 `Perfect` 同样也有一些其它问题，又换回来。

## 开始
### 下载 `vapor`
[详见官网](https://docs.vapor.codes/3.0/install/macos/)。

### 运行 `Hello, world!`
* `vapor new yourProjectName`。创建模版工程，当然可以加上 `--template=api` 来创建提供对应服务的模版工程，但我测试了一下好像跟其它模版工程没什么区别。
* `vapor xcode`。创建 Xcode 工程，特别特别慢，而且会有一定几率失败。（估计是学校的网太破

### MVC —— M
`Vapor` 默认是 `SQLite` 的**内存**数据库。我原本想看看 `Vapor` 自带的 `SQLite` 数据库中的表，但没翻着，最后想了一下，这是内存数据库啊，也就是说，每次 `Run` 数据都会被清空。可以从 `config.swift` 中看出：

```swift
// ...
let sqlite = try SQLiteDatabase(storage: .memory)
// ...
```

在 `Vapor` 文档中写了推荐使用 `Fluent` ORM 框架进行数据库表结构的管理，刚开始我并不了解关于 `Fluent` 的任何内容，可以查看模版文件中的 `Todo.swift`：

```swift
import FluentSQLite
import Vapor


final class Todo: SQLiteModel {
    /// 唯一标识符
    var id: Int?
    var title: String

    init(id: Int? = nil, title: String) {
        self.id = id
        self.title = title
    }
}

/// 实现数据库操作。如增加表字段，更新表结构
extension Todo: Migration { }

/// 允许从 HTTP 消息中编解码出对应数据
extension Todo: Content { }

/// 允许使用动态的使用在路由中定义的参数
extension Todo: Parameter { }
```

从模版文件中的 `Model` 可以看出来创建一张表结构相当于是**描述一个类**，之前有使用过 `Django` 的经验，看到 `Vapor` 的这种 ORM 这么 `Swifty` 确实眼前一亮。`Vapor` 同样可以遵循 `MVC` 设计模式进行构建，在生成的模版文件中也确实是基于 `MVC` 去做的。


### MVC —— C
如果我们只使用 `Vapor` 做 `API` 服务，可以不用管 `V` 层，在 `Vapor` 的“视图”部分，使用的 `Leaf` 库做的渲染，具体细节因为没学习过不做展开。

而对于 `C` 来说，整体的思路跟以往写 App 时的思路大致相当，在 `C` 层中处理好数据和视图的关系，只不过此处只需要处理数据和数据之间的关系就好了。

```swift
import Vapor

/// Controls basic CRUD operations on `Todo`s.
final class TodoController {
    /// Returns a list of all `Todo`s.
    func index(_ req: Request) throws -> Future<[Todo]> {
        return Todo.query(on: req).all()
    }

    /// Saves a decoded `Todo` to the database.
    func create(_ req: Request) throws -> Future<Todo> {
        return try req.content.decode(Todo.self).flatMap { todo in
            return todo.save(on: req)
        }
    }

    /// Deletes a parameterized `Todo`.
    func delete(_ req: Request) throws -> Future<HTTPStatus> {
        return try req.parameters.next(Todo.self).flatMap { todo in
            return todo.delete(on: req)
        }.transform(to: .ok)
    }
}
```

从以上模版文件中生成的 `TodoController` 可以看出，大量结合了 `Future` 异步特性，初次接触会有点懵，有同学推荐结合 `PromiseKit` 其实会更香。


## 从 `SQLite` 到 `MySQL`
为什么要换，原因很简单，不是 `SQLite` 不好，仅仅只是因为没用过而已。这部分 `Vapor` 官方文档讲的不够系统，虽然都点到了但是过于分散，而且感觉 `Vapor` 的文档是不是跟 Apple 学了一套，细节都不展开，遇到一些字段问题得亲自写下代码，然后看实现和注释，不写之前很难知道在描述什么。

### `Package.swift`
在 `Package.swift` 中写下对应库依赖，

```swift
import PackageDescription

let package = Package(
    name: "Unicorn-Server",
    products: [
        .library(name: "Unicorn-Server", targets: ["App"]),
    ],
    dependencies: [
        .package(url: "https://github.com/vapor/vapor.git", from: "3.0.0"),
        // here
        .package(url: "https://github.com/vapor/fluent-mysql.git", from: "3.0.0"),
    ],
    targets: [
        .target(name: "App",
                dependencies: [
                    "Vapor",
                    "FluentMySQL"
            ]),
        .target(name: "Run", dependencies: ["App"]),
        .testTarget(name: "AppTests", dependencies: ["App"])
    ]
)
```

触发更新

```shell
vapor xcode
```

`Vapor` 搞了我几次，更新依赖的时候特别慢，而且还更新失败，导致我现在每次更新时都要去确认一遍依赖是否更新成功。

### 更新 ORM
更新成功后，我们就可以根据之前生成的模版文件 `Todo.swift` 的样式改成 `MySQL` 版本的 ORM：

```swift
import FluentMySQL
import Vapor

/// A simple user.
final class User: MySQLModel {
    /// The unique identifier for this user.
    var id: Int?
    
    /// The user's full name.
    var name: String
    
    /// The user's current age in years.
    var age: Int
    
    /// Creates a new user.
    init(id: Int? = nil, name: String, age: Int) {
        self.id = id
        self.name = name
        self.age = age
    }
}

/// Allows `User` to be used as a dynamic migration.
extension User: Migration { }

/// Allows `User` to be encoded to and decoded from HTTP messages.
extension User: Content { }

/// Allows `User` to be used as a dynamic parameter in route definitions.
extension User: Parameter { }
```

以上是我新建的 User Model，换成 Todo Model 也是一样的。改动的地方只有两个，`import FluentMySQL` 和继承自 `MySQLModel`。这点还算不错，通过 `Fluent` 抹平了各种数据库的使用，不管你底层是什么数据库，都只需要导入然后切换继承即可。

### 修改 `config.swift`
```swift
import FluentMySQL
import Vapor

/// 应用初始化完会被调用
public func configure(_ config: inout Config, _ env: inout Environment, _ services: inout Services) throws {
    // === mysql ===
    // 首先注册数据库
    try services.register(FluentMySQLProvider())

    // 注册路由到路由器中进行管理
    let router = EngineRouter.default()
    try routes(router)
    services.register(router, as: Router.self)

    // 注册中间件
    // 创建一个中间件配置文件
    var middlewares = MiddlewareConfig()
    // 错误中间件。捕获错误并转化到 HTTP 返回体中
    middlewares.use(ErrorMiddleware.self)
    services.register(middlewares)
    
    // === mysql ===
    // 配置 MySQL 数据库
    let mysql = MySQLDatabase(config: MySQLDatabaseConfig(hostname: "", port: 3306, username: "", password: "", database: "", capabilities: .default, characterSet: .utf8mb4_unicode_ci, transport: .unverifiedTLS))

    // 注册 SQLite 数据库配置文件到数据库配置中心
    var databases = DatabasesConfig()
    // === mysql ===
    databases.add(database: mysql, as: .mysql)
    services.register(databases)

    // 配置迁移文件。相当于注册表
    var migrations = MigrationConfig()
    // === mysql ===
    migrations.add(model: User.self, database: .mysql)
    services.register(migrations)
}
```

注意 `MySQLDatabaseConfig` 的配置信息。如果我们的 `MySQL` 版本在 **8** 以上，目前只能选择 `unverifiedTLS` 进行验证连接MySQL容器时使用的安全连接选项，也即 `transport` 字段。在代码中用 `// === mysql ===` 进行标记的代码块是跟模版文件中使用 `SQLite` 所不同的地方。

### 运行
运行工程，进入 `MySQL` 进行查看。

```shell
mysql> show tables;
+----------------------+
| Tables_in_unicorn_db |
+----------------------+
| fluent               |
| Sticker              |
| User                 |
+----------------------+
3 rows in set (0.01 sec)

mysql> desc User;
+-------+--------------+------+-----+---------+----------------+
| Field | Type         | Null | Key | Default | Extra          |
+-------+--------------+------+-----+---------+----------------+
| id    | bigint(20)   | NO   | PRI | NULL    | auto_increment |
| name  | varchar(255) | NO   |     | NULL    |                |
| age   | bigint(20)   | NO   |     | NULL    |                |
+-------+--------------+------+-----+---------+----------------+
3 rows in set (0.01 sec)
```

`Vapor` 不像 `Django` 那般在生成的表加上前缀，而是你 ORM 类名是什么，最终生成的表名就是什么，这点很喜欢！

### 增加一个字段
`Vapor` 同样也没有像 `Django` 那么强大的工作流，很多人都说 `Perfect` 像 `Django`，我自己的认为 `Vapor` 像 `Flask`。

对 `Vapor` 修改表字段，不仅仅只是修改 `Model` 属性这么简单，同样也不像 `Django` 中修改完后，执行 `python manage.py makemigrations` 和 `python manage.py migrate` 就结束了，我们需要自己创建迁移文件，自己写清楚此次表结构到底发生了什么改变。

在泊学的[这篇文章](https://boxueio.com/series/vapor-fluent/ebook/473)中推荐在 `App` 目录下创建一个 `Migrations group`，方便操作。但我思考了一下，这么做势必会造成 `Model` 和对应的迁移文件割裂，然后在另外一个上级文件夹中又要对不同迁移文件所属的 `Model` 做切分，这很显然是有一些问题的。最后，我脑子冒出了一个非常可怕的想法：“`Django` 是一个非常强大、架构非常良好的框架！”。

最后我的目录是这样的：

```shell
Models
└── User
    ├── Migrations
    │   ├── 19-04-30-AddUserCreatedTime.swift
    │   └── 19-04-30-DeleteUserNickname.swift
    ├── UserController.swift
    └── User.swift
```

这是 `Django` 中的一个 `app` 文件树：
```shell
user_avatar
├── __init__.py
├── admin.py
├── apps.py
├── migrations
│   ├── 0001_initial.py
│   ├── 0002_auto_20190303_2154.py
│   ├── 0002_auto_20190303_2209.py
│   ├── 0003_auto_20190303_2154.py
│   ├── 0003_auto_20190322_1638.py
│   ├── 0004_merge_20190408_2131.py
│   └── __init__.py
├── models.py
├── tests.py
├── urls.py
└── views.py
```

已经删除掉了一些非重要信息。可以看到，`Django` 的 `app` 文件夹结构非常好！注意看 `migrations` 文件夹下的迁移文件命名。如果开发能力不错的话，我们是可以做到与业务无关的 `app` 发布供他人直接导入到工程中。

不过关于工程文件的管理，这是一个智者见智的事情啦～对于我个人来说，我反而更加喜欢 `Vapor`/`Flask` 一系，因为需要什么再加什么，整个设计模式也可以按照自己的喜好来做。

给 `User` Model 添加一个 `createdTime` 字段。
```swift
import FluentMySQL

struct AddUserCreatedTime: MySQLMigration {
    static func prepare(on conn: MySQLConnection) -> EventLoopFuture<Void> {
        return MySQLDatabase.update(User.self, on: conn, closure: {
            $0.field(for: \User.fluentCreatedAt)
        })
    }
    
    static func revert(on conn: MySQLConnection) -> EventLoopFuture<Void> {
        // 直接返回
        return conn.future()
    }
}
```

#### 删除一个字段
使用 `Swift` 开发服务端很容易受到使用 `Swift` 做其它开发的影响。刚开始时我确实认为在 `Model` 中把需要删除的字段删除就好了，然而运行工程后去查数据库发现并不是这么一回事。

首先，我们需要先创建一个文件来写 `Model` 的迁移代码，但这不是必须的，你可以把该 `Model` 后续需要进行表字段的 CURD 都写在同一个文件中，因为每一个迁移都是一个 `struct`。我的做法是像上文所说，对每一个迁移都做新文件，并且每一个迁移文件都写上“时间”和“做了什么”。

在 `prepare` 方法中调用 `DatabaseKit` 的 `create` 方法，`Fluent` 支持大部分数据库，且都基于 `DatabaseKit` 对支持的这些大部分数据库做了二次封装。

通过 `Fluent` 对表删除一个字段，需要在**增加表字段时就要做好**，否则需要重新写一个迁移文件，例如，我们可以把上文代码中的 `revert` 方法改为：

```swift
static func revert(on conn: MySQLConnection) -> EventLoopFuture<Void> {
    return MySQLDatabase.update(User.self, on: conn, closure: {
        $0.deleteField(for: \User.fluentCreatedAt)
    })
}
```

如果此时我们直接运行工程，是不会有任何效果的，因为直接运行工程并不会触发 `revert` 方法，我们需要激活 `Vapor` 两个命令，在 `config.swift` 中：

```swift
var commands = CommandConfig.default()
commands.useFluentCommands()
services.register(commands)
```

接着，在终端中输入：` vapor build && vapor run revert` 即可撤销上一次新增的字段。使用 ` vapor build && vapor run revert  -all` 可以撤销全部生成的表。

问题来了！当我的 `revert` 方法中写明当撤销迁移时，把表进行删除，一切正常。
```swift
return MySQLDatabase.delete(User.self, on: conn)
```

但如果我要执行当撤销迁移时，把表中 `fluentCreatedAt` 字段删除时，失败！！！搞了 N 久也没有成功，几乎翻遍了网上所有内容，也没法解决，几乎都是这么写然后执行撤回迁移命令就生效了。

如果我们从 `Model` 中已经提前删除掉了需要移除的字段，那么在 `migrations` 中，这个字段就没法被索引，因为已经被移除了，那么就无法被 `deleteField`。最终我的解决办法是，因为这个字段已经不需要了，那么直接写 SQL 删除掉这个字段。

隐约觉得，这不是 `Vapor` 的最佳实践。

### 修改一个表字段
暂留。


## Auth
在 `Vapor` 中有两种对用户鉴权的方式。一为适用 `API` 服务的 `Stateless` 方式，二为适用于 `Web` 的 `Sessions`，

### 添加依赖
```swift
// swift-tools-version:4.0
import PackageDescription

let package = Package(
    name: "Unicorn-Server",
    products: [
        .library(name: "Unicorn-Server", targets: ["App"]),
    ],
    dependencies: [
        .package(url: "https://github.com/vapor/vapor.git", from: "3.0.0"),
        .package(url: "https://github.com/SwiftyJSON/SwiftyJSON.git", from: "4.0.0"),
        .package(url: "https://github.com/vapor/fluent-mysql.git", from: "3.0.0"),
        // 添加 auth
        .package(url: "https://github.com/vapor/auth.git", from: "2.0.0"),
    ],
    targets: [
        .target(name: "App",
                dependencies: [
                    "Vapor",
                    "SwiftyJSON",
                    "FluentMySQL",
                    // 添加 auth
                    "Authentication"
            ]),
        .target(name: "Run", dependencies: ["App"]),
        .testTarget(name: "AppTests", dependencies: ["App"])
    ]
)
```

执行 `vapor xcode` 拉取依赖并重新生成 `Xcode` 工程。

### 注册
在 `config.swift` 中增加：

```swift
public func configure(_ config: inout Config, _ env: inout Environment, _ services: inout Services) throws {
    // ...

    try services.register(AuthenticationProvider())
    
    // ...
}
```

### Basic Authorization
简单来说，该方式就是验证密码。我们需要维护一个做 `Basic Authorization` 方式进行鉴权的 `Path` 集合。请求属于该集合中的 `Path` 时，都需要把用户名和密码用 `:` 进行连接成新的字符串，且做 `base64` 加密，例如，`username` 为 `pjhubs`，`password` 为 `pjhubs123`，则，拼接后的结果为 `pjhubs:pjhubs123`，加密完的结果为 `cGpodWJzOnBqaHViczEyMw==`。按照如下格式添加到每次发起 `HTTP` 请求的 `header` 中：

```
Authorization: Basic cGpodWJzOnBqaHViczEyMw==
```

### Bearer Authorization
当用户登录成功后，我们应该返回一个完整的 `token` 用于标识该用户已经在我们系统中登录且验证成功，并让该 `token` 和用户进行关联。使用 `Bearer Authorization` 方式进行权限验证，我们需要自行生成 `token`，可以使用任何方法进行生成，`Vapor` 官方并没有提供对应的生成工具，只要能够保持全局唯一即可。每次进行 `HTTP` 请求时，把 `token` 按照如下格式直接添加到 `HTTP request` 中，假设此次请求的 `token` 为 `pxoGJUtBVn7MXWoajWH+iw==`，则完整的 `HTTP header` 为：

```
Authorization: Bearer pxoGJUtBVn7MXWoajWH+iw==
```

### 创建 `Token` Model
```swift
import Foundation
import Vapor
import FluentMySQL
import Authentication


final class Token: MySQLModel {
    var id: Int?
    var userId: User.ID
    var token: String
    var fluentCreatedAt: Date?
    
    init(token: String, userId: User.ID) {
        self.token = token
        self.userId = userId
    }
}

extension Token {
    var user: Parent<Token, User> {
        return parent(\.userId)
    }
}

// 实现 `BearerAuthenticatable` 协议，并返回绑定的 `tokenKey` 以告知使用 `Token` Model 的哪个属性作为真正的 `token`
extension Token: BearerAuthenticatable {
    static var tokenKey: WritableKeyPath<Token, String> { return \Token.token }
}

extension Token: Migration { }
extension Token: Content { }
extension Token: Parameter { }

// 实现 `Authentication.Token` 协议，使 `Token` 成为 `Authentication.Token`
extension Token: Authentication.Token {
    // 指定协议中的 `UserType` 为自定义的 `User`
    typealias UserType = User
    // 置顶协议中的 `UserIDType` 为自定义的 `User.ID`
    typealias UserIDType = User.ID
    
    // `token` 与 `user` 进行绑定
    static var userIDKey: WritableKeyPath<Token, User.ID> {
        return \Token.userId
    }
}

extension Token {
    /// `token` 生成
    static func generate(for user: User) throws -> Token {
        let random = try CryptoRandom().generateData(count: 16)
        return try Token(token: random.base64EncodedString(), userId: user.requireID())
    }
}
```

### 添加配置
在 `config.swift` 中写下 `Token` 的配置信息。
```swift
migrations.add(model: Token.self, database: .mysql)
```

### 修改 `User` Model
让 `User` 和 `Token` 进行关联。

```Swift
import Vapor
import FluentMySQL
import Authentication

final class User: MySQLModel {
    var id: Int?
    var phoneNumber: String
    var nickname: String
    var password: String
    
    init(id: Int? = nil,
         phoneNumber: String,
         password: String,
         nickname: String) {
        self.id = id
        self.nickname = nickname
        self.password = password
        self.phoneNumber = phoneNumber
    }
}

extension User: Migration { }
extension User: Content { }
extension User: Parameter { }

// 实现 `TokenAuthenticatable`。当 `User` 中的方法需要进行 `token` 验证时，需要关联哪个 Model
extension User: TokenAuthenticatable {
    typealias TokenType = Token
}

extension User {
    func toPublic() -> User.Public {
        return User.Public(id: self.id!, nickname: self.nickname)
    }
}

extension User {
    /// User 对外输出信息，因为并不想把整个 `User` 实体的所有属性都暴露出去
    struct Public: Content {
        let id: Int
        let nickname: String
    }
}

extension Future where T: User {
    func toPublic() -> Future<User.Public> {
        return map(to: User.Public.self) { (user) in
            return user.toPublic()
        }
    }
}
```

### 路由方法
使用 `Basic Authorization` 方式做用户鉴权后，我们就可以把需要使用鉴权的方法和非鉴权的方法按照如下方式在 `UserController.swift` 文件分开进行路由，如果这个文件你没有，需要新建一个。

```swift
import Vapor
import Authentication

final class UserController: RouteCollection {
    
    // 重载 `boot` 方法，在控制器中定义路由
    func boot(router: Router) throws {
        let userRouter = router.grouped("api", "user")
        
        // 正常路由
        let userController = UserController()
        router.post("register", use: userController.register)
        router.post("login", use: userController.login)
        
        // `tokenAuthMiddleware` 该中间件能够自行寻找当前 `HTTP header` 的 `Authorization` 字段中的值，并取出与该 `token` 对应的 `user`，并把结果缓存到请求缓存中供后续其它方法使用
        // 需要进行 `token` 鉴权的路由
        let tokenAuthenticationMiddleware = User.tokenAuthMiddleware()
        let authedRoutes = userRouter.grouped(tokenAuthenticationMiddleware)
        authedRoutes.get("profile", use: userController.profile)
        authedRoutes.get("logout", use: userController.logout)
        authedRoutes.get("", use: userController.all)
        authedRoutes.get("delete", use: userController.delete)
        authedRoutes.get("update", use: userController.update)
    }

    func logout(_ req: Request) throws -> Future<HTTPResponse> {
        let user = try req.requireAuthenticated(User.self)
        return try Token
            .query(on: req)
            .filter(\Token.userId, .equal, user.requireID())
            .delete()
            .transform(to: HTTPResponse(status: .ok))
    }
    
    func profile(_ req: Request) throws -> Future<User.Public> {
        let user = try req.requireAuthenticated(User.self)
        return req.future(user.toPublic())
    }
    
    func all(_ req: Request) throws -> Future<[User.Public]> {
        return User.query(on: req).decode(data: User.Public.self).all()
    }
    
    func register(_ req: Request) throws -> Future<User.Public> {
        return try req.content.decode(User.self).flatMap({
            return $0.save(on: req).toPublic()
        })
    }
    
    func delete(_ req: Request) throws -> Future<HTTPStatus> {
        return try req.parameters.next(User.self).flatMap { todo in
            return todo.delete(on: req)
            }.transform(to: .ok)
    }
    
    func update(_ req: Request) throws -> Future<User.Public> {
        return try flatMap(to: User.Public.self, req.parameters.next(User.self), req.content.decode(User.self)) { (user, updatedUser) in
            user.nickname = updatedUser.nickname
            user.password = updatedUser.password
            return user.save(on: req).toPublic()
        }
    }
}
```

需要注意的是，如果某个路由方法需要从 `token` 关联的用户取信息才需要 `let user = try req.requireAuthenticated(User.self)` 这行代码取用户，否则如果我们仅仅只是需要对某个路由方法进行鉴权，只需要加入到 `tokenAuthenticationMiddleware` 的路由组中即可。

并且， 我们不需要传入当前登录用户有关的任何信息，仅仅只需要一个 `token` 即可。

### 修改 `config.swift`
最后，把我们实现了 `RouteCollection` 协议的 `userController` 加入到 `config.swift` 中进行路由注册即可。

```swift
import Vapor

public func routes(_ router: Router) throws {
    // 用户路由
    let usersController = UserController()
    try router.register(collection: usersController)
}
```

## 修改 server 默认端口号 
在 `config.swift` 中注册 `NIOServerConfig` 服务。例如如下所示，我修改为了 `8001`

```swift
let myService = NIOServerConfig.default(port: 8001)
services.register(myService)
```

## 后记
感觉当一些设计模式的 tips 杂糅在一起后，就特别像 `Django`。但是和 `Django` 又有很大的不同，在一些细节上 `Vapor` 处理的不够好，看得云里雾里的，文档不够简单明了，或许，老外都这样？

在这次的学习当中，心中冒出了很多次“为什么我要用这个破东西？”，但每次冒出这个想法时，最后都忍住了，因为这可是 `Swift` 啊！

github 地址：[Unicorn-Server](https://github.com/windstormeye/Unicorn-Server)