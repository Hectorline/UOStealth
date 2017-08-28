from common import *

while not Dead():
    CheckLag()
    #SetWarMode(False)
    #Wait(500)
    #SetWarMode(True)
    #Wait(500)
    CancelTarget()
    CancelWaitTarget()   
#    WaitTargetSelf()
#   UseSkill('evaluating intelligence')
#        SetFindDistance(100)
#        FindType(0x1F04, Ground())
#        itemList = GetFindedList()
#        for item in itemList:
#            x, y = GetX(item), GetY(item)
#            if (item not in usedList) and newMoveXY(x, y, True, 1, True):
#                Grab(item, 1)
#                AddToSystemJournal('found {0} - {1} : {2}'.format(item, len(itemList), len(usedList)))
#                usedList.append(item)

    WaitTargetSelf()
    Cast('Resurrection')
    Wait(10000)
    UseSkill('Meditation')
    Wait(20000)
    AddToSystemJournal('magery: {0} - meditation: {1}'.format(GetSkillValue('magery'), GetSkillValue('meditation')))       