"""
Receive and send method
"""

import socket
import os
from constant import *
MAX_FILE_SIZE = 1024*1024*50

def send(socket,header,msg = b""):
    """

    :param socket: socket sending message
    :param header: header flag, e.g. LOGIN 1 , LOGIN SUCCESS 101
    :param msg:    message content
    :return:
    """
    byte_msg = bytes(header+"\n\n",encoding = 'utf-8') + msg
    if header == str(LOGIN_USERNAME):
        print("-->boradcast info :",byte_msg)
    socket.sendall(byte_msg)



def receive(sock):
    data = sock.recv(1024)

    for i in range(len(data)-1):
        if data[i] == 10 and data[i+1] == 10 : #"\n\n"
            header = data[:i].decode("utf-8")
            rest = data[i+2:].decode("utf-8")
            return header, rest
    return data.decode("utf-8"),""


def read_file(file_path):
    """

    :param file_path: file_path
    :return: file content
    """
    with open(file_path,"rb") as f:
        lines = f.readline()


    return lines


def upload_file(sock,file_path,receiver):
    filename = os.path.basename(file_path)

    file_size = os.stat(file_path).st_size

    if file_size > MAX_FILE_SIZE:
        return False

    file_info = str(SEND_FILE) + receiver + "\r\n" + filename + "\r\n" +str(file_size)
    #print("file path: ",file_path)
    #print("file_info: ",file_info)
    #print("file_name: ",filename)
    #print("file_size: ",file_size)
    file_content = read_file(file_path)

    send(sock,file_info,file_content)

    return True

