from datetime import datetime, timedelta
from datetime import timedelta
from taming import utils, gumplib
import threading
from taming.persistency import *

from stealth import *
import taming.petmanager as petMan

polar_bear = [0x00D5]
white_wolf = [0x0025, 0x0022]
walrus = [0x00DD]
snow_panther = [0x0041, 0x0040]

################################# SETUP #######################################
types = snow_panther + white_wolf
instruments = [0x0E9C, 0x0EB2]
REWRITE_RAIL = False



########################### ADVANCED SETUP ####################################

spots = []
pets = []
ignore_set = set([])
SetFindDistance(25)
SetFindVertical(15)


def walk_to_next_spot():
    global current_spot
    current_spot += 1
    current_spot %= len(spots)
    x, y, z = spots[current_spot]
    #print x, y, z
    print "moving to spot {0}".format(current_spot)
    NewMoveXY(x, y, False, 0, False)


def walk_to(tupla):
    x, y, z = tupla
    #print x, y, z
    print "moving to {0} {1}".format(x, y)
    NewMoveXY(x, y, False, 0, False)
    petMan.check_pets(pets)


def move_to_mob(mob, timeout=10):
    print "moving to {0}".format(GetName(mob))
    end = datetime.now() + timedelta(seconds=10)
    while (utils.distance_to_mob(mob) > 2) and datetime.now() < end:
        targetx, targety = GetX(mob), GetY(mob)
        NewMoveXY(targetx, targety, True, 1, False)
        petMan.check_pets(pets)
    if datetime.now() > end:
        print "walk timeout, ignoring {0}, assuming as unreachable".format(GetName(mob))
        add_ignore(mob, ignore_set)


def use_taming():
    pass


def next_spot():
    number = (current_spot + 1) % len(spots)
    return spots[number]


def try_to_tame(animal, attempt):
    if animal in ignore_set:
        print "{0} in ignore list, ignoring".format(GetName(animal))
        return False
    move_to_mob(animal)
    print "moving to {0}".format(GetName(animal))
    used = False
    while not used:
        UseSkill('Animal Taming')
        WaitJournalLineSystem(datetime.now(), "must wait|which", 5000)
        if FoundedParamID() == 1:
            used = True
    WaitForTarget(2000)
    TargetToObject(animal)
    now = datetime.now()
    end = now + timedelta(seconds=35)
    while InJournalBetweenTimes("You have no chance|fail|accept|far|already|challenging|path|seen.", now, end) <= 0:
        Wait(1000)
        move_to_mob(animal)

    result = FoundedParamID()
    if result in [2, 5]:
        print "success!"
        return True
    elif result in [0, 4] or (result == 3 and attempt > 5):
        add_ignore(animal, ignore_set)
    return False


def move_away_from(mob):
    print "should be trying to move away"
    selfpos = utils.getXYZ(Self())
    enemypos = utils.getXYZ(mob)
    dx = selfpos[0] - enemypos[0]
    dy = selfpos[1] - enemypos[1]
    for offset in [(-2, -2), (-2, 0), (-2, 2), (0, 2), (2, 2), (2, 0), (2, -2), (0, -2)]:
        NewMoveXY(enemypos[0] + offset[0], enemypos[1] + offset[1], False, 0, False)
        print "moved {0}".format(offset)
        if utils.distance_to_mob(mob) > 1:
            break


def use_peace(mob):
    Wait(500)
    print "calming {0}".format(GetName(mob))
    now = datetime.now()
    CancelTarget()
    UseSkill("Peacemaking")
    WaitJournalLineSystem(now, "instrument|do you|wait", 5000)
    WaitForTarget(1000)
    # if WaitJournalLine(datetime.now(),"instrument|calm|wait",1000)>0:
    found = FoundedParamID()
    #print found
    if found == 2:
        Wait(1000)
        return
    if found == 0:
        utils.target_instrument(instruments)
        WaitForTarget(1000)
    TargetToObject(mob)


def try_to_kill(mob):
    if mob not in ignore_set:
        print "Killing {0}".format(GetName(mob))
        move_away_from(mob)
        #for killer in killers_names:
        petMan.order_to_kill(pets[0], mob)
        WaitForTarget(1000)
        TargetPresent()
        TargetToObject(mob)
        timeout = datetime.now() + timedelta(seconds=45)
        while (GetHP(mob) > 0) and datetime.now() < timeout:
            use_peace(mob)
            Wait(1000)
            print "hp: {0} timeout: {1}".format(GetHP(mob), (timeout - datetime.now()).seconds)


def setup_spots():
    print "Setting up rail..."
    spots = load_spots_list()
    if REWRITE_RAIL or len(spots) == 0:
        print "rewriting rail, please walk through the desired path, then come back to the start, making a closed path."
        spots = []
        start = utils.getXYZ()
        last_point = start
        while len(spots) < 10 or utils.distance_to_point(start) > 15:
            if utils.distance_to_point(last_point) > 10:
                current = utils.getXYZ()
                spots.append(current)
                last_point = current
                print "spots: {0}, distance: {1}".format(len(spots), utils.distance_to_point(start))
                Wait(500)
        print "new rail is done"
        save_spots(spots)
    else:
        spots = load_spots_list()
        print "loaded {0} spots from file".format(len(spots))
    print "rail is ok!."
    return spots


def get_closest_spot():
    closest_distance = utils.distance_to_point(spots[0])
    closest_spot = 0
    for spot in spots:
        if utils.distance_to_point(spot) < closest_distance:
            closest_distance = utils.distance_to_point(spot)
            closest_spot = spots.index(spot)

    print "closest spot is {0}, far {1} units".format(closest_spot, closest_distance)
    return closest_spot


def setup_ignore_set():
    print "loading ignore set..."
    global ignore_set
    if len(ignore_set) == 0:
        ignore_set = load_ignore_list()
        print "loaded {0} ignores".format(len(ignore_set))
    return ignore_set


def find_tamables():
    mobs = set(utils.find_mobs(types)) - ignore_set
    far = set()
    for mob in mobs:
        if utils.distance_between(utils.getXYZ(mob), next_spot()) < utils.distance_between(utils.getXYZ(mob),
                                                                                           spots[current_spot]):
            far.add(mob)
            print "{0} is closer to next spot".format(GetName(mob))
    mobs = mobs - far
    return mobs


######################################################
#####           START         ########################
######################################################


class Tamer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = True
        print "thread created"

    def run(self):
        print "thread started   "
        global pets
        pets = petMan.detect_pets()
        add_ignore(pets, ignore_set)
        global spots
        spots = setup_spots()
        setup_ignore_set()
        global current_spot
        current_spot = get_closest_spot()
        while self.running:
            walk_to_next_spot()
            mobs = find_tamables()
            while len(mobs) > 0:
                mob = mobs.pop()
                if mob not in ignore_set:
                    for attempt in range(10):
                        print "trying to tame, attempt {0}".format(attempt)
                        if try_to_tame(mob, attempt):
                            petMan.release(mob)
                            break
                    try_to_kill(mob)
                    walk_to(spots[current_spot])
                mobs = find_tamables()


import atexit


def exit_handler():
    tamer.running = False


atexit.register(exit_handler)

print "starting..."
import sys

sys.argv = [""]
#import Tkinter

tamer = Tamer()
#tamer.start()
tamer.run()
#top = Tkinter.Tk()
#top.mainloop()
#print "mainloop finished?"
#tamer.running = False
#tamer.join()

