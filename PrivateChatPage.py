from tkinter import *
from tkinter import messagebox
from constant import *
import time
import method

class PrivateChatPage:
    def __init__(self,father,user,receiver,sock,ChatHistory,state=True):
        self.state = state
        self.user = user
        self.master = Toplevel(father)
        self.master.title("{0} Chat with {1}".format(user,receiver))
        self.master.geometry("425x400")
        self.receiver = receiver
        self.sock = sock
        self.chat_history = ChatHistory

        self.text_recv = Text(self.master,width=58,height=19)
        self.text_recv.place(x=0,y=0)
        self.text_recv.tag_config('green',foreground = '#008b00')
        self.text_recv.tag_config('red',foreground = '#FF0000')
        self.text_recv.tag_config('blue',foreground = '#0000FF')
        self.text_recv.config(state = DISABLED)
        self.sb = Scrollbar(self.master,orient = "vertical")
        self.sb.place(x=410,y=0,height=270)
        self.text_recv.config(yscrollcommand = self.sb.set)


        self.text_msg = Text(self.master,width=59,height=6)
        self.text_msg.place(x=0,y=275)
        self.sb0 = Scrollbar(self.master,orient = "vertical")
        self.sb0.place(x=410,y=275,height=80)
        self.text_msg.config(yscrollcommand = self.sb0.set)
        self.sb0.config(command = self.text_msg.yview)

        self.sb.config(command = self.text_recv.yview)
        self.Bsend = Button(self.master,text = "发送",command = self.send)
        self.Bsend.place(x=385,y=365)


        if ChatHistory.get(receiver) is not None and len(ChatHistory[receiver])!=0:
            chats = ChatHistory[receiver]
            for chat in chats:
                if chat[0] == self.user:
                    self.show_msg('<Me>',chat[2],'blue',chat[1])
                elif chat[0] == self.receiver:
                    self.show_msg(self.receiver,chat[2],'green',chat[1])


    def send(self):
        text = self.text_msg.get('0.0',END)
        print("text ",text)
        if text is None or len(text)==0:
            return

        self.show_msg('<Me>',text,'blue')

        content = text.encode("utf-8")
        msg = str(SEND_MESSAGE) + self.receiver + "\r\n" + str(len(text))
        method.send(self.sock,msg,content)
        self.text_msg.delete('0.0',END)


    def show_msg(self,sender,msg,color,time_ = None):
        self.text_recv.config(state = NORMAL)
        self.text_recv.see(END)

        if time_ is None:
            msg_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        else :
            msg_time = time_

        self.text_recv.insert('end',"{0} {1}\n".format(sender,msg_time),color)
        self.text_recv.insert('end',"{0}\n".format(msg),color)
        self.text_recv.see('end')
        self.text_recv.config(state=DISABLED)
        #self.text_recv.delete('0.0','end')

        """
        if sender == '<Me>':
            pos1 = self.user
        else :
            pos1 = self.receiver
        user2room_history[receiver].append([pos1,msg_time,msg])
        """
