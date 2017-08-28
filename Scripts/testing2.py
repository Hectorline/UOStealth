from py_stealth.py_stealth import *


def CheckTiles():
    # Y0 = (GetY(Self)-1)
    # X0 = (GetX(Self))
    Tiles = []
    treeTiles = [3240, 3242, 3277, 3283, 3286, 3288, 3289, 3290,3291, 3294, 3296, 3299, 3302, 3393, 3394, 3395, 3396,             3415, 3416, 3417, 3418, 3419, 3438, 3439, 3440, 3441, 3442, 3460, 3461, 3462, 3480, 3482, 3488]
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
    print('Hola')
    return Tiles

Tiles = CheckTiles()
