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




def from_task(task):
    '''turn task to Titem'''
    newT = Titem(task.get_name())
    