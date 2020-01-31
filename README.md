# Chatroom
计算机网络课程pj，基于socket的网络聊天室。

## 环境
* python 3.7
* tkinter

## 运行方法
* 初始化数据库,执行```database.py```文件中的```init_database()```函数
* 启动客户端
  ```python server.py```
* 再启动服务端
  ```python client.py```
  服务端可并行，可开启多个服务端

## 功能 version2.0
目前已经实现的功能有：

- [x] 所有界面使用tkinter
- [x] 所有用户信息、聊天信息、好友关系、好友间私聊信息存储于sqlite数据库中
- [x] 用户可以注册账号、登陆
- [x] 一台电脑可以同时登陆多个用户
- [x] 登陆后即进入多人群聊界面，支持多人群聊
- [x] 多人群聊可发送文本信息、表情符号(emoji)、文件(不超过50M）
- [x] 多人群聊显示最近**5**条聊天记录和所有已经传送的文件
- [x] 多人群聊显示所有在线用户
- [x] 新用户加入或退出多人聊天室时有提醒
- [x] 多人聊天室信息颜色三类，分别显示**用户自己发送的消息**，**系统消息**，**其他用户发送的消息**
- [x] 用户可下载所有其他用户上传的文件
- [x] 用户可通过输入好友名的方式添加好友
- [x] 好友间可以私聊，所有私聊信息缓存
- [x] 添加好友时被添加方若在线，收到消息提示
- [x] 好友间私聊时，另一方若在线，自动弹出聊天界面

## 协议设计
**客户端**

 编号 | 助记符 | 消息体格式 | 应用场景 
-|-|-|-
 1 | LOGIN | ``` str(LOGIN) + username + "\r\n" + pwd ``` | 用户登陆 
 2 | REGISTER | ``` str(REGISTER) + user + "\r\n" + pwd ``` | 用户注册 
 3 | SEND_MESSAGE | **header** :```str(SEND_MESSAGE) + "\r\n" + str(len(text))```, **content**:```send_text``` | 多人群聊中用户发送消息
 4 | GET_ALL_USERS | ```str(GET_ALL_USERS)``` | 登陆多人聊天室后获得当前所有在线用户 
 5 | GET_ALL_CHAT_HISTORY | ```str(GET_ALL_CHAT_HISTORY) + username``` | 登陆多人聊天室后获得所有历史聊天记录 
 6 | SEND_EMOJI | **header** :```str(SEND_EMOJI) + "\r\n" + str(len(emoji))```,**content**: ```emoji``` | 多人群聊中用户发送表情符号 
 7 | SEND_FILE | **header** : ```file_info = str(SEND_FILE) + receiver + "\r\n" + filename + "\r\n" +str(file_size)```, **content** : ```file content``` | 多人群聊中用户发送文件 
 8 | GET_ALL_FILE_HISTORY | ```str(GET_ALL_FILE_HISTORY)``` | 登陆多人聊天室后获得所有发送文件的历史记录 
 9 | ADD_FRIEND | **header**:```str(ADD_FRIEND)```,**content**:```source_user+"\r\n"+target_user``` | 添加好友
 99 | DOWNFILE | **header**:```str(DOWNFILE)```,**content**:```username+"\r\n"+filename``` | 用户下载任意多人群聊中已经上传的文件
 98 | PRIVATE_INIT | **header**:```str(PRIVATE_INIT) + username + "\r\n" + friend_name``` | 获得用户与```friend_name```间的所有聊天记录
 0 | SHOW_ALL_FRIENDS | **header**:```str(SHOW_ALL_FRIENDS)```,**content**:```username``` | 获得用户所有好友名


**服务端**

 编号 | 助记符 | 应用场景 
 -|-|-
 101 | LOGIN_SUCCESS | 用户登录成功
 102 | LOGIN_WRONG_PWD | 用户登录时密码错误
 103 | LOGIN_ACCOUNT_NOT_EXIST | 用户登录时账号不存在
 104 | LOGIN_DUPLICATE |登陆时账号重复
 105 | LOGIN_USERNAME | 用户登录时以广播方式通知所有其他用户
 201 | REGISTER_SUCCESS | 注册新账号成功
 202 | REGISTER_ERROR | 注册新账号失败
 301 | SEND_MESSAGE_ALL | 多人聊天室中发送消息成功
 302 | SEND_MESSAGE_ERROR | 多人聊天室中发送消息失败
 303 | SEND_MESSAGE_PER | 好友间私聊时对方在线，成功发送消息
 304 | SEND_MESSAGE_PER_STORE | 好友间私聊时对方不在线，消息缓存到双方的聊天记录中
 404 | GET_USERS_ERROR | 获取所有在线用户的用户名失败
 401 | GET_SUCCESS | 成功获取所有在线用户的用户名
 501 | RET_HISTORY_SUCCESS | 成功获取多人聊天室中所有聊天记录
 502 | RET_HISTORY_ERROR | 获取多人聊天室中所有聊天记录失败
 601 | SEND_EMOJI_SUCCESS | 成功发送表情符号
 602 | SEND_EMOJI_ERROR | 发送表情符号失败
 701 | SEND_FILE_SUCCESS | 成功发送文件
 702 | SEND_FILE_ERROR | 发送文件失败
 801 | RET_ALL_FILES_SUCCESS | 成功获取所有发送的文件名
 802 | RET_ALL_FILES_ERROR | 获取所有发送的文件名失败
 800 | LOGOUT_INFO | 用户登出时以广播方式通知所有其他用户
 901 | ADD_FRIEND_SUCCESS | 成功添加好友 
 902 | ALREADY_ADD_ERROR | 添加好友错误：与对方已经是好友关系
 903 | USERNAME_NOT_EXIST | 添加好友错误：输入的用户名不存在
 904 | ADD_FRIEND_ERROR | 添加好友错误：其他异常错误
 905 | ADD_FRIEND_REMIND | 新好友提示：在线时收到其他用户的好友请求
 290 | DOWNFILE_SUCCESS | 成功下载多人群聊中的文件
 291 | DOWNFILE_ERROR | 下载多人群聊中的文件失败
 292 | PRIVATE_INIT_SUCCESS | 成功获得用户与某一好友所有聊天记录
 293 | PRIVATE_INIT_NONE | 用户与某一好友间聊天记录为空
 294 | PRIVATE_INIT_ERROR | 获取用户与某一好友所有聊天记录发送错误
 295 | SHOW_FRIENDS_SUCCESS | 成功获取用户的所有好友名
 296 | SHOW_FRIENDS_ERROR | 获取用户的所有好友发生错误
 297 | NO_FRIENDS | 用户暂无好友


 在设计的时候不足之处
 * 复用性考虑不足
 
   用户登陆成功后，需要首先获得聊天记录信息缓存、所有文件、该用户所有好友、与好友间聊天记录，
   这些是分别用**多个服务端请求**实现。其实可以**简化为一个请求**
 * 安全性考虑不足。
   * 尚未实现协议加密
   * 数据完整性缺乏考虑。即便有的协议在头部包括了数据长度，在接受时也未判断接受的数据长度与实际长度是否一致。
   * 数据库中聊天记录未加密


## 整体架构
### 数据库关系模式
* 用户信息 - 用户名、密码
  ```sql
     CREATE TABLE USERINFO
       (USERNAME TEXT PRIMARY KEY NOT NULL,
       PASSWORD TEXT NOT NULL);
  ```
  
* 聊天信息 - ID、发送方、时间、内容
  ```sql
     CREATE TABLE GROUP_CHAT_HISTORY
         ( ID TEXT PRIMARY KEY NOT NULL,
           SOURCE_USER TEXT NOT NULL,
           TIME DATETIME NOT NULL,
           CONTENT TEXT NOT NULL,
           FOREIGN KEY ("source_user") REFERENCES userinfo("username")
         );
   ```

* 文件信息 - ID、发送方、时间、文件名、文件内容
  ```sql
     CREATE TABLE GROUP_FILE_HISTORY
        (ID TEXT PRIMARY KEY NOT NULL,
         SOURCE_USER TEXT NOT NULL,
         TIME DATETIME NOT NULL,
         FILENAME TEXT NOT NULL,
         FILECONTENT TEXT NOT NULL,
         FOREIGN KEY ("source_user") REFERENCES userinfo("username")
         );
  ```

* 好友关系 - 用户1，用户2
  ```sql
  CREATE TABLE FRIENDS
    ( USERNAME1 TEXT NOT NULL,
      USERNAME2 TEXT NOT NULL,
      PRIMARY KEY (USERNAME1,USERNAME2),
      FOREIGN KEY ("username1") REFERENCES userinfo("username")
      FOREIGN KEY ("username2") REFERENCES userinfo("username")
    )
  ```
  
*  好友间聊天记录 - ID、发送方、接收方、时间、内容
   ```sql
   CREATE TABLE HISTORY_PRIVATE_CHAT
    ( "id" INTEGER not NULL,
      "target_user" TEXT not NULL,
      "source_user" TEXT not NULL,
      "time" DATETIME not NULL,
      "text" TEXT not NULL,
      PRIMARY KEY("id"),
      FOREIGN KEY ("target_user") REFERENCES "userinfo"("username")
      FOREIGN KEY ("source_user") REFERENCES "userinfo"("username")
    );
   ```

 
 ### socket通信
 ``` method.py ```中包含以下socket方法
 * send - 发送消息（utf-8编码）格式，参数为socket, 消息头部, 消息内容
   ```python
   def send(socket,header,msg = b""):
    byte_msg = bytes(header+"\n\n",encoding = 'utf-8') + msg
    socket.sendall(byte_msg)
   ```

* receive - 接收消息，根据```\n\n```分割头部和消息，utf-8解码后返回
  ```python
  def receive(sock):
    data = sock.recv(1024)
    for i in range(len(data)-1):
        if data[i] == 10 and data[i+1] == 10 : #"\n\n"分割头部和消息
            header = data[:i].decode("utf-8")
            rest = data[i+2:].decode("utf-8")
            return header, rest
    return data.decode("utf-8"),""
  ```
  
* 文件处理
  * **read_file(file_path)** 读取文件
  * **upload_file(sock,file_path,receiver)** 发送文件信息
  

### 服务端逻辑
* 监听多个连接
  ```python
    reads, writes, errors = select.select(connections,[],[])
    for cur in reads:
        if cur == sock: #new connection
              ···
        else : # old connection
              ···
              try :
                   data, rest = receive(cur)
               except Exception as e:
                    release(cur) # release this connection
                    continue
               handle(cur,data,rest) # handle client's request
   ```

* handle函数处理
  对消息头部进行分割，判断消息类型并进行相应处理
  ```python
  def handle(conn, msg, rest):
    state = ""
    try:
        type = int(msg[0])
    except Exception as e:
        print("!! wrong request",e)
        send(conn,str(WRONG_MESSAGE))
        return

    if type == REGISTER:
       ···
    elif type == LOGIN:
       ···
    ···   

  ```

### 客户端逻辑
用户端开启时进入登陆界面，第一次进入欢迎界面时，与服务端连接并建立会话.登陆成功后，开启监听服务端发来的数据。
 ```python
 sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        sock.connect((HOST,PORT))
        print(sock)
    except:
        print("Fail to connect (%s,%s)"%(HOST,PORT))
 ```
* 初始化界面为登陆，可选择 **登陆** / **注册**
* 登陆成功后初始化
  * 获取所有在线用户
  * 获取所有历史聊天记录
  * 获取所有历史发送文件
  * 获取该用户所有好友
  * 获取该用户与好友间聊天记录
* 开启服务端数据监听
  ```python
  _thread.start_new_thread(listener,(sock,window))
  ```
  其中```listener```函数与```handle``` 类似，针对不同协议编号进行处理
  
  ```python
  def listener(sock,root):
    print("?? then ??")
    listen_this = [sock]

    while True:
        reads, writes, errors = select.select(listen_this,[],[])
                    ···
                msg_type = data[:3]
                if msg_type == str(LOGIN_USERNAME):
                  ···
                elif msg_type == str(SEND_MESSAGE_ALL):
                  ···
      ······              
  ```

### 文件结构

```xml-dtd
└  client.py    % 客户端
└  server.py    % 服务端
└  constant.py  % 协议编号
└  method.py    % socket方法，包括send\receive等
└  events.py    % 客户端部分事件函数
└  database.py  % 数据库操作函数
```


## 运行截图
* 运行 ```client.py``` 初始界面
 ![welcome](https://github.com/WxxShirley/Chatroom/blob/master/imgs/welcome.png)
 
* 点击注册
 ![register](https://github.com/WxxShirley/Chatroom/blob/master/imgs/register.png)
 
* 多人聊天室主界面
  * 显示多人群聊中的近**5**条聊天聊天信息，系统消息（其他用户登陆/登出），其他用户发送的消息，以不同颜色区分
  * 多人聊天室可传送文件、表情符号、文本
    * tkinter无法显示emoji，因此我采用诸如 **[emoji-cake]** 的形式来表征一个emoji，目前可以发送的emoji较少，后期会再拓展。
  * 以列表```Listbox```形式显示
    * 当前所有在线用户
      * 随着**其他用户的登录/登出**而更新
    * 该用户所有好友
      * 点击“+”即可添加新好友
      * 随其他用户增加该用户为好友/该用户添加新好友而更新
      * 双击好友名可展开私聊
    * 所有多人群聊中已传送的文件
      * 用户双击文件名即可下载
      * 随用户上传新文件而更新 
  ![main_page](https://github.com/WxxShirley/Chatroom/blob/master/imgs_v2.0/mainPage.png)
 
* 添加好友
  * 用户输入想要添加好友的用户名，如果添加成功、另一方恰好在线，双方都有消息提示
  * 否则根据 **用户名不存在** 、 **已经是好友关系** 、 **其他异常错误** 等发送错误信息给用户
  ![add_friend1](https://github.com/WxxShirley/Chatroom/blob/master/imgs_v2.0/add_friend1.png)
  ![add_friend2](https://github.com/WxxShirley/Chatroom/blob/master/imgs_v2.0/add_friend2.png)
  ![add_friend3](https://github.com/WxxShirley/Chatroom/blob/master/imgs_v2.0/add_friend3.png)

* 好友间私聊
  * 双击好友名即可开始私聊
  * 目前仅支持文本信息
  * 所有聊天记录缓存
  * 若私聊的另一方也在线，发送私聊信息后另一方也会弹出对话信息
  ![friend_chat](https://github.com/WxxShirley/Chatroom/blob/master/imgs_v2.0/private_chat.png)
  ![friend_chat1](https://github.com/WxxShirley/Chatroom/blob/master/imgs_v2.0/private_chat2.png)
  ![friend_chat2](https://github.com/WxxShirley/Chatroom/blob/master/imgs_v2.0/private_chat3.png)

* 文件下载
  * 双击文件名即可下载
  ![dowfile](https://github.com/WxxShirley/Chatroom/blob/master/imgs_v2.0/down_file.png)
  
  
  
## 未来工作
待完善的功能 
- [ ] 创建群组，实现群聊
 
 
