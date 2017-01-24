'''time item class'''
from Thing import Thing
import datetime
from Task import Task


class Titem(Thing):
    '''time item for calendar'''
    def __init__(self, name):
        Thing.__init__(self, name)
        self.start_time = datetime.datetime.now().date()
        self.end_time = datetime.datetime.now().date()
        self.type = ''
        self.efficient = 0

    def get_all(self):
        '''return a tuple represent all info'''
        t_all = (self.get_name(), self.start_time.strftime("%Y-%m-%d"),\
        self.end_time.strftime("%Y-%m-%d"), self.start_time.strftime("%H:%M:%S"),\
        self.end_time.strftime("%H:%M:%S"), self.efficient, self.type)
        return t_all


def from_task(task):
    '''turn task to Titem'''
    newT = Titem(task.get_name())
    