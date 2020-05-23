import sqlite3
import time

conn = sqlite3.connect('database.db',isolation_level = None)


def init_database():
    #conn = sqlite3.connect("database.db")
    c = conn.cursor()
   
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

    conn.execute('''CREATE TABLE FRIENDS
    ( USERNAME1 TEXT NOT NULL,
      USERNAME2 TEXT NOT NULL,
      PRIMARY KEY (USERNAME1,USERNAME2),
      FOREIGN KEY ("username1") REFERENCES userinfo("username")
      FOREIGN KEY ("username2") REFERENCES userinfo("username")
    )
       
    ''')



    conn.execute('''CREATE TABLE HISTORY_PRIVATE_CHAT
    ( "id" INTEGER not NULL,
      "target_user" TEXT not NULL,
      "source_user" TEXT not NULL,
      "time" DATETIME not NULL,
      "text" TEXT not NULL,
      PRIMARY KEY("id"),
      FOREIGN KEY ("target_user") REFERENCES "userinfo"("username")
      FOREIGN KEY ("source_user") REFERENCES "userinfo"("username")
    );''')

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


def get_file_by_name(filename):
    tups = conn.execute('select * from group_file_history where filename = ?',(filename,)).fetchall()

    if len(tups)!= 0:
        return tups[0][4]
    return None




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
    num = conn.execute('''
     select count(*) from group_chat_history
    ''').fetchall()
    return num[0][0]


def count_bigGroup_file_len():
    num = conn.execute('''
        select count(*) from group_file_history
        ''').fetchall()
    return num[0][0]



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


def count_privateChat_num():
    ans = conn.execute('''
     select count(*) from history_private_chat
    ''').fetchall()
    return ans[0][0]


def add_privateChat_history(sender,receiver,message):
    # check sender and receiver
    username1 = get_user_by_name(sender)
    username2 = get_user_by_name(receiver)

    if username1 is None or username2 is None:
        print("user name not found")
        return "insert fail"

    count_num = count_privateChat_num()
    id = count_num + 1
    msg_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    conn.execute(
        '''
        insert into history_private_chat(id,target_user,source_user,time,text)
        values(?,?,?,?,?)
        ''',
        (id,receiver,sender,msg_time,message)
    )
    return "insert succ"

def get_privatechat_history(user1,user2):
    tups1 = conn.execute(' select * from history_private_chat where source_user = ? and target_user = ? order by time desc',(user1,user2,)).fetchall()
    tups2 = conn.execute('select * from history_private_chat where source_user = ? and target_user = ? order by time desc',(user2,user1,)).fetchall()

    lists = []
    for tup in tups1:
        lists.append([tup[2],tup[3],tup[4]])
    for tup in tups2:
        lists.append([tup[2],tup[3],tup[4]])
    lists.sort(key = lambda x:x[1])
    # lists结构： [发送方，时间，内容]
    return lists



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


def get_friends(username):
    #  tups = conn.execute('select * from userinfo where username = ?',(username,)).fetchall()
    tups = conn.execute('select * from friends where username1 = ?',(username,)).fetchall()

    tups_ = conn.execute('select * from friends where username2 = ?',(username,)).fetchall()
    res = [tup[1] for tup in tups]

    for tup in tups_:
        if tup[0] not in res:
            res.append(tup[0])
    return res


def add_friend(sender,replyer):
    # insert into group_file_history(id,source_user,time,filename,filecontent)
    conn.execute('''
     insert into friends(username1,username2)
     values(?,?)
    ''',(sender,replyer))


    return "add succ"




if __name__ == "__main__":
    init_database()
    #ans = get_friends("xixi")
    #for a in ans:
    #    print(a,end = ' ')

    #file = get_file_by_name("QuickFindUF.java")
    #print(file)
    #print(len(file))
    #ans = count_privateChat_num()
    #print(ans)
    
    # test code
    """
    chats = get_privatechat_history("xixi", "mama")
    for chat in chats:
        print(chat)

    tups = conn.execute('select * from history_private_chat').fetchall()
    for tup in tups:
        print(tup[0],tup[1],tup[2],tup[3],tup[4])
   
    print(get_friends("aerber"))
    """
