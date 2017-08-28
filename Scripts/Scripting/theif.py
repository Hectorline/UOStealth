from common import * 

startX, startY = 1323, 1624

def Steal():
    while not newMoveXY(startX, startY, True, 0, True):
        Wait(1000)

    
    while not Dead():
        CheckLag()
        UseSkill('hiding')
        Wait(10000)
        UseSkill('stealth')
        Wait(10000)
        x = startX
        y = startY
        
        #while not NewMoveXY(x + 35, y, True, 0, False):
        #    Wait(500)
        #while not NewMoveXY(x, y, True, 0, False):
        #    Wait(500)        
        #Wait(1000)
        #UseSkill('detecting hidden')
        #Wait(10000)
        AddToSystemJournal('hiding: {0} - stealth: {1} - detecting hidden: {2} '.format(GetSkillValue('hiding'), GetSkillValue('stealth'), GetSkillValue('detecting hidden')))
        
def Archery():
    while not Dead():
        CheckLag()
        SetWarMode(True)
        FindType(0x0F51, Backpack())
        if FindCount() > 0:        
            Equip(RhandLayer(), FindItem())  
        UseObject(0x7CC3CFEB)
        Wait(10000)
Archery()        