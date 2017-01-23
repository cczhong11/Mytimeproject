'''FOR calendar'''
import sqlite3
import datetime
from Titem import *

class Cal(object):
    def __init__(self,day):
        self.day = day
        self.Titems = []
        self.sync = False
        self.conn = sqlite3.connect('Cal.sqlite')
        self.create_table_sql()


    def add_Titems(self, titem):
        '''insert a item to sql'''
        newt = titem.get_all()
        cu0 =  self.conn.cursor()
        result = (self.find_max_id(),)
        save_sql = "INSERT INTO "+self.day+ " values (?, ?, ?, ?, ?, ?,?,?)"
        result = result + newt
        cu0.execute(save_sql, result)
        self.conn.commit()
        cu0.close()

    def find_max_id(self):
        '''get max id in two different table'''
        cu0 = self.conn.cursor()
        find_max_index = "SELECT MAX(cal_id) FROM "+self.day
        
        try:
            cu0.execute(find_max_index)
            result = int(cu0.fetchone()[0])
        except:
            result = -1
        cu0.close()
        return result+1

    def fetch_cal_id(self, titem):
        '''get cal_id'''
        sql = "SELECT cal_id from "+self.name+" WHERE name = '"+task.get_name()+"' AND finished = 0"
        cu0 = self.conn.cursor()
        cu0.execute(sql)
        result = cu0.fetchone()
        return result
    
    def create_table_sql(self):
        '''create sql table'''
        create_table_sql = "CREATE TABLE IF NOT EXISTS "+self.day+"(\
                          `cal_id` int(11) NOT NULL,\
                          `name` varchar(100) NOT NULL,\
                          `start_day` varchar(20) DEFAULT NULL,\
                          `end_day` varchar(20) DEFAULT NULL,\
                          `start_time` varchar(20) DEFAULT NULL,\
                          `end_time` varchar(20) DEFAULT 0,\
                          `efficient` int(5) DEFAULT 0,\
                           `type` int(5) DEFAULT 0,\
                          PRIMARY KEY (`task_id`))"        
        cu = self.conn.cursor()
        cu.execute(create_table_sql)
        self.conn.commit()
        
        cu.close()


    def add_all_Titems(self):
        '''add all to '''