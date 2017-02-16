'''report for my life task
from bokeh.plotting import figure, show, output_file'''
from bokeh.charts import Donut, show, output_file
from bokeh.models import HoverTool, ColumnDataSource

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

    def what_i_have_done(self, tasklist, ind, yom=0):
        '''print dot char'''        
        result = tasklist.report_u_habit(ind, yom)        
        for one in result:
            self.xname.append(one[0])
            self.yname.append(one[1])
        dot = figure(title="what i have done", tools="", toolbar_location=None,
            x_range=[0,max(self.yname)], y_range=self.xname)

        dot.segment(0,self.xname, self.yname, self.xname,  line_width=2, line_color="green", )
        dot.circle( self.yname,self.xname, size=15, fill_color="orange", line_color="green", line_width=3, )
        return dot

    def habit_tracker(self, tasklist):
        '''print rect chart'''

    def where_did_i_spend_time(self, cal):
        '''pie chart'''
        result = cal.report_doing(0,2)
        result = [get_time_delta(one) for one in result]
        df = pd.DataFrame(result, columns=['type', 'detail_type', 'duration'])        
        d = Donut(df, label=['type','detail_type'], values='duration',text_font_size='6pt')
        return(d)

    def efficient_time(self, cal):
        '''box chart'''

    def reading_progress(self, tasklist):
        '''rect chart'''

#---------------------------------------------------------
def get_time_delta(tup):
    '''rewrite tuple and get time delta'''
    a = datetime.datetime.strptime(tup[3],"%H:%M:%S") - datetime.datetime.strptime(tup[2],"%H:%M:%S")
    tup = tup[:2] + (a.seconds/3600,)
    return tup

def test_f():
    A = Tasklist("winter_holiday")
    C = Cal()
    R = Report()
    #get_time_delta(("a","b","11:02:00", "13:00:00"))
    p = R.where_did_i_spend_time(C)
    #p = R.what_i_have_done(A,5)
    output_file("report_test.html", title="test")
    show(p)

if __name__ == "__main__":
    test_f();



'''
xn = ['2017-1-1','2017-1-2']
yn = ['a','b']
co = ["#fb9a99","#cab2d6"]
al = [1,1]
xname = []
yname = []
color = []
alpha = []

i = 0
for i in xn:
    for j in yn:
        xname.append(i)
        yname.append(j)
        if i == 0:
            color.append(co[0])
            alpha.append(al[0])
            i = 1
            continue
        else:
            color.append(co[1])
            alpha.append(al[1])
            i = 0
source = ColumnDataSource(data=dict(
    xname=xname,
    yname=yname,
    colors=color,
    alphas=alpha,
    
))

p = figure(title="Les Mis Occurrences",
           x_axis_location="above", tools="hover,save",x_range=xn,y_range = yn,
           )

p.plot_width = 200
p.plot_height = 200
p.grid.grid_line_color = None
p.axis.axis_line_color = None
p.axis.major_tick_line_color = None
p.axis.major_label_text_font_size = "5pt"
p.axis.major_label_standoff = 0
p.xaxis.major_label_orientation = np.pi/3

p.rect('xname', 'yname', 1, 1, source=source,
       color='colors',  line_color=None,
       hover_line_color='black', hover_color='colors')

p.select_one(HoverTool).tooltips = [
    ('names', '@yname, @xname'),
   
]

output_file("report_test.html", title="les_mis.py example")

show(p) # show the plot'''
