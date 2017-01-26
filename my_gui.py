'''for gui'''
import tkinter
from Tasklist import Tasklist
from Task import Task
from tkinter import *
from cal import Cal
import datetime
from Titem import *
from tkinter import messagebox


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
    'priority','urgent','expected_time','tasklist(to do, later watch)','repeated_day']
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

    button = Button(filewin, text="add",command=add_new_task)
    button.grid(row=i,column=1)

def add_new_task():
    '''add new task for button'''
    name = Ent[0].get()
    deadline = Ent[1].get()
    new_task = Task(name, deadline)
    new_task.type_task = Ent[2].get()
    new_task.priority = Ent[3].get()
    new_task.urgent = Ent[4].get()
    new_task.expected_time = Ent[5].get()
    new_task.tasklistname = Ent[6].get()
    new_task.repeat_day = Ent[7].get()
    Ann.add_task(new_task)


def refresh_today():
    '''get new today'''
    for index in range(len(Ann.today)):
        if CheckVar[index].get() == 1:
            if Ent[index].get() != '':
                Ann.done_task(Ann.today[index], int(Ent[index].get()))
            else:
                Ann.done_task(Ann.today[index])

    show_today()

def show_today():
    '''show today tasks and done tasks'''
    #todaywin = Toplevel(TOP)
    destory_all(TOP)
    b_refresh = Button(TOP, text="Refreash", command=refresh_today)    
    Ann.add_to_today()
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
    Ann.add_to_tomorrow()
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
    print(Lb1.get(1))
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
    print(m2)
    for i in range(m2):
        Ent.append(Entry(TOP))
        Ent[i].grid(row=i, column=2)
    '''add type?'''
    button = Button(TOP, text="add",command=add_tomorrow)
    button.grid(row=0,column=3)


def add_tomorrow():
    '''add tomorrow calendar for button'''
    m1 = len(Ann.today)
    date = datetime.datetime.now().date()+datetime.timedelta(days=1)
    tits = []
    for i in range(24):
        thing = Ent[i].get()
        if thing.isdigit() is True:
            thing = StringVars[int(thing)].get().split(":")[1]
        time = datetime.datetime.strptime(StringVars[m1+i].get(),"%H:%M")
        tit = Titem(thing)
        tit.start_time =  time.replace(year=date.year, month=date.month, day=date.day)
        tit.end_time = tit.start_time+datetime.timedelta(minutes=30)
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
    for i in range(len(Cnn.Titems)):
        eff = int(Ent[i].get())
        Cnn.update_efficience(Cnn.Titems[i], eff) 

def show_today_cal():
    '''show today cal'''
    destory_all(TOP)
    Labels.clear()
    StringVars.clear()
    Labels2 = []
    StringVars2 = []
    Ent.clear()
    i = 0
    Cnn.add_all_Titems(datetime.datetime.now().date().strftime("%Y-%m-%d"))
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
    button = Button(TOP, text="update efficience",command=update_eff)
    button.grid(row=0,column=3)

def export_to_csv():
    '''export to csv'''
    date = datetime.datetime.now().date()+datetime.timedelta(days=1)
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
    menubar.add_cascade(label="Tasks", menu=taskmenu)
    calendarmenu = Menu(menubar, tearoff=0)
    calendarmenu.add_command(label="today", command=show_today_cal)
    calendarmenu.add_command(label="tomorrow", command=assign_tomorrow)
    menubar.add_cascade(label="Calendar", menu=calendarmenu)
    return menubar



if __name__ == "__main__":
    root = tkinter.Tk()
    root.geometry('800x600+0+0')
    TOP = Frame(root)
    MENUBAR = init_menu(root)
    TOP.pack()
    root.config(menu=MENUBAR)
    Ann = Tasklist("winter_holiday")
    Cnn = Cal()
    CheckVar = []
    Checkbox = []
    Ent = []
    Labels = []
    StringVars = []
    Lb1 = Listbox(TOP)
    frame2 = Frame(TOP)
    root.mainloop()