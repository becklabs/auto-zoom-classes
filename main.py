import pandas as pd
from dateparser import parse
from resources import _collect, _get
import os

if 'schedule_data' not in os.listdir():
    os.mkdir('schedule_data/')

for info in ['class_info','period_info','block_info']:
    if  info not in os.listdir('schedule_data/'):
        _collect(info)

class_info, period_info, block_info = _get()

        