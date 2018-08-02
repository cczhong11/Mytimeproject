import sqlite3
from cal import *
from Tasklist import *
from Task import *
from Titem import *
import datetime
import pandas as pd
import numpy as np
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.charts import Donut
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.layouts import column
conn = sqlite3.connect('tasks.sqlite')
Ann = Tasklist("winter_holiday")
Cnn = Cal()

sql = "select * from calendar"
cu0 =  conn.cursor()
cu0.execute(sql)
conn.commit()
result = cu0.fetchall()
cu0.close()
'''
for tit in result:
    tit = from_tuple_t(tit)
    
    sql = "Select * from 'winter_holiday' where name = ?"
    cu0 = conn.cursor()
    cu0.execute(sql, (tit.get_name(),))
    res = cu0.fetchone()    
    try:
        task2 = from_tuple(res)
        tit.type = task2.task_type
        tit.detail_type = task2.detail_type
        update_sql = "UPDATE calendar SET type = ? WHERE name = ?"
        update_sql2 = "UPDATE calendar SET Detail_type = ? WHERE name = ?"
        cu0.execute(update_sql, (tit.type, tit.get_name()))
        conn.commit()
        cu0.execute(update_sql2, (tit.detail_type, tit.get_name()))
        conn.commit()
        cu0.close()
    except:
        task = -1

cu0 = conn.cursor()
for tit in result:
    tit = from_tuple_t(tit)
    if tit.type!='':
        continue
    else:
        name = tit.get_name()
        if name.find("driving") != -1:
            tit.type = "life"
            tit.detail_type = "driving"
        if name.find("shopping")!=-1:
            tit.type = "life"
            tit.detail_type = "shopping"
        if name.find("hihocoder")!=-1:
            tit.type = "study"
            tit.detail_type = "programming"
        if name.find("pocket")!=-1:
            tit.type = "study"
            tit.detail_type = "reading"
        if name.find("travel")!=-1:
            tit.type = "life"
            tit.detail_type = "travel"
        
        update_sql = "UPDATE calendar SET type = ? WHERE name = ?"
        update_sql2 = "UPDATE calendar SET Detail_type = ? WHERE name = ?"
        cu0.execute(update_sql, (tit.type, tit.get_name()))
        conn.commit()
        cu0.execute(update_sql2, (tit.detail_type, tit.get_name()))
        conn.commit()
cu0.close()'''



from bokeh.layouts import column
from bokeh.sampledata.autompg import autompg

import pandas as pd

# simple examples with inferred meaning

# implied index
d1 = Donut([2, 4, 5, 2, 8])

# explicit index
d2 = Donut(pd.Series([2, 4, 5, 2, 8], index=['a', 'b', 'c', 'd', 'e']))

# given a categorical series of data with no aggregation
d3 = Donut(autompg.cyl.astype(str))

# given a categorical series of data with no aggregation
d4 = Donut(autompg.groupby('cyl').displ.mean())

# given a categorical series of data with no aggregation
d5 = Donut(autompg.groupby(['cyl', 'origin']).displ.mean(),
           hover_text='mean')

# no values specified
d6 = Donut(autompg, label='cyl', agg='count')
print(autompg)
# explicit examples
d7 = Donut(autompg, label='cyl',
           values='displ', agg='mean')

# nested donut chart for the provided labels, with colors assigned
# by the first level
d8 = Donut(autompg, label=['cyl', 'origin'],
           values='displ', agg='mean')

# show altering the spacing in levels
d9 = Donut(autompg, label=['cyl', 'origin'],
           values='displ', agg='mean', level_spacing=0.15)

# show altering the spacing in levels
d10 = Donut(autompg, label=['cyl', 'origin'],
           values='displ', agg='mean', level_spacing=[0.8, 0.3])

output_file("donut_multi.html", title="donut_multi.py example")

show(column(d1, d2, d3, d4, d5, d6, d7, d8, d9, d10))