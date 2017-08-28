# -*- coding: utf-8 -*-
from datetime import datetime as dt
from stealth import *
from common import *
#from mining import StartMining as mining

#RARE COLORS
daedra = 0x0494
sun = 0x0AB1
basilisk = 0x0487
mythril = 0x07EC

#OTHER COLORS
iron = 0x0000
copper = 0x08EB
bd = 0x0425
pagan = 0x050C
silver = 0x04EB

#MID COLORS
spectral = 0x0483
lavarock = 0x054E
icerock = 0x04E7

#METAL
ingots = 0x1BF2
ore = 0x19B9

#TOOLS
tools = 0x1EBC
pickaxe = 0x0E85
hammer = ''

#BAG
bag = ''

#TRASH ITEMS
#gears, scissors, butcher, lockpicks, pitchfork, keyring, buckler, metal shield, cutlass,short spear,katana,female breastplate, legs,breastplate,decorativeArmor
trash = [0x1053, 0x0F9E, 0x13F6, 0x14FB, 0x0E87, 0x1011, 0x1B73, 0x1B7B, 0x1440, 0x1402, 0x13FE,0x1C04,0x1411,0x1415,0x151A]
trash_container = 0x4A52985E
#OTHER
forge = 0x19A5
working = False
level, color = 0,0

def SmeltIngots():
    #go to forge point if cant find - 2580 446
    if FindTypeEx(ore, color, Backpack(), False):
        AddToSystemJournal('Finding forge')
        SetFindDistance(150)
        FindType(forge, Ground())
        foundForge = FindItem()
        if foundForge:
            if GetDistance(foundForge) > 1:
                counter = 0
                AddToSystemJournal('Forge found, moving to it')
                newMoveXY(GetX(foundForge), GetY(foundForge), True, 1, True)
                while GetDistance(foundForge) > 1 or counter < 100 and CheckLag():
                    Wait(1000)
                    FindType(forge, Ground())
                    foundForge = FindItem()
                    AddToSystemJournal('moving to x: {0}, y: {1} - distance: {2}'.format(GetX(foundForge), GetY(foundForge),GetDistance(foundForge)))
                    counter += 1
                    if GetDistance(foundForge) <= 1:
                        break
        else:
            #newMoveXY(2580, 446, True, 1, True)
            Wait(10000)
        FindTypeEx(ore, color, Backpack(), False)
        while FindCount() > 0 and CheckLag():
            UseObject(FindItem())
            Wait(1000)
            FindTypeEx(ore, color, Backpack(), False)
            if FindCount() <= 0:
                break
        return                
        
    elif Weight() < 60000:
        #2573 459 - start mining point
        #mining()
        return
    else:
        return

def CheckMenu():
    global level, color
    CancelTarget()
    CancelWaitTarget()
    if MenuHookPresent():
        CancelMenu()
    if MenuPresent():
        CloseMenu()
    if level < 15.0:
        WaitMenu('What ', 'Parts')
        WaitMenu('What ', 'Gears')
    elif level < 30.0:
        WaitMenu('What ', 'Tools')
        WaitMenu('What ', 'Scissors')
    elif level < 50.0:
        WaitMenu('What ', 'Deadly')
        WaitMenu('What ', 'Butcher')
    elif level < 80.0:
        WaitMenu('What ', 'Tools')
        WaitMenu('What ', 'Lockpicks')
    elif level < 90.0:
        WaitMenu('What ', 'Deadly Tools')
        WaitMenu('What ', 'Pitchfork')
    elif level < 130.0:
        WaitMenu('What ', 'Miscellaneous')
        WaitMenu('What ', 'key ring')

    Wait(1000)
    return

def CheckColor():
    global color
    if level < 90:
        color = iron
        FindTypeEx(ingots, color, Backpack(), False)
        quantity = FindQuantity()
        if quantity <= 50:
            color = copper

    elif level < 95:
        color = iron
        FindTypeEx(ingots, color, Backpack(), False)
        quantity = FindQuantity()
        if quantity <= 50:
            mining()

    elif level < 100.5:
        color = copper

    elif level < 105.5:
        color = bd

    elif level < 110.5:
        color = pagan

    elif level < 115.5:
        color = silver

    elif level < 118.5:
        color = spectral

    elif level < 122.5:
        color = lavarock

    elif level < 125:
        color = icerock

    elif level < 127.5:
        color = icerock

    elif level < 130:
        color = basilisk
    
    return

def Tinkering():
    global working, color
    counter = 0
    CheckColor()   
    if CheckLag():
        FindTypeEx(ingots, color, Backpack(), False)
        item = FindItem()
        count = FindCount()
        quantity = FindQuantity()
        AddToSystemJournal('{0} ingots - weight: {3} - your skilllevel is {1} - {2}'.format(quantity, level, working, Weight()))

    if CheckLag() and count > 0 and quantity > 50:
        CheckMenu()
        now = dt.now()
        CancelTarget()
        CancelWaitTarget()
        WaitTargetObject(item)
        UseType(tools, iron)
        while InJournalBetweenTimes('You stop.', now, dt.now()) <= 0 and counter < 50:
            Wait(1000)
            CheckLag()
            counter += 1
            if InJournalBetweenTimes('You stop.', now, dt.now()) >= 0 or counter >= 50:
                working = False
                break
    else:
        if quantity < 50:
            DropHere(item)
        SmeltIngots()
    working = False
    return

def BS():
    while not Dead():
        CheckLag()
        DropToTrash(trash, trash_container)
        Wait(5000)
        Wait(1000)
        
def Start():
    global working, level
    while not Dead():
        level = GetSkillValue('tinkering')
        if level == 130:
            mining()
        if not working:
            CheckLag() 
            if not ObjAtLayer(RhandLayer()):
                if FindType(pickaxe, Backpack()):
                    Equip(RhandLayer(), FindItem())
                    Wait(1000)
            #ArmsLore()
            working = True
            CheckLag()
            Tinkering()
            Wait(1000)
            CheckLag()
            DropToTrash(trash, trash_container)
            working = False
        else:
            Wait(1000)

        working = False
    return

BS()
