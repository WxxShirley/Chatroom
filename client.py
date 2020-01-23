import socket
import select
import sys

import tkinter as tk
from tkinter import *
import tkinter.messagebox
from emoji import emojize
from PIL import Image,ImageTk
from emoji_page import *
from tkinter import filedialog

from LoginPage import *
import _thread
import time
import os
import method

HOST = "127.0.0.1"
PORT = 65435
User = None


def send_emoji_1():
    emoji = "[emoji-happy]"
    header = str(SEND_EMOJI) + "" + "\r\n" + str(len(emoji))
    msg = emoji.encode("utf-8")
    try:
        method.send(sock, header, msg)
    except Exception as e:
        messagebox.showerror('Error', 'Send emoji error')
        print('error,', e)

    print("got this emoji", emoji)
    show_msg('<Me>', emoji, 'blue', is_file=False, msg_time=None)


def send_emoji_2():
    emoji = '[emoji-HappyWithHalo]'
    header = str(SEND_EMOJI) + "" + "\r\n" + str(len(emoji))
    msg = emoji.encode("utf-8")
    try:
        method.send(sock, header, msg)
    except Exception as e:
        messagebox.showerror('Error', 'Send emoji error')
        print('error,', e)

    print("got this emoji", emoji)
    show_msg('<Me>', emoji, 'blue', is_file=False, msg_time=None)

def send_emoji_3():
    emoji = '[emoji-cake]'
    header = str(SEND_EMOJI) + "" + "\r\n" + str(len(emoji))
    msg = emoji.encode("utf-8")
    try:
        method.send(sock, header, msg)
    except Exception as e:
        messagebox.showerror('Error', 'Send emoji error')
        print('error,', e)

    print("got this emoji", emoji)
    show_msg('<Me>', emoji, 'blue', is_file=False, msg_time=None)

def send_emoji_4():
    emoji = "[emoji-hotpot]"
    header = str(SEND_EMOJI) + "" + "\r\n" + str(len(emoji))
    msg = emoji.encode("utf-8")
    try:
        method.send(sock, header, msg)
    except Exception as e:
        messagebox.showerror('Error', 'Send emoji error')
        print('error,', e)

    print("got this emoji", emoji)
    show_msg('<Me>', emoji, 'blue', is_file=False, msg_time=None)



def get_users(sock,user):
    header = str(GET_ALL_USERS)

    method.send(sock,header)

    try:
        data, rest = method.receive(sock)
    except Exception as e:
        messagebox.showerror('Error','Get users error!')
        return None

    state = data
    if state == str(GET_SUCCESS):
        #rest = rest.decode("utf-8")
        users = rest.split("\r\n")
        print("find users: ")
        for user in users:
            print(user)
        return users

def get_chat_history(sock,user):
    header = str(GET_ALL_CHAT_HISTORY)
    msg = user.encode("utf-8")
    method.send(sock,header,msg)

    try:
        data, rest = method.receive(sock)
    except Exception as e:
        messagebox.showerror('Error','Get chat history error!')
        print('get chat history error',e)
        return

    state = data[:3]
    if state == str(RET_HISTORY_ERROR):
        messagebox.showerror('Error','--Get chat history error!')
        return

    if state == str(RET_HISTORY_SUCCESS):
        msgs = rest.split("\r\n")
        count = 0
        for msg in msgs:
            detail = msg.split("\t")
            if len(detail)>=2 and count<5:
                print(detail)
                name = detail[0]
                time = detail[1]
                content = detail[2]
                count += 1
                if name != user:
                    show_msg(name,content,'green',msg_time = time)
                else :
                    show_msg('<Me>',content,'blue',msg_time = time)
        return





def get_history_files():
    header = str(GET_ALL_FILE_HISTORY)
    method.send(sock,header)

    try:
        data,rest = method.receive(sock)
    except Exception as e:
        print("get history file errors")
        messagebox.showerror('Error','Get history files error!')
        return

    names = rest.split("\r\n")
    return names



def show_msg(sender,msg,color,is_file = False,msg_time = None):
    if msg_time == None:
        msg_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

    text_recv.config(state = NORMAL)
    text_recv.see(END)

    text_recv.insert('end',"{0} {1} \n".format(sender,msg_time),color)

    if is_file == False :
        text_recv.insert('end','{0} \n'.format(msg))

    text_recv.see('end')
    text_recv.config(state = DISABLED)


def send_message():
    text = input_text.get('0.0','end')
    header = str(SEND_MESSAGE) + "\r\n" + str(len(text))

    if text is None:
        return
    try:
        send_text = text.encode("utf-8")
        method.send(sock,header,send_text)
        show_msg('<Me>',text,'blue',is_file = False)
    except Exception as e:
        messagebox.showerror('Error','Sending message error!')
        print('send msg error,',e)

    input_text.delete('0.0','end')



def send_file():
    file_path = filedialog.askopenfilename(title = "Choose Files 🤓")
    if os.path.exists(file_path) == False:
        return
    state = method.upload_file(sock,file_path,"")
    if state == False:
        messagebox.showerror('Error','File size can not exceed 50 M!')

    show_msg("<Me>","send file: {0}\n".format(file_path),'blue')
    print(file_path)

    filename = os.path.basename(file_path)
    if filename not in files:
        files.append(filename)
        fileListbox.insert('end',filename)




def create_new_groupChat():
    pass

def private_chat(event):
    pass



def listener(sock,root):
    print("?? then ??")
    listen_this = [sock]

    while True:
        reads, writes, errors = select.select(listen_this,[],[])

        for master in reads:
            if master == sock:
                try:
                    data, rest = method.receive(master)
                    print(data,rest)
                    print("--- check which step is in ---")
                    print(data[:3])
                except Exception as e:
                    messagebox.showerror('Error','Receive Error!')
                    continue

                if len(data)==0:
                    print("receive wrong data: len==0")
                    continue
                try:
                    msg_type = data[:3]
                    print("check msg_tpye",msg_type)
                    if msg_type == str(LOGIN_USERNAME):
                        ## new user login in
                        new_user = rest
                        #new_user = rest.decode("utf-8")
                        hinter = new_user + " login!"
                        show_msg('<System>', hinter, 'red', is_file=False)
                        list.insert('end',new_user)
                        users.append(new_user)
                        #SEND_MESSAGE_ALL
                    elif msg_type == str(SEND_MESSAGE_ALL):
                        print("get this step")
                        try:
                            data_ = data[3:]
                            sender, length = data_.split("\r\n")
                        except Exception as e:
                            messagebox.showerror('Error','Receive message error!')
                        show_msg(sender,rest,'green')

                    elif msg_type == str(SEND_EMOJI_SUCCESS):
                        print("get this step: receive emoji")
                        try:
                            sender, length = data[3:].split("\r\n")

                        except Exception as e:
                            messagebox.showerror('Error','Receive emoji error!')

                        show_msg(sender,rest,'green')

                    elif msg_type == str(SEND_EMOJI_ERROR):
                        print("send emoji error")
                        messagebox.showerror('Error','Sending emoji error!')


                    elif msg_type == str(SEND_FILE_SUCCESS):
                        print("got file~~")
                        try:
                            sender, filename, file_len = data[3:].split("\r\n")
                            show_msg(sender,'send file: '+filename, 'green')

                            if filename not in files:
                                files.append(filename)
                                fileListbox.insert('end', filename)

                        except Exception as e:
                            print("split file header error, ",e)
                            messagebox.showerror('Error','Sendiing file error! ')

                    elif msg_type == str(SEND_FILE_ERROR):
                        messageboxs.showerror('Error','Sending file error!')



                except Exception as e:
                    messagebox.showerror('Error','Detect information type error!')



if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        sock.connect((HOST,PORT))
        print(sock)
    except:
        print("Fail to connect (%s,%s)"%(HOST,PORT))

    print("Client Begin...")

    root = tk.Tk()

    login = LoginPage(window = root,sock = sock)

    if login.flag is None:
        print("----LOGIN FAILUSER END -----")
        exit()

    User = login.flag # get the user
    print("----CHATTING BEGIN -----")

    ## Initialize chatroom
    ## - step1:get all online users
    ## - step2:get all stored chat history information

    users = get_users(sock,User)

    window = tk.Tk()

    # initialize
    window.title('WChat 😊 '+User)
    window.geometry('800x600')

    # canvas - listing user's img, chat button, friends button
    cv = tk.Canvas(window, background='orange', width=90, height=600)
    cv.place(x=0, y=0)

    # user_imgs
    ## when database is completed, introduce user's img and load user's img when initialized
    img = Image.open('./imgs/胖虎.jpg')
    image_file = ImageTk.PhotoImage(img)
    image = cv.create_image(45, 30, anchor='n', image=image_file)

    chat_button = tk.Button(cv, text='👻Chat', font=('Arial', 12), width=10, height=1, )
    chat_button.place(x=10, y=150)

    ## click this and page swithes
    friends_button = tk.Button(cv, text='👥friends', font=('Arial', 12), width=10, height=1)
    friends_button.place(x=10, y=200)

    l = tk.Label(window, text='🧐Users', font=('Arial', 13), width=10, height=2)
    l.place(x=100, y=10)

    # create new group chat
    add_button = tk.Button(window, text='➕', font=('Arial', 12), width=4, height=2, command=create_new_groupChat)
    add_button.place(x=200, y=10)

    # list all online users
    list = tk.Listbox(window)
    list.place(x=95, y=45, height=250, width=140)
    for u in users:
        list.insert('end', u)

    # list all recent files
    file_label = tk.Label(window,text='🤓Recent files',font = ('Arial,13'),width = 15,height=2)
    file_label.place(x=95,y=300)

    fileListbox = tk.Listbox(window)
    fileListbox.place(x=95,y=330,height=250,width=140)

    files = get_history_files()
    #files = ['recomm.pdf','qiuqiuhu_memo.txt']
    for file in files:
        if len(file)>0:
            fileListbox.insert('end',file)


    ## private chat
    list.bind('<Double-Button-1>', private_chat)

    cv1 = tk.Canvas(window, background='white', width=540, height=400, bd=1, highlightbackground='orange')
    cv1.place(x=250, y=10)

    text_recv = tk.Text(cv1, width=460, height=350)
    text_recv.place(x=10, y=10)
    # 3 colors to represent different kinds of msg
    text_recv.tag_config('green', foreground='#008b00')
    text_recv.tag_config('red', foreground='#FF0000')
    text_recv.tag_config('blue', foreground='#0000FF')

    s_bar = tk.Scrollbar(cv1, orient='vertical')
    s_bar.place(x=0, y=0)
    text_recv.config(yscrollcommand=s_bar.set)
    s_bar.config(command=text_recv.yview)

    cv2 = tk.Canvas(window, background='white', width=540, height=160, bd=1, highlightbackground='orange')
    cv2.place(x=250, y=425)

    emoji_button = tk.Button(cv2, text='Emoji️')
    emoji_button.place(x=10, y=10)

    file_button = tk.Button(cv2, text='Files', command=send_file)
    file_button.place(x=55, y=10)

    send_button = tk.Button(cv2, text='Send', command=send_message)
    send_button.place(x=90, y=10)

    # textvariable
    input_text = tk.Text(cv2, width=460, height=90)
    input_text.place(x=5, y=30)

    get_chat_history(sock, User)


    """
    Emoji Page
    """
    e_page = Toplevel(window)
    e_page.title('WChat 😎 Emoji')
    e_page.geometry('100x80')

    frame = tk.Frame(e_page)
    frame.place(x=5, y=5)

    frame_l = tk.Frame(frame)
    frame_r = tk.Frame(frame)
    frame_l.pack(side='left')
    frame_r.pack(side='right')

    tk.Button(frame_l, text='😜', command=send_emoji_1).pack()
    tk.Button(frame_l, text='😇', command=send_emoji_2).pack()

    tk.Button(frame_r, text='🍰',command=send_emoji_3).pack()
    tk.Button(frame_r, text='🥘',command=send_emoji_4).pack()

    _thread.start_new_thread(listener,(sock,window))


    window.mainloop()