import socket
import select
import sys

import tkinter as tk
#from tkinter import *
import tkinter.messagebox
from emoji import emojize
#from PIL import Image,ImageTk
import PIL.Image
import PIL.ImageTk
from emoji_page import *
from tkinter import filedialog

from LoginPage import *
from PrivateChatPage import *
import _thread
import time
import os
import method

HOST = "127.0.0.1"
PORT = 65435
User = None
user2room = {}
#user2room_history = {}
groups = []

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





def room_exists(room):
    if room is None:
        return False
    if int(room.master.winfo_exists())==0:
        return False
    return True


def private_chat(event):
    choice = friend_list.get(friend_list.curselection())
    if choice == User:
        return
    if room_exists(user2room.get(choice))==False:
        # init - get chat history

        user2room[choice] = PrivateChatPage(window,User,choice,sock,user2room_history)





def send_add_friend_request():
    header = str(ADD_FRIEND)
    name_ = friend_name.get()
    msg = User + "\r\n" + name_
    msg = msg.encode("utf-8")
    try:
        method.send(sock,header,msg)
    except Exception as e:
        print("!!Send add-friend-request error:",e)

def add_friend():
    win_ = Toplevel(window)
    win_.title("Add Friends🤣")
    win_.geometry("300x200")

    tk.Label(win_,text = 'User name:',font = ('Arial',14)).place(x=10,y=40)
    entry_usr_name = tk.Entry(win_,textvariable = friend_name,font = ('Arial',12))
    entry_usr_name.place(x=90,y=40)

    add_button = tk.Button(win_,text = 'Add',font = ('Arial',12),width=10,height=2,command = send_add_friend_request)
    add_button.place(x=80,y=80)


def get_all_friends():
    try:
        msg = User.encode("utf-8")
        method.send(sock,str(SHOW_ALL_FRIENDS),msg)
    except Exception as e:
        print("get friends error ",e)

    try:
        data,rest = method.receive(sock)
    except Exception as e:
        print("receive friends error, ",e)

    friends = []

    if data[:3] == str(SHOW_FRIENDS_SUCCESS):
        friends = rest.split("\r\n")
        return friends

    if data[:3] == str(SHOW_FRIENDS_ERROR):
        print("server get friends error")

    if data[:3] == str(NO_FRIENDS):
        print(User+" have no friends at this time ")


    return friends



def download_file(event):
    #fileListbox.bind('<Double-Button-1>',download_file)
    choice = fileListbox.get(fileListbox.curselection())
    print("select: ",choice,type(choice),User)
    msg = User + "\r\n" + choice
    msg = msg.encode("utf-8")
    try:
        method.send(sock,str(DOWNFILE),msg)
    except Exception as e:
        print("send downfile request error ",e)
        messagebox.showerror('Error','Download file error!')
        return




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
                    print("receiver error :",e)
                    #messagebox.showerror('Error','Receive Error!{0}'.format(e))
                    continue

                if data[:3] == str(ADD_FRIEND_SUCCESS):
                    print("receive, new friend: ",rest)


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
                        messagebox.showerror('Error','Sending file error!')


                    elif msg_type == str(ADD_FRIEND_SUCCESS):
                        friend_name = rest
                        print("friend name,",friend_name)
                        messagebox.showinfo('Info','Adding '+friend_name+" successfully! ~ ")

                        friends.append(friend_name)
                        friend_list.insert('end', friend_name)



                    elif msg_type == str(ALREADY_ADD_ERROR):
                        print("already be friends")
                        messagebox.showerror('Error','You have been friends!')
                    elif msg_type == str(USERNAME_NOT_EXIST):
                        print("username not exits")
                        messagebox.showerror('Error','Username not exist!')
                    elif msg_type == str(ADD_FRIEND_ERROR):
                        print("other error")
                        messagebox.showerror('Error','Adding friend error!')

                    elif msg_type == str(ADD_FRIEND_REMIND):
                        new_friend = rest
                        messagebox.showinfo('Info',"New friend: "+new_friend+"!~")
                        friends.append(new_friend)
                        friend_list.insert('end', new_friend)

                    elif msg_type == str(LOGOUT_INFO):
                        logout_user = rest
                        hinter = logout_user + " log out!"
                        show_msg('<System>', hinter, 'red')
                        list.delete(users.index(logout_user))
                        users.remove(logout_user)


                    elif msg_type == str(DOWNFILE_ERROR):
                        messagebox.showerror('Error','Download file error,please try again!')

                    elif msg_type == str(DOWNFILE_SUCCESS):
                        try:
                            filename,content = data[3:],rest
                        except Exception as e:
                            print("receive downfile return msg error ",e)

                        file_path = tkinter.filedialog.askdirectory()
                        file_path = os.path.join(file_path,filename)
                        content = content.encode("utf-8")
                        with open(file_path,"wb") as f:
                            f.write(content)
                        messagebox.showinfo("Info","Download file success!\n Saved in: "+file_path)


                    elif msg_type == str(SEND_MESSAGE_PER_STORE):
                        messagebox.showinfo('Info',rest+" is offline, message is cached!")

                    elif msg_type == str(SEND_MESSAGE_PER):
                        try :
                            sender, text = rest.split("\r\n")

                        except Exception as e:
                            print("split SEND_MESSAGE_PER error: ",e)


                        if room_exists(user2room.get(sender)):
                            user2room[sender].show_msg(sender,text,'green')
                        else:
                            user2room[sender] = PrivateChatPage(window,User,sender,sock,user2room_history)
                            user2room[sender].show_msg(sender,text,'green')


                except Exception as e:
                    print("encounter error: ",e)
                    messagebox.showerror('Error','Detect information type error!')


def get_friends_chat_history():
    for friend in friends:
        try:
            header = str(PRIVATE_INIT) + User + "\r\n" + friend
            method.send(sock, header, )
        except Exception as e:
            print("private chat page init error ", e)
            # messagebox.showerror('Error','Private ChatPage initialize error!')

        try:
            data, rest = method.receive(sock)
            msg_type = data[:3]
            print(msg_type)
            user1, user2 = data[3:].split("\r\n")
            if msg_type == str(PRIVATE_INIT_SUCCESS):
                lists = rest.split("\r\n")
                #assert user1 == User
                chat_list = []
                for list in lists:
                    chat_list.append(list.split("\t"))
                user2room_history[user2] = chat_list

            elif msg_type == str(PRIVATE_INIT_NONE):
                user2room_history[user2] = []

            elif msg_type == str(PRIVATE_INIT_ERROR):
                user2room_history[user2] = []
                messagebox.showerror('Error',"Fetch chat history with "+user2+" error!")

        except Exception as e:
            print("receive friends chat history error:",e)
            #user2room_history[user2] = []

    #for key in user2room_history.keys():
        #print(key,user2room_history[key])



def create_group():
    win_ = Toplevel()
    win_.title("Create NewGroup🤣")
    win_.geometry("300x200")

    tk.Label(win_, text='Group name:', font=('Arial', 14)).place(x=10, y=40)
    #entry_group_name = tk.Entry(win_, textvariable=, font=('Arial', 12))
    #entry_group_name.place(x=90, y=40)

    create_button = tk.Button(win_, text='Create', font=('Arial', 12), width=10, height=2, command=send_add_friend_request)
    create_button.place(x=80, y=80)


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

    user2room_history = {}

    ## Initialize chatroom
    ## - step1:get all online users
    ## - step2:get all stored chat history information
    ## - step3:get friends info
    ## - step4:get all friends chatting history
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
    img = PIL.Image.open('胖虎2.jpg')

    image_file = PIL.ImageTk.PhotoImage(img)
    image = cv.create_image(45, 30, anchor='n', image=image_file)

    chat_button = tk.Button(cv, text='👻Chat', font=('Arial', 12), width=10, height=1, )
    chat_button.place(x=10, y=150)

    ## click this and page swithes
    """
    friend_name = tk.StringVar()
    friends_button = tk.Button(cv, text='👥friends', font=('Arial', 12), width=10, height=1,command = show_friends)
    friends_button.place(x=10, y=200)
    """

    # get all friends
    friends = get_all_friends()

    top = None
    win_ = None

    l = tk.Label(window, text='🧐Online Users', font=('Arial', 13), width=15, height=2)
    l.place(x=100, y=10)

    # list all online users
    sb = Scrollbar(window)
    sb.pack(side=RIGHT,fill=Y)
    list = tk.Listbox(window,yscrollcommand=sb.set)
    list.place(x=95,y=45,height=80,width=140)
    sb.config(command=list.yview)
    for u in users:
        list.insert('end',u)

    # list all friends
    friend_label = tk.Label(window,text = '👫friends',font=('Arial',13),width=10,height=2)
    friend_label.place(x=100,y=140)

    friend_name = tk.StringVar()
    add_friend_button = tk.Button(window, text='➕', font=('Arial', 12), width=4, height=2, command=add_friend)
    add_friend_button.place(x=200, y=140)

    sb_ = Scrollbar(window)
    sb_.pack(side=RIGHT,fill=Y)
    friend_list = tk.Listbox(window,yscrollcommand = sb_.set)
    friend_list.place(x=95,y=170,height=80,width=140)
    sb_.config(command=friend_list.yview)

    if len(friends)!=0:
        print("friends not none")
        for f in friends:
            friend_list.insert('end',f)
    # FUNCTION double click: private chat
    # user2room_history
    if len(friends)!=0:
        get_friends_chat_history()
    friend_list.bind('<Double-Button-1>', private_chat)



    # list all chatting groups
    tk.Label(window,text = '👥groups',font=('Arial',13),width=10,height=2).place(x=100,y=270)
    tk.Button(window,text='➕', font=('Arial', 12), width=4, height=2, command=create_group).place(x=200,y=270)

    s_b = Scrollbar(window)
    s_b.pack(side=RIGHT,fill=Y)
    group_list = tk.Listbox(window,yscrollcommand = s_b.set)
    group_list.place(x=100,y=300,height=100,width=140)
    s_b.config(command=group_list.yview)


    # list all recent files
    file_label = tk.Label(window,text='🤓Recent files',font = ('Arial,13'),width = 15,height=2)
    file_label.place(x=100,y=410)

    sbb = Scrollbar(window)
    sbb.pack(side=RIGHT,fill=Y)
    fileListbox = tk.Listbox(window,yscrollcommand = sbb.set,bd = 1,highlightbackground='orange',)
    fileListbox.place(x=100,y=450,height=120,width=140)
    sbb.config(command=fileListbox.yview)

    files = get_history_files()
    for file in files:
        if len(file)>0:
            fileListbox.insert('end',file)
    # FUNCTION double click: download file
    fileListbox.bind('<Double-Button-1>',download_file)


    #cv1 = tk.Canvas(window, background='white', width=540, height=400, bd=1, highlightbackground='orange')
    #cv1.place(x=250, y=10)
    s_bar = Scrollbar(window,orient = "vertical")
    s_bar.place(x=500,y=10,height=60)
    text_recv = tk.Text(window, width=460, height=60)
    text_recv.place(x=260, y=10,height=400)
    #text_recv.place(x=260,y=15)
    text_recv.config(yscrollcommand = s_bar.set)
    # 3 colors to represent different kinds of msg
    text_recv.tag_config('green', foreground='#008b00')
    text_recv.tag_config('red', foreground='#FF0000')
    text_recv.tag_config('blue', foreground='#0000FF')
    s_bar.config(command=text_recv.yview)

    '''
    self.text_msg = Text(self.master,width=59,height=6)
        self.text_msg.place(x=0,y=275)
        self.sb0 = Scrollbar(self.master,orient = "vertical")
        self.sb0.place(x=410,y=275,height=80)
        self.text_msg.config(yscrollcommand = self.sb0.set)
        self.sb0.config(command = self.text_msg.yview)
    '''



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