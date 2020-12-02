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
stimNames = open(_thisDir + os.sep + 'stim.csv', 'rU')
stimReader = csv.reader(stimNames, delimiter=',', dialect=csv.excel_tab)
imgNames = []
for row in stimReader:
    imgNames.append(row[0])

# opens file for data writing
expName = "MDT_ENCODING"
expInfo['date'] = data.getDateStr()
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])
filename = filename + '_V{0}.csv'.format(expInfo['version'])
dataFile = open(filename, 'w')
dataWriter = csv.writer(dataFile, delimiter=',')
dataWriter.writerow(['img', 'earlyResp', 'earlyRespLatency', 'resp', 'latency'])

# INTRO
win = visual.Window([800,600], monitor="testMonitor", units="pix", color= (1,1,1))
intro = visual.TextStim(win, text=
"""Welcome to the first section. Please press any key when you are ready to begin.
""",
color=(-1,-1,-1))
intro.draw()
win.flip()
event.waitKeys()

# INTRO INSTRUCTIONS
instr1 = visual.TextStim(win, text=
"""In this session, you will be viewing a series of images and answering some questions about them.
Please use the keyboard to answer. Press Y for yes and N for no.

Press SPACE to continue.
""", color=(-1,-1,-1), alignText='center')
instr1.draw()
win.flip()
event.waitKeys(keyList=['space'])

#######################
## BLOCK 0: PRACTICE ##
#######################

practiceStart = visual.TextStim(win, text="PRACTICE ROUND", color=(-1,-1,-1), alignText='center')
practiceStart.draw()
win.flip()
core.wait(5)

practInstr1_1 = visual.TextStim(win, text="In this round, you will be answering the question:", 
    color=(-1,-1,-1), alignText='center', pos=(0,100))
practInstr1_2 = visual.TextStim(win, text="Would this item fit inside a lady's shoebox?", 
    font='Arial', color=(-1,-1,-1), alignText='center', bold=True, pos=(0,50), height=20, units='pix')
practInstr1_3 = visual.TextStim(win, text=
"""It does not matter what kind of shoebox you imagine as long as you stay consistent.

Press SPACE to continue.
""", color=(-1,-1,-1), alignText='center', pos=(0,-50))
practInstr1_1.draw()
practInstr1_2.draw()
practInstr1_3.draw()
win.flip()
event.waitKeys(keyList=['space'])

practInstr2 = visual.TextStim(win, text=
"""The image will be shown first, then an answer screen.
When prompted, please press Y for yes and N for no.
Only answer when you see the ANSWER screen, not the image itself.

Press SPACE to continue.
""", color=(-1,-1,-1), alignText='center')
practInstr2.draw()
win.flip()
event.waitKeys(keyList=['space'])

PRACTICE_IMGS = ['001a.jpg', '013a.jpg', '005a.jpg', '002a.jpg']
practiceTrials = data.TrialHandler([{'i': i} for i in range(4)], 1, method='random')
img = visual.ImageStim(win=win, image=None, units = "pix")
waitGo = visual.TextStim(win=win, text=None, alignText='center')
for trial in practiceTrials:
    imgFile = "imgs{0}/".format(expInfo['version']) + PRACTICE_IMGS[trial['i']]
    img.setImage(imgFile)
    img.draw()
    waitGo.color = "#FF0000"
    waitGo.setText("WAIT")
    waitGo.setPos((0, 250))
    waitGo.draw()
    win.flip()
    core.wait(2)
    waitGo.color = "#000000"
    waitGo.setText(
    """
    ANSWER: 

    Y - yes
    N - no

    """)
    waitGo.setPos((0, 0))
    waitGo.draw()
    win.flip()
    resp = event.waitKeys(keyList=['y', 'n', 'q'])
    if resp[0] == 'q':
        core.quit()
        break

######################
## BLOCK 1: SHOEBOX ##
######################

random.shuffle(imgNames)

# variable number
NUM_IMAGES = 5
beforeBreak = imgNames[:NUM_IMAGES]
afterBreak = imgNames[NUM_IMAGES:2*NUM_IMAGES]

trials = data.TrialHandler([{'i': i} for i in range(NUM_IMAGES)], 1, method='sequential')

img = visual.ImageStim(win=win, image=None, units = "pix")

part1Start = visual.TextStim(win, text="PART 1", color=(-1,-1,-1), alignText='center')
part1Start.draw()
win.flip()
core.wait(5)

# FIRST 30 IMAGES
shoeBoxInstr1 = visual.TextStim(win, text="In this round, you will be answering the question:", 
    color=(-1,-1,-1), alignText='center', pos=(0,100))
shoeBoxInstr2 = visual.TextStim(win, text="Would this item fit inside a lady's shoebox?", 
    font='Arial', color=(-1,-1,-1), alignText='center', bold=True, pos=(0,50), height=20, units='pix')
shoeBoxInstr3 = visual.TextStim(win, text=
"""It does not matter what kind of shoebox you imagine as long as you stay consistent.

Press SPACE to continue.
""", color=(-1,-1,-1), alignText='center', pos=(0,-50))
shoeBoxInstr1.draw()
shoeBoxInstr2.draw()
shoeBoxInstr3.draw()
win.flip()
event.waitKeys(keyList=['space'])

for i in range(NUM_IMAGES):
    # show the image
    imgFile = "imgs{0}/".format(expInfo['version']) + beforeBreak[i]
    img.setImage(imgFile)
    img.draw()
    win.flip()
    # measure if an early response occurs
    timer = core.Clock()
    earlyResp = None
    earlyRespTime = None
    while timer.getTime() <= 2:
        testResp = event.getKeys(keyList=['y','n'])
        if testResp:
           earlyRespTime = timer.getTime()
           earlyResp = testResp[0]
    # answer screen
    timer = core.Clock()
    waitGo.setText(
    """
    ANSWER: 

    Y - yes
    N - no

    """)
    waitGo.setPos((0, 0))
    waitGo.draw()
    win.flip()
    resp = event.waitKeys(keyList=['y', 'n', 'q'])
    if resp[0] == 'q':
        core.quit()
        break
    dataWriter.writerow([imgFile[6:], earlyResp, earlyRespTime, resp[0], timer.getTime()])

# BREAK
breakInstr = visual.TextStim(win, text="Now we will take a short break for 5 seconds.", color=(-1,-1,-1), alignText='center');
breakInstr.draw()
win.flip()
core.wait(6)

# LAST 30 IMAGES
remindAfterBreak1 = visual.TextStim(win, text="Remember, you are answering the question:", 
    color=(-1,-1,-1), alignText='center', pos=(0,70))
remindAfterBreak2 = visual.TextStim(win, text="Would this item fit inside a lady's shoebox?", 
    font='Arial', color=(-1,-1,-1), alignText='center', bold=True, pos=(0,30), height=20, units='pix')
remindAfterBreak3 = visual.TextStim(win, text="Press SPACE to resume the trial.", color=(-1,-1,-1), alignText='center', pos=(0,-30))
remindAfterBreak1.draw()
remindAfterBreak2.draw()
remindAfterBreak3.draw()
win.flip()
event.waitKeys(keyList=['space'])

for i in range(NUM_IMAGES):
    # show the image
    print(i)
    imgFile = "imgs{0}/".format(expInfo['version']) + afterBreak[i]
    img.setImage(imgFile)
    img.draw()
    win.flip()
    # measure if an early response occurs
    timer = core.Clock()
    earlyResp = None
    earlyRespTime = None
    while timer.getTime() <= 2:
        testResp = event.getKeys(keyList=['y','n'])
        if testResp:
           earlyRespTime = timer.getTime()
           earlyResp = testResp[0]
    # answer screen
    timer = core.Clock()
    waitGo.setText(
    """
    ANSWER: 

    Y - yes
    N - no

    """)
    waitGo.setPos((0, 0))
    waitGo.draw()
    win.flip()
    resp = event.waitKeys(keyList=['y', 'n', 'q'])
    if resp[0] == 'q':
        core.quit()
        break
    dataWriter.writerow([imgFile[6:], earlyResp, earlyRespTime, resp[0], timer.getTime()])

# BREAK
breakBtwnSections = visual.TextStim(win, text="Now we will take a longer break for 10 seconds.", color=(-1,-1,-1), alignText='center');
breakBtwnSections.draw()
win.flip()
core.wait(11)

####################
## BLOCK 2: CARRY ##
####################

dataWriter.writerow(['-', '-', 'CARRY', '-', '-'])

random.shuffle(imgNames)

beforeBreak = imgNames[:NUM_IMAGES]
afterBreak = imgNames[NUM_IMAGES:2*NUM_IMAGES]

trials = data.TrialHandler([{'i': i} for i in range(NUM_IMAGES)], 1, method='sequential')

img = visual.ImageStim(win=win, image=None, units="pix")

part2Start = visual.TextStim(win, text="PART 2", color=(-1,-1,-1), alignText='center')
part2Start.draw()
win.flip()
core.wait(5)

# FIRST 30 IMAGES
carryInstr1 = visual.TextStim(win, text="In this round, you will be answering a new question:", 
    color=(-1,-1,-1), alignText='center', pos=(0,100))
carryInstr2 = visual.TextStim(win, text="Can you pick up the object with one hand and carry it across the room?", 
    font='Arial', color=(-1,-1,-1), alignText='center', bold=True, pos=(0,50), height=20, units='pix')
carryInstr3 = visual.TextStim(win, text=
"""Remember to press Y for yes and N for no.

Press SPACE to when you are ready to begin.
""", color=(-1,-1,-1), alignText='center', pos=(0,-50))
carryInstr1.draw()
carryInstr2.draw()
carryInstr3.draw()
win.flip()
event.waitKeys(keyList=['space'])

for i in range(NUM_IMAGES):
    # show the image
    imgFile = "imgs{0}/".format(expInfo['version']) + beforeBreak[i]
    img.setImage(imgFile)
    img.draw()
    win.flip()
    # measure if an early response occurs
    timer = core.Clock()
    earlyResp = None
    earlyRespTime = None
    while timer.getTime() <= 2:
        testResp = event.getKeys(keyList=['y','n'])
        if testResp:
           earlyRespTime = timer.getTime()
           earlyResp = testResp[0]
    # answer screen
    timer = core.Clock()
    waitGo.setText(
    """
    ANSWER: 

    Y - yes
    N - no

    """)
    waitGo.setPos((0, 0))
    waitGo.draw()
    win.flip()
    resp = event.waitKeys(keyList=['y', 'n', 'q'])
    if resp[0] == 'q':
        core.quit()
        break
    dataWriter.writerow([imgFile[6:], earlyResp, earlyRespTime, resp[0], timer.getTime()])

# BREAK
breakInstr = visual.TextStim(win, text="Now we will take a short break for 5 seconds.", color=(-1,-1,-1), alignText='center');
breakInstr.draw()
win.flip()
core.wait(6)

# LAST 30 IMAGES
remindAfterBreak1 = visual.TextStim(win, text="Remember, you are answering the question:", 
    color=(-1,-1,-1), alignText='center', pos=(0,100))
remindAfterBreak2 = visual.TextStim(win, text="Can you pick up the object with one hand and carry it across the room?", 
    font='Arial', color=(-1,-1,-1), alignText='center', bold=True, pos=(0,50), height=20, units='pix')
remindAfterBreak3 = visual.TextStim(win, text=
"""Remember to press Y for yes and N for no.

Press SPACE to when you are ready to begin.
""", color=(-1,-1,-1), alignText='center', pos=(0,-30))
remindAfterBreak1.draw()
remindAfterBreak2.draw()
remindAfterBreak3.draw()
win.flip()
event.waitKeys(keyList=['space'])

trials = data.TrialHandler([{'i': i} for i in range(NUM_IMAGES)], 1, method='sequential')

for i in range(NUM_IMAGES):
    # show the image
    imgFile = "imgs{0}/".format(expInfo['version']) + afterBreak[i]
    img.setImage(imgFile)
    img.draw()
    win.flip()
    # measure if an early response occurs
    timer = core.Clock()
    earlyResp = None
    earlyRespTime = None
    while timer.getTime() <= 2:
        testResp = event.getKeys(keyList=['y','n'])
        if testResp:
           earlyRespTime = timer.getTime()
           earlyResp = testResp[0]
    # answer screen
    timer = core.Clock()
    waitGo.setText(
    """
    ANSWER: 

    Y - yes
    N - no

    """)
    waitGo.setPos((0, 0))
    waitGo.draw()
    win.flip()
    resp = event.waitKeys(keyList=['y', 'n', 'q'])
    if resp[0] == 'q':
        core.quit()
        break
    dataWriter.writerow([imgFile[6:], earlyResp, earlyRespTime, resp[0], timer.getTime()])

endScreen = visual.TextStim(win, text=
    """This phase of the study is now over!

    Press SPACE when you are ready to quit.""",
                            color=(-1,-1,-1), alignText='center')
endScreen.draw()
win.flip()
event.waitKeys()

dataFile.close()

core.quit()
