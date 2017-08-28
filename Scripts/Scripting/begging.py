from common import * 
from datetime import datetime as dt

vendor_list, used_vendors, bad_vendors = [], [], []
distance, counter = 30, 0

bad_vendors += [0x000207FE, Self()]

#startX, startY = 1490, 1550 #brit
startX, startY = 5717, 1134 #market
bankX, bankY = 1442, 1690
ressX, ressY = 1475, 1645

gold, food = 0x0EED, 0x097E

def Begging():
    global used_vendors, vendor_list, distance, counter
    SetFindDistance(distance)
    FindType(0x0190, Ground())
    vendor_list = GetFindedList()
    FindType(0x0191, Ground())
    vendor_list += GetFindedList()
    for item in vendor_list:
        CheckLag()
        CheckHP()
        #if Hungry():
            #if not GoToBank():
                #SetARStatus(False)
                #Disconnect()  
                #break
        x, y = GetX(item), GetY(item)
        AddToSystemJournal('x: {0}, y: {1} - {2}'.format(x,y,len(used_vendors)))    
        AddToSystemJournal('id: {0} - {1}'.format(item, len(vendor_list)))  
        if item not in used_vendors and item not in bad_vendors and IsNPC(item) and newMoveXY(x, y, True, 5, True):
            now = dt.now()
            CancelTarget()
            CancelWaitTarget()
            WaitTargetObject(item)   
            UseSkill('begging') 
            CheckLag()
            Wait(1000)
            if not InJournalBetweenTimes('You can only beg from NPC\'s.|You must target a human!', now, dt.now()) >= 0:
                Wait(20000)
            else:    
                bad_vendors.append(item)
                Wait(500) 
            used_vendors.append(item) 
            AddToSystemJournal('skilllevel: {0} - gold: {1}'.format(GetSkillValue('begging'), Gold()))
        else:
            used_vendors.append(item)
        Wait(1000)
        #if Gold() >= 10000:
            #GoToBank() 
    if (len(used_vendors) >= len(vendor_list)):
        AddToSystemJournal('starting new loop...')    
        used_vendors = []
        while not NewMoveXY(startX, startY, True, 0, True):
            Wait(1000)   
             
def GoToBank():
    while not newMoveXY(bankX, bankY, True, 0, True):    
        CheckHP()
        Wait(500)
    UOSay('bank')
    CheckHP()
    CheckLag()
    if ObjAtLayer(BankLayer()) > 0: 
        AddToSystemJournal('Bank Box ID: {0}'.format(ObjAtLayer(BankLayer())));
        if FindType(gold, Backpack()) > 0:
            MoveItem(FindItem(), 0, ObjAtLayer(BankLayer()),0,0,0)
            Wait(1500)
        if FindType(food, Backpack()) <= 0:
            if FindType(food, ObjAtLayer(BankLayer())) >= 0:
                MoveItem(FindItem(), 5, Backpack(),0,0,0)
                Wait(1500)
            else:
                return False
    return True
    
def StartBegging():    
    while not NewMoveXY(startX, startY, True, 0, True):
        Wait(1000)
    while not Dead():                                
        CheckLag()
        Begging()
        Wait(1000)
    #if Dead():
        #while not NewMoveXY(ressX, ressY, True, 0, True):
            #Wait(1000)
    #if not Dead():
        #return StartBegging()
StartBegging()