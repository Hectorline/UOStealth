from datetime import datetime as dt
from common import * 

used_sheeps = []

vendor = 0x0190
sheep = 0x00CF
sheep_menu = 0x20E6
iron = 0x0000
scissors = 0x0F9E
wool = 0x0DF8
yarn = 0x0E1D
bolts = 0x0F95
wheelX = 1472
wheelY = 1685
counter = 0
startDistance = 7
maxDistance = 15
distance = startDistance

bankX = 1442
bankY = 1690
startX = 1517 #GetX(Self())
startY = 1548 #GetY(Self())
ressX = 1475
ressY = 1645
loop = 0

AutoBuy(sheep_menu, iron, 3)    

def MakeCloth():
    while not NewMoveXY(1471, 1696, True, 0, True):
        Wait(1000)
    OpenDoor()
    while not NewMoveXY(wheelX, wheelY, True, 0, True):
        Wait(1000)
    FindType(wool, Backpack())
    while FindQuantity() > 5:
        UseObject(FindItem())
        Wait(3000)
        FindType(wool, Backpack())
    FindType(yarn, Backpack())
    while FindQuantity() > 5:
        UseObject(FindItem())
        Wait(3000)
        FindType(yarn, Backpack())

def GoToBank():
    while not NewMoveXY(bankX, bankY, True, 0, True):    
        CheckHP()
        Wait(100)
    UOSay('bank')
    CheckHP()
    CheckLag()
    Wait(1000)
    if ObjAtLayer(BankLayer()) > 0:         AddToSystemJournal('Bank Box ID: {0}'.format(ObjAtLayer(BankLayer())));
        if FindType(bolts, Backpack()) > 0:
            MoveItem(FindItem(), 0, ObjAtLayer(BankLayer()),0,0,0)
            Wait(1500)
        if FindType(scissors, Backpack()) <= 0:
            if FindType(scissors, ObjAtLayer(BankLayer())) >= 0:
                MoveItem(FindItem(), 0, Backpack(),0,0,0)
                Wait(1500)
        return True 
    return False
        
def Whool():
    global used_sheeps, distance, counter, loop
    
    SetFindDistance(distance)
    FindType(sheep, Ground())
    sheep_list = GetFindedList()
    if len(sheep_list) <= 0:
        if NewMoveXY(startX, startY, True, 0, True):
            used_sheeps = []
            SetFindDistance(8)
            FindType(vendor, Ground())            
            vendor_list = GetFindedList()
            for item in vendor_list:
                AddToSystemJournal('Vendor ID: {0} - {1}'.format(item, vendor_list));
                if item != Self():
                    x, y = GetX(item), GetY(item)
                    if NewMoveXY(x, y, True, 2, True):
                        Wait(1500)
                        UOSay('buy')
        
    if (len(used_sheeps) >= len(sheep_list)):
        AddToSystemJournal('starting new loop...')    
        used_sheeps = []
        distance = startDistance
        counter += 1
        if counter > 10:
            counter = 0  
            if NewMoveXY(startX, startY, True, 0, True):
                return True
            else:
                AddToSystemJournal('in stuck, exiting...')    
                return True

        
    for item in sheep_list:
        x, y = GetX(item), GetY(item)  
        if (item not in used_sheeps) and (IsNPC(item)) and NewMoveXY(x, y, True, 1, True):
            CancelTarget()
            CancelWaitTarget()
            CheckHP()
            now = dt.now()     
            UseType(scissors, iron)
            while not InJournalBetweenTimes('Select the object to cut.', now, dt.now()) >=0 and counter <= 10:
                Wait(1000)
                counter += 1
            counter = 0
            WaitTargetObject(item)   
            now = dt.now()     
            while not InJournalBetweenTimes('Failed.|Success|Canceled|You stop', now, dt.now()) >=0 and counter <= 10:
                CheckHP()
                counter += 1
                Wait(1000)
                if InJournalBetweenTimes('Failed.', now, dt.now()) >=0:
                    loop += 1
                    counter = 0
                    if loop > 0:
                        used_sheeps.append(item)
                        loop = 0
                    break
            #Shout()
            ArmsLore()
            AddToSystemJournal('{0}:{1} - {2}'.format(x,y,len(used_sheeps)))    
            AddToSystemJournal('id: {0} - {1}'.format(item, len(sheep_list)))   
            AddToSystemJournal('skilllevel: {0}'.format(GetSkillValue('tailoring')))   
    counter = 0
    return True        
    
while True:
    if Dead():
        while not NewMoveXY(ressX, ressY, True, 0, True):
            Wait(1000)  
        AddToSystemJournal('resurected')

    if FindType(scissors, Backpack()) <= 0:
        GoToBank()
                               
    Wait(1000) 
    if Weight() > 250:
        if FindType(wool, Backpack()) > 0:
            AddToSystemJournal('going to wheel...')   
            MakeCloth()
            while not NewMoveXY(1471,1694,True,0,False):
                Wait(1000)
            OpenDoor()
        AddToSystemJournal('going to bank...')   
        GoToBank()

    while not NewMoveXY(startX, startY, True, 1, True):  
        Wait(1000)
    while not Whool():
        CheckHP()
        Wait(1000)                                 
    Wait(1000)
   
            
            