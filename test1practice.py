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
    core.quit()

# gets stimuli names from csv file
stimNames = open(_thisDir + os.sep + 'test1stim.csv', 'rU')
stimReader = csv.reader(stimNames, delimiter=',', dialect=csv.excel_tab)
pracImgs = []
for row in stimReader:
    pracImgs.append(row[0])
pracImgs = pracImgs[1:]
pracImgs = [x for x in pracImgs if x]

# opens file for data writing
expName = "MDT_TEST_PRACTICE"
expInfo['date'] = data.getDateStr()
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])
filename = filename + '_V{0}_PRACTICE.csv'.format(expInfo['version'])
dataFile = open(filename, 'w')
dataWriter = csv.writer(dataFile, delimiter=',')
dataWriter.writerow(['trial', 'img', 'earlyResp', 'earlyLatency', 'resp', 'latency', 'lateResp', 'lateLatency'])

# INTRO
win = visual.Window([800,600], monitor="testMonitor", units="pix", color= (1,1,1))
intro = visual.TextStim(win, text=
"""Welcome to the second section. Please press any key when you are ready to begin.
""",
color=(-1,-1,-1))
intro.draw()
win.flip()
event.waitKeys()

# INTRO INSTRUCTIONS
instr1 = visual.TextStim(win, text=
"""In this session, your task is to determine if the object is OLD or NEW.
OLD means it was presented in the study session. 
NEW means it was NOT presented in the study session.

Press SPACE to continue.
""", color=(-1,-1,-1), alignText='center')
instr1.draw()
win.flip()
event.waitKeys(keyList=['space'])

instr2 = visual.TextStim(win, text=
"""Some of the objects may be similar to the OLD objects, but are not exactly the same.
If the picture is exactly the same, then it is OLD.
If there is a change in any feature of the object (color, orientation, quantity, etc) the picture is NEW.

Press SPACE when you are ready to begin.
""", color=(-1,-1,-1), alignText='center')
instr2.draw()
win.flip()
event.waitKeys(keyList=['space'])

#######################
## BLOCK 0: PRACTICE ##
#######################

practiceStart = visual.TextStim(win, text="PRACTICE ROUND", color=(-1,-1,-1), alignText='center')
practiceStart.draw()
win.flip()
core.wait(5)

practiceInstr = visual.TextStim(win, text=
"""In this practice round, you will be answering if the object presented is OLD or NEW.
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
correctness = visual.TextStim(win=win, text=None, alignText='center', color=(-1,-1,-1))
passed = False

while not passed:
    random.shuffle(pracImgs)
    score = 0 # 75% to pass practice
    for i in range(len(pracImgs)):
        imgFile = "imgs{0}/".format(expInfo['version']) + pracImgs[i]
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
        possResponses = [earlyResp, resp, lateResp]
        if ('foil' in imgFile or 'b' in imgFile) and ('1' in possResponses or '2' in possResponses):
            correctness.text = "Correct! This image was NEW."
            score += 1
        elif 'foil' in imgFile or 'b' in imgFile:
            correctness.text = "Incorrect! This image was NEW."
        elif ('3' in possResponses or '4' in possResponses):
            correctness.text = "Correct! This image was OLD."
            score += 1
        else:
            correctness.text = "Incorrect! This image was OLD."
        correctness.draw()
        win.flip()
        core.wait(2)
        dataWriter.writerow([i, imgFile[6:], earlyResp, earlyLatency, resp, latency, lateResp, lateLatency])
    dataWriter.writerow(['-'] * 8)
    if score >= 5:
        passed = True
    else:
        failureText = visual.TextStim(win=win, text=
            """Sorry, you had too many incorrect answers!

            Press SPACE to try the practice round again.
            """, color=(-1,-1,-1), alignText='center')
        failureText.draw()
        win.flip()
        event.waitKeys(keyList=['space'])

endScreen = visual.TextStim(win, text=
    """The practice round is over!

    Press any key when you are ready to quit.""",
                            color=(-1,-1,-1), alignText='center')
endScreen.draw()
win.flip()
event.waitKeys()

dataFile.close()

core.quit()






