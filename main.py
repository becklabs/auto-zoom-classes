from resources_new import _parse, get_period, join_class
from tkinter import Tk,Button,Label,Entry,Frame
import tkinter.font as TkFont
from functools import partial

class_info, period_info, block_info = _parse()

def button_pressed(class_info,period_info,block_info):
    period = get_period(period_info, block_info)
    join_class(class_info, period, label)

root = Tk()


font = TkFont.Font(family="Helvetica",size=18,weight="bold")
font1 = TkFont.Font(family="Helvetica",size=12)

root.title("Class Joiner")

button = Button(root, 
                   text='Join Current Class', 
                   font = font,
                   width=15,
                   command=partial(button_pressed,class_info,period_info,block_info))
button.pack(padx=25, pady=10)

label = Label(root, fg="#2D8CFF",font = font1)
label.pack()

root.mainloop() 
