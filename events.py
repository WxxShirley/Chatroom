import socket
import sys
import os
import select

from constant import *
from database import *
import method
from server import broadcast

def register(conn,msg):
    try:
        user,pwd = msg.split("\r\n")
        assert user.find("\t") == -1
        assert pwd.find("\t") == -1
    except Exception as e:
        print("!! wrong register",e)
        return str(WRONG_MESSAGE)

    r = get_user_by_name(user)
    if r:
        print("!! Existing user")
        return str(REGISTER_ERROR)
    else :
        add_user(user,pwd)
        return str(REGISTER_SUCCESS)



def login(conn,msg):
    try:
        user, pwd = msg.split("\r\n")
        assert user.find("\t") == -1
        assert pwd.find("\t") == -1
    except Exception as e:
        print("!! wrong login",e)
        return str(LOGIN_ERROR)

    u = get_user_by_name(user)
    if u:
        db_pwd = u["password"]
        if pwd == db_pwd:
            return str(LOGIN_SUCCESS),user
        else:
            return str(LOGIN_WRONG_PWD),""
    else :
        return str(LOGIN_ACCOUNT_NOT_EXIST),""


