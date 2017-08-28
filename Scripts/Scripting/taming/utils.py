__author__ = 'Will'
from stealth import *
import math
from datetime import datetime, timedelta
#print dir(stealth)

latest_cast = datetime.now()
close_wounds_delay = 3

def getXYZ(mob=None):
    if not mob:
        mob = Self()
    X = GetX(mob)
    Y = GetY(mob)
    Z = GetZ(mob)
    return (X,Y,Z)

def try_to_heal(mob):
    global latest_cast
    if (datetime.now() - latest_cast) > timedelta(seconds=close_wounds_delay):
        Cast("close wounds")
        WaitForTarget(3000)
        TargetToObject(mob)


def find_items_on(types,place):
    found = []
    for type in types:
        if FindTypeEx(type,0xFFFF,place,True):
            found.extend(GetFindedList())
    #for item in found:
        #print GetName(item)
    return found


def target_instrument(instruments):
    WaitForTarget(500)
    itens = find_items_on(instruments,Backpack())
    if len(itens):
        TargetToObject(itens[0])


def find_mobs(types):
    found = []
    for type in types:
        if FindType(type,Ground()):
            found.extend(GetFindedList())
    #for item in found:
        #print GetName(item)
    return found


def distance_to_point(pos):
    #print "distance from {0} to {1}".format(tuple,getXYZ())
    x, y, z = getXYZ()
    dx = x - pos[0]
    dy = y - pos[1]
    distance = math.sqrt(dx**2 + dy**2)
    return distance

def distance_between(pos1,pos2):
    dx = pos1[0] - pos2[0]
    dy = pos1[1] - pos2[1]
    distance = math.sqrt(dx**2 + dy**2)
    return distance

def distance_to_mob(mob):
    pos = (GetX(mob),GetY(mob))
    #print "distance from {0} to {1}".format(tuple,getXYZ())
    x, y, z = getXYZ()
    dx = x - pos[0]
    dy = y - pos[1]
    distance = math.sqrt(dx**2 + dy**2)
    return distance