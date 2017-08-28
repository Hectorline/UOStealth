"""
This module will make it easier for you to work with Gumps. Freely inspired by Chrome696 Gumps.pas

Created by Boydon
Only tested with Python 3.x

from http://stealth.od.ua/forum/viewtopic.php?f=15&t=2508
"""

import time
import re

from stealth import *


# def GetGumpID(gump_index):
   # """Replaces the built-in function that as of Stealth 4.04 is broken"""
   # for line in GetGumpFullLines(gump_index):
      # if line.find('GumpID') != -1:
         # gump_id_line = line
         # break
   # else:
      # return 0

   # return int(gump_id_line.split(' ')[1], 16)

def lastGumpIndex():
   """Returns the index of the last opened Gump"""
   return (GetGumpsCount() - 1) if GetGumpsCount() > 0 else -1
   
   
def serialFromIndex(gumpIndex = -1):
   """Returns the serial of the Gump with index gumpIndex. If not specified the last index will be used"""
   return GetGumpSerial(lastGumpIndex() if gumpIndex < 0 else gumpIndex)
   
   
def idFromIndex(gumpIndex = -1):
   """Returns the ID of the Gump with index gumpIndex. If not specified the last index will be used"""
   return GetGumpID(lastGumpIndex() if gumpIndex < 0 else gumpIndex)

def toDict(gumpIndex = -1):
   """Returns the Gump information obtained by GetGumpFullLines formatted in a handy and pretty dictionary.
   If no index is provided the last one will be used.
   This function exist mainly as a workaround for the fact that GetGumpInfo is not available in Python.
   Some collections may be missing. If this is the case contact me.
   """
   
   # we split every two spaces, should the format change this will be broken
   reTokens = re.compile(r"[\s]{2,}")
   gumpDict = {}
   
   # internal use only
   def _gumpList2Dict(strToList, dictKey, keys):
      """For internal use only, this function will exctract all the tokens in strToList, and combine them with keys to form a dictionary.
         This new dictionay will be appended to the gumpDict dictonary in a list of dictionraies with key dictKey"""
         
      global gumpDict
      
      # when we split we can have integers or strings. If we get integer they will be forced to that type (comparison will be easier)
      # we also want to be sure that we are not extracting the header line with the keys
      tokenList = [int(token) if str.isdigit(token) else token for token in reTokens.split(strToList) if token not in keys]
      
      if tokenList:
         if gumpDict.get(dictKey, False):
            gumpDict[dictKey].append(dict(zip(keys, tokenList)))
         else:
            gumpDict[dictKey] = [dict(zip(keys, tokenList))]
      pass
   
   lines = GetGumpFullLines(lastGumpIndex() if gumpIndex < 0 else gumpIndex)
   for line in lines:
      pieces = line.split(': ')
      if pieces[0]:
         if pieces[0] == 'Serial':
            gumpDict['Serial'] = pieces[1]
         elif pieces[0] == 'GumpID':
            gumpDict['Id'] = pieces[1]
         elif pieces[0] == 'X':
            gumpDict['X'] = pieces[1]
         elif pieces[0] == 'Y':
            gumpDict['Y'] = pieces[1]
         elif pieces[0] == 'Pages':
            gumpDict['Pages'] = pieces[1]
         elif pieces[0] == 'Gump Options':
            subpieces = pieces[1].split(' ')
            if subpieces:
               gumpDict['GumpOptions'] = [subpiece for subpiece in subpieces]
         elif pieces[0] == 'GumpPicTiled':
            _gumpList2Dict(pieces[1], 'GumpPicTiled', ['X', 'Y', 'Width', 'Height', 'Gump_ID', 'ElemNum'])
         elif pieces[0].find('ResizePic') != -1:
            _gumpList2Dict(pieces[1], 'ResizePic', ['X', 'Y', 'ID', 'Width', 'Height' ,'Page', 'ElemNum'])
         elif pieces[0].find('XmfHTMLGumpColor') != -1:
            _gumpList2Dict(pieces[1], 'XmfHTMLGumpColor', ['X', 'Y', 'Width', 'Height', 'ClilocID', 'Background', 'scrollbar', 'Hue', 'ElemNum', 'ClilocText'])
         elif pieces[0].find('XmfHTMLTok') != -1:
            _gumpList2Dict(pieces[1], 'XmfHTMLTok', ['X', 'Y', 'Width', 'Height', 'Background', 'scrollbar', 'Color', 'ClilocID', 'Arguments', 'ElemNum', 'ClilocText'])
         elif pieces[0].find('CheckerTrans') != -1:
            _gumpList2Dict(pieces[1], 'CheckerTrans', ['X', 'Y', 'Width', 'Height', 'Page', 'ElemNum'])
         elif pieces[0].find('GumpButton') != -1:
            _gumpList2Dict(pieces[1], 'GumpButton', ['X', 'Y', 'Released_ID', 'Pressed_ID', 'Quit', 'Page_ID', 'Return_value', 'Page', 'ElemNum'])
         elif pieces[0].find('GumpText') != -1:
            _gumpList2Dict(pieces[1], 'GumpText', ['X', 'Y','Color', 'Text_ID', 'Page', 'ElemNum'])
         elif pieces[0].find('GumpPic') != -1:
            _gumpList2Dict(pieces[1], 'GumpPic', ['X', 'Y', 'ID', 'Hue', 'Page', 'ElemNum'])
         elif pieces[0].find('CroppedText') != -1:
            _gumpList2Dict(pieces[1], 'CroppedText', ['X', 'Y', 'Width', 'Height', 'Color', 'Text_ID', 'Page', 'ElemNum'])
         elif pieces[0].find('XmfHtmlGump') != -1:
            _gumpList2Dict(pieces[1], 'XmfHtmlGump', ['X', 'Y', 'Width', 'Height', 'ClilocID', 'Background', 'scrollbar', 'Page', 'ElemNum', 'ClilocText'])
         
         # else:
            # print(pieces[0])
      
      # print(pieces)      
   
   return gumpDict      

def waitForGumpID(gumpID, timeout=5000, delay=100):
   """Waits for a gump that has the given gumpID for 'timeout' milliseconds with a 'delay' sleep.
      After the timeout, if the gumpID is not the expected one it will return False else it will return True."""
   #from millisec to secs
   timeout /= 1000
   timeout += time.time()
   
   while time.time() <= timeout:
      if idFromIndex() == gumpID:
         return True
      else:
         #print " {0} != {1} , ... count: {2}".format(idFromIndex(),gumpID,GetGumpsCount())
         Wait(delay)
   
   return False

def waitForNewGumpSerial(gumpSerial, gumpCount, timeout=5000, delay=1):
   """Waits for a gump that has a Serial different from the one passed in the 'gumpSerial' argument with a 'delay' sleep.
      After 'timeout' milliseconds, if the gumpSerial is not changet it will return False, eltre True."""
   #from millisec to secs
   timeout /= 1000
   timeout += time.time()
   
   while time.time() <= timeout:
      if serialFromIndex() != gumpSerial and GetGumpsCount() == gumpCount:
         return True
      else:
         Wait(delay)
         
   return False

def clickButton(button, gumpIndex = -1, gumpID=0, wait=True, timeout=5000, delay=1):
   """Click on a button and if the wait argument is True it waits for a new serial with a delay sleep
      - gumpIndex: once the button has been clicked wich index should we check for a new gump?
      - gumpID: the expected id of the new gump after we click
      - wait: should we wait for a new gump?
      - timeout: how many milliseconds should we wait for a new gump?
      - delay: how many milliseconds should we sleep?
      """
   
   gumpSerial = serialFromIndex()
   _gumpIndex = lastGumpIndex() if gumpIndex < 0 else gumpIndex
   NumGumpButton(_gumpIndex, button)
   #WaitGump(str(button))
   
   if wait:
      if not gumpID or gumpID == 0:
         raise TypeError('clickButton is expecting a gumpID. None passed')
   
      timeout /= 1000
      timeout += time.time()
      while time.time() <= timeout:
         if serialFromIndex() != gumpSerial and idFromIndex() == gumpID:
            return True
         else:
            Wait(delay)
      return False
   else:
      return True
      
   return None
   
def clickButtonByClicloc(clilocID, rangeX, rangeY, gumpIndex = -1, gumpID = 0, wait = True):
   """Shortcut for clickButtonByCliclocPage with page 1.
      This is present mainly for backward compatibility."""
      
   return clickButtonByCliclocPage(clilocID, rangeX, rangeY, 1, gumpIndex, gumpID, wait)
   
def clickButtonByCliclocPage(clilocID, rangeX, rangeY, page = 1, gumpIndex = -1, gumpID = 0, wait = True):
   """This will click a button searching for a cliloc at a given range.
      This function is useful for craft menus: the typical situation is the button graphic repeated many times with different clilocs always
      at the same distance from the button.
      
      - clilocID: the ID of the clilock to look for
      - rangeX: the X distance of the button from clicloID
      - rangeY: the Y distance of the button from clicloID
      - page: the page of the gump in wich the button to click is appearing. This is calculated, not part of the gump itself
      
      - gumpIndex, gumpID, wait: for remaining args please check the clickButton pyDoc as this function is finally wrapping around it
      """
   
   if not isinstance(clilocID, int):
      raise TypeError('clickButtonByClicloc is expecting an iteger as clilocID argument, it got an {0}'.format(type(int)))
   
   gump = {}
   
   _gumpIndex = lastGumpIndex() if gumpIndex < 0 else gumpIndex
   
   gump = toDict(_gumpIndex)
   # while not gump.get('XmfHTMLGumpColor', False)
   
   #we start at page 0
   curPage = 0
   
   if gump.get('XmfHTMLGumpColor', False):
      for XHGC in gump['XmfHTMLGumpColor']:
         if XHGC['ClilocID'] == clilocID:
            for button in gump['GumpButton']:
               if (button['X'] == (XHGC['X'] - rangeX)) and (button['Y'] == (XHGC['Y'] - rangeY)):
                  curPage += 1
                  if curPage == page:
                     return clickButton(button['Return_value'], _gumpIndex, gumpID, wait)
   else:
      # gumpErrorLog = open(r"" + StealthPath() + "gumpError.log", "w")
      # 
      # print ("Unexpected condition in clickButtonByCliclocPage!")
      # print ("The function was called with the following arguments: clilocID: %s, rangeX: %s, rangeY: %s, page: %s, gumpIndex: %s, _gumpIndex: %s, gumpID: %s, wait:%s" % (clilocID, rangeX, rangeY, page, gumpIndex, _gumpIndex, gumpID, wait))
      # 
      # print ("Unexpected condition in clickButtonByCliclocPage!", file=gumpErrorLog)
      # print ("The function was called with the following arguments: clilocID: %s, rangeX: %s, rangeY: %s, page: %s, gumpIndex: %s, _gumpIndex: %s, gumpID: %s, wait:%s" % (clilocID, rangeX, rangeY, page, gumpIndex, _gumpIndex, gumpID, wait), file=gumpErrorLog)
      # # print ("_gumpIndex has value %s" % (_gumpIndex,))
      # # print ("_gumpIndex has value %s" % (_gumpIndex,), file=gumpErrorLog)
      # 
      # import traceback
      # # print("---------- PRINT_STACK ----------")
      # # traceback.print_stack()
      # print("---------- PRINT_STACK ----------", file=gumpErrorLog)
      # traceback.print_stack(file=gumpErrorLog)
      # 
      # # print("---------- PRINT_EXC ----------")
      # # traceback.print_exc()
      # print("---------- PRINT_EXC ----------", file=gumpErrorLog)
      # traceback.print_exc(file=gumpErrorLog)
      # 
      # # print("---------- REPR ----------")
      # # print(repr(traceback.extract_stack()))
      # # print(repr(traceback.format_stack()))
      # print("---------- REPR ----------", file=gumpErrorLog)
      # print(repr(traceback.extract_stack()), file=gumpErrorLog)
      # print(repr(traceback.format_stack()), file=gumpErrorLog)
      # 
      # 
      # #raise Exception('Impossible to find XmfHTMLGumpColor in the gump: %s' % (str(gump),))
      return False

def gumpFromObject(objectID, gumpID=0, wait=True, timeout=5000, delay=1, useDelay=700):
   """Uses the object with ID objectID and if 'wait' is true it will wait for a new Gump with ID 'gumpID'.
      After 'timeout' milliseconds looped with a sleep of 'delay' it will return true if the expected GumpID is fould, else False."""
      
   gumpSerial = serialFromIndex()
   UseObject(objectID)
   Wait(useDelay)
   
   if wait:
      if not gumpID or gumpID == 0:
         raise TypeError('gumpFromObject is expecting a gumpID. None passed')
      
      timeout /= 1000
      timeout += time.time()
      while time.time() <= timeout:
         if serialFromIndex() != gumpSerial and idFromIndex() == gumpID:
            return True
         else:
            Wait(delay)
      return False
   
   return None
   
def clilocFindMinButtonRange(clilocID, toSearch = 'XmfHTMLGumpColor',  gumpIndex = -1):
   """This function, given a clilocID, will find the nearest button by position and return the offset in a tuple.
      This should be used together with clickButtonByClicloc to make you life easier in calculating ranges.
      The distance from the button is calculated summing the X distance with the Y distance, so results may not be reliable.
      Please test the results and use this wisely."""
      
   _gumpIndex = lastGumpIndex() if gumpIndex < 0 else gumpIndex
   gump = toDict(_gumpIndex)
   
   #we inizialize it with really high values
   textRange = (1000000, 1000000)
   
   if gump.get(toSearch, False):
      for XHGC in gump[toSearch]:
         if XHGC['ClilocID'] == clilocID:
            for button in gump['GumpButton']:
               foundRange = ((XHGC['X'] - button['X']), (XHGC['Y'] - button['Y']))
               # we compare absolute values of tuples
               # print ( (tuple(map(abs, foundRange)) , tuple(map(abs, textRange))), tuple(map(abs, foundRange)) < tuple(map(abs, textRange)) )
               if ( sum(tuple(map(abs, foundRange))) < sum(tuple(map(abs, textRange))) ):
                  textRange = foundRange
   
      return textRange
   else:
      raise Exception('The gumps has no collection "{}"'.format(toSearch))
   
def closeGump(gumpIndex = -1, simpleGump = False, wait=True, timeout=5000, delay=1):
   """Closes gump with index gumpIndex if in simple mode (the default) else it won't check the gumpIndex and it will send a Result 0"""
   
   _gumpIndex = lastGumpIndex() if gumpIndex < 0 else gumpIndex
   gumpSerial = serialFromIndex(_gumpIndex)

   if simpleGump:
      CloseSimpleGump(_gumpIndex)
   else:
      clickButton(0, _gumpIndex, 0, False)
   
   if wait:
      timeout /= 1000
      timeout += time.time()
      while time.time() <= timeout:
         if serialFromIndex() != gumpSerial:
            return True
         else:
            Wait (delay)
      return False
      
def closeAllGumps():
   while GetGumpsCount():
      if not closeGump():
         print ("closeAllGumps could not close one or more Gumps")
         return False
   
   return True
      
def clickButtonByTileart(tileart, gumpIndex = -1, gumpID=0, wait=True, timeout=5000, delay=1):
   """This function will search within a gump for a button that has as released/pressed graphic a given tileart and click it. 
      The following arguments can be passed:
      - tileart is the graphic we are looking for;
      - gumpIndex the index of the gump we have to search (optional, will default to the last index);
      - gumpID the ID of the gump to wait once the button has been clicked (optional, but needs to be specified if wait is Ttue)
      - wait boolen to decide if we want to wait for a button once that the button has been clicked. If this is True gumpID must be specified
      - timeout max time to wait for gump in millisec
      - delay time to wait between loops"""
   
   gumpSerial = serialFromIndex()
   _gumpIndex = lastGumpIndex() if gumpIndex < 0 else gumpIndex
   gump = toDict(_gumpIndex)
   
   for button in gump['GumpButton']:
      if button['Released_ID'] == tileart or button['Pressed_ID'] == tileart:
         return clickButton(button['Return_value'], _gumpIndex, gumpID, wait, timeout, delay)
   else:
      raise Exception('Error in clickButtonByTileart: could not find the desired tileart in the gump!')
   
def searchClilocText(clilocID, gumpIndex = -1):
   """Search for a given clicloID in gump numbered by gumpIndex. If found it will return True, else it will return false """
   
   _gumpIndex = lastGumpIndex() if gumpIndex < 0 else gumpIndex
   
   gump = toDict(_gumpIndex)
   for XHGC in gump['XmfHTMLGumpColor']:
      if XHGC['ClilocID'] == clilocID:
         return True
   
   return False
   
def setWaitHook(waitHook):
   """The Wait function from Stealth is used many times in this module. This function will allow you to hook it: this can
      be very usefull in certain situations where you want to perform the same check many times (f.e. when you want to check for a world save
      or you want to have reliable journal scanning).
      
      The only argument (waitHook) is the function you want to use to replace the original Wait."""
      
   
   global Wait
   Wait = waitHook
   return True