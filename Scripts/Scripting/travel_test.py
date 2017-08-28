from stealth import *
from py_stealth.py_stealth import *

gumpDelay = 1000
def Recall(runebookID, stockRuneEntry):
    UseObject(runebookID)
    Wait(CheckLag(30000))
    Wait(gumpDelay)
    WaitGump(str(5 + ((stockRuneEntry - 1) * 6)))
    Wait(CheckLag(30000))
    Wait(gumpDelay)

if __name__ == '__main__':
    Recall()