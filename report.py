'''report for my life task'''
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.charts import Donut
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.layouts import layout, column
from Tasklist import *
from cal import Cal
import datetime
import pandas as pd
import numpy as np

class Report(object):
    '''report class'''
    def __init__(self):
        self.xname = []
        self.yname = []
        self.color = []
        self.alpha = []
        self.Ann = Tasklist("winter_holiday")
        self.Cnn = Cal()        
        self.Ann.add_to_all()

    def what_i_have_done(self, tasklist, ind, yom=0):
        '''print dot char'''
        self.clear_list()
        result = tasklist.report_u_habit(ind, yom)
        for one in result:
            self.xname.append(one[0])
            self.yname.append(one[1])
            dot = figure(title="what i have done", tools="", toolbar_location=None,
                        x_range=[0, max(self.yname)], y_range=self.xname)

        dot.segment(0,self.xname, self.yname, self.xname,  line_width=2, line_color="green", )
        dot.circle( self.yname,self.xname, size=15, fill_color="orange", line_color="green", line_width=3, )
        return dot

    def habit_tracker(self, tasklist, show_tasks, ind, yom=0):
        '''print rect chart'''
        self.clear_list()
        result = [tasklist.report_habit(one, ind, yom) for one in show_tasks]
        week = ['MON', 'TUE', 'WES', 'THU', 'FRI', 'SAT', 'SUN']
        days = []
        j = 0
        if yom == 0:
            nstart = datetime.date(2017, 1, 2) + datetime.timedelta(days=7*(ind-1))
            for one in show_tasks:
                for i in range(7):
                    k = (nstart+ datetime.timedelta(days=i*1)).strftime("%Y-%m-%d")
                    days.append(k)
                    self.xname.append(week[i])
                    self.yname.append(one)
                    self.alpha.append(1)
                    if len(result[j]) == 0:
                        self.color.append("#ed0909")
                        continue
                    #else:
                    minr = from_tup_to_list(result[j])
                    if k in minr:
                        self.color.append("#42f445")
                    else:
                        self.color.append("#ed0909")
                j += 1
        p = figure(title="my daily Report",
           x_axis_location="above", tools="hover,save",x_range=week,y_range = show_tasks,
           )
        source = ColumnDataSource(data=dict(
            xnames=self.xname,
            ynames=self.yname,
            colors=self.color,
            alphas=self.alpha,
            day = days
        ))
        p.plot_width = 400
        p.plot_height = 800
        p.grid.grid_line_color = "black"
        p.axis.axis_line_color = None
        p.axis.major_tick_line_color = None
        p.axis.major_label_text_font_size = "5pt"
        p.axis.major_label_standoff = 0
        p.rect(self.xname, self.yname, 1,1, source=source,
               color='colors',  line_color=None, 
               hover_line_color='black', hover_color='colors', )

        p.select_one(HoverTool).tooltips = [
            ('names', '@ynames, @xnames,@day'),]
        return p

    def where_did_i_spend_time(self, cal, ind, yom=0):
        '''pie chart'''
        result = cal.report_doing(ind, yom)
        result = [get_time_delta(one) for one in result]        
        df = pd.DataFrame(result, columns=['type', 'detail_type', 'duration'])        
        d = Donut(df, label=['type','detail_type'], values='duration',text_font_size='6pt')
        d.plot_width = 800
        d.plot_height = 600
        return(d)

    def efficient_time(self, cal):
        '''box chart'''

    def reading_progress(self, tasklist):
        '''rect chart'''

    def clear_list(self):
        '''clear all list'''
        self.xname.clear()
        self.yname.clear()
        self.color.clear()
        self.alpha.clear()

    def weekly(self, week):
        '''weekly summary'''
        
        #p1 = R.habit_tracker(A, get_text(A.all_task), week)
        p2 = self.where_did_i_spend_time(self.Cnn, week)
        p3 = self.what_i_have_done(self.Ann, week)
        output_file("report_test.html", title="test")
        #show(p1)
        show(column(p2, p3))
    
    def weekly_summary(self, week):
        '''weekly habits summary'''
        output_file("report_test2.html", title="test")
        p1 = self.habit_tracker(self.Ann, get_text(self.Ann.all_task), week)
        show(p1)
#---------------------------------------------------------
def get_time_delta(tup):
    '''rewrite tuple and get time delta'''
    a = datetime.datetime.strptime(tup[3],"%H:%M:%S") - datetime.datetime.strptime(tup[2],"%H:%M:%S")
    tup = tup[:2] + (a.seconds/3600,)
    return tup

def get_text(tasks):
    '''turn tasks to text'''
    a = []
    for one in tasks:
        a.append(one.get_name())
    return a

def from_tup_to_list(tup):
    b = []
    for j in tup:
        b.append(j[0])        
    return b
def test_f():    
    R = Report()
    R.weekly(7)
    R.weekly_summary(7)
if __name__ == "__main__":
    test_f()

