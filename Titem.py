'''time item class'''
from Thing import Thing
import datetime
from Task import Task
import copy

class Titem(Thing):
    '''time item for calendar'''
    def __init__(self, name):
        Thing.__init__(self, name)
        self.start_time = datetime.datetime.now().date()
        self.end_time = datetime.datetime.now().date()
        self.type = ''
        self.detail_type=''
        self.efficient = 0

    def get_all(self):
        '''return a tuple represent all info'''
        t_all = (self.get_name(), self.start_time.strftime("%Y-%m-%d"),\
        self.end_time.strftime("%Y-%m-%d"), self.start_time.strftime("%H:%M:%S"),\
        self.end_time.strftime("%H:%M:%S"), self.efficient, self.type, self.detail_type)
        return t_all

    def combine(self, titem):
        '''combine another titem'''
        if self.get_name() == titem.get_name():
            if self.end_time == titem.start_time:
                self.end_time = titem.end_time
                return True
        return False

def copy_t(tit):
    '''copy a tit to another'''
    ntit = Titem('')
    ntit = copy.deepcopy(tit)
    #ntit.start_time = tit.start_time
    #ntit.end_time = tit.end_time
    #ntit.type = tit.type
    #ntit.detail_type= tit.type
    ntit.efficient = 10
    return ntit

def from_task(task):
    '''turn task to Titem'''
    newT = Titem(task.get_name())

def from_tuple(tup):
    '''TURN TUPLE TO SQL'''
    a = Titem(tup[1])
    str1 = tup[2] +" " + tup[4]
    str2 = tup[3] +" " + tup[5]
    a.start_time = datetime.datetime.strptime(str1, "%Y-%m-%d %H:%M:%S")
    a.end_time = datetime.datetime.strptime(str2, "%Y-%m-%d %H:%M:%S")
    a.efficient = tup[6]
    a.type = tup[7]
    a.detail_type = tup[8]
    return a