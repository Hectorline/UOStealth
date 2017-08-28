from stealth import *
from py_stealth import *
import runebook as rb
import datetime
GumpIgnore = 0
IngotsStorage =
HomeRuneBook =
HomeRuneIndex =
HomeX =
HomeY =
Arm =

Axe =
Logtype
WaitTime
RecallTime
LagWait
WaitCycles

Method = 'r'
CurrentRune = 0

def MoveItems(items):
    while FindType(LogType,Backpack) > 0:
        if Dead or not Connected:
            break
        while ObjAtLayer(LhandLayer) == 0:
            Equip(LhandLayer,Axe)
            Wait(1000)
        UseObject(Axe)
        WaitForTarget(LagWait)
        TargetToObject(FindItem)
        CheckLag(LagWait)
    for item in items:
        if Dead or not Connected:
            break
        CheckLag(LagWait)
        while Findtype(item, Backpack)>1:
            if Dead or not Connected:
                break
            MoveItem(Finditem,GetQuantity(Finditem), IngotsStorage,0,0,0)
            CheckLag(LagWait)
            Wait(WaitTime)

def Recall(runebookID, stockRuneEntry):
    UseObject(runebookID)
    Wait(CheckLag(30000))
    Wait(gumpDelay)
    WaitGump(str(5 + ((stockRuneEntry - 1) * 6)))
    Wait(CheckLag(30000))
    Wait(gumpDelay)
    return true


def GoBase():
    return Recall(HomeRuneBook, HomeRuneIndex)

def NextRune():
    global CurrentRune
    CurrentRune += 1
    if CurrentRune > 15:
        CurrentRune = 0
        global CurrentBook
        CurrentBook += 1
        if CurrentBook > len(RuneBooks):
            CurrentBook = 0
    for i in range(WaitCycles):
        if Dead or not Connected:
            break
        Result = self.Recall(RuneBooks[CurrentBook], CurrentRune)
        if Result:
            break
        CurrentRune += 1
        Result = self.Recall(RuneBooks[CurrentBook], CurrentRune)
        if Result:
            break
        GoBase()
        Wait(10000)


def Checkstate(x,y):
    if Dead or not Connected:
        break
    if MaxWeight < Weight + 70:
        while True:
            if Dead or not Connected:
                break
            if GoBase:
                break
            Move(Resources)
            while True:
                if Dead or not Connected:
                    break
                if RecallRune(RuneBooks[CurrentBook], CurrentRune)
                    break
    NewMoveXY(x,y,True,1,True)


def Chop(tile,x,y,z):

    while True:
        while ObjAtLayer(LhandLayer) == 0:
            Equip(LhandLayer, Axe)
            Wait(1000)
        if Dead or not Connected:
            break
        if TargetPresent:
            CancelTarget
        CheckState(x,y)
        CheckLag(LagWait)
        Wait(WaitTime)
        UseObject(Axe)
        CheckLag(LagWait)
        WaitForTarget(LagWait)
        if TargetPresent:
            StartTime = datetime.datetime.now()
            TargetToTile(Tile, x, y, z)
            CheckLag(LagWait)
            if InJournalBetweenTimes('t use an axe |is too far away|cannot be seen|s not enough wood here to harvest', StartTime, datetime.datetime.now())
                Wait(200)
                CheckState(x, y)

def CheckTiles(*args):
    Y0 = (GetY(Self)-1)
    X0 = (GetX(Self))
    treeTiles = [3240,3242,3277,3283,3286,3288,3289,3290,3291,3294,3296,3299,3302,3393,3394,3395,3396,3415,3416,3417,3418,3419,3438,3439,3440,3441,3442,3460,3461,3462,3480,3482,3488]

    for y in range(10,-11,-1):
        Y0 = (GetY(Self)+y)
        for x in range(10,-11, -1):
            X0 = (GetX(Self)+x)
            StaticData=ReadStaticsXY(X0,Y0,WorldNum)
            if GetLayerCount(X0,Y0,WorldNum)<1:
                continue
            TSTData=GetStaticTileData(StaticData.Statics[0].Tile)
            h = len(TSTData)
            for tree in treeTiles:
                if StaticData.Statics[0].Tile == tree:
                    SetLength
    pass

def ChopPoint():
    if Dead or not Connected:
        return
    Tiles=CheckTiles
    for i to len(Tiles):
       NewMoveXY(Tiles[i][1],Tiles[i][2],True, 1, True)
       Chop(Tiles[i][0],Tiles[i][1],Tiles[i][2],Tiles[i][3])
    CurrentRune+=1


if __name__ == '__main__':
    if not Connected():
        Connect()
        Wait(10000)
    cTime=datetime.datetime.now()
    RuneBooks=[]
    Resources=[]
    while True:
        if not Connected():
            Connect()
            Wait(10000)
        NextRune()
        ChopPoint()
