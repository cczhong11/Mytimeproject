
class Thing(object):
    '''base class'''
    def __init__(self, name):
        self.__name = name
        self.done = False

    def print_name(self):
        '''print name'''
        print('%s \n' % (self.get_name()))

    def get_name(self):
        '''get private name'''
        return self.__name

    def set_name(self, name):
        '''set private name'''
        self.__name = name
        