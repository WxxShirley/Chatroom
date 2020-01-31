import socket
import sys
import os
import select

from constant import *
from method import *
from events import *
from database import *

"""
Global Variables 
 - conn : all connections
 - (HOST,PORT)
 - conn2user : dictionary(store users corresponding to their connections)
 - user2conn : dictionary(store conns corresponding to users)
"""


HOST = "127.0.0.1"
PORT = 65435

# BROADCAST
def broadcast(conn,msg,rest = b""):
    print("--->> broadcast <<----",msg,rest)
    for receiver in connections:
        # conditions
        if receiver!=conn and receiver!=sock and conn2user.get(conn) is not None:
            try:
                send(receiver,msg,rest)
            except Exception as e:
                print("!! broadcast error,",e)



# RELEASE CONNECTION
def release(conn):
    # print release information
    print("## release connection: ",conn,"    ##")

    # del this from CONNECTIONS
    connections.remove(conn)

    if user2conn.get(conn2user[conn])==conn:
        user = conn2user[conn]
        rest = user.encode("utf-8")
        broadcast(conn,str(LOGOUT_INFO),rest)
        del user2conn[user]


    # close this
    conn.close()
    del conn2user[conn]


# HANDLE MESSAGE
def handle(conn, msg, rest):
    state = ""
    try:
        type = int(msg[0])
    except Exception as e:
        print("!! wrong request",e)
        send(conn,str(WRONG_MESSAGE))
        return

    #print(msg[:2])

    if len(msg)>=2 and  int(msg[0])==9 and int(msg[1])==9 :
        print("in downfile")
        try:
            user,choice_file = rest.split("\r\n")
            assert user.find("\t")==-1
            assert choice_file.find("\t")==-1
        except Exception as e:
            print("split downfile error ",e)
            method.send(conn,str(DOWNFILE_ERROR))
            return

        file_content = get_file_by_name(choice_file)
        if file_content is not None:
            header = str(DOWNFILE_SUCCESS) + choice_file

            method.send(conn,header,file_content)
            return
        else :
            print("file not exist")
            method.send(conn,str(DOWNFILE_ERROR))
            return

    if len(msg)>=2 and int(msg[0])==9 and int(msg[1])==8:
        print("in init private chat history")
        user1,user2 = msg[2:].split("\r\n")

        assert user1==conn2user[conn]

        # chat结构： [发送方，时间，内容]
        chats = get_privatechat_history(user1,user2)
        if len(chats)>0:
            msg = ""
            for chat in chats:
                cont_ = chat[0]+"\t"+chat[1]+"\t"+chat[2]
                msg += cont_
                if chats.index(chat) != len(chats)-1 :
                    msg += "\r\n"
            header = str(PRIVATE_INIT_SUCCESS) + user1 + "\r\n" + user2
            print("msg: ",msg)
            msg = msg.encode("utf-8")
            try:
                method.send(conn,header,msg)
            except Exception as e:
                print("send private chat history error ",e)
                method.send(conn,str(PRIVATE_INIT_ERROR))
            return
        else :
            header = str(PRIVATE_INIT_NONE) + user1 + "\r\n" + user2
            method.send(conn,header,)
            return



    if type == REGISTER:
        # msg = str(REGISTER) + user + "\r\n" + pwd
        msg = msg[1:]
        state = register(conn,msg)
        send(conn,state)
        return

    elif type == LOGIN:
        # msg = heaer + user + \r\n + pwd
        msg = msg[1:]
        state,user = login(conn,msg)
        if user !="":
            if user2conn.get(user) is not None:
                state = str(LOGIN_DUPLICATE)
        if state == str(LOGIN_SUCCESS):
            conn2user[conn] = user
            user2conn[user] = conn
            print("---Existing users with conns:")
            for key in conn2user.keys():
                print(key,conn2user[key])

            print("---Existing conns with users:")
            for key in user2conn.keys():
                print(key,user2conn[key])

            header = str(LOGIN_USERNAME)
            msg = user.encode("utf-8")
            broadcast(conn,header,msg)
        send(conn,state)
        return

    elif type == GET_ALL_USERS:
        user_list = user2conn.keys()
        if user_list is None:
            state = str(GET_USERS_ERROR)
            send(conn,state)
            return
        else:
            users = "\r\n".join(user_list)
            users = users.encode("utf-8")
            header = str(GET_SUCCESS)
            msg = users
            print("send users:",msg)
            send(conn,header,msg)
            return

    elif type == SEND_MESSAGE:
        try:
            sender = conn2user[conn]
            text = msg[1:]
            receiver, length = text.split("\r\n")
            print("in SEND_MESSAGE_STEP, receiver = {0}, sender = {1}, message content = {2}".format(receiver,sender,rest))
            #length = int(length)
            if len(receiver)==0 :
                print("in bigGroup")
                header = str(SEND_MESSAGE_ALL) + sender + "\r\n" + length
                print("header: ",header)
                text = rest.encode("utf-8")
                print("in this steo")
                add_bigGroup_chat_history(sender, rest)
                print("succ insert into big group chat history")
                try:
                    broadcast(conn, header, text)
                    return
                except Exception as e:
                    print("send message error(during broadcast,", e)
                    header = str(SEND_ERROR)
                    method.send(conn, header)
                return

            else :
                send_sock = user2conn.get(receiver)

                if send_sock is None: #用户不在线，把聊天信息缓存给该用户
                    add_privateChat_history(sender,receiver,rest)
                    # 提示消息已经缓存
                    print("message is stored")
                    msg = receiver.encode("utf-8")
                    method.send(conn,str(SEND_MESSAGE_PER_STORE),msg)
                    return
                else :
                    add_privateChat_history(sender,receiver,rest)
                    try:
                        msg = sender + "\r\n" +rest
                        msg = msg.encode("utf-8")
                        method.send(send_sock,str(SEND_MESSAGE_PER),msg)
                    except Exception as e:
                        print("send private chat error {0}, receiver: {1}".format(e,receiver))
                    return

        except Exception as e:
            print("Wrong message， ",e)
            state = str(WRONG_MESSAGE)
            send(conn,state)
            return

    elif type == GET_ALL_CHAT_HISTORY:
        username = rest
        try:
            tups = get_chat_history()
        except Exception as e:
            print("get chat history error ",e)
            header = str(RET_HISTORY_ERROR)
            method.send(conn,header)
            return

        msg = ""
        for tup in tups:
            single_history = ""
            single_history += tup[1] + "\t"
            single_history += tup[2] + "\t"
            single_history += tup[3] + "\t"
            msg += single_history + "\r\n"

        header = str(RET_HISTORY_SUCCESS) + "\r\n" + str(len(msg))
        msg = msg.encode("utf-8")
        method.send(conn,header,msg)
        return

    elif type == SEND_EMOJI:
        print("in send_emoji")
        emoji = rest
        sender = conn2user[conn]
        msg = msg[1:]
        try:
            receiver, length = msg.split("\r\n")
            print(receiver,length)
        except Exception as e:
            print("receive emoji error:",e)
            state = str(SEND_EMOJI_ERROR)
            method.send(conn,state)
            return

        if len(receiver)==0:
            header = str(SEND_EMOJI_SUCCESS) + sender + "\r\n" + str(len(emoji))
            text = emoji.encode("utf-8")
            try:
                broadcast(conn,header,text)
            except Exception as e:
                print("broadcast error (during sending emojis) :",e)
                header = str(SEND_EMOJI_ERROR)
                method.send(conn,header)
            return

    elif type == SEND_FILE:
        print("in send file")
        file_content = rest.encode("utf-8")
        msg = msg[1:]
        try:
            receiver, filename, file_size = msg.split("\r\n")
            sender = conn2user[conn]
        except Exception as e:
            print("receive file error: ",e)
            method.send(conn,str(SEND_FILE_ERROR))
            return

        if len(receiver)== 0:
            header = str(SEND_FILE_SUCCESS) + sender + "\r\n" + filename + "\r\n" + file_size
            print("sending header,",header)
            try:
                broadcast(conn,header,file_content)
                #raw_content = file_content.decode("utf-8")
                add_bigGroup_file_history(sender,filename,file_content)
            except Exception as e:
                print("broadcast error (during sending file) ",e)
                method.send(conn,str(SEND_FILE_ERROR))
            return

    elif type == GET_ALL_FILE_HISTORY:
        print("in get history file name")
        filenames = get_file_history()
        print("got filenames :",filenames)
        filenames = filenames.encode("utf-8")
        try:
            method.send(conn,str(RET_ALL_FILES_SUCCESS),filenames)
        except Exception as e:
            method.send(conn,str(RET_ALL_FILES_ERROR))
            print("send files history error,",e)

        return

    elif type == ADD_FRIEND:
        try:
            sender,replyer = rest.split("\r\n")
            assert(sender.find("\t")==-1)
            assert(replyer.find("\t")==-1)
        except Exception as e:
            print("split user and friend-name error ",e)
            method.send(conn,str(ADD_FRIEND_ERROR))
            return

        if get_user_by_name(replyer) is None:
            print("friend's name not exist")
            method.send(conn,str(USERNAME_NOT_EXIST))
            return

        friends = get_friends(sender)
        if replyer in friends:
            print("already friends")
            method.send(conn,str(ALREADY_ADD_ERROR))
            return

        state = add_friend(sender,replyer)
        print("new friend: ",replyer)
        if state == "add succ":
            msg = replyer.encode("utf-8")
            try:
                method.send(conn,str(ADD_FRIEND_SUCCESS),msg)
                print("send reminder")
                if user2conn.get(replyer) is not None:
                    # 如果对方在线，要实时更新
                    sock_ = user2conn[replyer]
                    msg_ = sender.encode("utf-8")
                    method.send(sock_,str(ADD_FRIEND_REMIND),msg_)
                return

            except Exception as e:
                print("send add-friend reply error ",e)
                method.send(conn, str(ADD_FRIEND_ERROR))
            return
        else :
            method.send(conn, str(ADD_FRIEND_ERROR))
            print("database error")


    elif type == SHOW_ALL_FRIENDS:
        u = rest
        u_ = conn2user[conn]
        #assert u==u_
        print(u,u_)
        friends = get_friends(u)
        if len(friends)==0:
            print("has no friends ")
            method.send(conn,str(NO_FRIENDS))
            return

        msg = "\r\n".join(friends)
        try:
            print(msg)
            method.send(conn,str(SHOW_FRIENDS_SUCCESS),msg.encode("utf-8"))
        except Exception as e:
            print("send all friends error",e)
            method.send(conn,str(SHOW_FRIENDS_ERROR))
            return









if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.bind((HOST,PORT))
    sock.listen()

    print("******* Server Starting (",HOST,",",PORT,") *******")

    connections = [sock]

    conn2user = {}
    user2conn = {}

    # keep Listening

    while True:
        reads, writes, errors = select.select(connections,[],[])
        for cur in reads:
            if cur == sock: #new connection
                conn, addr = sock.accept()
                print("## new connection",addr,"   ##")
                connections.append(conn)
                conn2user[conn] = None
            else : # old connection
                print("## now: ",cur,"  ##")

                try :
                    data, rest = receive(cur)

                except Exception as e:
                    print(e)
                    release(cur) # release this connection
                    continue

                if data:
                    print(" request: ",data.encode("utf-8"))
                    if len(data)==0:
                        print("!!Error: wrong message")
                    else :
                        handle(cur,data,rest)
                else :
                    print("!!Error: receive data error")
                    release(cur)


    sock.close()