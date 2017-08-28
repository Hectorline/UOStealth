# -*- coding: utf-8 -*-

from datetime import datetime as dt
from stealth import *
from common import *
#OTHER COLORS
ore = 0x19B9

#               iron,   copper, bd,     pagan,  silver
trash_colors = [0x0000, 0x08EB, 0x0425, 0x050C, 0x04EB]

bad_points = []
pickaxe = 0x0E85
failMsg = 'You loosen some rocks but fail to find any useable ore|Oh no your tool breaks|You dig some ore and put it in your backpack'
emptyMsg = 'It seems, that you|You can\'t mine|There is no metal|You stop'
badMsg = 'see that|mine here.|Ёто слишком далеко.|too far'
tmpMsg = 'Ёто слишком далеко.'
	
def FindTiles(center_x, center_y, radius):
    min_x, min_y = center_x-radius, center_y-radius
    max_x, max_y = center_x+radius, center_y+radius
    tiles_coords = []
    for tile in range(1339,1359)+range(2269,2289)+range(1969,1999):
        tiles_coords += GetStaticTilesArray(min_x,min_y,max_x,max_y,WorldNum(),tile)
    return tiles_coords


def MineOre(t,x,y):
    CancelWaitTarget()
    CancelTarget()
    now = dt.now()
    counter = 0
    global loop
    if not ObjAtLayer(RhandLayer()):
        if FindType(pickaxe, Backpack()):
            Equip(RhandLayer(), FindItem())
            Wait(1000)
        else:
            AddToSystemJournal('no pickaxe found!')
            Wait(1000)
            return
    if CheckLag():
        UseObject(ObjAtLayer(RhandLayer()))
    while not InJournalBetweenTimes('¬ыберите', now, dt.now()) >=0 and counter <= 60:
        Wait(1000)
        counter += 1
    counter = 0
    if CheckLag():    
        WaitTargetTile(t,x,y,0)
    now = dt.now()
    while not InJournalBetweenTimes(badMsg+'|'+emptyMsg, now, dt.now()) >=0 and counter <= 180:
        #now = dt.now()
        counter += 1
        Wait(1000)
        CheckLag()
        if InJournalBetweenTimes(badMsg+'|'+emptyMsg, now, dt.now()) >=0:
        #    loop = 0
        #    MineOre(t,x,y)
            break
        #for color in trash_colors:
          #if FindTypeEx(ore, color, Backpack(), False):
              #while FindCount() > 0:
                  #DropHere(FindItem())        
                  #Wait(1500)
                  #FindTypeEx(ore, color, Backpack(), False) 
              #break
                             
    if FindType(0x14ED, Backpack()):
        while FindCount() > 0:
            DropHere(FindItem())        
            Wait(1000)
            FindType(0x14ED, Backpack())
    if InJournalBetweenTimes(badMsg, now, dt.now()) >=0:
        if [x,y] not in bad_points:
            bad_points.append([x,y])
    return

def StartMining():
    while not newMoveXY(5792, 1028, True, 0, True):
        Wait(1000)
    while Weight() < 60000:
        loop = 0
        for t,x,y,z in FindTiles(GetX(Self()),GetY(Self()), 7):
            if ([x,y] not in bad_points) and newMoveXY(x,y,True,2,False):
                AddToSystemJournal('mining at {0} {1} - weight: {2} - stamina: {3} - mining: {4}'.format(x, y, Weight(), GetStam(Self()), GetSkillValue('mining')))
                MineOre(t,x,y)


    return

StartMining()