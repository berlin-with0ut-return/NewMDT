from psychopy import core, visual, event, gui, data
import csv
import random
import os
import pandas as pd
import numpy as np

expInfo = {'participant': '', 'session': '001', 'version': 1}
infoDlg = gui.DlgFromDict(dictionary=expInfo,
        title='Experiment')
if not infoDlg.OK:
    core.quit()
    core.quit()

expInfo['date'] = data.getDateStr()
    
expName = 'TEST'

_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])
filename = filename + '_V{0}_TEST.csv'.format(expInfo['version'])

data = {'col_1': [3, 2, 1, 0], 'col_2': ['a', 'b', 'c', 'd']}
data = pd.DataFrame.from_dict(data)

data.to_csv(filename[:-8] + 'RESULTS.csv')
