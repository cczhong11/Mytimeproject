
"""This script prompts a user to enter a message to encode or decode
 3  using a classic Caeser shift substitution (3 letter shift)"""
import datetime
from Thing import Thing

class Task(Thing):
    '''task class for task item'''
    def __init__(self, name, deadline, tasklistname=None, finished=False):
        Thing.__init__(self, name)
        self.deadline = datetime.datetime.strptime(deadline, "%Y-%m-%d")
        self.task_type = None
        self.week = self.deadline.isocalendar()[1]
        self.already_time = 0
        self.priority = 0
        self.expected_time = 0
        self.tasklistname = tasklistname
        self.finished = finished
        self.repeat_day = 0
        self.urgent = 0
        self.donetime = []
        self.index = 0
        self.addtime = datetime.datetime.now()

    def print_time_summary(self):
        '''this method can printout time summary for task'''
        print("taskname:%s \t;you expected spent %d hours;\t you spent %d hours" \
        % (self.get_name(), self.expected_time, self.already_time))

    def print_simple_summary(self):
        '''this method can print out simple summary'''
        print("taskname:%s ; task deadline:%s" \
        %(self.get_name(), self.deadline.strftime("%Y-%m-%d")))

    def ask_details(self):
        '''ask details for task'''
        self.task_type = input("this task type:study,life,work,other:")
        self.priority = input("this task priority is 0-5: ")
        self.urgent = input("this task urgent is 0-5: ")
        self.expected_time = int(input("this task expected finished time(hours):"))
        self.tasklistname = input("this task list is (to do/watch/later):")
        self.repeat_day = input("how often should I repeat this task:")

    def add_hours(self, add_time=1):
        '''Add time for a task'''
        self.already_time = self.already_time + add_time
        self.donetime.append(datetime.datetime.now())

    def is_overtime(self):
        '''judge whether task is over time'''
        if self.finished != True:
            if self.already_time > self.expected_time:
                return True
        return False
    def get_all(self):
        '''return a tuple represent all info'''
        t_all = (self.get_name(), self.deadline.strftime("%Y-%m-%d"), \
            self.tasklistname, self.task_type, self.week, self.already_time,\
            self.expected_time, self.finished, self.repeat_day, self.addtime.strftime("%Y-%m-%d"),\
        self.priority, self.urgent)
        return t_all
    
    def get_string(self):
        string = self.get_name()+"\t"+ self.deadline.strftime("%Y-%m-%d")
        return string

def from_tuple(tup):
    '''turn tuple to task'''
    newtask = Task(tup[1], tup[2])
    newtask.tasklistname = tup[3]
    newtask.task_type = tup[4]
    newtask.week = tup[5]
    newtask.already_time = tup[6]
    newtask.expected_time = tup[7]
    newtask.finished = tup[8]
    newtask.repeat_day = tup[9]
    newtask.addtime = tup[10]
    newtask.priority = tup[11]
    newtask.urgent = tup[12]
    return newtask

if __name__ == "__main__":
    A = Task("my first task", "2016-12-31")
    A.print_simple_summary()
    A.ask_details()
    print(A.get_all())

