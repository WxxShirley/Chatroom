import tkinter as tk
from tkinter import *
from constant import *
from method import *
import re
import os
import tkinter.messagebox
from PIL import Image,ImageTk

class LoginPage:
    def __init__(self,window = None,sock = None):

        # username and password
        self.username = StringVar()
        self.password = StringVar()

        # initialize
        self.sock = sock
        self.window = window
        self.flag = None

        window.title('WChat😄')
        window.geometry('400x300')

        canvas = tk.Canvas(window,width=400,height=135,bg='white')
        img = Image.open('胖虎.jpg')
        image_file = ImageTk.PhotoImage(img)
        image = canvas.create_image(200,10,anchor = 'n',image = image_file)
        canvas.pack(side = 'top')
        tk.Label(window,text = 'Welcome',font = ('Arial',16)).pack()

        tk.Label(window,text = 'User name:',font = ('Arial',14)).place(x=50,y=175)
        tk.Label(window,text = 'Password:',font = ('Arial',14)).place(x=50,y=210)

        entry_usr_name = tk.Entry(window,textvariable = self.username,font=('Arial',14),show = None)
        entry_usr_name.place(x = 140, y = 175)

        entry_usr_pwd = tk.Entry(window,textvariable = self.password,font = ('Arial',14),show = '*')
        entry_usr_pwd.place(x=140,y=210)

        btn_login = tk.Button(window,text = 'Login',command = self.usr_login)
        btn_login.place(x=160,y=250)

        btn_sign_up = tk.Button(window,text = 'Sign up',command = self.usr_sign_up)
        btn_sign_up.place(x=210,y=250)

        window.mainloop()

    def usr_login(self):
        user = self.username.get()
        pwd  = self.password.get()

        if not user:
            messagebox.showerror('Error','Please check your username!')
            return
        if not pwd:
            messagebox.showerror('Error','Please check your password!')
            return

        print("Get username and password: (%s,%s)"%(user,pwd))

        """
        Send LOGIN-INFORMATION 
             heaer + user + \r\n + pwd 
        """
        msg = str(LOGIN) + user + "\r\n" + pwd
        send(self.sock, msg)

        try:
            data, _ = receive(self.sock)
        except:
            print("!! login error,",e)

        if data == str(LOGIN_SUCCESS):
            messagebox.showinfo('Info','Login success!')
            print("success")

            # !!! successful login ,set LOGIN.FLAG = USER
            self.flag = user
            self.window.destroy()
        elif data == str(LOGIN_WRONG_PWD):
            messagebox.showerror('Error','Wrong password!')
            self.password.set("")

        elif data == str(LOGIN_ACCOUNT_NOT_EXIST):
            messagebox.showerror('Error','Account not exists!')
            self.username.set("")
            self.password.set("")
        elif data == str(LOGIN_DUPLICATE):
            messagebox.showerror('Error','Duplicated login!')
            self.username.set("")
            self.password.set("")



    def usr_sign_up(self):
        def register():
            user,pwd,pwd_ = str(name.get()), str(pwd1.get()), str(pwd2.get())

            if not user or len(user)==0 or user.find(" ")!=-1 or user.find("\t")!=-1:
                messagebox.showerror('Error','Please check your username!')
                return
            if pwd!=pwd_ :
                pwd1.set("")
                pwd2.set("")
                messagebox.showerror('Error','Inconsistent passwords')
                return

            # pwd consists of 6-16 letter and number
            regex = re.compile('^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,16}$')
            if not regex.match(pwd):
                pwd1.set("")
                pwd2.set("")
                messagebox.showerror('Error','Password consists of 6-16 bits of letter and number!')
                return

            msg = str(REGISTER) + user + "\r\n" + pwd
            send(self.sock,msg)

            try:
                data,_ = receive(self.sock)
            except:
                print("!! register error",e)

            #REGISTER_SUCCESS
            if data == str(REGISTER_SUCCESS):
                messagebox.showinfo('Info','Register success!')
                win.destroy()
            elif data == str(REGISTER_ERROR):
                messagebox.showerror('Error','Register error,please try again!')
            return


        win = Toplevel(self.window)
        win.title("WChat-Resigeter 🤗")
        win.geometry('400x300')

        name,pwd1,pwd2 = StringVar(),StringVar(),StringVar()
        name.set("")
        pwd1.set("")
        pwd2.set("")

        canvas = tk.Canvas(win, width=400, height=120, bg='white')
        img = Image.open('register.jpg')
        image_file = ImageTk.PhotoImage(img)
        image = canvas.create_image(200, 20, anchor='n', image=image_file)
        canvas.pack(side='top')
        tk.Label(win, text='Register', font=('Arial', 16)).pack()

        tk.Label(win,text = "User name: ",font = ('Arial',14)).place(x=50,y=165)
        tk.Label(win,text = "Password: ",font = ('Arial',14)).place(x=50,y=195)
        tk.Label(win,text = "Confirm pwd: ",font = ('Arial',14)).place(x=50,y=230)

        entry_username = tk.Entry(win,textvariable = name,font = ('Arial',14))
        entry_username.place(x=150,y=165)

        entry_pwd1 = tk.Entry(win,textvariable = pwd1,show = '*',font = ('Arial',14))
        entry_pwd1.place(x=150,y=195)

        entry_pwd2 = tk.Entry(win,textvariable = pwd2,show = '*',font = ('Arial',14))
        entry_pwd2.place(x=150,y=230)

        register_button = tk.Button(win,text = 'register',command = register)
        register_button.place(x=180,y=260)


        win.mainloop()

if __name__ == "__main__":
    page = LoginPage()


