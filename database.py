import sqlite3
import time

conn = sqlite3.connect('database.db',isolation_level = None)


def init_database():
    #conn = sqlite3.connect("database.db")
    #c = conn.cursor()
    """
    c.execute('''CREATE TABLE USERINFO
     (USERNAME TEXT PRIMARY KEY NOT NULL,
     PASSWORD TEXT NOT NULL);
    ''')

    conn.execute('''
     DROP TABLE IF EXISTS GROUP_CHAT_HISTORY
    ''')

    conn.execute('''CREATE TABLE GROUP_CHAT_HISTORY
        ( ID TEXT PRIMARY KEY NOT NULL,
          SOURCE_USER TEXT NOT NULL,
          TIME DATETIME NOT NULL,
          CONTENT TEXT NOT NULL,
          FOREIGN KEY ("source_user") REFERENCES userinfo("username")
        );
        ''')

    conn.execute('''
    DROP TABLE IF EXISTS GROUP_FILE_HISTORY
    ''')


    conn.execute('''CREATE TABLE GROUP_FILE_HISTORY
      (ID TEXT PRIMARY KEY NOT NULL,
       SOURCE_USER TEXT NOT NULL,
       TIME DATETIME NOT NULL,
       FILENAME TEXT NOT NULL,
       FILECONTENT TEXT NOT NULL,
       FOREIGN KEY ("source_user") REFERENCES userinfo("username")
      );
    ''')

    """

    conn.commit()
    conn.close()


def get_user_by_name(username):
    """

    :param username: searching username
    :return:
           {
             username:
             password
           }
    """
    tups = conn.execute('select * from userinfo where username = ?',(username,)).fetchall()
    if len(tups)!=1:
        print('Database: cannot get user by username')
        return None
    return {'username':tups[0][0],'password':tups[0][1]}


def add_user(username,password):
    conn.execute(
        '''
        insert into userinfo(username,password)
        values(?,?)
        ''',
        (username,password)
    )
    #return "insert successfully"


def get_all_users():
    tups = conn.execute(
        '''
        select username from userinfo
        '''
    )
    if tups is not None:
        return tups
    return None

def count_bigGroup_chat_len():
    tups = conn.execute(
        '''
        select * from group_chat_history
        '''
    )
    count = 0
    for tup in tups:
        count += 1
    return count


def count_bigGroup_file_len():
    tups = conn.execute(
        '''
        select * from group_file_history
        '''
    )
    count = 0
    for tup in tups:
        count += 1
    return count



def add_bigGroup_chat_history(sender,text):
    # check sender
    res = get_user_by_name(sender)
    # compute length
    length = count_bigGroup_chat_len()
    if res is None:
        return "insert failure"
    msg_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    if length is None:
        return "insert failure"
    id = length + 1

    conn.execute(
        '''
        insert into group_chat_history(id,source_user,time,content)
        values(?,?,?,?)
        ''',
        (id,sender,msg_time,text)
    )
    print("add success")
    return "insert success"


def add_bigGroup_file_history(sender,file_name,file_content):
    # check sender
    res = get_user_by_name(sender)
    if res is None:
        return "insert failure"
    time_ = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    # compute length
    length = count_bigGroup_file_len()
    if length is None:
        return "insert failure"

    id = length + 1
    print("id: {0}, sender: {1}, time: {2}, file_name: {3}, file_content: {4}".format(id,sender,time_,file_name,file_content))
    conn.execute(
        '''
        insert into group_file_history(id,source_user,time,filename,filecontent)
        values(?,?,?,?,?)
        ''',
        (id,sender,time_,file_name,file_content)
    )
    print("add success (file history)")
    return "insert success"



def get_chat_history():
    tups = conn.execute('''
      select * from group_chat_history order by time desc
    '''
    )
    return tups


def get_file_history():
    tups = conn.execute('''
     select * from group_file_history order by time desc
    ''')

    count = count_bigGroup_file_len()
    msg = ""
    if count < 5:
        print("here")
        for tup in tups:
           msg += tup[3] + "\r\n"
        return msg
    else :
        print("up here")
        idx ,msg = 0, ""
        for tup in tups:

            if idx>=5:
                break
            msg += tup[3] + "\r\n"

            idx += 1

    return msg



if __name__ == "__main__":
    #init_database()
    tups = get_file_history()
    print(tups)
