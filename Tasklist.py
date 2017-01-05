'''for tasklists'''
import sqlite3
import datetime
from Task import *


class Tasklist(object):
    '''save task'''
    def __init__(self, name):
        self.name = name
        self.tasks = [Task("first", "1970-1-1")]
        self.hadsync = False
        self.conn = sqlite3.connect('tasks.sqlite')
        self.create_table_sql()
        self.today = []

    def new_task(self):
        '''add tasks to tasklists'''
        taskname = input("your new task: ")
        tasktime = input("your task deadline(yyyy-mm-dd): ")
        newtask = Task(taskname, tasktime)
        newtask.ask_details()
        newtask.print_simple_summary()
        return newtask
    
    def find_max_id(self, tol, id):
        '''get max id in two different table'''
        cu0 = self.conn.cursor()
        if tol == 0:
            find_max_index = "SELECT MAX("+id+") FROM "+self.name
        else :
            find_max_index = "SELECT MAX("+id+") FROM log_"+self.name
        cu0.execute(find_max_index)
        result = int(cu0.fetchone()[0])
        cu0.close()
        return result+1

    def add_task(self, task):
        '''add task to sqlite'''
        newt = task.get_all()
        cu0 =  self.conn.cursor()
        result = (self.find_max_id(0, "task_id"),)
        save_sql = "INSERT INTO "+self.name+ " values (?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?)"
        result = result + newt
        cu0.execute(save_sql, result)
        self.conn.commit()
        cu0.close()



    def create_table_sql(self):
        '''create sql table'''
        create_table_sql = "CREATE TABLE IF NOT EXISTS "+self.name+"(\
                          `task_id` int(11) NOT NULL,\
                          `name` varchar(100) NOT NULL,\
                          `deadline` varchar(20) DEFAULT NULL,\
                          `tasklistname` varchar(20) DEFAULT NULL,\
                          `task_type` varchar(20) DEFAULT NULL,\
                          `week` int(5) DEFAULT 0,\
                          `already_time` int(5) DEFAULT 0,\
                          `expected_time` int(5) DEFAULT 0,\
                          `finished` BOOLEAN DEFAULT FALSE,\
                          `repeated_day` int(5) DEFAULT 0,\
                          `addtime` varchar(20) DEFAULT NULL,\
                          `priority` int(10) DEFAULT NULL,\
                            `urgent` int(10) DEFAULT NULL,\
                           PRIMARY KEY (`task_id`))"
        create_table_log = "CREATE TABLE IF NOT EXISTS "+"log_"+self.name+"(\
                          `id` int(11) NOT NULL,\
                          'task_id' int(11) NOT NULL,\
                          `name` varchar(20) NOT NULL,\
                          `deadline` varchar(20) DEFAULT NULL,\
                          `donetime` varchar(20) DEFAULT NULL,\
                            PRIMARY KEY (`id`))"
        cu = self.conn.cursor()
        cu.execute(create_table_sql)
        self.conn.commit()
        cu.execute(create_table_log)
        self.conn.commit()
        cu.close()

    def sync(self):
        '''sync with wunderlists? maybe cannot success'''
        pass

    def delete_task(self, task):
        '''delete a tasks'''
        if task is not None:
            self.tasks.remove(task)
        else:
            print("No such tasks")

    def find_task(self, index):
        '''find a task'''
        pass


    def fetch_task_id(self, task):
        '''get task_id'''
        sql = "SELECT task_id from "+self.name+" where name is "+task.get_name()+" AND finished is 0"
        cu0 = self.conn.cursor()
        cu0.execute(sql)
        result = cu0.fetchone()
        return result

    def done_task(self, task, addtime=1):
        '''add done log to log and add time to already'''
        data = self.fetch_task_id(task)
        data = data+(task.get_name(), task.deadline.strftime("%Y-%m-%d"),\
        datetime.datetime.now().strftime("%Y-%m-%d"))
        data = (self.find_max_id(1, "id"), )+data
        cu0 = self.conn.cursor()
        save_sql = "INSERT INTO log_"+self.name+ " values (?, ?, ?, ?, ?)"
        cu0.execute(save_sql, data)
        self.conn.commit()
        task.add_hours(addtime)
        update_sql = "UPDATE "+self.name+" SET already_time = ? WHERE task_id = ?"
        cu0.execute(update_sql, (task.already_time, data[0]))
        cu0.close()


    def print_today(self):
        '''print all item should be done today'''
        sql = "Select * from "+self.name+" where finished is 0"
        cu0 = self.conn.cursor()
        cu0.execute(sql)
        result = cu0.fetchall()
        i = 0
        for task in result:
            task = from_tuple(task)
            day = (task.deadline - datetime.datetime.now()).days
            if (task.deadline - datetime.datetime.today()).days < 1:
                self.today.append(task)
                print("%d:%s" % (i, task.get_name()))
                i += 1
            elif day%task.repeat_day == 0:
                self.today.append(task)
                print("%d:%s" % (i, task.get_name()))
                i += 1

if __name__ == "__main__":
    A = Tasklist("test")
    while 1:
        print(" 0: add tasks\n 1:done task \n 2: print all task")
        Key = input("your choice:")
        if int(Key) == 0:
            AT = A.new_task()
            A.add_task(AT)
            print("this task add successfully")
        elif int(Key) == 1:
            A.print_today()
            Index = input("choose task to be done: ")
            Time = input("how much time you spent in the task: ")
            A.done_task(A.today[int(Index)], int(Time))
        