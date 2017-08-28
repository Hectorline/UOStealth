from stealth import *
import runebook as rb
import datetime


class Lumber():
    def __init__(self):
        self.Axe = 1105240798
        self.BoardStorage = 1078440743
        self.HomeRuneBook = 1147922026
        self.HomeRuneIndex = 0
        self.Method = 'r'
        self.RuneBooks = [1148064390, 1148110783]

        self.Resources = [7127, 12687, 12689, 12127, 12697, 12688]
        self.LagWait = 1000

        self.WaitCycles = 7
        self.WaitTime = 500

        self.LogType = 7133
        self.RecallTime = 3000

        self.CurrentRune = 0
        self.CurrentBook = 0
        pass

    def MoveItems(self, items):
        while FindType(self.LogType, Backpack) > 0:
            if Dead or not Connected:
                break
            while ObjAtLayer(LhandLayer) == 0:
                Equip(LhandLayer, self.Axe)
                Wait(1000)
            UseObject(self.Axe)
            WaitForTarget(self.LagWait)
            TargetToObject(FindItem)
            CheckLag(self.LagWait)
        for item in items:
            if Dead or not Connected:
                break
            CheckLag(self.LagWait)
            while FindType(item, Backpack) > 1:
                if Dead or not Connected:
                    break
                MoveItem(FindItem, GetQuantity(FindItem), self.BoardStorage, 0, 0, 0)
                CheckLag(self.LagWait)
                Wait(self.WaitTime)

    @staticmethod
    def RecallRune(runebook, rune, method):
        Runebook = rb.Runebook(runebook)
        return Runebook.travel(rune, method)

    def GoBase(self):
        return self.RecallRune(self.HomeRuneBook, self.HomeRuneIndex, self.Method)

    def NextRune(self):
        self.CurrentRune += 1
        if self.CurrentRune > 15:
            self.CurrentRune = 0
            self.CurrentBook += 1
            if self.CurrentBook > len(self.RuneBooks):
                self.CurrentBook = 0
        for i in range(self.WaitCycles):
            if Dead or not Connected:
                break
            Result = self.RecallRune(self.RuneBooks[self.CurrentBook], self.CurrentRune, self.Method)
            if Result:
                break
            self.CurrentRune += 1
            Result = self.RecallRune(self.RuneBooks[self.CurrentBook], self.CurrentRune, self.Method)
            if Result:
                break
            self.GoBase()
            Wait(10000)

    def CheckState(self, x, y):
        if Dead or not Connected:
            return
        if 477 < Weight() + 70:
            while True:
                if Dead or not Connected:
                    break
                if self.GoBase:
                    break
                self.MoveItems(self.Resources)
                while True:
                    if Dead or not Connected:
                        break
                    if self.RecallRune(self.RuneBooks[self.CurrentBook], self.CurrentRune, self.Method):
                        break
        NewMoveXY(x, y, True, 1, True)

    def Chop(self, tile, x, y, z):

        while True:
            while ObjAtLayer(LhandLayer) == 0:
                Equip(LhandLayer, self.Axe)
                Wait(1000)
            if Dead or not Connected:
                break
            if TargetPresent:
                CancelTarget()
            self.CheckState(x, y)
            CheckLag(self.LagWait)
            Wait(self.WaitTime)
            UseObject(self.Axe)
            CheckLag(self.LagWait)
            WaitForTarget(self.LagWait)
            if TargetPresent:
                StartTime = datetime.datetime.now()
                TargetToTile(tile, x, y, z)
                CheckLag(self.LagWait)
                if InJournalBetweenTimes(
                        't use an self.Axe |is too far away|cannot be seen|s not enough wood here to harvest',
                        StartTime, datetime.datetime.now()):
                    Wait(200)
                    self.CheckState(x, y)

    @staticmethod
    def CheckTiles():
        # Y0 = (GetY(Self)-1)
        # X0 = (GetX(Self))
        Tiles = []
        treeTiles = [3240, 3242, 3277, 3283, 3286, 3288, 3289, 3290, 3291, 3294, 3296, 3299, 3302, 3393, 3394, 3395,
                     3396, 3415, 3416, 3417, 3418, 3419, 3438, 3439, 3440, 3441, 3442, 3460, 3461, 3462, 3480, 3482,
                     3488]
        for y in range(10, -11, -1):
            Y0 = GetY(Self()) + y
            for x in range(10, -11, -1):
                X0 = GetX(Self()) + x
                StaticData = ReadStaticsXY(X0, Y0, WorldNum())
                if GetLayerCount(X0, Y0, WorldNum()) < 1:
                    continue
                if StaticData:
                    for obj in StaticData:
                        if obj.Tile in treeTiles:
                            Tiles.append(obj)
        return Tiles

    def ChopPoint(self):
        if Dead or not Connected:
            return
        Tiles = self.CheckTiles()
        for i in Tiles:
            NewMoveXY(Tiles[i].X, Tiles[i].Y, True, 1, True)
            self.Chop(Tiles[i].Tile, Tiles[i].X, Tiles[i].Y, Tiles[i].Z)
        self.CurrentRune += 1


if __name__ == '__main__':
    Lumber = Lumber()
    if not Connected():
        Connect()
        Wait(10000)
    cTime = datetime.datetime.now()
    while True:     
        print('In loop')
        if not Connected():
            Connect()
            Wait(10000)
        Lumber.NextRune()
        Lumber.ChopPoint()
