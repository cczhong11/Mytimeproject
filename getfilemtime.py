import os
import datetime
def getmdtime(path):
    k = os.path.getmtime(path)
    md = datetime.datetime.fromtimestamp(int(k))
    return md


PATH='E:/sync'
def write_this_week_work(paths,currentday):
    file = str(currentday.isocalendar()[1])+"_file_added.txt"
    f = open("log/"+file,"w+", encoding="utf-8")
    for path in paths:
        try:
            for i in os.walk(paths):
                folder = i[0]
                folder=folder.replace("\\",r"/")
                #print(folder)
                if 'git' in folder or 'pycache' in folder or 'vscode' in folder or 'Rproj' in folder:
                    continue
                
                flag = 0
                for one in i[2]:
                    filetext = i[0]+'/'+one
                    date = getmdtime(filetext)
                    if date<=datetime.datetime.now() and date>=currentday-datetime.timedelta(days=7):            
                        if flag==0:
                            print(i[0]+'\n-----------------------------')
                            f.write(i[0]+'\n-----------------------------\n')
                            flag =1
                        print(one)
                        f.write(one+'\n')
                    
                if flag==1:
                    print('-----------------------------')
                    f.write('-----------------------------\n')
        except:
            continue
    f.close()
    
def write_today_work(paths,currentday):
    s=''
    for path in paths:
        try:
            for i in os.walk(path):
                folder = i[0]
                folder=folder.replace("\\",r"/")
                #print(folder)
                if 'git' in folder or 'pycache' in folder or 'vscode' in folder or 'Rproj' in folder:
                    continue
                
                flag = 0
                for one in i[2]:
                    filetext = i[0]+'/'+one
                    date = getmdtime(filetext)
                    if date<=currentday and date>=currentday-datetime.timedelta(days=1):            
                        if flag==0:
                            print(i[0]+'\n-----------------------------')
                            s=s+i[0]+'\n-----------------------------\n'
                            flag =1
                        print(one)
                        s=s+one+'\n'
                    
                if flag==1:
                    print('-----------------------------')
                    s=s+'-----------------------------\n\n'
        except:
            continue
    return s
#write_this_week_work(PATH,datetime.datetime.now())