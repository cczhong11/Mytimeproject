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
        self.all_task = []

    def new_task(self):
        '''add tasks to tasklists'''
        taskname = input("your new task: ")
        tasktime = input("your task deadline(yyyy-mm-dd): ")
        newtask = Task(taskname, tasktime)
        newtask.ask_details()
        newtask.print_simple_summary()
        return newtask

    def find_max_id(self, tol, tid):
        '''get max id in two different table'''
        cu0 = self.conn.cursor()
        if tol == 0:
            find_max_index = "SELECT MAX("+tid+") FROM "+self.name
        else :
            find_max_index = "SELECT MAX("+tid+") FROM log_"+self.name
        try:
            cu0.execute(find_max_index)
            result = int(cu0.fetchone()[0])
        except:
            result = -1
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
                          `done_time` varchar(20) DEFAULT NULL,\
                          `done_week` int(5) DEFAULT 0,\
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
        sql = "SELECT task_id from "+self.name+" WHERE name = '"+task.get_name()+"' AND finished = 0"
        cu0 = self.conn.cursor()
        cu0.execute(sql)
        result = cu0.fetchone()
        return result

    def done_task(self, task, addtime=1):
        '''add done log to log and add time to already'''
        data0 = self.fetch_task_id(task)
        data = data0+(task.get_name(), task.deadline.strftime("%Y-%m-%d"),\
        datetime.datetime.now().strftime("%Y-%m-%d"))
        data = (self.find_max_id(1, "id"), )+data+(datetime.datetime.now().isocalendar()[1],)
        cu0 = self.conn.cursor()
        save_sql = "INSERT INTO log_"+self.name+ " values (?, ?, ?, ?, ?, ?)"
        cu0.execute(save_sql, data)
        self.conn.commit()
        task.add_hours(addtime)
        update_sql = "UPDATE "+self.name+" SET already_time = ? WHERE task_id = ?"
        cu0.execute(update_sql, (task.already_time, data0[0]))
        self.conn.commit()
        cu0.close()


    def update_finished(self, task):
        '''update finished in table'''
        data0 = self.fetch_task_id(task)
        update_sql = "UPDATE "+self.name+" SET finished = ? WHERE task_id = ?"
        cu0 = self.conn.cursor()
        cu0.execute(update_sql, (1, data0[0]))
        self.conn.commit()
        cu0.close()

    def print_all(self):
        '''print all tasks'''
        sql = "Select * from "+self.name+" where finished = 0 order by deadline ASC"
        cu0 = self.conn.cursor()
        cu0.execute(sql)
        result = cu0.fetchall()
        i = 0
        self.all_task.clear()
        print("---------------------------")
        for task in result:
            task = from_tuple(task)
            self.all_task.append(task)
            print("%d:%s \t %s" % (i, task.get_name(),task.deadline.strftime("%Y-%m-%d")))
            i += 1
        print("---------------------------")
        cu0.close()



    def print_today(self):
        '''print all item should be done today'''
        sql = "Select * from "+self.name+" where finished = 0 order by deadline ASC"
        cu0 = self.conn.cursor()
        cu0.execute(sql)
        result = cu0.fetchall()
        sql_id = "Select task_id from log_"+self.name+" where done_time = '"+\
        datetime.datetime.today().strftime("%Y-%m-%d")+"'"
        cu0.execute(sql_id)
        result_id = cu0.fetchall()
        self.today.clear()
        i = 0
        print("---------------------------")
        for task in result:
            task = from_tuple(task)
            task_id = self.fetch_task_id(task)[0]
            if task_id in [i[0] for i in result_id]:
                continue
            day = (task.deadline - datetime.datetime.now()).days
            if (task.deadline - datetime.datetime.today()).days < 1:
                self.today.append(task)
                print("%d:%s" % (i, task.get_name()))
                i += 1
            elif day%task.repeat_day == 0:
                self.today.append(task)
                print("%d:%s" % (i, task.get_name()))
                i += 1
        print("---------------------------")
        cu0.close()

if __name__ == "__main__":
    A = Tasklist("winter_holiday")
    while 1:
        print(" 0: add tasks\n 1: done task \n 2: print all task")
        Key = input("your choice:")
        if int(Key) == 0:
            AT = A.new_task()
            A.add_task(AT)
            print("this task add successfully")
        elif int(Key) == 1:
            A.print_today()
            Index = input("choose task to be done: ")
            if Index == 'q':
                continue
            Time = input("how much time you spent in the task and did you finished(0 or 1): ")
            T = Time.split()
            A.done_task(A.today[int(Index)], int(T[0]))
            if int(T[1]) == 1:
                A.update_finished(A.today[int(Index)])

        elif int(Key) == 2:
            A.print_all()
            Index = input("choose task to be done: ")
            if Index == 'q':
                continue
            Time = input("how much time you spent in the task and did you finished(0 or 1): ")
            T = Time.split()
            A.done_task(A.all_task[int(Index)], int(T[0]))
            if int(T[1]) == 1:
                A.update_finished(A.all_task[int(Index)])
