# Chatroom
计算机网络课程pj，基于socket的网络聊天室。

## 环境
* python 3.7
* tkinter

## 运行方法
* 先启动客户端
  ```python server.py```
* 再启动服务端
  ```python client.py```
  服务端可并行，可开启多个服务端

## 功能 version1.0
目前已经实现的功能有：

- [x] 所有界面使用tkinter
- [x] 所有用户信息、聊天信息存储于sqlite数据库中
- [x] 用户可以注册账号、登陆
- [x] 一台电脑可以同时登陆多个用户
- [x] 登陆后即进入多人群聊界面，支持多人群聊
- [x] 多人群聊可发送文本信息、表情符号(emoji)、文件(不超过50M）
- [x] 多人群聊显示最近**5**条聊天记录和最近**5**个传送的文件
- [x] 多人群聊显示所有在线用户
- [x] 新用户加入或退出多人聊天室时有提醒
- [x] 多人聊天室信息颜色三类，分别显示**用户自己发送的消息**，**系统消息**，**其他用户发送的消息**

## 协议设计
**客户端**
| 编号 | 助记符 | 消息体格式 | 应用场景 |
| ---- | :------------: | :---------------------------------------------: | :-----------------------------------------------------: |
| 1 | LOGIN | ``` str(LOGIN) + username + "\r\n" + pwd ``` | 用户登陆 | 
| 2 | REGISTER | ``` str(REGISTER) + user + "\r\n" + pwd ``` | 用户注册 |
| 3 | SEND_MESSAGE | **header** :```str(SEND_MESSAGE) + "\r\n" + str(len(text))```, **content**:```send_text``` | 多人群聊中用户发送消息 |
| 4 | GET_ALL_USERS | ```str(GET_ALL_USERS)``` | 登陆多人聊天室后获得当前所有在线用户 |
| 5 | GET_ALL_CHAT_HISTORY | ```str(GET_ALL_CHAT_HISTORY) + username``` | 登陆多人聊天室后获得所有历史聊天记录 | 
| 6 | SEND_EMOJI | **header** :```str(SEND_EMOJI) + "\r\n" + str(len(emoji))```,**content**: ```emoji``` | 多人群聊中用户发送表情符号 |
| 7 | SEND_FILE | **header** : ```file_info = str(SEND_FILE) + receiver + "\r\n" + filename + "\r\n" +str(file_size)```, **content** : ```file content``` | 多人群聊中用户发送文件 |
| 8 | GET_ALL_FILE_HISTORY | ```str(GET_ALL_FILE_HISTORY)``` | 登陆多人聊天室后获得所有发送文件的历史记录 |

**服务端**
| 编号 | 助记符 | 消息题格式 | 应用场景 |
