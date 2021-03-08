import pandas as pd
from dateparser import parse
import datetime
import os
import webbrowser
from tkinter import Tk,Label,Entry,Frame,Button

class Table:
    def __init__(self,columns=[],wname='Table'):
        self.root = Tk()
        self.root.title(wname)
        self.topFrame = Frame(self.root)
        self.topFrame.pack()
        self.bottomFrame = Frame(self.root)
        self.bottomFrame.pack(side='bottom')
        self.labels = []
        self.entries = []
        self.columns = list(columns.keys())
        for column in self.columns:
            label = Label(self.topFrame)
            label.config(text=str(column),font=('Arial',12,'bold'))
            label.grid(row = 0,column=self.columns.index(column))
            ex_label = Label(self.topFrame)
            ex_label.config(text='Ex: '+str(columns.get(column)))
            ex_label.grid(row = 1,column=self.columns.index(column))
            curr_entry = Entry(self.topFrame, width=20, fg='Black', font=('Arial',14,'normal'))
            self.entries.append(curr_entry)
            curr_entry.grid(row = 2,column=self.columns.index(column))
        self.button1 = Button(self.bottomFrame, text="Add Another Row", command=self.add_new_row).grid(row=0,column=0)
        self.button2 = Button(self.bottomFrame, text="Done", command=self.save).grid(row=0,column=2)
        self.root.mainloop()
    
    def add_new_row(self):
            total_columns,total_rows = self.topFrame.grid_size()
            for col in range(total_columns):
                curr_entry = Entry(self.topFrame, width=20, fg='black', 
                                       font=('Arial',14,'normal'))
                curr_entry.grid(row=total_rows+1,column=col)
                self.entries.append(curr_entry)

    def save(self):
        total_columns,total_rows = self.topFrame.grid_size()
        strata = []
        for row in range(total_rows):
            row_data = [str(entry.get()) for entry in self.entries if entry.grid_info()['row'] == row]
            strata.append(row_data)
        self.strata = []
        for row in strata:
            if len(row) == total_columns: 
                self.strata.append(row)
        self.root.destroy()
    
    def get_data(self):
        return self.strata
   
def class_info():
    #Column name: example input
    table = Table(columns={'Class Name': 'Physics','Meeting URL':'https://zoom.us/j/','Period #':'1'},wname='Class Info')
    data = table.get_data()
    print(data)
    class_info = pd.DataFrame(columns = ['classkey','url','period'])
    for row in data:
        class_info.loc[data.index(row),'classkey'] = str(row[0])
        class_info.loc[data.index(row),'url'] = str(row[1])
        class_info.loc[data.index(row),'period'] = int(row[2])
    class_info.to_csv('schedule_data/class_info.csv',index=False)
    
def period_info():
    table = Table(columns={'Weekday':'Monday','Period Sequence':'1,2,3,4,5'},wname='Period Info')
    data = table.get_data()
    period_info = pd.DataFrame(columns = ['weekday','period_list'])
    for row in data:
        period_info.loc[data.index(row),'weekday'] = str(row[0]).lower()
        period_info.loc[data.index(row),'period_list'] = str(row[1])
    period_info.to_csv('schedule_data/period_info.csv',index=False)
    
def block_info():
    table = Table(columns={'Block #': '4','Start Time':'11:30 AM','End Time': '1:30 PM'},wname='Block Info')
    data = table.get_data()
    block_info = pd.DataFrame(columns=['block','start_time','end_time'])
    for row in data:
        block_info.loc[data.index(row),'block'] = int(row[0])
        block_info.loc[data.index(row),'start_time'] = parse(row[1]).time()
        block_info.loc[data.index(row),'end_time'] = parse(row[2]).time()
    block_info.to_csv('schedule_data/block_info.csv',index=False)

def _collect(info):
    if info == 'class_info':
        class_info()
    if info == 'period_info':
        period_info()
    if info == 'block_info':
        block_info()

def _get():
    if 'schedule_data' not in os.listdir():
        os.mkdir('schedule_data/')
    
    for info in ['class_info','period_info','block_info']:
        if  info+'.csv' not in os.listdir('schedule_data/'):
            _collect(info)
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
    block_info = block_info.drop(columns=['block'],axis=1)
    block_info['start_time'] = [parse(i).time() for i in block_info['start_time']]
    block_info['end_time'] = [parse(i).time() for i in block_info['end_time']]
    
    return class_info, period_info, block_info

def get_period(period_info, block_info):
    now = datetime.datetime.now()
    time = now.time()
    weekday = now.strftime('%A').lower()
    period_list = []
    if weekday in period_info.index:
        period_list = period_info.loc[weekday,'period_list']
    period = None
    if len(period_list) != 0:
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
