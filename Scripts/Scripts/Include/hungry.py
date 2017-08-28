from stealth import *
from datetime import datetime as dt

def Hungry(NeededLevel, Container):
    if not Connected(): return
    if (NeededLevel < 0) or (NeededLevel > 10): return
    HArray = [
        'You are absolutely stuffed!',
        'You are stuffed',
        'hungry at all',
        'You are a little hungry',
        'You are somewhat hungry',
        'You are REALLY hungry',
        'Your stomash hurts',
        'Your stomash hurts and you feel dizzy',
        'You are starving',
        'You are almost dying of hunger',
        'You are DYING of hunger...'
    ]
    HasError = True
    TimeSayHungry = dt.now()
    UOSay('.hungry')
    Wait(100)
    i=0
    while i < 100:
        for c in range(0,11):
            if InJournalBetweenTimes(HArray[c], TimeSayHungry, dt.now()) >= 0:
                CurrentLevel = c
                HasError = False
                i = 100
            Wait(100)
            i += 1
    if HasError:
        AddToSystemJournal('Error with Hungry: Lag? Conection error? Something else?')
        return
    difference = CurrentLevel - NeededLevel
    FindType(0x097B, Container)
    if (difference > 0) and (FindCount() > 0):
        for i in range(1, difference):
            FoodId = FindType(0x097B, Container)
            if FoodId != 0x00: UseObject(FoodId)
            Wait(200)
    if FindType(0x097B, Container) == 0: AddToSystemJournal('No Food')
        
        
def hungry(NeededLevel, Container):
    Hungry(NeededLevel, Container)