#!/usr/bin/env python
# -*- coding: utf-8 -*-

from psychopy import core, visual, event, gui, data
import csv
import random
import os

_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# INTRO DIALOG BOX
expInfo = {'participant': '', 'session': '001', 'version': 1}
infoDlg = gui.DlgFromDict(dictionary=expInfo,
        title='Experiment')
if not infoDlg.OK:
    core.quit()

win = visual.Window([800,600], monitor="testMonitor", units="pix", color=(1,1,1))

# gets stimuli names from csv file
stimNames = open(_thisDir + os.sep + 'test1stim.csv', 'rU')
stimReader = csv.reader(stimNames, delimiter=',', dialect=csv.excel_tab)
imgs = []
for row in stimReader:
    imgs.append(row[4])
imgs = imgs[1:]
imgs = [x for x in imgs if x]

expName = "MDT_TEST_BLOCK1"
expInfo['date'] = data.getDateStr()
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])
filename = filename + '_V{0}_BLOCK4.csv'.format(expInfo['version'])
dataFile = open(filename, 'w')
dataWriter = csv.writer(dataFile, delimiter=',')
dataWriter.writerow(['img', 'earlyResp', 'earlyLatency', 'resp', 'latency', 'lateResp', 'lateLatency'])

##################
## INSTRUCTIONS ##
##################

instr1 = visual.TextStim(win, text=
"""Remember, your task is to determine if the object is OLD or NEW.
OLD means it was presented in the first session. 
NEW means it was NOT presented in the first session.

Press SPACE to continue.
""", color=(-1,-1,-1), alignText='center')
instr1.draw()
win.flip()
event.waitKeys(keyList=['space'])

instr2 = visual.TextStim(win, text=
"""Some of the objects may be similar to the OLD objects, but are not exactly the same.
If the picture is exactly the same, then it is OLD.
If there is any change in orientation, color, or quantity, the picture is NEW.

Press SPACE when you are ready to begin.
""", color=(-1,-1,-1), alignText='center')
instr2.draw()
win.flip()
event.waitKeys(keyList=['space'])

practiceStart = visual.TextStim(win, text="BLOCK 4", color=(-1,-1,-1), alignText='center')
practiceStart.draw()
win.flip()
core.wait(5)

practiceInstr = visual.TextStim(win, text=
"""In this round, you will be answering if the object presented is OLD or NEW.
Please only answer when you see the ANSWER screen.

Press SPACE to continue.
""", color=(-1,-1,-1), alignText='center')
practiceInstr.draw()
win.flip()
event.waitKeys(keyList=['space'])

practiceInstr = visual.TextStim(win, text=
"""To answer, use the keys 1, 2, 3, and 4.
1 - definitely NEW
2 - maybe NEW
3 - maybe OLD
4 - definitely OLD

Press SPACE to begin the trial.
""", color=(-1,-1,-1), alignText='center')
practiceInstr.draw()
win.flip()
event.waitKeys(keyList=['space'])

keyboardImg = visual.ImageStim(win=win, image="MDT test Keyboard.png", units='pix')
keyboardImg.draw()
win.flip()
core.wait(4)

img = visual.ImageStim(win=win, image=None, units = "pix")
answerKeysImg = visual.ImageStim(win=win, image="MDT Keyboard Instr.png", units="pix")

random.shuffle(imgs)
for i in range(len(imgs)):
    imgFile = "imgs{0}/".format(expInfo['version']) + imgs[i]
    img.setImage(imgFile)
    img.draw()
    win.flip()
    timer = core.Clock()
    earlyResp = None
    earlyLatency = None
    while timer.getTime() <= 3:
        checkResp = event.getKeys(keyList=['1','2','3','4'])
        if checkResp:
            earlyResp = checkResp[0]
            earlyLatency = timer.getTime()
    answerKeysImg.draw()
    win.flip()
    timer = core.Clock()
    resp = None
    latency = None
    while timer.getTime() <= 3:
        checkResp = event.getKeys(keyList=['1','2','3','4','q'])
        if checkResp:
            if 'q' in checkResp:
                dataFile.close()
                core.quit()
            resp = checkResp[0]
            latency = timer.getTime()
    win.flip()
    lateResp = None
    lateLatency = None
    timer = core.Clock()
    while timer.getTime() <= 1:
        checkResp = event.getKeys(keyList=['1','2','3','4'])
        if checkResp:
            lateResp = checkResp[0]
            lateLatency = timer.getTime()
    dataWriter.writerow([imgFile[6:], earlyResp, earlyLatency, resp, latency, lateResp, lateLatency])

endScreen = visual.TextStim(win, text=
    """This test block is over! Make sure to complete all 4 blocks.

    Press any key when you are ready to quit.
    """,
                            color=(-1,-1,-1), alignText='center')
endScreen.draw()
win.flip()
event.waitKeys()

dataFile.close()

core.quit()


