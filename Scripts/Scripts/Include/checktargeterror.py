from stealth import *
from datetime import datetime as dt
from datetime import timedelta as td

def CheckTargetError(lines, checktime):
    #5 minutes in DateTime = (1.0 * checktime) / 1440 = 0.00347
    d = dt.now() - td(0, 60 * checktime)
    InJournalBetweenTimes('I am already performing another action|doing something', d, dt.now());
    if LineCount() > lines:
        AddToSystemJournal('Error with target. Disconnected')
        ClearJournal()
        Disconnect()
        