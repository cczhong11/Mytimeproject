'''for gui'''
import tkinter
from Tasklist import Tasklist
from tkinter import *



def donothing():
    '''do nothing'''
    filewin = Toplevel(TOP)
    button = Button(filewin, text="Do nothing button")
    button.pack()

def show_today():
    '''show today tasks and done tasks'''
    todaywin = Toplevel(TOP)
    b_refresh = Button(todaywin, text="Refreash")
    A = Tasklist("winter_holiday")
    A.add_to_today()
    CheckVar = []
    Checkbox = []
    i = 0
    b_refresh.pack()
    todaywin.geometry('800x600+0+0')
    for task in A.today:
        CheckVar.append(IntVar())
        Checkbox.append(Checkbutton(todaywin, text=str(i)+":"+task.get_string(), \
                variable=CheckVar[i], onvalue=1, offvalue=0, height=2, \
                 width=50))
        Checkbox[i].pack()
        i += 1
        
    

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
    taskmenu.add_command(label="Tommorrow tasks", command=donothing)
    taskmenu.add_command(label="Show as type", command=donothing)
    taskmenu.add_command(label="Show with prority and urgent", command=donothing)
    taskmenu.add_command(label="Finished tasks", command=donothing)
    menubar.add_cascade(label="Tasks", menu=taskmenu)
    calendarmenu = Menu(menubar, tearoff=0)
    calendarmenu.add_command(label="today", command=donothing)
    calendarmenu.add_command(label="tomorrow", command=donothing)
    menubar.add_cascade(label="Calendar", menu=calendarmenu)
    return menubar

if __name__ == "__main__":
    TOP = tkinter.Tk()
    TOP.geometry('800x600+0+0')
    MENUBAR = init_menu(TOP)
    TOP.config(menu=MENUBAR)
    TOP.mainloop()