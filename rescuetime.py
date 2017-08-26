'''save rescuetime report'''
import requests
import datetime
import json
import sqlite3
import csv
from decimal import *
getcontext().prec = 3
apikey = 'B639kTMYdfFanKzSRlarPeLnKgR1zt_4ZkuHRbDS'
conn = sqlite3.connect('rescuetime/rescue_time.sqlite')
samsung_api='B63UW63A9a_O6fCEOfzMxAd0Gl2ANxChWZ082NKg'
index = ['id','date','productivity_pulse','very_productive_percentage','productive_percentage','neutral_percentage','distracting_percentage','very_distracting_percentage','all_productive_percentage','all_distracting_percentage','uncategorized_percentage','business_percentage','communication_and_scheduling_percentage','social_networking_percentage','design_and_composition_percentage','entertainment_percentage','news_percentage','software_development_percentage','reference_and_learning_percentage','shopping_percentage','utilities_percentage','total_hours','very_productive_hours','productive_hours','neutral_hours','distracting_hours','very_distracting_hours','all_productive_hours','all_distracting_hours','uncategorized_hours','business_hours','communication_and_scheduling_hours','social_networking_hours','design_and_composition_hours','entertainment_hours','news_hours','software_development_hours','reference_and_learning_hours','shopping_hours','utilities_hours','total_duration_formatted','very_productive_duration_formatted','productive_duration_formatted','neutral_duration_formatted','distracting_duration_formatted','very_distracting_duration_formatted','all_productive_duration_formatted','all_distracting_duration_formatted','uncategorized_duration_formatted','business_duration_formatted','communication_and_scheduling_duration_formatted','social_networking_duration_formatted','design_and_composition_duration_formatted','entertainment_duration_formatted','news_duration_formatted','software_development_duration_formatted','reference_and_learning_duration_formatted','shopping_duration_formatted','utilities_duration_formatted']
def init():
    '''build sqlite'''
    create_table_sql = "CREATE TABLE IF NOT EXISTS daily_summary( \
                          'id' varchar(20) DEFAULT NULL, \
                          'date' varchar(20) DEFAULT NULL, \
                          'productivity_pulse' varchar(20) DEFAULT NULL, \
                          'very_productive_percentage' varchar(20) DEFAULT NULL, \
                          'productive_percentage' varchar(20) DEFAULT NULL, \
                          'neutral_percentage' varchar(20) DEFAULT NULL, \
                          'distracting_percentage' varchar(20) DEFAULT NULL, \
                          'very_distracting_percentage' varchar(20) DEFAULT NULL, \
                          'all_productive_percentage' varchar(20) DEFAULT NULL, \
                          'all_distracting_percentage' varchar(20) DEFAULT NULL, \
                          'uncategorized_percentage' varchar(20) DEFAULT NULL, \
                          'business_percentage' varchar(20) DEFAULT NULL, \
                          'communication_and_scheduling_percentage' varchar(20) DEFAULT NULL, \
                          'social_networking_percentage' varchar(20) DEFAULT NULL, \
                          'design_and_composition_percentage' varchar(20) DEFAULT NULL, \
                          'entertainment_percentage' varchar(20) DEFAULT NULL, \
                          'news_percentage' varchar(20) DEFAULT NULL, \
                          'software_development_percentage' varchar(20) DEFAULT NULL, \
                          'reference_and_learning_percentage' varchar(20) DEFAULT NULL, \
                          'shopping_percentage' varchar(20) DEFAULT NULL, \
                          'utilities_percentage' varchar(20) DEFAULT NULL, \
                          'total_hours' varchar(20) DEFAULT NULL, \
                          'very_productive_hours' varchar(20) DEFAULT NULL, \
                          'productive_hours' varchar(20) DEFAULT NULL, \
                          'neutral_hours' varchar(20) DEFAULT NULL, \
                          'distracting_hours' varchar(20) DEFAULT NULL, \
                          'very_distracting_hours' varchar(20) DEFAULT NULL, \
                          'all_productive_hours' varchar(20) DEFAULT NULL, \
                          'all_distracting_hours' varchar(20) DEFAULT NULL, \
                          'uncategorized_hours' varchar(20) DEFAULT NULL, \
                          'business_hours' varchar(20) DEFAULT NULL, \
                          'communication_and_scheduling_hours' varchar(20) DEFAULT NULL, \
                          'social_networking_hours' varchar(20) DEFAULT NULL, \
                          'design_and_composition_hours' varchar(20) DEFAULT NULL, \
                          'entertainment_hours' varchar(20) DEFAULT NULL, \
                          'news_hours' varchar(20) DEFAULT NULL, \
                          'software_development_hours' varchar(20) DEFAULT NULL, \
                          'reference_and_learning_hours' varchar(20) DEFAULT NULL, \
                          'shopping_hours' varchar(20) DEFAULT NULL, \
                          'utilities_hours' varchar(20) DEFAULT NULL, \
                          'total_duration_formatted' varchar(20) DEFAULT NULL, \
                          'very_productive_duration_formatted' varchar(20) DEFAULT NULL, \
                          'productive_duration_formatted' varchar(20) DEFAULT NULL, \
                          'neutral_duration_formatted' varchar(20) DEFAULT NULL, \
                          'distracting_duration_formatted' varchar(20) DEFAULT NULL, \
                          'very_distracting_duration_formatted' varchar(20) DEFAULT NULL, \
                          'all_productive_duration_formatted' varchar(20) DEFAULT NULL, \
                          'all_distracting_duration_formatted' varchar(20) DEFAULT NULL, \
                          'uncategorized_duration_formatted' varchar(20) DEFAULT NULL, \
                          'business_duration_formatted' varchar(20) DEFAULT NULL, \
                          'communication_and_scheduling_duration_formatted' varchar(20) DEFAULT NULL, \
                          'social_networking_duration_formatted' varchar(20) DEFAULT NULL, \
                          'design_and_composition_duration_formatted' varchar(20) DEFAULT NULL, \
                          'entertainment_duration_formatted' varchar(20) DEFAULT NULL, \
                          'news_duration_formatted' varchar(20) DEFAULT NULL, \
                          'software_development_duration_formatted' varchar(20) DEFAULT NULL, \
                          'reference_and_learning_duration_formatted' varchar(20) DEFAULT NULL, \
                          'shopping_duration_formatted' varchar(20) DEFAULT NULL, \
                          'utilities_duration_formatted' varchar(20) DEFAULT NULL, \
                          PRIMARY KEY (`id`))"
    Create_day="CREATE TABLE IF NOT EXISTS day_note( \
                          'id' int(50) DEFAULT NULL, \
                          'date' varchar(50) DEFAULT NULL, \
                          'Time Spent' varchar(20) DEFAULT NULL, \
                          'Number of People' varchar(20) DEFAULT NULL, \
                          'Activity' varchar(20) DEFAULT NULL, \
                           'Category' varchar(20) DEFAULT NULL, \
                           'Productivity' varchar(20) DEFAULT NULL, \
                           PRIMARY KEY (`id`))"
           
    cu = conn.cursor()
    cu.execute(create_table_sql)
    conn.commit()
    cu.execute(Create_day)
    conn.commit()
    cu.close()

def find_max_id():
    '''get max id in two different table'''
    cu0 = conn.cursor()        
    find_max_index = "SELECT MAX(id) FROM day_note"
    try:
        cu0.execute(find_max_index)
        result = int(cu0.fetchone()[0])
    except:
        result = -1
    cu0.close()
    return result+1
def find_last_day():
    '''get last day'''
    cu0 = conn.cursor() 
    find_max_index = "SELECT * FROM day_note where id=(SELECT MAX(id) FROM day_note)"
    cu0.execute(find_max_index)
    result = cu0.fetchone()[1].split('T')[0]
    cu0.close()
    return result
def get_daily_summary(day):
    '''get daily summay and save into sqlite'''
    url = "https://www.rescuetime.com/anapi/daily_summary_feed?key="
    insert_sql = "INSERT INTO daily_summary values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"

    r = requests.get(url+samsung_api)
    result = r.json()
    # add judge whether in the sql 
    #print(r.text)
    for aaa in result:        
        p = [aaa[a] for a in index]
        cu = conn.cursor()
        try:
            cu.execute(insert_sql, tuple(p))
            conn.commit()
        except:
            cu.close()    
            break
    
def download_csv(day):
    '''download csv'''
    URL="https://www.rescuetime.com/anapi/data?key="+samsung_api+"&perspective=interval&restrict_kind=activity&restrict_begin="+day+"&restrict_end="+day+"&format=csv"
    with requests.Session() as s:
        download = s.get(URL)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        insert_sql = "INSERT INTO day_note values (?,?,?,?,?,?,?)"
        cu = conn.cursor()
        my_list.remove(my_list[0])
        for row in my_list:            
            p = tuple(row)
            cu.execute(insert_sql, (find_max_id(),)+p)
            conn.commit()           
        
        cu.close()

def get_day_hour(day,hour):
    '''get day and hour from sql'''
    string2 = day.strftime("%Y-%m-%d")+'T'+hour.strftime("%H:%M:%S")
    
    find_sql = "select * from day_note where date=?"
    cu = conn.cursor()
    cu.execute(find_sql, (string2,))
    result = cu.fetchall()
    efftime = 0
    sumtime = 0
    inefftime=0    
    if len(result)==0:
        return -1
    for one in result:
        time = int(one[2])
        sumtime += time
        if one[6] == '1' or one[6] == '2':
            efftime += time
        elif one[6] == '-1' or one[6] == '-2':
            inefftime += time
    return (sumtime/60, efftime/sumtime, inefftime/sumtime)

def get_hour(day,hour):
    '''get all day with same hour'''
    avgs=0
    avge=0
    avgi=0
    N  = 0
    for one in day:
        result = get_day_hour(one,hour)
        if result==-1:
            continue
        if N == 0:
            avgs = result[0]
            avge = result[1]
            avgi = result[2]
        else:
            avgs = avgs*(1-1/(N+1))+result[0]/(N+1)
            avge = avge*(1-1/(N+1))+result[1]/(N+1)
            avgi = avgi*(1-1/(N+1))+result[2]/(N+1)
        N = N+1
    return(avgs, avge, avgi)

def get_all_from_rescuetime(day):
    '''get data for report'''
    hour = datetime.datetime(year=2000,month=1,day=1,hour=8)
    alltime=[]
    allsum=[]
    alleff=[]
    allineff=[]
    for time in range(16):
        nhour = hour+datetime.timedelta(hours=time)
        result = get_hour(day, nhour)
        alltime.append(time+8)#nhour.strftime("%H:%M:%S"))
        allsum.append(result[0])
        alleff.append(result[1])
        allineff.append(result[2])
    return alltime,allsum,alleff,allineff

def fetch_data():
    '''fetch from web'''
    get_daily_summary(1)
    a = datetime.datetime.strptime(find_last_day(),'%Y-%m-%d')
    l = (datetime.datetime.now()-a).days
    for i in range(1,l):
        b = a+datetime.timedelta(days=i)
        download_csv(b.strftime("%Y-%m-%d"))

if __name__ == "__main__":
    init()
    fetch_data()