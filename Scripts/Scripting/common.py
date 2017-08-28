# -*- coding: utf-8 -*-
from datetime import datetime as dt
from stealth import *

SetARStatus(True)
SetMoveOpenDoor(True)

def CheckHP():
    if GetHP(Self()) < GetMaxHP(Self()):
        UOSay('.guards')
        Wait(1000)
        return False
    return True

def Hungry():
	now = dt.now()
	UOSay('.hungry')
	if InJournalBetweenTimes('You are DYING of hunger...', now, dt.now()) >= 0:
		return True
	return False

def ArmsLore():
    CancelTarget()
    CancelWaitTarget()
    WaitTargetObject(ObjAtLayer(RhandLayer()))
    UseSkill('Arms lore')
    Wait(100)
    return

def CheckLag():
    now = dt.now()
    counter = 0
    ClickOnObject(Backpack())
    while InJournalBetweenTimes('a backpack', now, dt.now()) <= 0 and counter < 100:
        Wait(100)
        counter += 1
        if counter >= 100:
            return False
    return True
    
def Shout():
    #for s in emptyMsg.split('|')+[' stop fail why can {0}'.format(badMsg)]:
    #UOSay('{0}'.format(emptyMsg.replace('|', ' ')))
    #Wait(500)
    #UOSay('{0}'.format(failMsg.replace('|', ' ')))
    #Wait(500)
    #UOSay('stop fail no start nothing too far else')
    #UOSay('любые скрипты! 100% автоматизации!')
    Wait(500)
    return    

def DropToTrash(items, container):
    for item in items:
        if FindType(item, Backpack()):
            while FindCount() > 0:
                if CheckLag():
                    CancelTarget()
                    CancelWaitTarget()
                    MoveItem(FindItem(),0,container,0,0,0)
                    Wait(2000)
                    AddToSystemJournal('{0} dropped of {1}'.format(FindItem(), FindCount()))
                    FindType(item, Backpack())
                    if FindCount() <= 0:
                        break
                        return True
    return     
