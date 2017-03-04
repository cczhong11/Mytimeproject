'''for gui'''
import tkinter
from Tasklist import Tasklist
from Task import Task
from tkinter import *
from cal import Cal
import datetime
from Titem import *
from tkinter import messagebox
from report import Report
CURRENTDAY = datetime.datetime.now()
ssss = 0
Ann = Tasklist("new_term")
def destory_all(frame0):
    '''destory all widget'''
    for widget in frame0.winfo_children():
        widget.destroy()

def donothing():
    '''do nothing'''
    filewin = Toplevel(TOP)
    button = Button(filewin, text="Do nothing button")
    button.pack()

def add_newtask():
    '''add new task'''
    filewin = Toplevel(TOP)
    string_task = ['name','deadline(YYYY-MM-DD)','type(study,life,work,other)',\
    'priority','urgent','expected_time','tasklist(to do, later watch)','repeated_day', 'detail_type']
    Labels.clear()
    StringVars.clear()
    Ent.clear()
    i = 0
    for string_t in string_task:
        Ent.append(Entry(filewin))
        StringVars.append(StringVar())
        Labels.append(Label(filewin, textvariable=StringVars[i]))
        StringVars[i].set(string_t)
        Labels[i].grid(row=i,column=0)
        Ent[i].grid(row=i,column=1)
        i += 1

    button = Button(filewin, text="add",command=lambda :add_new_task(filewin))
    button.grid(row=i,column=1)
def add_activity():
    '''add new task'''
    filewin = Toplevel(TOP)    
    string_task = ['name','type', 'detail_type']
    Labels.clear()
    StringVars.clear()
    Ent.clear()
    i = 0
    for string_t in string_task:
        Ent.append(Entry(filewin))
        StringVars.append(StringVar())
        Labels.append(Label(filewin, textvariable=StringVars[i]))
        StringVars[i].set(string_t)
        Labels[i].grid(row=i, column=0)
        Ent[i].grid(row=i, column=1)
        i += 1

    button = Button(filewin, text="add",command=lambda :add_new_activity(filewin))
    button.grid(row=i,column=1)



def add_new_task(filewin):
    '''add new task for button'''
    name = Ent[0].get()
    deadline = Ent[1].get()
    new_task = Task(name, deadline)
    new_task.task_type = Ent[2].get()
    new_task.priority = Ent[3].get()
    new_task.urgent = Ent[4].get()
    new_task.expected_time = Ent[5].get()
    new_task.tasklistname = Ent[6].get()
    new_task.repeat_day = Ent[7].get()
    new_task.detail_type = Ent[8].get()
    Ann.add_task(new_task)
    filewin.destroy()

def add_new_activity(filewin):
    '''add new task for button'''
    name = Ent[0].get()
    type0 = Ent[1].get()    
    detail_type = Ent[2].get()
    Cnn.add_activity(name, type0, detail_type)
    Cnn.fetch_activity()
    filewin.destroy()

def refresh_today():
    '''get new today'''
    for index in range(len(Ann.today)):
        if CheckVar[index].get() == 1:
            thing = Ent[index].get()
            if  thing != '':
                if len(thing.split(';'))==1:
                    Ann.done_task(Ann.today[index], float(Ent[index].get()), day0=CURRENTDAY)
                else:
                    things = thing.split(';')
                    Ann.done_task(Ann.today[index], float(things[0]), day0=CURRENTDAY)
                    times = things[1].split('-')
                    date = CURRENTDAY.date()
                    time1 = datetime.datetime.strptime(times[0],"%H:%M")
                    time2 = datetime.datetime.strptime(times[1],"%H:%M")
                    newT = from_task(Ann.today[index])
                    newT.start_time = time1.replace(year=date.year, month=date.month, day=date.day)
                    newT.end_time = time2.replace(year=date.year, month=date.month, day=date.day)
                    Cnn.add_Titems(newT)
                    if len(things)==3:
                        Cnn.update_efficience(newT, int(things[2]))
                    else:
                        Cnn.update_efficience(newT, 10)
            else:
                Ann.done_task(Ann.today[index], day0=CURRENTDAY)
    show_today()

def show_today():
    '''show today tasks and done tasks'''
    #todaywin = Toplevel(TOP)
    destory_all(TOP)
    b_refresh = Button(TOP, text="Refreash", command=refresh_today)    
    Ann.add_to_today(CURRENTDAY)
    CheckVar.clear()
    Checkbox.clear()
    Ent.clear()
    i = 0
    b_refresh.grid(row = 0,column=0)
    #todaywin.geometry('800x600+0+0')
    for task in Ann.today:
        CheckVar.append(IntVar())
        Checkbox.append(Checkbutton(TOP, text=str(i)+":"+task.get_string(), \
                variable=CheckVar[i], onvalue=1, offvalue=0, height=1, \
                 width=50))
        Checkbox[i].grid(row=i+1, column=0)
        Ent.append(Entry(TOP))
        Ent[i].grid(row=i+1, column=1)
        i += 1


def show_tomorrow():
    '''show tomorrow tasks '''
    #todaywin = Toplevel(TOP)
    destory_all(TOP)
    Labels.clear()
    StringVars.clear()
    i = 0
    Ann.add_to_tomorrow(CURRENTDAY)
    #todaywin.geometry('800x600+0+0')
    for task in Ann.today:
        StringVars.append(StringVar())
        Labels.append(Label(TOP, textvariable=StringVars[i]))
        StringVars[i].set(str(i)+":"+task.get_string())
        Labels[i].grid(row=i,column=0)
        i += 1

def show_all():
    '''show all tasks '''
    #todaywin = Toplevel(TOP)
    destory_all(TOP)
    Labels.clear()
    StringVars.clear()
    i = 0
    Ann.add_to_all()
    #todaywin.geometry('800x600+0+0')
    for task in Ann.all_task:
        StringVars.append(StringVar())
        Labels.append(Label(TOP, textvariable=StringVars[i]))
        StringVars[i].set(str(i)+":"+task.get_string())
        Labels[i].grid(row=i, column=0)
        i += 1

def finish_t():
    '''finish task for button'''
    for index in range(len(Ann.all_task)):
        if CheckVar[index].get() == 1:            
            Ann.update_finished(Ann.all_task[index])

    finish_task()


def finish_task():
    '''finish task'''
    destory_all(TOP)
    b_refresh = Button(TOP, text="Finished", command=finish_t)    
    Ann.add_to_all()
    CheckVar.clear()
    Checkbox.clear()
    i = 0
    b_refresh.grid(row = 0, column=0)
    #todaywin.geometry('800x600+0+0')
    for task in Ann.all_task:
        CheckVar.append(IntVar())
        Checkbox.append(Checkbutton(TOP, text=str(i)+":"+task.get_string(), \
                variable=CheckVar[i], onvalue=1, offvalue=0, height=1, \
                 width=50))
        Checkbox[i].grid(row=i+1, column=0)
        i += 1


def show_type(type0):
    '''after click'''
    if type0!='':
        Ann.add_to_type(type0)
    for i in Labels:
        i.destroy()
    Labels.clear()
    StringVars.clear()
    i = 0
    for task in Ann.type_task:
        StringVars.append(StringVar())
        Labels.append(Label(TOP, textvariable=StringVars[i]))
        StringVars[i].set(str(i)+":"+task.get_string())
        Labels[i].grid(row=i+2, column=0)
        i += 1


def show_as_type():
    '''show tasks type'''
    destory_all(TOP)
    Lb1 = Listbox(TOP)
    Lb1.insert(1, "study")
    Lb1.insert(2, "life")
    Lb1.insert(3, "work")
    Lb1.insert(4, "other")
    Lb1.insert(5, "to do") 
    Lb1.insert(6, "later")
    Lb1.insert(7, "watch")
    
    Lb1.grid(row=0, column=0)    
    frame2 = Frame(TOP)
    frame2.grid(row=2, column=0)
    button1 = Button(TOP, text="Yes", command=lambda: show_type(Lb1.get(Lb1.curselection()[0])))
    button1.grid(row=1, column=0)




'''calendar ------------------------------'''
def assign_tomorrow():
    '''assign for tomorrow window'''
    destory_all(TOP)
    Labels.clear()
    StringVars.clear()
    Ent.clear()
    i = 0
    Ann.add_to_tomorrow()
    
    #todaywin.geometry('800x600+0+0')
    for task in Ann.today:
        StringVars.append(StringVar())
        Labels.append(Label(TOP, textvariable=StringVars[i]))
        StringVars[i].set(str(i)+":"+task.get_name())
        Labels[i].grid(row=i, column=0)
        i += 1
    m1 = i
    i = 0
    for itime in range(8, 23):
        if itime in [8, 12, 18]:
            continue
        StringVars.append(StringVar())
        Labels.append(Label(TOP, textvariable=StringVars[m1+i]))
        StringVars[m1+i].set(str(itime)+":00")
        Labels[m1+i].grid(row=i, column=1)
        i += 1
        StringVars.append(StringVar())
        Labels.append(Label(TOP, textvariable=StringVars[m1+i]))
        StringVars[m1+i].set(str(itime)+":30")
        Labels[m1+i].grid(row=i,column=1)
        i += 1
    m2 = i

    for i in range(m2):
        Ent.append(Entry(TOP))
        Ent[i].grid(row=i, column=2)
    '''add type?'''
    i = 0
    m3 = len(StringVars)
    for task in Cnn.activities:
        StringVars.append(StringVar())
        Labels.append(Label(TOP, textvariable=StringVars[m3+i]))
        StringVars[m3+i].set(str(i+100)+":"+task[0])
        Labels[m3+i].grid(row=i, column=3)
        i += 1
    button = Button(TOP, text="add",command=add_tomorrow)
    button.grid(row=0,column=4)


def add_tomorrow():
    '''add tomorrow calendar for button'''
    m1 = len(Ann.today)
    date = CURRENTDAY.date()+datetime.timedelta(days=1)
    tits = []
    for i in range(24):
        thing = Ent[i].get()
        if len(thing)!=0:
            ntype =''
            ndtype=''
            if thing.isdigit() is True:
                if int(thing) <100:
                    thing = StringVars[int(thing)].get().split(":")[1]
                    ntask = Ann.find_by_name(thing)
                    ntype = ntask.task_type
                    ndtype = ntask.detail_type
                else:
                    k = int(thing)-100
                    thing = Cnn.activities[k][0]
                    ntype = Cnn.activities[k][1]
                    ndtype = Cnn.activities[k][2]
            else:
                if len(thing.split(";")) == 3:
                    things = thing.split(";")
                    thing = things[0]
                    ntype = things[1]
                    ndtype = things[2]
            time = datetime.datetime.strptime(StringVars[m1+i].get(),"%H:%M")
            tit = Titem(thing)
            tit.start_time =  time.replace(year=date.year, month=date.month, day=date.day)
            tit.end_time = tit.start_time+datetime.timedelta(minutes=30)
            tit.type = ntype
            tit.detail_type = ndtype
            tits.append(tit)
    j = 0
    for i in range(23):
        tit1 = tits[j]
        tit2 = tits[j+1]
        if tit1.combine(tit2):
            tits.remove(tit2)
            if i == 22:
                Cnn.add_Titems(tit1)
        else:
            j += 1
            Cnn.add_Titems(tit1)

def update_eff():
    '''update for efficience button'''
    global  CURRENTDAY
    for i in range(len(Cnn.Titems)):
        thing = Ent[i].get().split(";")
        eff = int(thing[0])
        if eff < 6 and len(thing) == 4:
            ntit = copy_t(Cnn.Titems[i])            
            ntit.set_name(thing[1])
            ntit.type = thing[2]
            ntit.detail_type = thing[3]
            Cnn.update_efficience(Cnn.Titems[i], eff, ntit)
        elif len(thing) == 2:
            ntit = copy_t(Cnn.Titems[i])            
            k = int(thing[1])-100
            ntit.set_name(Cnn.activities[k][0])
            ntit.type = Cnn.activities[k][1]
            ntit.detail_type = Cnn.activities[k][2]
            Cnn.update_efficience(Cnn.Titems[i], eff, ntit)
        else:
            Cnn.update_efficience(Cnn.Titems[i], eff)
        name = Cnn.Titems[i].get_name()
        duration = (Cnn.Titems[i].end_time-Cnn.Titems[i].start_time).seconds/3600
        duration = duration*eff/10
        Ta = Ann.find_by_name(name)
        if Ta != -1:
            Ann.done_task(Ta,(duration),day0=CURRENTDAY)

def assign_yesterday():
    '''assign global varible CURRENTDAY to yesterday'''
    global  CURRENTDAY
    CURRENTDAY = datetime.datetime.now()-datetime.timedelta(days=1)
    messagebox.showinfo("Message", "Ok!")

def show_today_cal():
    '''show today cal'''    
    destory_all(TOP)
    Labels.clear()
    StringVars.clear()
    Labels2 = []
    StringVars2 = []
    Ent.clear()
    i = 0
    #print(CURRENTDAY)
    Cnn.add_all_Titems(CURRENTDAY.date().strftime("%Y-%m-%d"))
    for tit in Cnn.Titems:
        StringVars.append(StringVar())
        Labels.append(Label(TOP, textvariable=StringVars[i]))
        StringVars[i].set(tit.start_time.strftime("%H:%M")+"-"+ tit.end_time.strftime("%H:%M"))
        Labels[i].grid(row=i, column=0)
        StringVars2.append(StringVar())
        Labels2.append(Label(TOP, textvariable=StringVars2[i]))
        StringVars2[i].set(tit.get_name())
        Labels2[i].grid(row=i, column=1)
        Ent.append(Entry(TOP))
        Ent[i].grid(row=i, column=2)
        i += 1
    m3 = i
    i = 0
    for task in Cnn.activities:
       StringVars.append(StringVar())
       Labels.append(Label(TOP, textvariable=StringVars[m3+i]))
       StringVars[m3+i].set(str(i+100)+":"+task[0])
       Labels[m3+i].grid(row=i, column=3)
       i += 1
    button = Button(TOP, text="update efficience",command=update_eff)
    button.grid(row=0,column=4)

def report_week():
    '''Report for this week'''
    global CURRENTDAY
    Rnn.weekly(CURRENTDAY.isocalendar()[1])

def report_tracker():
    '''report for habit tracker'''
    global CURRENTDAY
    Rnn.weekly_summary(CURRENTDAY.isocalendar()[1])

def export_to_csv():
    '''export to csv'''
    date = CURRENTDAY.date()+datetime.timedelta(days=1)
    day = date.strftime("%Y-%m-%d")
    Cnn.write_to_csv(day)
    messagebox.showinfo("Message", day+"Ok!")



def init_menu(top):
    '''initialize Menu'''
    menubar = Menu(top)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Import from csv for tasks", command=donothing)
    filemenu.add_command(label="Import from csv for calendar", command=donothing)
    filemenu.add_command(label="Sync your tasks", command=donothing)
    filemenu.add_command(label="Sync your calendar", command=donothing)
    filemenu.add_command(label="Export csv for tasks", command=donothing)
    filemenu.add_command(label="Export csv for calendar", command=export_to_csv)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=top.quit)
    menubar.add_cascade(label="File", menu=filemenu)
    taskmenu = Menu(menubar, tearoff=0)
    taskmenu.add_command(label="Add new tasks", command=add_newtask)
    taskmenu.add_separator()

    taskmenu.add_command(label="Today tasks", command=show_today)
    taskmenu.add_command(label="Tommorrow tasks", command=show_tomorrow)
    taskmenu.add_command(label="Show as type", command=show_as_type)
    taskmenu.add_command(label="Show with prority and urgent", command=donothing)
    taskmenu.add_command(label="Finished tasks", command=finish_task)
    taskmenu.add_command(label="Show all tasks", command=show_all)
    if ssss == 1:
        taskmenu.add_command(label="Switch to other tasklist", command=switch_t)
    menubar.add_cascade(label="Tasks", menu=taskmenu)
    calendarmenu = Menu(menubar, tearoff=0)
    calendarmenu.add_command(label="Today", command=show_today_cal)
    calendarmenu.add_command(label="Tomorrow", command=assign_tomorrow)
    calendarmenu.add_separator()
    calendarmenu.add_command(label="Return to yesterday", command=assign_yesterday)
    calendarmenu.add_command(label="Add activity", command=add_activity)
    menubar.add_cascade(label="Calendar", menu=calendarmenu)
    reportmenu = Menu(menubar, tearoff=0)
    reportmenu.add_command(label="This week summary", command=report_week)
    reportmenu.add_command(label="This week task tracker", command=report_tracker)
     
    
    menubar.add_cascade(label="Report", menu=reportmenu)
    return menubar

def switch_t():
    global Ann
    if Ann.name == "winter_holiday":
        Ann = Tasklist("new_term")
    else:
     Ann = Tasklist("winter_holiday")

if __name__ == "__main__":
    root = tkinter.Tk()
    root.geometry('800x600+100+0')
    TOP = Frame(root)
    MENUBAR = init_menu(root)
    TOP.pack()
    root.config(menu=MENUBAR)
    #Ann = Tasklist("winter_holiday")
    #Ann = Tasklist("new_term")
     
    Cnn = Cal()
    Rnn = Report(Ann)
    Cnn.fetch_activity()
    CheckVar = []
    Checkbox = []
    Ent = []
    Labels = []
    StringVars = []
    Lb1 = Listbox(TOP)
    frame2 = Frame(TOP)
    root.mainloop()