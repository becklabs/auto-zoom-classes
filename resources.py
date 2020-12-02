import pandas as pd
from dateparser import parse
import datetime
import os
import webbrowser

def class_info():
    data = pd.DataFrame(columns = ['classkey','url','period'])
    i = 0
    more_classes = 'y'
    while more_classes == 'y':
        data.loc[i,'classkey'] = str(input('Class Name: '))
        data.loc[i,'url'] = str(input('Class Meeting Link: '))
        data.loc[i,'period'] = int(input('Class Period #: '))
        more_classes = str(input('Add another class?(y/n): '))
        i+=1
    data.to_csv('schedule_data/class_info.csv',index=False)

def period_info():
    i = 0
    period_info = pd.DataFrame(columns = ['weekday','period_list'])
    weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday']
    for weekday in weekdays:
        period_info.loc[i,'weekday'] = weekday
        period_info.loc[i,'period_list'] = input(weekday+' '+'period sequence(comma seperated): ')
        i+=1
    period_info.to_csv('schedule_data/period_info.csv',index=False)
    
def block_info():
    i = 0
    more = 'y'
    block_info = pd.DataFrame(columns=['block','start_time','end_time'])
    while more == 'y':
        block_info.loc[i,'block'] = int(input('Block Number: '))
        block_info.loc[i,'start_time'] = parse(input('Block Start Time: ')).time()
        block_info.loc[i,'end_time'] = parse(input('Block End Time: ')).time()
        more = input('Add another block?(y/n): ')
        i+=1
    block_info.to_csv('schedule_data/block_info.csv',index=False)

def _collect(info):
    if info == 'class_info':
        class_info()
    if info == 'period_info':
        period_info()
    if info == 'block_info':
        block_info()

def _get():
        return pd.read_csv('schedule_data/class_info.csv'), pd.read_csv('schedule_data/period_info.csv'), pd.read_csv('schedule_data/block_info.csv')

def _parse():
    class_info, period_info, block_info = _get()
    #Parse class_info
    class_info = class_info.set_index(class_info['period'])
    class_info = class_info.drop(columns=['period'],axis=1)
    
    #Parse period_info
    period_info = period_info.set_index(period_info['weekday'])
    period_info = period_info.drop(columns=['weekday'],axis=1)
    period_info['period_list'] = [i.split(',') for i in period_info['period_list']]
    
    #Parse block_info
    block_info = block_info.set_index(block_info['block'])
    block_info = block_info.drop(columns=['Unnamed: 0','block'],axis=1)
    block_info['start_time'] = [parse(i).time() for i in block_info['start_time']]
    block_info['end_time'] = [parse(i).time() for i in block_info['end_time']]
    
    return class_info, period_info, block_info

def get_period(period_info, block_info):
    now = datetime.datetime.now()
    time = now.time()
    weekday = now.strftime('%A')
    
    if 'schedule_data' not in os.listdir():
        os.mkdir('schedule_data/')
    
    for info in ['class_info','period_info','block_info']:
        if  info+'.csv' not in os.listdir('schedule_data/'):
            _collect(info)
    
    
    period_list = period_info.loc[weekday,'period_list']
    period = None
    for block in range(1,len(block_info['start_time'])+1):
        if block_info.loc[block,'start_time'] <= time <= block_info.loc[block,'end_time']:
            period = period_list[block-1]
            break
    return period

def join_class(class_info, period, label):
    if period is not None:
        class_name = class_info.loc[int(period),'classkey']
        url = class_info.loc[int(period),'url']
        label.config(text=str('Joining: '+class_name))
        webbrowser.open(url)
    else:
        label.config(text=str('No current class'))