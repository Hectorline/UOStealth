from py_stealth import *

try:
	from stealth import *
except:
	from py_stealth import *

Profiles = ['OoOoO']

Tailor = 416617  # Deandra the Tailor
Blacksmith = 376  # Rhiamon the Blacksmith


def ConnectChar(profile):
    print"Connecting with profile {}".format(profile)
    while not Connected():
        Connect()
        Wait(10000)
    print("{} connected".format(profile))


def DisconnectChar():
    print("Disconnecting...")
    while Connected():
        Disconnect()
        Wait(10000)
    print("Disconnected")


def RunTo(x, y):
    while x != GetX(Self()) or y != GetY(Self()):
        NewMoveXY(x, y, False, 0, True)
        Wait(1000)


def GoThroughDoor(x, y):
    while x != GetX(Self()) or y != GetY(Self()):
        OpenDoor()
        Wait(1000)
        NewMoveXY(x, y, False, 0, True)
        Wait(500)


def MoveAround():
    RunTo(991, 524)
    RunTo(991, 523)  # So we face the door
    GoThroughDoor(991, 521)
    RunTo(991, 519)
    RunTo(990, 519)
    GoThroughDoor(988, 519)
    RunTo(978, 525)  # Tailor reached
    GetBod(Tailor)
    GetBod(Tailor)
    RunTo(978, 514)  # Blacksmith reached
    GetBod(Blacksmith)
    GetBod(Blacksmith)
    RunTo(987, 518)
    RunTo(988, 518)
    GoThroughDoor(991, 518)
    RunTo(991, 520)
    RunTo(991, 521)
    GoThroughDoor(991, 524)
    RunTo(992, 527)


def GetBod(npc):
    RequestContextMenu(npc)
    SetContextMenuHook(npc, 1)
    Wait(1000)
    WaitGump('1')
    Wait(2000)


def SortBods():
    res = FindTypeEx(8793, 0, Backpack(), False)
    FoundBooks = GetFindedList()
    res = FindTypeEx(8792, 1155, Backpack(), False)  # Tailor
    FoundTailorBods = GetFindedList()
    res = FindTypeEx(8792, 1102, Backpack(), False)  # Blacksmith
    FoundBlacksmithBods = GetFindedList()
    for book in FoundBooks:
        tooltip = GetTooltip(book)
        if 'tailor' in tooltip:
            for tbod in FoundTailorBods:
                MoveItem(tbod, 0, book, 0, 0, 0)
                Wait(100)
        else:
            for bbod in FoundBlacksmithBods:
                MoveItem(bbod, 0, book, 0, 0, 0)
                Wait(100)


# Main body
if __name__ == '__main__':
    print("Hello")
    DisconnectChar()
    NextRound = Timer() + 7200000
    while True:
        for Char in Profiles:
            changed = ChangeProfile(Char)
            if changed != 0:
                print("Error while changing to profile {}. Result {}".format(Char, changed))
            ConnectChar(Char)
            GetBod(Tailor)
            GetBod(Tailor)
            GetBod(Blacksmith)
            GetBod(Blacksmith)
            SortBods()
            DisconnectChar()
        while Timer() < NextRound:
            Wait(30000)
        NextRound = Timer() + 7200000
