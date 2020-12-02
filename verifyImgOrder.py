import csv
import random
import os

_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

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

avg_ratio = 0
for i in range(100):
    blockOrder = counterbalance()
    allImgs = []
    for block in blockOrder:
        allImgs += getImages(block)
    imageNames = set([img[:3] for img in allImgs if 'foil' not in img])
    imgIndices = {x[1]: x[0] for x in enumerate(allImgs)}
    a_before_b = 0
    b_before_a = 0
    for name in imageNames:
        target = name + 'a.jpg'
        lure = name + 'b.jpg'
        if imgIndices[target] > imgIndices[lure]:
            a_before_b += 1
        else:
            b_before_a += 1
    print(allImgs)
    avg_ratio += (a_before_b)/(a_before_b + b_before_a)

print(avg_ratio/100)