# AutoQuest - Diogo Palma (mail@diogopalma.com) @ July, 2011.
# Description: this script aims to complete any type of craft or stackable packed items quests.

from py_stealth.py_stealth import *
import random
import datetime
import winsound, sys

sys.setrecursionlimit(50000)

# Configuration
runebookID = 0x40019F8E
stockRuneEntry = 1
questRuneEntry = 2
recallDelay = 4000
questGiverID = 0x00001443
inCoords = [535, 992]
outCoords = [6984, 338]
questCoords = [7038, 380]
rewardBagID = 0x4001A0C5
stockBagID = 0x40019E1B
petID = 0x000318D0
useBank = True
usePet = False
useTrash = False  # If you set false junk items will be randomly placed on the ground.
rewardLog = True  # Create log entry for each reward you receive.
rewardBeep = True  # Play sound when receive reward?
SetPauseScriptOnDisconnectStatus(True)  # Pause script if disconnected?
SetARStatus(True)  # Auto reconnect?

# Definitions
acceptQuestButton = 4
continueRewardButton = 8
acceptRewardButton = 5
actionDelay = 575
gumpDelay = 1150
itemDelay = 1000
trashType = 0x0E77
rewardBagType = 0x0E75

# Quest title, Item type, Item amount, Tool type, Craft menu gump buttons
questTypes = [['Lethal Darts', 0x1BFB, 10, 0, []],
              ['A Simple Bow', 0x13B2, 10, 0x1022, [15, 2]],
              ['Ingenious Archery, Part I', 0x0F50, 10, 0x1022, [15, 9]],
              ['Ingenious Archery, Part II', 0x13FD, 8, 0x1022, [15, 16]],
              ['Ingenious Archery, Part III', 0x26C3, 10, 0x1022, [15, 30]]
              ]
rewardTypes = [0x1022, 0x1034]
resourceTypes = [[0x1BFB, 0, 1000, 10]]


# Auto Quest
def startQuest():
    closeGumps()
    if IsNPC(questGiverID) is False:
        AddToSystemJournal('Error: unable to find the quest giver, try to reach it.')
        Wait(actionDelay)
        NewMoveXY(questCoords[0], questCoords[1], True, 0, True)
        startQuest()
    else:
        UseObject(questGiverID)
        Wait(CheckLag(30000))
        Wait(gumpDelay)
        questGump = GetGumpsCount() - 1
        textGump = GetGumpTextLines(questGump)
        foundQuest = False
        for i in range(len(questTypes)):
            for j in range(len(textGump)):
                if questTypes[i][0] == textGump[j]:
                    foundQuest = True
                    questName = questTypes[i][0]
                    questItem = questTypes[i][1]
                    questItemAmount = questTypes[i][2]
                    questTool = questTypes[i][3]
                    questToolButtons = questTypes[i][4]
                    WaitGump(str(acceptQuestButton))
                    AddToSystemJournal('Quest accepted: {0}'.format(questName))
                    if len(questToolButtons) > 0:
                        craftItem(questItem, questItemAmount, questTool, questToolButtons)
                    else:
                        getItem(questItem, questItemAmount)
        if foundQuest is False:
            AddToSystemJournal('Error: unable to accept a new quest, refuse it.')
            startQuest()


def craftItem(item, amount, tool, buttons):
    firstCraft = True
    oldTool = 0
    AddToSystemJournal('Start craft: {0} quest items.'.format(amount))
    craftedItems = FindType(item, Backpack())
    while FindCount() < amount:
        hasResources = checkResources()
        if hasResources is False:
            restockResources(0)
            break
        else:
            category = buttons[0]
            option = buttons[1]
            newTool = FindType(tool, Backpack())
            if newTool != oldTool:
                UseObject(newTool)
                Wait(CheckLag(30000))
                Wait(gumpDelay)
            oldTool = newTool
            if firstCraft is True:
                firstCraft = False
                WaitGump(str(category))
                Wait(CheckLag(30000))
                Wait(actionDelay)
            WaitGump(str(option))
            updateItems = FindType(item, Backpack())
    if FindCount() >= amount:
        Wait(CheckLag(30000))
        Wait(gumpDelay)
        items = GetFindedList()
        questItem(items)


def checkResources():
    for i in range(len(resourceTypes)):
        resource = resourceTypes[i][0]
        amountPet = resourceTypes[i][1]
        amountChar = resourceTypes[i][2]
        amountCritical = resourceTypes[i][3]
        FindType(resource, Backpack())
        if FindQuantity() <= amountCritical or FindCount() == 0:
            if usePet is True:
                if ObjAtLayer(HorseLayer()) != 0:
                    UseObject(Self())
                    Wait(CheckLag(30000))
                    Wait(actionDelay)
                RequestContextMenu(petID)
                SetContextMenuHook(petID, 9)
                Wait(CheckLag(30000))
                Wait(gumpDelay)
                obj = FindType(resource, LastContainer())
            if GetQuantity(obj) >= amountChar:
                MoveItem(obj, amountChar, Backpack(), 0, 0, 0)
                Wait(CheckLag(30000))
                Wait(actionDelay)
                return True
            elif GetQuantity(obj) == 1:
                MoveItem(obj, 1, Backpack(), 0, 0, 0)
                Wait(CheckLag(30000))
                Wait(actionDelay)
                return True
            else:
                return False
    return False


def restockResources(amount):
    restock = True
    closeGumps()
    AddToSystemJournal('Restock needed, going to stock coordinates.')
    if ObjAtLayer(HorseLayer()) == 0 and usePet is True:
        UseObject(petID)
        Wait(CheckLag(30000))
        Wait(actionDelay)
    NewMoveXY(outCoords[0], outCoords[1], True, 0, True)
    UseObject(runebookID)
    Wait(CheckLag(30000))
    Wait(gumpDelay)
    WaitGump(str(5 + ((stockRuneEntry - 1) * 6)))
    Wait(CheckLag(30000))
    Wait(gumpDelay)
    if usePet is True:
        UseObject(Self())
        Wait(CheckLag(30000))
    Wait(actionDelay)
    if useBank is True:
        UOSay('I would like to open my bank box.')
        Wait(CheckLag(30000))
        Wait(gumpDelay)
    stock = stockBagID
    if UseObject(stockBagID) is False and useBank is True:
        stock = ObjAtLayer(BankLayer())
    Wait(CheckLag(30000))
    Wait(actionDelay)
    if usePet is True:
        RequestContextMenu(petID)
        SetContextMenuHook(petID, 9)
        Wait(CheckLag(30000))
        Wait(gumpDelay)
    for i in range(len(resourceTypes)):
        resource = resourceTypes[i][0]
        amountPet = resourceTypes[i][1]
        amountChar = resourceTypes[i][2]
        if usePet is True:
            obj = FindType(resource, LastContainer())
            if GetQuantity(obj) > 1:
                MoveItem(obj, GetQuantity(obj), stock, 0, 0, 0)
                Wait(CheckLag(30000))
                Wait(actionDelay)
            else:
                items = GetFindedList()
                for item in items:
                    MoveItem(item, 1, stock, 0, 0, 0)
                    Wait(CheckLag(30000))
                    Wait(actionDelay)
        obj = FindType(resource, Backpack())
        if GetQuantity(obj) > 1:
            MoveItem(obj, GetQuantity(obj), stock, 0, 0, 0)
            Wait(CheckLag(30000))
            Wait(actionDelay)
        else:
            items = GetFindedList()
            for item in items:
                MoveItem(item, 1, stock, 0, 0, 0)
                Wait(CheckLag(30000))
                Wait(actionDelay)
        stack = FindType(resource, stock)
        if usePet is True:
            if FindQuantity() >= amountPet:
                MoveItem(stack, amountPet, LastContainer(), 0, 0, 0)
                Wait(CheckLag(30000))
                Wait(actionDelay)
            elif FindQuantity() < amountPet and FindQuantity() > amount:
                if (GetQuantity(stack) > 1):
                    MoveItem(stack, GetQuantity(stack), LastContainer(), 0, 0, 0)
                    Wait(CheckLag(30000))
                    Wait(actionDelay)
                else:
                    items = GetFindedList()
                    for item in items[:amountPet]:
                        MoveItem(item, 1, LastContainer(), 0, 0, 0)
                        Wait(CheckLag(30000))
                        Wait(actionDelay)
            else:
                restock = False
        if restock is True:
            if FindQuantity() >= amountChar:
                MoveItem(stack, amountChar, Backpack(), 0, 0, 0)
                Wait(CheckLag(30000))
                Wait(actionDelay)
            elif amountChar > FindQuantity() > amount:
                if GetQuantity(stack) > 1:
                    MoveItem(stack, GetQuantity(stack), Backpack(), 0, 0, 0)
                    Wait(CheckLag(30000))
                    Wait(actionDelay)
                else:
                    items = GetFindedList()
                    for item in items[:amountChar]:
                        MoveItem(item, 1, Backpack(), 0, 0, 0)
                        Wait(CheckLag(30000))
                        Wait(actionDelay)
            elif usePet is False:
                restock = False
    if restock is True:
        if usePet is True:
            UseObject(petID)
            Wait(CheckLag(30000))
            Wait(actionDelay)
        Wait(recallDelay)
        UseObject(runebookID)
        Wait(CheckLag(30000))
        Wait(gumpDelay)
        WaitGump(str(5 + ((questRuneEntry - 1) * 7)))
        Wait(CheckLag(30000))
        Wait(gumpDelay)
        Wait(actionDelay)
        NewMoveXY(inCoords[0], inCoords[1], True, 0, True)
        AddToSystemJournal('Resources successfully restocked, start quest again.')
        startQuest()
    else:
        AddToSystemJournal('Error: unable to collect needed resources, buy from vendors.')
        # TODO: create vendor buy method


def getItem(item, amount):
    obj = FindType(item, Backpack())
    if usePet is True:
        RequestContextMenu(petID)
        SetContextMenuHook(petID, 9)
        Wait(CheckLag(30000))
        Wait(gumpDelay)
        obj = FindType(item, LastContainer())
    if FindQuantity() < amount:
        AddToSystemJournal('Restock needed, doesnt have {0} quest items.'.format(amount))
        restockResources(amount)
    else:
        MoveItem(obj, amount, Backpack(), 0, 0, 0)
        AddToSystemJournal('Get from pack: {0} quest items.'.format(amount, item))
        Wait(CheckLag(30000))
        Wait(actionDelay)
        stack = FindType(item, Backpack())
        questItem([stack])


def trashItem(items):
    for i in range(len(items)):
        if useTrash is True:
            MoveItem(items[i], 1, FindType(trashType, Ground()), 0, 0, 0)
        else:
            MoveItem(items[i], 1, Ground(), GetX(Self()) + random.randrange(-2, 2),
                     GetY(Self()) + random.randrange(-2, 2), GetZ(Self()))
        Wait(CheckLag(30000))
        Wait(actionDelay)


def questItem(items):
    RequestContextMenu(Self())
    SetContextMenuHook(Self(), 6)
    Wait(CheckLag(30000))
    Wait(actionDelay)
    for i in range(len(items)):
        if isQuestItem(items[i]) is False:
            TargetToObject(items[i])
            Wait(CheckLag(30000))
            Wait(actionDelay)
    getReward()


def closeGumps():
    gumps = GetGumpsCount()
    for i in range(gumps):
        if IsGumpCanBeClosed(i) is True:
            Wait(CheckLag(30000))
            Wait(actionDelay)
            CloseSimpleGump(i)
        else:
            WaitGump('0')


def isQuestItem(item):
    toolTip = GetTooltip(item)
    if 'Quest Item' in toolTip:
        return True
    return False


def getReward():
    closeGumps()
    UseObject(questGiverID)
    Wait(CheckLag(30000))
    Wait(gumpDelay)
    WaitGump(str(continueRewardButton))
    Wait(CheckLag(30000))
    Wait(actionDelay)
    WaitGump(str(acceptRewardButton))
    Wait(CheckLag(30000))
    Wait(itemDelay)
    checkRewards()
    Wait(CheckLag(30000))
    Wait(actionDelay)
    startQuest()


def checkRewards():
    FindType(rewardBagType, Backpack())
    rewards = GetFindedList()
    for i in range(len(rewards)):
        if IsContainer(rewards[i]) is True and rewards[i] != rewardBagID:
            UseObject(rewards[i])
            Wait(CheckLag(30000))
            Wait(gumpDelay)
            for j in range(len(rewardTypes)):
                FindType(rewardTypes[j], rewards[i])
                reward = GetFindedList()
                for k in range(len(reward)):
                    toolTip = GetTooltip(reward[k])
                    if rewardBeep is True:
                        winsound.Beep(500, 2000)
                    AddToSystemJournal('Received an important reward, insure it and move to bag.')
                    if rewardLog is True:
                        rewardsLog = open('Scripts/AutoQuest/Logs/{0}.txt'.format(datetime.date.today()), 'a')
                        rewardsLog.writelines(
                            '{0} | {1} | {2}\n'.format(CharName(), toolTip, str(datetime.datetime.now())))
                        rewardsLog.close()
                    MoveItem(reward[k], 1, rewardBagID, 0, 0, 0)
                    Wait(CheckLag(30000))
                    Wait(actionDelay)
                    RequestContextMenu(Self())
                    SetContextMenuHook(Self(), 3)
                    Wait(CheckLag(30000))
                    Wait(actionDelay)
                    TargetToObject(reward[k])
                    Wait(CheckLag(30000))
                    Wait(actionDelay)
        trashItem([rewards[i]])
        Wait(CheckLag(30000))
        Wait(actionDelay)


restockResources(0)
