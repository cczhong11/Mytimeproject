import sqlite3
from cal import *
from Tasklist import *
from Task import *
from Titem import *

conn = sqlite3.connect('tasks.sqlite')
Ann = Tasklist("winter_holiday")
Cnn = Cal()

sql = "select * from calendar"
cu0 =  conn.cursor()
cu0.execute(sql)
conn.commit()
result = cu0.fetchall()
cu0.close()
'''
for tit in result:
    tit = from_tuple_t(tit)
    
    sql = "Select * from 'winter_holiday' where name = ?"
    cu0 = conn.cursor()
    cu0.execute(sql, (tit.get_name(),))
    res = cu0.fetchone()    
    try:
        task2 = from_tuple(res)
        tit.type = task2.task_type
        tit.detail_type = task2.detail_type
        update_sql = "UPDATE calendar SET type = ? WHERE name = ?"
        update_sql2 = "UPDATE calendar SET Detail_type = ? WHERE name = ?"
        cu0.execute(update_sql, (tit.type, tit.get_name()))
        conn.commit()
        cu0.execute(update_sql2, (tit.detail_type, tit.get_name()))
        conn.commit()
        cu0.close()
    except:
        task = -1
'''
cu0 = conn.cursor()
for tit in result:
    tit = from_tuple_t(tit)
    if tit.type!='':
        continue
    else:
        name = tit.get_name()
        if name.find("driving") != -1:
            tit.type = "life"
            tit.detail_type = "driving"
        if name.find("shopping")!=-1:
            tit.type = "life"
            tit.detail_type = "shopping"
        if name.find("hihocoder")!=-1:
            tit.type = "study"
            tit.detail_type = "programming"
        if name.find("pocket")!=-1:
            tit.type = "study"
            tit.detail_type = "reading"
        if name.find("travel")!=-1:
            tit.type = "life"
            tit.detail_type = "travel"
        
        update_sql = "UPDATE calendar SET type = ? WHERE name = ?"
        update_sql2 = "UPDATE calendar SET Detail_type = ? WHERE name = ?"
        cu0.execute(update_sql, (tit.type, tit.get_name()))
        conn.commit()
        cu0.execute(update_sql2, (tit.detail_type, tit.get_name()))
        conn.commit()
cu0.close()