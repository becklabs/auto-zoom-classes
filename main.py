from resources import _parse, get_period, join_class
import tkinter as tk
import tkinter.font as TkFont
from tkinter import ttk
from functools import partial

class_info, period_info, block_info = _parse()

def button_pressed(class_info,period_info,block_info):
    period = get_period(period_info, block_info)
    join_class(class_info, period, label)

root = tk.Tk()
font = TkFont.Font(family="Helvetica",size=28,weight="bold")
font1 = TkFont.Font(family="Helvetica",size=18)
root.title("Class Auto-Joiner")
button = tk.Button(root, 
                   text='Auto-Join Class', 
                   font = font,
                   width=15,
                   command=partial(button_pressed,class_info,period_info,block_info))
button.pack()

label = tk.Label(root, fg="#2D8CFF",font = font1)
label.pack()

root.mainloop()


    
