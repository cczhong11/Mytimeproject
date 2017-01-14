'''for gui'''
import tkinter
from Tasklist import Tasklist
from tkinter import *

def destory_all(frame0):
    '''destory all widget'''
    for widget in frame0.winfo_children():
        widget.destroy()

def donothing():
    '''do nothing'''
    filewin = Toplevel(TOP)
    button = Button(filewin, text="Do nothing button")
    button.pack()

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
    '''show today tasks and done tasks'''
    #todaywin = Toplevel(TOP)
    destory_all(TOP)
    Labels.clear()
    StringVars.clear()
    i = 0
    Ann.add_to_tomorrow()
    #todaywin.geometry('800x600+0+0')
    for task in Ann.today:
        StringVars.append(StringVar())
        Labels.append(Label(frame2, textvariable=StringVars[i]))
        StringVars[i].set(str(i)+":"+task.get_string())
        Labels[i].grid(row=i,column=0)
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
        Labels[i].grid(row=i+2,column=0)
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

def init_menu(top):
    '''initialize Menu'''
    menubar = Menu(top)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Import from csv for tasks", command=donothing)
    filemenu.add_command(label="Import from csv for calendar", command=donothing)
    filemenu.add_command(label="Sync your tasks", command=donothing)
    filemenu.add_command(label="Sync your calendar", command=donothing)
    filemenu.add_command(label="Export csv for tasks", command=donothing)
    filemenu.add_command(label="Export csv for calendar", command=donothing)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=top.quit)
    menubar.add_cascade(label="File", menu=filemenu)
    taskmenu = Menu(menubar, tearoff=0)
    taskmenu.add_command(label="Add new tasks", command=donothing)
    taskmenu.add_separator()

    taskmenu.add_command(label="Today tasks", command=show_today)
    taskmenu.add_command(label="Tommorrow tasks", command=show_tomorrow)
    taskmenu.add_command(label="Show as type", command=show_as_type)
    taskmenu.add_command(label="Show with prority and urgent", command=donothing)
    taskmenu.add_command(label="Finished tasks", command=donothing)
    taskmenu.add_command(label="Show all tasks", command=donothing)
    menubar.add_cascade(label="Tasks", menu=taskmenu)
    calendarmenu = Menu(menubar, tearoff=0)
    calendarmenu.add_command(label="today", command=donothing)
    calendarmenu.add_command(label="tomorrow", command=donothing)
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
    CheckVar = []
    Checkbox = []
    Ent = []
    Labels = []
    StringVars = []
    Lb1 = Listbox(TOP)
    frame2 = Frame(TOP)
    root.mainloop()