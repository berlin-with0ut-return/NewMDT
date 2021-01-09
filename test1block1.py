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

# define keys
DEF_OLD = 'd'
MAYBE_OLD = 'f'
MAYBE_NEW = 'j'
DEF_NEW = 'k'

# INTRO DIALOG BOX
expInfo = {'participant': '', 'session': '001', 'version': 1}
infoDlg = gui.DlgFromDict(dictionary=expInfo,
        title='Experiment')
if not infoDlg.OK:
    core.quit()

# opens file for data writing
expName = "MDT_TEST"
expInfo['date'] = data.getDateStr()
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])
filename = filename + '_V{0}_TEST.csv'.format(expInfo['version'])
dataFile = open(filename, 'w')
dataWriter = csv.writer(dataFile, delimiter=',', lineterminator='\n')
dataWriter.writerow(['trial', 'img', 'earlyResp', 'earlyLatency', 'resp', 'latency', 'lateResp', 'lateLatency'])

# INTRO
win = visual.Window([800,600], monitor="testMonitor", color= (1,1,1), fullscr=True)
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
"""Some objects may be similar to OLD objects, but are not exactly the same.

If the object is exactly the same as the one in the study session, it is OLD.

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
core.wait(2)

practiceInstr = visual.TextStim(win, text=
"""In this round, you will be answering if the object presented is OLD or NEW.
Please only answer when you see the ANSWER screen.

Press SPACE to continue.
""", color=(-1,-1,-1), alignText='center')
practiceInstr.draw()
win.flip()
event.waitKeys(keyList=['space'])

practiceInstr = visual.TextStim(win, text=
"""To answer, use the keys {0}, {1}, {2}, and {3}.
{0} - definitely NEW
{1} - maybe NEW
{2} - maybe OLD
{3} - definitely OLD

Press SPACE to begin the trial.
""".format(DEF_OLD, MAYBE_OLD, MAYBE_NEW, DEF_NEW), color=(-1,-1,-1), alignText='center')
practiceInstr.draw()
win.flip()
event.waitKeys(keyList=['space'])

keyboardImg = visual.ImageStim(win=win, image="MDT test Keyboard.png", units='pix')
keyboardImg.draw()
win.flip()
core.wait(3)

img = visual.ImageStim(win=win, image=None)
answerKeysImg = visual.ImageStim(win=win, image="MDT Keyboard Instr.png")

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
    return imgs

def counterbalance():
    order = [1, 2, 3, 4]
    random.shuffle(order)
    return order

blockOrder = counterbalance()

def runTrial(blockImgs, showBreak):
    for i in range(len(blockImgs)):
        imgFile = "imgs{0}/".format(expInfo['version']) + blockImgs[i]
        img.setImage(imgFile)
        img.draw()
        win.flip()
        timer = core.Clock()
        earlyResp = None
        earlyLatency = None
        while timer.getTime() <= 2:
            checkResp = event.getKeys(keyList=[DEF_OLD, MAYBE_OLD, MAYBE_NEW, DEF_NEW])
            if checkResp:
                earlyResp = checkResp[0]
                earlyLatency = timer.getTime()
        answerKeysImg.draw()
        win.flip()
        timer = core.Clock()
        resp = None
        latency = None
        while timer.getTime() <= 2:
            checkResp = event.getKeys(keyList=[DEF_OLD, MAYBE_OLD, MAYBE_NEW, DEF_NEW,'q'])
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
            checkResp = event.getKeys(keyList=[DEF_OLD, MAYBE_OLD, MAYBE_NEW, DEF_NEW])
            if checkResp:
                lateResp = checkResp[0]
                lateLatency = timer.getTime()
        possResponses = [earlyResp, resp, lateResp]
        dataWriter.writerow([i, imgFile[6:], earlyResp, earlyLatency, resp, latency, lateResp, lateLatency])
    if showBreak:
        breakInstr = visual.TextStim(win, text="Now we will take a short break for 5 seconds.", 
            color=(-1,-1,-1), alignText='center')
        breakInstr.draw()
        win.flip()
        core.wait(5)

for blk in range(len(blockOrder)):
    blockImgs = getImages(blockOrder[blk])
    random.shuffle(blockImgs)
    roundBegins = visual.TextStim(win, text="Round {0}".format(blk + 1), color=(-1,-1,-1))
    roundBegins.draw()
    win.flip()
    core.wait(2)
    runTrial(blockImgs, (blk == len(blockOrder) - 1))

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

def score_correctness(row):
    if 'a' in row['img']:
        if row['resp'] == DEF_OLD or row['resp'] == MAYBE_OLD:
            return 1
        elif row['resp'] == DEF_NEW or row['resp'] == MAYBE_NEW:
            return 0
    elif 'b' in row['img'] or 'foil' in row['img']:
        if row['resp'] == DEF_OLD or row['resp'] == MAYBE_OLD:
            return 0
        elif row['resp'] == DEF_NEW or row['resp'] == MAYBE_NEW:
            return 1

def score_confidence(row):
    if row['resp'] == DEF_NEW or row['resp'] == DEF_OLD:
        return 1
    else:
        return 0

valid_resp['correctness'] = valid_resp.apply(score_correctness, axis=1)

valid_resp['confidence'] = valid_resp.apply(score_confidence, axis=1)

lures = valid_resp[valid_resp['img'].str.contains('b')]
targets = valid_resp[valid_resp['img'].str.contains('a')]
novels = valid_resp[valid_resp['img'].str.contains('foil')]

output = {'total': np.zeros(6), 
         'percent': np.zeros(6),
         'high_conf': np.zeros(6),
         'low_conf': np.zeros(6),
          'high_conf_pct': np.zeros(6),
          'low_conf_pct': np.zeros(6)}
output_tbl = pd.DataFrame(output, index=["lure_hit", "lure_miss",
                                        "target_hit", "target_miss",
                                        "novel_hit", "novel_miss"])

def compute_rows(tbl):
    """Returns a 2-item list RES of hit/miss data for a lure, target, or novel table.
    
    RES[0] is the hits. RES[1] is the misses.
    """
    hit_res = [0] * 6
    miss_res = [0] * 6
    hits = tbl[tbl['correctness'] == 1]
    misses = tbl[tbl['correctness'] == 0]
    # counts
    num_hits = len(hits.index)
    num_misses = len(misses.index)
    print(num_hits, num_misses)
    # percentages
    pct_hits = num_hits/(num_hits + num_misses)
    pct_misses = num_misses/(num_hits + num_misses)
    # confidence counts
    num_hc_hit = sum(hits['confidence'])
    num_lc_hit = num_hits - num_hc_hit
    num_hc_miss = sum(misses['confidence'])
    num_lc_miss = num_misses - num_hc_miss
    # confidence percents
    pct_hc_hit = num_hc_hit/num_hits if num_hits else None
    pct_lc_hit = num_lc_hit/num_hits if num_hits else None
    pct_hc_miss = num_hc_miss/num_misses if num_misses else None
    pct_lc_miss = num_lc_miss/num_misses if num_misses else None
    return [[num_hits, pct_hits, num_hc_hit, num_lc_hit, pct_hc_hit, pct_lc_hit], 
           [num_misses, pct_misses, num_hc_miss, num_lc_miss, pct_hc_miss, pct_lc_miss]]

lure_res = compute_rows(lures)
target_res = compute_rows(targets)
novel_res = compute_rows(novels)

output_tbl.loc['lure_hit'] = lure_res[0]
output_tbl.loc['lure_miss'] = lure_res[1]
output_tbl.loc['target_hit'] = target_res[0]
output_tbl.loc['target_miss'] = target_res[1]
output_tbl.loc['novel_hit'] = novel_res[0]
output_tbl.loc['novel_miss'] = novel_res[1]

output_tbl.to_csv(filename[:-8] + 'RESULTS.csv')

core.quit()