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

    # close this
    conn.close()


# HANDLE MESSAGE
def handle(conn, msg, rest):
    state = ""
    try:
        type = int(msg[0])
    except Exception as e:
        print("!! wrong request",e)
        send(conn,str(WRONG_MESSAGE))
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
            length = int(length)
            if len(receiver)==0 :
                #bigGroup_sendMSG(conn,rest,sender)
                header = str(SEND_MESSAGE_ALL) + sender + "\r\n" + str(length)
                text = rest.encode("utf-8")
                add_bigGroup_chat_history(sender, rest)

                try:
                    broadcast(conn, header, text)
                except Exception as e:
                    print("send message error(during broadcast,", e)
                    header = str(SEND_ERROR)
                    method.send(conn, header)
                return

        except Exception as e:
            print("Wrong message",e)
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
                raw_content = file_content.decode("utf-8")
                add_bigGroup_file_history(sender,filename,raw_content)
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