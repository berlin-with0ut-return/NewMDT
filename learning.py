#!/usr/bin/env python
# -*- coding: utf-8 -*-

from psychopy import core, visual, event, gui, data
import csv
import random
import os

_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

info = {'participant': '', 'session': '001'}
infoDlg = gui.DlgFromDict(dictionary=info,
        title='Experiment')
if not infoDlg.OK:
    core.quit()

expName = "MDT_TESTING"
filename = _thisDir + os.sep + u'data/%s_%s' % (info['participant'], expName)
dataFile = open(filename+'.csv', 'w')  # a simple text file with 'comma-separated-values'
dataFile.write('resp')

win = visual.Window([800,600], monitor="testMonitor", units="pix")
intro = visual.TextStim(win, text="welcome to test")
intro.draw()
win.flip()
core.wait(3)

instr1 = visual.TextStim(win, text=
"""instr1...
press any key to continue
""")
instr1.draw()
win.flip()
event.waitKeys()

instr2 = visual.TextStim(win, text="""instr2...
press any key to continue
""")
instr2.draw()
win.flip()
event.waitKeys()

NUM_IMAGES = 5

trials = data.TrialHandler([{'i': i} for i in range(NUM_IMAGES)], 1, method='random')

imgNums = list(range(NUM_IMAGES))
random.shuffle(imgNums)

img = visual.ImageStim(win=win, image=None, units = "pix")

for trial in trials:
    imgFile = "imgs/" + str(imgNums[trial['i']]) + ".jpg"
    img.setImage(imgFile)
    img.draw()
    win.flip()
    resp = event.waitKeys()
    trials.addData('Resp', resp)
    dataFile.write('\n' + resp[0])

dataFile.close()

core.quit()
