__author__ = 'Will'
from stealth import *
import utils
import gumplib


RELEASE_GUMP = -1868773567

# ['0|6107|Command: Guard|0|0',
#  '1|6108|Command: Follow|0|0',
#  '2|6111|Command: Kill|0|0',
#  '3|6112|Command: Stop|0|0',
#  '4|6114|Command: Stay|0|0',
#  '5|6110|Add Friend|0|0',
#  '6|6099|Remove Friend|0|0',
#  '7|6113|Transfer|0|0',
#  '8|6118|Release|0|0']

def detect_pets():
    old_distance = GetFindDistance()
    SetFindDistance(2)
    huge_list = [i for i in range(0xFFFF)]
    found = utils.find_mobs(huge_list)
    SetFindDistance(old_distance)
    pets = []
    print found
    for mob in found:
        desc = GetTooltip(mob)
        RequestContextMenu(mob)
        Wait(1000)
        menu = GetContextMenu()
        if "(tame)" in desc and len(menu) > 3 and "Command" in menu[0]:
            pets.append(mob)
        ClearContextMenu()
    print "found pets: {0}".format([GetName(pet) for pet in pets])
    return pets


def check_pets(pets):
    lower = 20
    healing_pet = None
    for pet in pets:
        if utils.distance_to_mob(pet) > 5:
            order_to_guard()
        if GetHP(pet) < lower:
            healing_pet = pet
            lower = GetHP(pet)
    if healing_pet:
        utils.try_to_heal(pet)



def order_to_kill(mob,target):
    SetContextMenuHook(mob, 2)
    RequestContextMenu(mob)
    ClearContextMenu()


def release(mob):
    SetContextMenuHook(mob, 8)
    RequestContextMenu(mob)
    ClearContextMenu()
    gumplib.waitForGumpID(RELEASE_GUMP)
    gumplib.clickButton(2, gumpID=RELEASE_GUMP)
    print "released?"


def order_to_guard(mob=None, target=None):
    if mob:
        SetContextMenuHook(mob, 0)
        RequestContextMenu(mob)
    else:
        UOSay("all guard")
    WaitForTarget(1000)
    if not target:
        target = Self()
    TargetToObject(target)
    print "guarded {0}".format(GetName(target))



# def release(mob):
#
#     RequestContextMenu(mob)
#     ClearContextMenu()
#     gumplib.waitForGumpID(RELEASE_GUMP)
#     gumplib.clickButton(2, gumpID=RELEASE_GUMP)
#     print "released?"