import tkinter as tk
from tkinter import *
from constant import *
from method import *
import re
import os
import tkinter.messagebox
from PIL import Image,ImageTk
from client import *

class EmojiPage:
    def send_emoji_1(self):
        header = str(SEND_EMOJI)
        emoji = '😜'
        msg = emoji.encode("utf-8")
        try:
            method.send(self.sock, header, msg)
        except Exception as e :
            messagebox.showerror('Error', 'Send emoji error')
            print('error,',e)

        print("got this emoji", emoji)
        show_msg('<Me>', emoji, 'blue', is_file=False, msg_time=None,recv_text = self.text_recv)

    def send_emoji_2(self):
        header = str(SEND_EMOJI)
        emoji = '😇'
        msg = emoji.encode("utf-8")
        try:
            method.send(self.sock, header, msg)
        except:
            messagebox.showerror('Error', 'Send emoji error')

        print("got this emoji", )
        show_msg('<Me>', emoji, 'blue', is_file=False, msg_time=None,recv_text = self.text_recv)

    def __init__(self,master = None,sock = None, text_recv = None):
        self.sock = sock
        self.text_recv = text_recv
        self.win = Toplevel(master)

        self.win.title("WChat 😎 Emoji")
        self.win.geometry('300x200')

        frame = tk.Frame(self.win)
        frame.place(x=5, y=5)

        frame_l = tk.Frame(frame)
        frame_r = tk.Frame(frame)
        frame_l.pack(side='left')
        frame_r.pack(side='right')

        tk.Button(frame_l, text='😜', command=self.send_emoji_1).pack()
        tk.Button(frame_l, text='😇', command=self.send_emoji_2).pack()
        tk.Button(frame_l, text='😂').pack()
        tk.Button(frame_l, text='😘').pack()
        tk.Button(frame_l, text='👩‍').pack()
        tk.Button(frame_l, text='🤩').pack()
        tk.Button(frame_l, text='😞').pack()
        tk.Button(frame_l, text='😟').pack()
        tk.Button(frame_l, text='😒').pack()

        emoji2 = "🍰🥘🍔🌮🍕🍟🌭🍖🍗"
        for e in emoji2:
            tk.Button(frame_r, text=e).pack()
        """
        tk.Button(frame_r,text = '🍰').pack()
        tk.Button(frame_r, text='🥘').pack()
        tk.Button(frame_r, text='🍔').pack()
        tk.Button(frame_r, text='🌮').pack()
        tk.Button(frame_r, text='🍕').pack()
        tk.Button(frame_r,text = '🍟').pack()
        tk.Button(frame_r, text='🌭').pack()
        tk.Button(frame_r, text='🍖').pack()
        tk.Button(frame_r, text='🍗').pack()
        """

        frame_ = tk.Frame(self.win)
        frame_.place(x=100, y=5)
        frame_l_ = tk.Frame(frame_)
        frame_r_ = tk.Frame(frame_)
        frame_l_.pack(side='left')
        frame_r_.pack(side='right')

        tk.Button(frame_l_, text='🐶').pack()
        tk.Button(frame_l_, text='🐹').pack()
        tk.Button(frame_l_, text='🐰').pack()
        tk.Button(frame_l_, text='🐻').pack()
        tk.Button(frame_l_, text='🐼').pack()
        tk.Button(frame_l_, text='🐨').pack()
        tk.Button(frame_l_, text='🐯').pack()
        tk.Button(frame_l_, text='🐴').pack()
        tk.Button(frame_l_, text='🙈').pack()

        tk.Button(frame_r_, text='🍎').pack()
        tk.Button(frame_r_, text='🍋').pack()
        tk.Button(frame_r_, text='🍌').pack()
        tk.Button(frame_r_, text='🍉').pack()
        tk.Button(frame_r_, text='🍇').pack()
        tk.Button(frame_r_, text='🍓').pack()
        tk.Button(frame_r_, text='🍑').pack()
        tk.Button(frame_r_, text='🥝').pack()
        tk.Button(frame_r_, text='🍒').pack()

        frame_3 = tk.Frame(self.win)
        frame_3.place(x=200, y=5)
        frame_l_3 = tk.Frame(frame_3)
        frame_r_3 = tk.Frame(frame_3)
        frame_l_3.pack(side='left')
        frame_r_3.pack(side='right')

        tk.Button(frame_l_3, text='😚').pack()
        tk.Button(frame_l_3, text='😋').pack()
        tk.Button(frame_l_3, text='😛').pack()
        tk.Button(frame_l_3, text='😝').pack()
        tk.Button(frame_l_3, text='🤓').pack()
        tk.Button(frame_l_3, text='😏').pack()
        tk.Button(frame_l_3, text='😒').pack()
        tk.Button(frame_l_3, text='😢').pack()
        tk.Button(frame_l_3, text='😭').pack()

        tk.Button(frame_r_3, text='😤').pack()
        tk.Button(frame_r_3, text='😠').pack()
        tk.Button(frame_r_3, text='😡').pack()
        tk.Button(frame_r_3, text='🤯').pack()
        tk.Button(frame_r_3, text='😳').pack()
        tk.Button(frame_r_3, text='😨').pack()
        tk.Button(frame_r_3, text='😱').pack()
        tk.Button(frame_r_3, text='🙃').pack()
        tk.Button(frame_r_3, text='😌').pack()

        self.win.mainloop()

