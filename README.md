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

 在设计的时候不足之处
 * 拓展性考虑不足。如果将多人聊天拓展为**Group模式**和**私聊模式**，发送文件、消息、表情符号等协议能否与原有的大群组中协议复用
 * 安全性考虑不足。
   * 尚未实现协议加密
   * 数据完整性缺乏考虑。即便有的协议在头部包括了数据长度，在接受时也未判断接受的数据长度与实际长度是否一致。
   * 数据库中聊天记录未加密

## 整体架构
### 数据库关系模式
* 用户信息
  ```sql
     CREATE TABLE USERINFO
       (USERNAME TEXT PRIMARY KEY NOT NULL,
       PASSWORD TEXT NOT NULL);
  ```
  
* 聊天信息
  ```sql
     CREATE TABLE GROUP_CHAT_HISTORY
         ( ID TEXT PRIMARY KEY NOT NULL,
           SOURCE_USER TEXT NOT NULL,
           TIME DATETIME NOT NULL,
           CONTENT TEXT NOT NULL,
           FOREIGN KEY ("source_user") REFERENCES userinfo("username")
         );
   ```

* 文件信息
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
 
 ### socket通信
 ``` method.py ```中包含以下socket方法
 * send - 发送消息（utf-8编码）格式，参数为socket, 消息头部, 消息内容
   ```python
   def send(socket,header,msg = b""):
    """
    :param socket: socket sending message
    :param header: header flag, e.g. LOGIN 1 , LOGIN SUCCESS 101
    :param msg:    message content
    :return:
    """
    byte_msg = bytes(header+"\n\n",encoding = 'utf-8') + msg
    socket.sendall(byte_msg)

   ```

* receive - 接收消息，根据```\n\n```分割头部和消息，utf-8解码后返回
  ```python
  def receive(sock):
    data = sock.recv(1024)
    for i in range(len(data)-1):
        if data[i] == 10 and data[i+1] == 10 : #"\n\n"
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
  while True:
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
               handle(cur,data,rest)
   ```

* handle函数处理
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
  * 获取所有历史发送文件名
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
        for master in reads:
            if master == sock:
                try:
                    data, rest = method.receive(master)
                except Exception as e:
                    messagebox.showerror('Error','Receive Error!')
                    continue
                    
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
└ constant.py  % 协议编号
└ method.py    % socket方法，包括send\receive等
└ events.py    % 客户端部分事件函数
└ database.py  % 数据库操作函数
```

## 运行截图
* 运行 ```client.py``` 初始界面
 ![welcome](https://github.com/WxxShirley/Chatroom/blob/master/imgs/welcome.png)
 
* 点击注册
 ![register](https://github.com/WxxShirley/Chatroom/blob/master/imgs/register.png)
 
* 多人聊天室主界面
  * 为简洁，只显示近五条聊天记录和发送的文件名。
  * **friends**为待开发功能
 ![main_page](https://github.com/WxxShirley/Chatroom/blob/master/imgs/main_page.png)
 
* 发送的内容多样化，包括文本信息、文件、表情。
  其中tkinter无法显示emoji，因此我采用诸如 **[emoji-cake]** 的形式来表征一个emoji，目前可以发送的emoji较少，后期会再拓展。
  ![send_files](https://github.com/WxxShirley/Chatroom/blob/master/imgs/send_files.png)
  ![send_message](https://github.com/WxxShirley/Chatroom/blob/master/imgs/send_message.png)

  
## 未来工作
待完善的功能 
希望1月底可以完成💪
- [ ] 用户间好友关系
- [ ] 用户的个人信息中包括本地图片上传的头像
- [ ] 实现群聊和私聊
 
 
