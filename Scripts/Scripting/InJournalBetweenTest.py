try:
    from py_stealth.py_stealth import *
except:
    from stealth import *

import datetime

def InJournalBetweenTimesTest():
    StartTime = datetime.datetime.now()
    Wait(2000)
    UOSay("Hello")
    Wait(2000)
    NowTime = datetime.datetime.now()
    if InJournalBetweenTimes("Hello", StartTime, NowTime)>0:
        print("It Works")
    else:
        print("Couldn't find a text")

def WeightTest():
    if 477 < Weight() + 70:
        print("overcarried")
    else:
        print("not found")

if __name__ == '__main__':
    InJournalBetweenTimesTest()
    WeightTest()