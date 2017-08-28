from common import *

def Musicanship():
    if not ObjAtLayer(RhandLayer()):
        if FindType(0x0EB2, Backpack()):
            UseType(0x0EB2,0x0000)
        else:            
            UseType(0x0EB3,0x0000)       
    else:
        UseObject(ObjAtLayer(RhandLayer()))
    AddToSystemJournal('musicianship: {0}'.format(GetSkillValue('musicianship')))   
    return
        
def Enticement():
    #WaitTargetObject(0x0037FB9E)
    UseSkill('peacemaking')
    return

while not Dead():
    CheckLag()
    CancelTarget()
    CancelWaitTarget()   
    Enticement()
    Wait(10000)