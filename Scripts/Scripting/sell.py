from common import *

iron = 0x0000
pillow = 0x0AD1
vendor = 0x0191

def Sell():
    while True and CheckLag():
        Wait(1000)         
        FindType(pillow, Backpack())
        if FindCount() > 45:
            AddToSystemJournal('pillows count: {0}'.format(FindCount()))
            FindType(vendor, Ground())
            #while not NewMoveXY(GetX(FindItem()), GetY(FindItem()), True, 1, True):
             #   Wait(1000)
            CancelTarget()
            CancelWaitTarget()
            WaitTargetType(pillow)
            UOSay('sell all')
            Wait(10000)
           # break   
        Wait(1000)

Sell()            