"""Runebook class. Minimal runebook support.

Created by Boydon
Only tested with Python 3.x"""

import datetime

import gumps
from stealth import *


class Runebook():
    """An easy way to handle runebooks."""

    # type of the runebook as class attribute
    type = 0x22C5

    def __init__(self, runeBookID):
        """runeBookID: the ID of the runebook we want to use """

        self.runeBookID = runeBookID
        self.runeNames = []

    def findRuneByName(self, findName):
        """Finds a rune by a given name.
           findName: the name to look for"""

        returnRunes = []
        runeNr = 1

        runeNames = self.listRunes(update=True)

        for runeName in runeNames:
            if findName.lower() in runeName.lower():
                returnRunes.append(runeNr)
            runeNr += 1

        return returnRunes

    def listRunes(self, update=False):
        """Return a list with the names of all the runes.
           Results are cached in self.runeNames and only updated if update == True """

        # if results are cached we return them
        if self.runeNames and not update:
            # print('Using listRunes chache...')
            return self.runeNames

        # print('NOT using listRunes chache...')
        runeNames = []

        while not gumps.gumpFromObject(self.runeBookID, 0x059, wait=True, timeout=5000, delay=1):
            Wait(1)

        textLines = []
        gumpDict = {}

        while not textLines:
            textLines = GetGumpTextLines(gumps.lastGumpIndex())
            Wait(1)

        while not gumpDict:
            gumpDict = gumps.toDict(gumps.lastGumpIndex())
            Wait(1)

        # this is a little bit hard to remember: we are mapping textLines elements using the gumpDict CroppedTexts elements
        # if we are at page one and the descripion is not empty we get the corresponding element in textLines
        runeNames = [textLines[x['Text_ID']] for x in gumpDict['CroppedText'] if
                     x['Page'] == 1 and textLines[x['Text_ID']] != 'Empty']

        self.runeNames = runeNames

        gumps.closeGump()

        return runeNames

    def countRunes(self):
        """Returns the number of runes in the runebook."""
        return len(self.listRunes())

    def travel(self, runeNr, method='r', tryAgain=['fizzles', 'recover', 'reagents', 'tithing', 'mana']):
        """   Travel using the runebook. You need to pass the following parameters:
           - runeNr with the number of the rune you want to travel to (must be between 1 and 16);
           - the method you want to use to travel:
              + 'r' for recall;
              + 'g' for gate;
              + 's' for scroll;
              + 'c' for sacred journey;
           - a list of situations in wich the function won't return the result status, but will try again (see below for return details).

           The following values are returned:
           - 'success'      if the travel was successful
           - 'fizzles'      if the spell fizzles (only for recall)
           - 'blocked'      if the destination is blocked;
           - 'recover'    if you haven't yet recovered from former spell;
           - 'charges'      if the runebook has no more recall scrolls to use;
           - 'reagents'   if you need more reagents;
           - 'tithing'      if you need more tithing points;
           - 'mana'         if you don't have enough mana
           - 'marked'      ??
           - 'nomagic'      if you are travelling from a location where you can't use magic;
           - 'unknow'      if we couldn't recall for an unknow reason. This should never be the case.

           If you add any of thos return values to the tryAgain argument, the function wont return, but instead it will try again to travel.
           Defauld ignored return statuses are:
           - fizzles;
           - recover;
           - reagents;
           - tithing;
           - mana;
           Beware with what you do. You may end in an endless loop here.
        """

        # check on rune number
        if runeNr not in list(range(1, 17)):
            raise Exception('The rune number for runeBookTravel must be between 1 and 16, got {0}'.format(runeNr))

        # check on recal method
        if method not in ['r', 'g', 's', 'c']:
            raise Exception('Unkwon runebook travel method: {0}'.format(method))

        # check on tryAgain arg type
        if not isinstance(tryAgain, list):
            raise TypeError('runeBookTravel is expecting a list as tryAgain argument, got a {0}'.format(type(tryAgain)))

        # translation of FoundedParamID  to be used later on
        fpTranslations = [None] * 9
        fpTranslations[0] = 'fizzles'  # fizzles
        fpTranslations[1] = 'blocked'  # location is blocked
        fpTranslations[2] = 'recover'  # not yet recovered
        fpTranslations[3] = 'charges'  # no charges left
        fpTranslations[4] = 'reagents'  # more reagents
        fpTranslations[5] = 'tithing'  # tithing points
        fpTranslations[6] = 'mana'  # insufficient mana
        fpTranslations[7] = 'marked'  # not marked
        fpTranslations[8] = 'nomagic'  # cannot teleport from here

        while True:
            # we save our starting position
            start = (GetX(Self()), GetY(Self()))

            # we open the rune book
            while not gumps.gumpFromObject(self.runeBookID, 0x059, wait=True, timeout=5000, delay=1):
                Wait(1)

            # TODO: add check to verify that runeNr is present in runebookId

            # button value calculated by recall method
            if method == 'r':
                button = 5 + ((runeNr - 1) * 6)
            elif method == 'g':
                button = 6 + ((runeNr - 1) * 6)
                # TODO implement movement trough the GATE
            elif method == 'c':
                button = 7 + ((runeNr - 1) * 6)
            elif method == 's':
                raise Exception('Runebook scroll traveling not implemented yet!')

            # maybe timeout should be an argument?
            now = datetime.datetime.now()
            timeout = now + datetime.timedelta(seconds=7)
            gumps.clickButton(button, -1, 0, False)

            if WaitJournalLine(now,
                               'fizzles|location is blocked|not yet recovered|no charges left|more reagents|tithing points|insufficient mana|not marked|cannot teleport from here',
                               4000):
                if fpTranslations[FoundedParamID()] not in tryAgain:
                    return fpTranslations[FoundedParamID()]
            else:
                if method == 'g':
                    return 'success'
                while datetime.datetime.now() < timeout:
                    if (GetX(Self()), GetY(Self())) != start:
                        return 'success'
                    else:
                        Wait(1)

        return 'unknow'