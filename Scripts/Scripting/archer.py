from common import * 
startX, startY = 1503, 1622 #brit
bankX, bankY = 1442, 1690
ressX, ressY = 1475, 1645
animal = 0x00CF#sheep 0x00D9#dog 0x00CD#cat 

def StartArcher():
  
    while not Dead():
        while not NewMoveXY(startX, startY, True, 0, True):
            Wait(1000)
        CheckLag()
        CancelTarget()
        CancelWaitTarget()
        if MenuHookPresent():   
            CancelMenu()
        if MenuPresent():
            CloseMenu()     
        #WaitMenu( 'Select a category.' , 'Creatures' );
        #WaitMenu( 'Select a creature.' , 'Yulia-Timoshenko' );
        #UseSkill('tracking')
        SetFindDistance(5)
        FindType(animal, Ground())
        CheckLag()
        if FindCount() > 0:
            if GetDistance(FindItem()) > 5:
                x = GetX(FindItem())
                y = GetY(FindItem())
                while not NewMoveXY(x,y,True,5,True):
                    Wait(1000)
            else:
                WaitTargetObject(FindItem())
                UseSkill('animal lore')
                Wait(10000)
            AddToSystemJournal('tracking: {0}, animal lore: {1}'.format(GetSkillValue('tracking'),GetSkillValue('animal lore')))
        else:
            AddToSystemJournal('no animals found')
    if Dead():
        while not NewMoveXY(ressX, ressY, True, 0, True):
            if not Dead():
                return StartArcher()
            Wait(5000)


#StartArcher()        
def Archery():
    while not Dead():
        CheckLag()
        SetWarMode(True)  
        FindType(0x23C4, Backpack())
        if FindCount() > 0:        
            Equip(RhandLayer(), FindItem())    
        UseObject(0x7CC3CFEB)
        Wait(5000)   
Archery()