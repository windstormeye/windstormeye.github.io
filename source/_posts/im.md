---
title: 搞事情之如何快速完成 IM 
date: 2019-04-26 15:21:20
tags:
- 即时通讯
- iOS
- 搞事情系列
---

> 搞事情系列文章主要是为了继续延续自己的 “T” 字形战略所做，同时也代表着毕设相关内容的学习总结。本文章是快速对接即时通讯完成需求，主要是记录在集成即时通讯的过程中遇到的一些问题和总结。

## 前言
接入即时通讯是大一的比赛作品“[大学+](https://github.com/windstormeye/CampusPlus)”，当时和另外一个小伙伴一起写下第一行代码，到靠着这个作品砍下了一些小奖，同时也让当时的自己快速的入门了与 iOS 开发相关一部分内容。

现在要在毕设中同样接入 IM，调研了目前比较流行的 IM 服务提供商后，最终选择了**融云**负责即时聊天业务。在调研的过程中除了能够提供稳定的基础聊天服务，最好还要有个 `UIKit`，因为自己的时间并不多，想着直接在 IM 服务提供商所带的 `UIKit` 做二次开发。

## IM 服务提供商调研
### 阿里云
不知为何，我对阿里云的产品总是提不起来兴趣。最开始是接入了阿里云短信做验证码，在对接的过程中我不是很喜欢阿里云的做法，阿里云短信的 server SDK 只提供一个跟运营商的通道，至于短信验证码的内容，需要我们自己做维护，包括验证码的生成、匹配和过期。

而相对我之前一直在使用 mob 来说，同样可以选择 client 触发短信验证码的发送，而 server 要做的事情仅仅只是匹配而已，不需要对验证码的生成和过期做处理。

当然这一点看法智者见智，对于我个人来说，短信验证码并不是核心业务，虽然整个对接过程也不复杂，但整体情况对比来看我不是很舒服。最重要的是如果你要测试阿里云短信必须得先充钱，这其实就陷入了一个死循环“我的逻辑还没跑通，凭什么先交钱？不交钱怎么开通服务？”，一条短信虽然也没几个钱，但确实会让人不太爽。反观 mob 提供了开发环境每天 20 条免费短信用于测试。

经过接入阿里云短信的过程后，我对阿里云系产品就失去了兴趣，包括阿里云通信。

### 腾讯云
在调研腾讯云 IM 的过程中，官网上的这句宣传语真是直击内心。

> 腾讯是国内最大也是最早的即时通讯开发商，QQ 和微信已经成为每个互联网用户必不可少的应用。现在，腾讯将高并发、高可靠的即时通讯能力进行开放，开发者可以很容易的根据腾讯提供的 SDK 将即时通讯功能集成入 App 中。

这还有什么好挑的？当时决定立马接入，其它不调研了。

#### 文档？？？
腾讯云通信的 iOS SDK 应该是去年 8 月份左右做了更新，感觉很踏实。当初始化完 `AppKey` 后准备接入“消息列表 VC”时我死活找不到官网文档上描述的类。

后来我怀疑估计是偶然问题，凭着自己的经验，猜出了正确的“消息列表 VC”类，并成功的初始化，接着开始对接“会话界面 VC”，也就是 `AddC2CController`，一开始 Xcode 并没有进行代码补全的提示，以为是 Xcode 本身的问题，开始的清缓存、重启 Xcode 等操作，把工程恢复到了最佳，可当我最后一次敲下 `AddC2CController` 时，依然没有提示。

翻了一遍 pods 中 `TUIKit` 中的所有类，惊奇的发现居然没有 `AddC2CController` 这个类！反复从官方文档中上下求索，可最终的结果是，我又凭着自己的经验找到了相似的类名，但初始化完成后，并不是我想要的结果，总不能把所有类都初始化一遍吧？

最后无法忍受，很不开心的发了工单。等待了一个星期后，文档依旧没有更新，我彻底放弃了。刚才又去看了一眼，嗯，依旧没有更新......


### 网易云信
个别大佬不推荐使用，据说要凉了，那我就算了吧。

### leanCloud
之前就听说了 leanCloud 全家桶很香。本来也打算上 leanCloud 全家桶，但粗略的文档看过去怎么好像都跟其云数据库绑定到了一起，跟之前大一时我和另外一个小伙伴不会写数据库，使用了当时比较火的云数据库提供商 Bmob 做法类似，再加上被前面腾讯云搞得有些疲惫了，对全新事物已经很难提起兴趣了，只想着能够越快解决这个问题就好。

### 融云
最后再三思考后，还是回到了融云上。刚开始也确实打算直接使用融云的 `UIKit`，但仔细对比了融云 `UIKit` 能够提供定制化的地方和 UI 设计图最终的效果差距甚远，遂放弃，准备只接入融云的核心通信库，使用第三方 IM UI 库完成。

## UI 库调研
最开始我是想省事直接用 IM 服务提供商的 `UIKit`，但在看过了腾讯云和融云提供的 UI 定制太局限了，而且不管怎么做，都很难复刻出跟设计图一样的效果。

![IM UI](https://i.loli.net/2019/04/26/5cc2e8be8f93b.png)

![IM UI](https://i.loli.net/2019/04/26/5cc2e8be9210d.png)

### MessagerKit
github 地址：[https://github.com/steve228uk/MessengerKit](https://github.com/steve228uk/MessengerKit)。

一开始看上了这个库，基本上把大部分功能都实现了，但是跟设计图上的一些细节还是有差距，比如说需要自己的做拓展支持语音、地图等自定义消息体、消息体框特殊圆角。这部分工作是清明节回家做的，整体上对接完成后其实还算 OK。

### MessageKit
直到有一天中午，突然看到了 [MessageKit](https://github.com/MessageKit/MessageKit) 这个库！几乎完成了所有功能，把我开心坏了！立马着手开始全部切换。

等到调好了一切细节后，发现这个库有一个坑爹的地方，点击输入框整个聊天界面的 `collectionView` 会上移一个固定距离，不管我怎么调，甚至把官方 demo 放到我的工程里也同样会出现这个问题，继续折腾了将近一个小时后，放弃了。无缘无故用户在点击输入框的时候整个聊天界面多往上移动大概 40px 的距离，不能忍。

### MessagerKit
嗯，我又换回来了 😅，最终决定还是用回第一次的库。来来回回将近三四天的时间都在切换这两个 UI 库上，基本上都是快写完了才发现有些奇怪的地方，然后全部推翻再重来。

## 接入融云
首先按照融云的官方文档进行账号的注册和应用的创建。拿到 `Appkey`，集成 `RongCloudIM/IMLib` 到工程中。

### 登录
官方文档并不推荐在客户端生成 `token` 进行融云 SDK 的登录，因为生成 `token` 的过程涉及到的 `AppSecret` 的固定，如果 app 被反编译则有极大可能导致泄漏。但是如果你心够大或者只是做个 demo 玩玩，在客户端本地请求生成 `token` 也不是不可以，以下是基于融云 server python sdk 的 `token` 生成代码：

```python
@decorator.request_methon('GET')
@decorator.request_check_args([])
def getRCToken(request):
    from rongcloud import RongCloud

    uid = request.GET.get('uid')
    nick_name = request.GET.get('nick_name')

    app_key = settings.RC_APP_KEY
    app_secret = settings.RC_APP_SECRET
    rcloud = RongCloud(app_key, app_secret)

    r = rcloud.User.getToken(userId=uid,
                             name=nick_name,
                             portraitUri='https://avatars0.githubusercontent.com/u/15074681?s=460&v=4')

    r_json = eval(str(r.response.content, encoding='utf-8'))
    if r_json['code'] == 200:
        json = {
            'token': r_json['token']
        }
        return utils.SuccessResponse(json, request)
    else:
        masLogger.log(request, 2333, str(r.response.content, encoding='utf-8'))
        return utils.ErrorResponse(2333, 'RCToken error', request)
```

在客户端上进行请求生成 `token` 的接口即可

### 发送消息
发送消息主要是使用如下方法：

```Objc
- (RCMessage *)sendMessage:(RCConversationType)conversationType
                  targetId:(NSString *)targetId
                   content:(RCMessageContent *)content
               pushContent:(NSString *)pushContent
                  pushData:(NSString *)pushData
                   success:(void (^)(long messageId))successBlock
                     error:(void (^)(RCErrorCode nErrorCode, long messageId))errorBlock;
```

关于该方法的使用在注释中已经写的很明白，我们需要做的就是把它进行一个封装，使其对外更好的使用：

```swift
/// 发送文本消息
func sendText(textString: String,
              userID: String,
              complateHandler: @escaping ((Int) -> Void),
              failerHandler: @escaping ((RCErrorCode) -> Void)) {
    let text = RCTextMessage(content: textString)
    RCIMClient.shared()?.sendMessage(.ConversationType_PRIVATE,
                                      targetId: userID,
                                      content: text,
                                      pushContent: nil,
                                      pushData: nil,
                                      success: { (mesId) in
                                        complateHandler(mesId)
    }, error: { (errorCode, mesId) in
        failerHandler(errorCode)
    })
}
```

以上为发送文本消息的方法。需要注意的是，在调用该方法之前必须确定要消息体的类型等前置条件，必须得先确定要发送的消息体类型来调用不同的方法，比如图片、语音和视频等，包括自定义消息体，地图等。

### 接收消息
关于消息的接收，融云并没有限制消息监听器的类型，只要你是 `NSObject` 子类就可以实现代理方法接收消息。所以，我把消息接收稍微封装了一下：

```swift
extension PJIM: RCIMClientReceiveMessageDelegate {
    func onReceived(_ message: RCMessage!, left nLeft: Int32, object: Any!) {
        print(message.objectName)
        switch message.objectName {
        case "RC:TxtMsg":
            let text = message.content as! RCTextMessage
            let m = Message(type: .text,
                            textContent: text.content,
                            audioContent: nil,
                            sendUserId: message.senderUserId,
                            msgId: message.messageId,
                            msgDirection: message.messageDirection,
                            msgStatus: message.sentStatus,
                            msgReceivedTime: message.receivedTime,
                            msgSentTime: message.sentTime)
            getMsg?(m)
            print(m.textContent!)
        case "RCImageMessage": break
        default: break
        }
    }
}
```

其中 `Message` 是我根据业务自建的一个结构体，因为 `RCMessage` 的属性太多了，很多都用不到，当然你也可以选择不封装：

```swift
extension PJIM {
    enum MessageType {
        case text
        case audio
    }
    
    struct Message {
        var type: MessageType
        var textContent: String?
        var audioContent: Data?
        var sendUserId: String
        var msgId: Int
        var msgDirection: RCMessageDirection
        var msgStatus: RCSentStatus
        var msgReceivedTime: Int64
        var msgSentTime: Int64
    }

    struct MessageListCell {
        var avatar: Int
        var nickName: String
        var uid: String
        var message: Message?
    }
}
```

至此，我们通过了两个方法就完成了消息的发送和接收～可以愉快的玩耍一番了！

### 获取消息列表
如果你是免费用户，那么从融云获取消息列表只是本地数据，如果用户更换了设备、重装了 app 等都**会导致消息列表的丢失**；如果你是收费用户，从融云服务器上拉取到的消息列表貌似**只有区区七天（再长也是多几天而已）**，所以如果对消息列表有追求的同学需要注意了。

我的消息列表还涉及到了用户信息的获取，这部分是异步请求，结合融云的同步获取本地消息列表，这就形成了一个异步操作保持顺序性的问题。为了到达“简洁”的操作，我只使用了“信号量”的方法完成。

```swift
/// 获取本地会话列表
func getConversionList(_ complateHandler: @escaping (([MessageListCell]) -> Void)) {
    let cTypes = [NSNumber(value: RCConversationType.ConversationType_PRIVATE.rawValue)]
    let cList = RCIMClient.shared()?.getConversationList(cTypes) as? [RCConversation]
    
    var msgListCells = [MessageListCell]()
    guard cList != nil else { return complateHandler(msgListCells)}
    
    if cList?.count != 0 {
        var cIndex = 0
        for c in cList! {
            let currentMessage = RCMessage(type: .ConversationType_PRIVATE,
                                            targetId: c.targetId,
                                            direction: c.lastestMessageDirection,
                                            messageId: c.lastestMessageId,
                                            content: c.lastestMessage)
            currentMessage?.sentTime = c.sentTime
            currentMessage?.receivedTime = c.receivedTime
            currentMessage?.senderUserId = c.senderUserId
            currentMessage?.sentStatus = c.sentStatus
            
            if currentMessage != nil {
                
                let message = getMessage(with: currentMessage!)
                if message == nil { break }
                
                // 获取用户信息，可以替换为你的，如果不需要获取用户信息，可以删除
                PJUser.shared.details(details_uid: c.targetId,
                                      getSelf: false,
                                      completeHandler: {
                                        let msgCell = MessageListCell(avatar: $0.avatar!,
                                                                      nickName: $0.nick_name!,
                                                                      uid: $0.uid!,
                                                                      message: message!)
                                        msgListCells.append(msgCell)
                                        
                                        if cIndex == cList!.count - 1 {
                                            var finalCells = [MessageListCell]()
                                            for cell in cList! {
                                                _ = msgListCells.filter({
                                                    if $0.uid == cell.targetId {
                                                        finalCells.append($0)
                                                        return true
                                                    }; return false
                                                })
                                            }
                                            
                                            complateHandler(finalCells)
                                        }
                                    
                                        cIndex += 1
                }) { print($0.errorMsg) }
            }
        }
    } else {
        complateHandler(msgListCells)
    }
}
```

### PJIM 
结合融云形成一个简单数据服务就写好了，通过单例在任何你想要进行消息的发送和接收，完整代码如下。其中有一部分是业务耦合较为严重的方法不方便展开，看着替换即可。

```swift
//
//  PJIM.swift
//  PIGPEN
//
//  Created by PJHubs on 2019/4/9.
//  Copyright © 2019 PJHubs. All rights reserved.
//

import Foundation

@objc class PJIM: NSObject {
    var getMsg: ((Message) -> Void)?
    
    private static let instance = PJIM()
    class func share() -> PJIM {
        return instance
    }
    
    override init() {
        super.init()
        RCIMClient.shared()?.setReceiveMessageDelegate(self, object: nil)
    }
    
    /// 发送文本消息
    func sendText(textString: String,
                  userID: String,
                  complateHandler: @escaping ((Int) -> Void),
                  failerHandler: @escaping ((RCErrorCode) -> Void)) {
        let text = RCTextMessage(content: textString)
        RCIMClient.shared()?.sendMessage(.ConversationType_PRIVATE,
                                         targetId: userID,
                                         content: text,
                                         pushContent: nil,
                                         pushData: nil,
                                         success: { (mesId) in
                                            complateHandler(mesId)
        }, error: { (errorCode, mesId) in
            failerHandler(errorCode)
        })
    }
    
    /// 获取本地会话列表
    func getConversionList(_ complateHandler: @escaping (([MessageListCell]) -> Void)) {
        let cTypes = [NSNumber(value: RCConversationType.ConversationType_PRIVATE.rawValue)]
        let cList = RCIMClient.shared()?.getConversationList(cTypes) as? [RCConversation]
        
        var msgListCells = [MessageListCell]()
        guard cList != nil else { return complateHandler(msgListCells)}
        
        if cList?.count != 0 {
            var cIndex = 0
            for c in cList! {
                let currentMessage = RCMessage(type: .ConversationType_PRIVATE,
                                               targetId: c.targetId,
                                               direction: c.lastestMessageDirection,
                                               messageId: c.lastestMessageId,
                                               content: c.lastestMessage)
                currentMessage?.sentTime = c.sentTime
                currentMessage?.receivedTime = c.receivedTime
                currentMessage?.senderUserId = c.senderUserId
                currentMessage?.sentStatus = c.sentStatus
                
                if currentMessage != nil {
                    
                    let message = getMessage(with: currentMessage!)
                    if message == nil { break }
                    
                    PJUser.shared.details(details_uid: c.targetId,
                                          getSelf: false,
                                          completeHandler: {
                                            let msgCell = MessageListCell(avatar: $0.avatar!,
                                                                          nickName: $0.nick_name!,
                                                                          uid: $0.uid!,
                                                                          message: message!)
                                            msgListCells.append(msgCell)
                                            
                                            if cIndex == cList!.count - 1 {
                                                var finalCells = [MessageListCell]()
                                                for cell in cList! {
                                                    _ = msgListCells.filter({
                                                        if $0.uid == cell.targetId {
                                                            finalCells.append($0)
                                                            return true
                                                        }; return false
                                                    })
                                                }
                                                
                                                complateHandler(finalCells)
                                            }
                                        
                                            cIndex += 1
                    }) { print($0.errorMsg) }
                }
            }
        } else {
            complateHandler(msgListCells)
        }
    }
    
    private func getMessage(with rcMessage: RCMessage) -> Message? {
        switch rcMessage.objectName {
            case "RC:TxtMsg":
                let text = rcMessage.content as! RCTextMessage
                let m = Message(type: .text,
                                textContent: text.content,
                                audioContent: nil,
                                sendUserId: rcMessage.senderUserId,
                                msgId: rcMessage.messageId,
                                msgDirection: rcMessage.messageDirection,
                                msgStatus: rcMessage.sentStatus,
                                msgReceivedTime: rcMessage.receivedTime,
                                msgSentTime: rcMessage.sentTime)
                return m
            case "RCImageMessage": break
            default: break
        }
        return nil
    }
}

extension PJIM: RCIMClientReceiveMessageDelegate {
    func onReceived(_ message: RCMessage!, left nLeft: Int32, object: Any!) {
        print(message.objectName)
        switch message.objectName {
        case "RC:TxtMsg":
            let text = message.content as! RCTextMessage
            let m = Message(type: .text,
                            textContent: text.content,
                            audioContent: nil,
                            sendUserId: message.senderUserId,
                            msgId: message.messageId,
                            msgDirection: message.messageDirection,
                            msgStatus: message.sentStatus,
                            msgReceivedTime: message.receivedTime,
                            msgSentTime: message.sentTime)
            getMsg?(m)
            print(m.textContent!)
        case "RCImageMessage": break
        default: break
        }
    }
}


extension PJIM {
    enum MessageType {
        case text
        case audio
    }
    
    struct Message {
        var type: MessageType
        var textContent: String?
        var audioContent: Data?
        var sendUserId: String
        var msgId: Int
        var msgDirection: RCMessageDirection
        var msgStatus: RCSentStatus
        var msgReceivedTime: Int64
        var msgSentTime: Int64
    }
    
    struct MessageListCell {
        var avatar: Int
        var nickName: String
        var uid: String
        var message: Message?
    }
}
```

## UI 
经过之前的一番调整，即时聊天的数据源都准备好了，接下来就是要画界面了。关于 UI 库的选择上文已经说明经过了几番折腾后，最终的选择是 [MessengerKit](https://github.com/steve228uk/MessengerKit)。因为 UI 实现都很普通，没什么可以做拓展的地方，以下是一些我任何值得关注的地方：

### ViewModel
融云提供的 `RCMessage` 类结构和 `MessengerKit` 所要求的数据类型不一样，需要我们单独针对 `MessengerKit` 做一个 `ViewModel` 喂食。

### 发送者和接收者
`MessengerKit` 聊天气泡的切换是根据“发送者”和“接收者”的 `id` 进行的，我们需要处理好从融云拉取过来的消息列表，根据“发送者” `id` 和“接受者” `id`（也即 `targetId`）进行分割为不同的 `section`，以下是我的处理过程：

```swift
private func didSetMessageCell() {
  // 如果有未读消息数，进入聊天后就全部已读
  let badge = RCIMClient.shared()!.getUnreadCount(.ConversationType_PRIVATE, targetId: messageCell!.uid)
  if (badge != 0) {
      RCIMClient.shared()!.clearMessagesUnreadStatus(.ConversationType_PRIVATE, targetId: messageCell!.uid)
      UIApplication.shared.applicationIconBadgeNumber -= Int(badge)
  }
  
  titleString = messageCell!.nickName
  friendUser = ChatUser(displayName: messageCell!.nickName,
                        avatar: UIImage(named: "\(messageCell!.avatar)"),
                        isSender: false)
  meUser = ChatUser(displayName: PJUser.shared.userModel.nick_name!,
                    avatar: UIImage(named: "\(PJUser.shared.userModel.avatar!)"),
                        isSender: true)
  
  func update(_ ms: [RCMessage]) {
      var m_index = 0
      var tempMsgs = [MSGMessage]()
      var tempMsgUserId = messageCell?.uid
      messages.append(tempMsgs)
      
      // 便利所有消息，按照 sendId 和 targetId 进行分离
      for m in ms {
          let text = m.content as! RCTextMessage
          if tempMsgUserId != m.senderUserId {
              tempMsgs.removeAll()
              messages.append(tempMsgs)
              m_index += 1
              tempMsgUserId = m.senderUserId
          }
          
          let c_m: MSGMessage?
          if m.senderUserId != PJUser.shared.userModel.uid! {
              c_m = MSGMessage(id: m.messageId,
                                body: .text(text.content),
                                user: friendUser!,
                                sentAt: Date(timeIntervalSince1970: TimeInterval(m.sentTime)))
          } else {
              c_m = MSGMessage(id: m.messageId,
                                body: .text(text.content),
                                user: meUser!,
                                sentAt: Date(timeIntervalSince1970: TimeInterval(m.sentTime)))
          }
          // 设置消息已读状态
          RCIMClient.shared()?.setMessageSentStatus(m.messageId, sentStatus: .SentStatus_READ)
          
          tempMsgs.insert(c_m!, at: 0)
          messages.insert(tempMsgs, at: m_index)
          messages.remove(at: m_index + 1)
      }
      
      messages.reverse()
  }
  
  let ms = RCIMClient.shared()?.getLatestMessages(.ConversationType_PRIVATE, targetId: messageCell?.uid, count: 30) as? [RCMessage]
  // 如果本地无消息，从融云服务器上拉取
  if ms != nil {
      update(ms!)
      DispatchQueue.main.async {
          // reloadData 时主线程被占用，scrollToBottom 等待，reloadData 完成后，再执行 scrollToBottom
          self.collectionView.reloadData()
          DispatchQueue.main.async {
              self.collectionView.scrollToBottom(animated: false)
          }
      }
  } else {
      // TODO: 这部分有问题，需要交钱才能拉取到服务器上的历史消息
      RCIMClient.shared()?.getRemoteHistoryMessages(.ConversationType_PRIVATE, targetId: PJUser.shared.userModel.uid!, recordTime: 0, count: 20, success: { (messages: [RCMessage]) in
              update(messages)
          } as? ([Any]?) -> Void, error: { (errorCode) in
              print(errorCode.rawValue)
      })
  }
}
```

## 消息推送
这部分融云文档写得很好了～记得在 Xcode 中把 `Background Modes` 的“远程推送”打开。·

## 总结
以上是我完成了一期 IM 过程中的思考和总结，解决问题的方法还有些许不足，吸取了之前的做其它产品的教训，本次严格遵循 “MVP” 的开发流程，小步快跑，一期工作主要是先跑起来，让其它小伙伴聊起来。
