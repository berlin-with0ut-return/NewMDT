#!/usr/bin/env python
# -*- coding: utf-8 -*-

from psychopy import core, visual, event, gui, data
import csv
import random
import os
import pandas as pd
import numpy as np

_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# INTRO DIALOG BOX
expInfo = {'participant': '', 'session': '001', 'version': 1}
infoDlg = gui.DlgFromDict(dictionary=expInfo,
        title='Experiment')
if not infoDlg.OK:
    core.quit()
    core.quit()

# opens file for data writing
expName = "MDT_TEST"
expInfo['date'] = data.getDateStr()
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])
filename = filename + '_V{0}_TEST.csv'.format(expInfo['version'])
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
"""In this session, your task is to answer if the object is OLD or NEW.
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

##################
## BLOCKS BEGIN ##
##################

start = visual.TextStim(win, text="INSTRUCTIONS", color=(-1,-1,-1), alignText='center')
start.draw()
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

# TODO: FUNCTION(Int block) -> list(images)
# function run_trial(images)

def getImages(block):
    stimNames = open(_thisDir + os.sep + 'test1stim.csv', 'rU')
    stimReader = csv.reader(stimNames, delimiter=',', dialect=csv.excel_tab)
    imgs = []
    for row in stimReader:
        imgs.append(row[block])
    imgs = imgs[1:]
    imgs = [x for x in imgs if x]
    random.shuffle(imgs)
    return imgs[:3]

def counterbalance():
    order = [1, 2, 3, 4]
    random.shuffle(order)
    return order

blockOrder = counterbalance()

def runTrial(blockImgs):
    for i in range(len(blockImgs)):
        imgFile = "imgs{0}/".format(expInfo['version']) + blockImgs[i]
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
        dataWriter.writerow([i, imgFile[6:], earlyResp, earlyLatency, resp, latency, lateResp, lateLatency])
    breakInstr = visual.TextStim(win, text="Now we will take a short break for 5 seconds.", color=(-1,-1,-1), alignText='center')
    breakInstr.draw()
    win.flip()
    core.wait(6)

for blk in range(len(blockOrder)):
    blockImgs = getImages(blockOrder[blk])
    random.shuffle(blockImgs)
    roundBegins = visual.TextStim(win, text="Round {0}".format(blk + 1), color=(-1,-1,-1))
    roundBegins.draw()
    win.flip()
    core.wait(2)
    runTrial(blockImgs)

endScreen = visual.TextStim(win, text=
    """You have completed the study!

    Press any key when you are ready to quit.""",
                            color=(-1,-1,-1), alignText='center')
endScreen.draw()
win.flip()
event.waitKeys()

dataFile.close()

## ANALYSIS

data = pd.read_csv(filename)

def get_responses(data):
    return data[['img', 'earlyResp', 'resp', 'lateResp']]

def fill_row(row):
    if np.isnan(row['resp']):
        if not np.isnan(row['lateResp']):
            return row['lateResp']
        elif not np.isnan(row['earlyResp']):
            return row['earlyResp']
        else:
            return -1
    return row['resp']

def clear_blanks(tbl):
    tbl['resp'] = tbl.apply(fill_row, axis=1)
    return tbl[tbl['resp'] != -1][['img', 'resp']]

valid_resp = clear_blanks(get_responses(data))

def score_hits_misses(row):
    if 'a' in row['img']:
        if row['resp'] == 4 or row['resp'] == 3:
            return 1
        elif row['resp'] == 1 or row['resp'] == 2:
            return 0
    elif 'b' in row['img'] or 'foil' in row['img']:
        if row['resp'] == 4 or row['resp'] == 3:
            return 0
        elif row['resp'] == 1 or row['resp'] == 2:
            return 1

valid_resp['correctness'] = valid_resp.apply(score_hits_misses, axis=1)

lures = valid_resp[valid_resp['img'].str.contains('b')]
novels = valid_resp[valid_resp['img'].str.contains('foil')]

def score_FA_CR(tbl):
    return 1 - tbl['correctness']

lures['FA'] = score_FA_CR(lures)
novels['FA'] = score_FA_CR(novels)

def gather_results(lures, novels):
    """Returns a dictionary of String: Double describing accuracy"""
    lures_FA = np.mean(lures['FA'])
    lures_CR = 1 - lures_FA
    novels_FA = np.mean(novels['FA'])
    novels_CR = 1 - novels_FA
    return {'Lure FA': lures_FA,
           'Lure CR': lures_CR, 
           'Novel FA': novels_FA, 
           'Novel CR': novels_CR}

res = gather_results(lures, novels)

def LDI(lureCR, novelFA):
    return lureCR - novelFA

outputName = filename[:-8] + "RESULTS.csv"
ouputFile = open(outputName, 'w')
writer = csv.writer(ouputFile, delimiter=',')
for k, v in res.items():
    writer.writerow([k, v])
ouputFile.close()


