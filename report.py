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
from rescuetime import *

class Report(object):
    '''report class'''
    def __init__(self,ann):
        self.xname = []
        self.yname = []
        self.color = []
        self.alpha = []
        self.Ann = ann
        self.Cnn = Cal()        
        self.Ann.add_to_all()

    def what_i_have_done(self, tasklist, ind, yom=0):
        '''print dot char'''
        self.clear_list()
        result = tasklist.report_u_habit(ind, yom)
        for one in result:
            self.xname.append(one[0])
            self.yname.append(one[1])
        
        dot = figure(title="what i have done", tools="", toolbar_location=None, x_range=[0, max(self.yname)], y_range=self.xname)

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
        source = ColumnDataSource({'type': list(df['type']),'detail_type':list(df['detail_type']), 'duration':list(df['duration'])})       
        grouped = df.groupby(['type', 'detail_type']).sum()
        grouped.to_csv("report/report_time_week_"+str(ind)+".csv", encoding='utf-8')
        d = Donut(data=df, label=['type','detail_type'], values='duration',text_font_size='6pt')
        d.plot_width = 800
        d.plot_height = 600
        return(d)

    def efficient_time(self, cal,ind,yom=0):
        '''dot chart for my inefficient time'''        
        xname1=[]
        yname1=[]
        result = cal.report_ineff(ind)
        print(result)
        for one in result:
            xname1.append(one[0])
            yname1.append(one[1])
        
        dot1 = figure(title="what i did not do", tools="", toolbar_location=None, x_range=[0, max(yname1)], y_range=xname1)

        dot1.segment(0,xname1, yname1, xname1,  line_width=2, line_color="green", )
        dot1.circle( yname1,xname1, size=15, fill_color="orange", line_color="green", line_width=3, )
        xname2=[]
        yname2=[]
        result = cal.report_ineff(ind,ineff=0)
        for one in result:
            xname2.append(one[0])
            yname2.append(one[1])
        
        dot2 = figure(title="what i real do", tools="", toolbar_location=None, x_range=[0, max(yname2)], y_range=xname2)

        dot2.segment(0,xname2, yname2, xname2,  line_width=2, line_color="green", )
        dot2.circle( yname2,xname2, size=15, fill_color="orange", line_color="green", line_width=3, )
        
        return (dot1,dot2)

    def reading_progress(self, tasklist):
        '''rect chart'''

    def rescuetime_result(self, week,ind=0):
        '''print data'''
        if ind==0:
            nstart = datetime.date(2017, 1, 2) + datetime.timedelta(days=7*(week-1))
            result = get_all_from_rescuetime([nstart + datetime.timedelta(days=i) for i in range(0 - nstart.weekday(), 7 - nstart.weekday())])
            p11 = figure(title="on computer time",width=400, height=200)
            p11.vbar(x=result[0], width=0.2, bottom=0,
                top=result[1], color="firebrick")
            p12 = figure(title="efficient time",width=400, height=200)
            p12.vbar(x=result[0], width=0.2, bottom=0,
                top=result[2], color="firebrick")
            p13 = figure(title="inefficient time",width=400, height=200)
            p13.vbar(x=result[0], width=0.2, bottom=0,
                top=result[3], color="firebrick")
        return (p11,p12,p13)


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
        output_file("report/report_pie_"+str(week)+".html", title="weekly summary")
        p4=self.rescuetime_result(week)
        p5 = self.efficient_time(self.Cnn, week)
        #show(p1)
        show(column(p2, p3,p4[0],p4[1],p4[2],p5[0],p5[1]))
    
    def weekly_summary(self, week):
        '''weekly habits summary'''
        output_file("report/report_tracker_"+str(week)+".html", title="habit tracker")
        p1 = self.habit_tracker(self.Ann, self.Ann.get_this_week(week), week)
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
    R = Report(Tasklist("new_term"))
    R.weekly(9)
    #R.weekly_summary(9)
if __name__ == "__main__":
    test_f()

