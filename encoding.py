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

# define keys for input
YES_KEY = 'f'
NO_KEY = 'j'

# opens file for data writing
expName = "MDT_ENCODING"
expInfo['date'] = data.getDateStr()
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])
filename = filename + '_V{0}.csv'.format(expInfo['version'])
dataFile = open(filename, 'w')
dataWriter = csv.writer(dataFile, delimiter=',', lineterminator = '\n')
dataWriter.writerow(['img', 'earlyResp', 'earlyRespLatency', 'resp', 'latency'])

# INTRO
win = visual.Window([800,600], fullscr=True, monitor="testMonitor", color= (1,1,1))
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
core.wait(3)

practInstr = visual.TextStim(win, text=
"""In this round, you will be answering the question:

Would this item fit inside a lady's shoebox?

It does not matter what kind of shoebox you imagine as long as you stay consistent.

Press SPACE to continue.
""", 
    color=(-1,-1,-1), alignText='center')
practInstr.draw()
win.flip()
event.waitKeys(keyList=['space'])

practInstr2 = visual.TextStim(win, text=
"""The image will be shown first, then an answer screen.
When prompted, please press {0} for yes and {1} for no.
Only answer when you see the ANSWER screen, not the image itself.

Press SPACE to continue.
""".format(YES_KEY.upper(), NO_KEY.upper()), 
    color=(-1,-1,-1), alignText='center')
practInstr2.draw()
win.flip()
event.waitKeys(keyList=['space'])

PRACTICE_IMGS = ['001a.jpg', '013a.jpg', '005a.jpg', '002a.jpg']
practiceTrials = data.TrialHandler([{'i': i} for i in range(len(PRACTICE_IMGS))], 1, method='random')
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

    {0} - yes
    {1} - no

    """.format(YES_KEY.upper(), NO_KEY.upper()))
    waitGo.setPos((0, 0))
    waitGo.draw()
    win.flip()
    resp = event.waitKeys(keyList=[YES_KEY, NO_KEY, 'q'])
    if resp[0] == 'q':
        core.quit()
        break

######################
## BLOCK 1: SHOEBOX ##
######################

random.shuffle(imgNames)

# variable number
NUM_IMAGES = 30
beforeBreak = imgNames[:NUM_IMAGES]
afterBreak = imgNames[NUM_IMAGES:2*NUM_IMAGES]

trials = data.TrialHandler([{'i': i} for i in range(NUM_IMAGES)], 1, method='sequential')

img = visual.ImageStim(win=win, image=None, units = "pix")

part1Start = visual.TextStim(win, text="PART 1", color=(-1,-1,-1), alignText='center')
part1Start.draw()
win.flip()
core.wait(3)

# FIRST 30 IMAGES
shoeBoxInstr = visual.TextStim(win, color=(-1,-1,-1), alignText='center', text= 
"""In this round, you will be answering the question:

Would this item fit inside a lady's shoebox?

It does not matter what kind of shoebox you imagine as long as you stay consistent.

Press SPACE to continue.
""")
shoeBoxInstr.draw()
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
        testResp = event.getKeys(keyList=[YES_KEY, NO_KEY])
        if testResp:
           earlyRespTime = timer.getTime()
           earlyResp = testResp[0]
    # answer screen
    timer = core.Clock()
    waitGo.setText(
    """
    ANSWER: 

    {0} - yes
    {1} - no

    """.format(YES_KEY.upper(), NO_KEY.upper()))
    waitGo.setPos((0, 0))
    waitGo.draw()
    win.flip()
    resp = event.waitKeys(keyList=[YES_KEY, NO_KEY, 'q'])
    if resp[0] == 'q':
        core.quit()
        break
    dataWriter.writerow([imgFile[6:], earlyResp, earlyRespTime, resp[0], timer.getTime()])

# BREAK
breakInstr = visual.TextStim(win, text="Now we will take a short break for 5 seconds.", color=(-1,-1,-1), alignText='center');
breakInstr.draw()
win.flip()
core.wait(5)

# LAST 30 IMAGES
remindAfterBreak = visual.TextStim(win, text=
"""Remember, you are answering the question:
    
Would this item fit inside a lady's shoebox?
    
Press SPACE to resume the trial.
""", 
    color=(-1,-1,-1), alignText='center')
remindAfterBreak.draw()
win.flip()
event.waitKeys(keyList=['space'])

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
        testResp = event.getKeys(keyList=[YES_KEY, NO_KEY])
        if testResp:
           earlyRespTime = timer.getTime()
           earlyResp = testResp[0]
    # answer screen
    timer = core.Clock()
    waitGo.setText(
    """
    ANSWER: 

    {0} - yes
    {1} - no

    """.format(YES_KEY.upper(), NO_KEY.upper()))
    waitGo.setPos((0, 0))
    waitGo.draw()
    win.flip()
    resp = event.waitKeys(keyList=[YES_KEY, NO_KEY, 'q'])
    if resp[0] == 'q':
        core.quit()
        break
    dataWriter.writerow([imgFile[6:], earlyResp, earlyRespTime, resp[0], timer.getTime()])

# BREAK
breakBtwnSections = visual.TextStim(win, text="Now we will take a longer break for 10 seconds.", color=(-1,-1,-1), alignText='center');
breakBtwnSections.draw()
win.flip()
core.wait(10)

####################
## BLOCK 2: CARRY ##
####################

dataWriter.writerow(['-', '-', 'CARRY', '-', '-'])

random.shuffle(imgNames)

beforeBreak = imgNames[:NUM_IMAGES]
afterBreak = imgNames[NUM_IMAGES:2*NUM_IMAGES]

trials = data.TrialHandler([{'i': i} for i in range(NUM_IMAGES)], 1, method='sequential')

img = visual.ImageStim(win=win, image=None)

part2Start = visual.TextStim(win, text="PART 2", color=(-1,-1,-1), alignText='center')
part2Start.draw()
win.flip()
core.wait(3)

# FIRST 30 IMAGES
carryInstr = visual.TextStim(win, text=
"""In this round, you will be answering a new question:
    
Can you pick up the object with one hand and carry it across the room?
    
Remember to press {0} for yes and {1} for no.
    
Press SPACE when you are ready to begin.
""".format(YES_KEY.upper(), NO_KEY.upper()), 
    color=(-1,-1,-1), alignText='center')
carryInstr.draw()
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
        testResp = event.getKeys(keyList=[YES_KEY, NO_KEY])
        if testResp:
           earlyRespTime = timer.getTime()
           earlyResp = testResp[0]
    # answer screen
    timer = core.Clock()
    waitGo.setText(
    """
    ANSWER: 

    {0} - yes
    {1} - no

    """.format(YES_KEY.upper(), NO_KEY.upper()))
    waitGo.setPos((0, 0))
    waitGo.draw()
    win.flip()
    resp = event.waitKeys(keyList=[YES_KEY, NO_KEY, 'q'])
    if resp[0] == 'q':
        core.quit()
        break
    dataWriter.writerow([imgFile[6:], earlyResp, earlyRespTime, resp[0], timer.getTime()])

# BREAK
breakInstr = visual.TextStim(win, text="Now we will take a short break for 5 seconds.", color=(-1,-1,-1), alignText='center');
breakInstr.draw()
win.flip()
core.wait(5)

# LAST 30 IMAGES
remindAfterBreak = visual.TextStim(win, text=
"""Remember, you are answering the question:
    
Can you pick up the object with one hand and carry it across the room?
    
Remember to press {0} for yes and {1} for no.

Press SPACE to when you are ready to begin.
    """.format(YES_KEY.upper(), NO_KEY.upper()), 
    color=(-1,-1,-1), alignText='center')
remindAfterBreak.draw()
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
        testResp = event.getKeys(keyList=[YES_KEY, NO_KEY])
        if testResp:
           earlyRespTime = timer.getTime()
           earlyResp = testResp[0]
    # answer screen
    timer = core.Clock()
    waitGo.setText(
    """
    ANSWER: 

    {0} - yes
    {1} - no

    """.format(YES_KEY.upper(), NO_KEY.upper()))
    waitGo.setPos((0, 0))
    waitGo.draw()
    win.flip()
    resp = event.waitKeys(keyList=[YES_KEY, NO_KEY, 'q'])
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
