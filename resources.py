import pandas as pd
from dateparser import parse

def class_info():
    print('Running first time setup... input class info below')
    print('\n')
    data = pd.DataFrame(columns = ['classkey','url','period'])
    i = 0
    more_classes = 'y'
    while more_classes == 'y':
        data.loc[i,'classkey'] = str(input('Class Name: '))
        data.loc[i,'url'] = str(input('Class Meeting Link: '))
        data.loc[i,'period'] = int(input('Class Period #: '))
        more_classes = str(input('Add another class?(y/n): '))
        i+=1
    data.to_csv('classes.csv',index=False)

def period_info():
    i = 0
    more = 'y'
    period_info = pd.DataFrame(columns = ['weekday','period_list'])
    while more == 'y':
        period_info.loc[i,'weekday'] = input('Weekday(Ex: Monday): ')
        period_info.loc[i,'period_list'] = [int(x) for x in input('Period sequence: ').split(',')]
        more = input('Add another block?(y/n): ')
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
        return pd.read_csv('schedule_info/class_info.csv'),
        pd.read_csv('schedule_info/period_info.csv'),
        pd.read_csv('schedule_info/block_info.csv')

def parse_():
    class_info, period_info, block_info = _get()
    


