# Copyright (C) 2013 Lorenzo Boydon Persichetti
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

################################# TO DO LIST ##########################################
# TO DO LIST:
#
# The following methods have no wrapper yet:
# - Script_GetContextMenuRec
#######################################################################################

"""
The idea of this wrapper is to be fully compatible with the current standard implementation of Stealth Python.
The code has been developed using Python 3.x
"""

from ctypes import *
import os as _os
import sys as _sys

# from json import loads


_is64bit = True if _sys.maxsize != 0x7FFFFFFF else False
_sys.path.append(_os.path.split(_os.path.dirname(__file__))[0])
for _path in _sys.path:
    _dll_path = _os.path.join(_path,
                              "Script_x64.dll" if _is64bit else "Script.dll")
    if _os.path.exists(_dll_path):
        stealth_dll = WinDLL(_dll_path)
        break
else:
    error = bytes("Can't find Script.dll")
    windll.user32.MessageBoxA(0, error, bytes('Error'), 0)
    exit()


def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    reverse = dict((value, key) for key, value in enums.items())
    enums['reverse_mapping'] = reverse
    return type('Enum', (), enums)


# Event Enumeration
TPacketEvent = (
    # {0}
    'evItemInfo', 'evItemDeleted', 'evSpeech', 'evDrawGamePlayer',
    'evMoveRejection', 'evDrawContainer', 'evAddItemToContainer',
    'evAddMultipleItemsInCont', 'evRejectMoveItem', 'evUpdateChar',
    # {10}
    'evDrawObject', 'evMenu', 'evMapMessage', 'evAllow_RefuseAttack',
    'evClilocSpeech', 'evClilocSpeechAffix', 'evUnicodeSpeech',
    'evBuff_DebuffSystem', 'evClientSendResync', 'evCharAnimation',
    # {20}
    'evICQDisconnect', 'evICQConnect', 'evICQIncomingText', 'evICQError',
    'evIncomingGump', 'evTimer1', 'evTimer2', 'evWindowsMessage',
    'evSound', 'evDeath',
    # {30}
    'evQuestArrow', 'evPartyInvite', 'evMapPin', 'evGumpTextEntry',
    'evGraphicalEffect', 'evIRCIncomingText', 'evSkypeEvent',
    'evSetGlobalVar', 'evUpdateObjStats',
)

TTileDataFlags = (
    # {0}
    'tsfBackground', 'tsfWeapon', 'tsfTransparent', 'tsfTranslucent',
    'tsfWall', 'tsfDamaging', 'tsfImpassable', 'tsfWet',
    'tsfUnknown', 'tsfSurface',
    # {10}
    'tsfBridge', 'tsfGeneric', 'tsfWindow', 'tsfNoShoot', 'tsfPrefixA',
    'tsfPrefixAn', 'tsfInternal', 'tsfFoliage', 'tsfPartialHue',
    'tsfUnknown1',
    # {20}
    'tsfMap', 'tsfContainer', 'tsfWearable', 'tsfLightSource',
    'tsfAnimated', 'tsfNoDiagonal', 'tsfUnknown2',
    'tsfArmor', 'tsfRoof', 'tsfDoor',
    # {30}
    'tsfStairBack', 'tsfStairRight', 'tlfTranslucent',
    'tlfWall', 'tlfDamaging', 'tlfImpassable', 'tlfWet',
    'tlfSurface', 'tlfBridge', 'tlfPrefixA',
    # {40}
    'tlfPrefixAn', 'tlfInternal', 'tlfMap', 'tlfUnknown3',
)


########################### CUSTOM RECORDS STRUCTURES #################################
# About data    
class TAboutData(Structure):
    """Struct for GetStealthInfo results"""
    _fields_ = [
        ('StealthVersion', c_ushort * 3),
        ('Build', c_ushort),
        ('BuildDate', c_double),
        ('GITRevNumber', c_ushort),
        ('GITRevision', c_ubyte * 10),
    ]


# Extended Info
class TExtendedInfo(Structure):
    """Struct for GetExtInfo results """
    _pack_ = 1
    _fields_ = [
        ('MaxWeight', c_ushort),
        ('Race', c_ubyte),
        ('StatCap', c_ushort),
        ('PetsCurrent', c_ubyte),
        ('PetsMax', c_ubyte),
        ('FireResist', c_ushort),
        ('ColdResist', c_ushort),
        ('PoisonResist', c_ushort),
        ('EnergyResist', c_ushort),
        ('Luck', c_short),
        ('DamageMin', c_ushort),
        ('DamageMax', c_ushort),
        ('Tithing_points', c_uint),
        ('Hit_Chance_Incr', c_ushort),
        ('Swing_Speed_Incr', c_ushort),
        ('Damage_Chance_Incr', c_ushort),
        ('Lower_Reagent_Cost', c_ushort),
        ('HP_Regen', c_ushort),
        ('Stam_Regen', c_ushort),
        ('Mana_Regen', c_ushort),
        ('Reflect_Phys_Damage', c_ushort),
        ('Enhance_Potions', c_ushort),
        ('Defense_Chance_Incr', c_ushort),
        ('Spell_Damage_Incr', c_ushort),
        ('Faster_Cast_Recovery', c_ushort),
        ('Faster_Casting', c_ushort),
        ('Lower_Mana_Cost', c_ushort),
        ('Strength_Incr', c_ushort),
        ('Dext_Incr', c_ushort),
        ('Int_Incr', c_ushort),
        ('HP_Incr', c_ushort),
        ('Stam_Incr', c_ushort),
        ('Mana_Incr', c_ushort),
        ('Max_HP_Incr', c_ushort),
        ('Max_Stam_Incr', c_ushort),
        ('Max_Mana_Increase', c_ushort)
    ]


# Land Tile Data
class TLandTileData(Structure):
    _pack_ = 1
    _fields_ = [
        ('Flags', c_uint),
        ('Flags2', c_uint),
        ('TextureID', c_ushort),
        ('Name', c_char * 20)
    ]


# Static Tile Data
class TStaticTileDataNew(Structure):
    _pack_ = 1
    _fields_ = [
        ('Flags', c_ulonglong),
        ('Height', c_int),
        ('RadarColorRGBA', c_ubyte * 4),
        ('Name', c_char * 20),
    ]


# Target Info
class TTargetInfo(Structure):
    _pack_ = 1
    _fields_ = [
        ('ID', c_uint),
        ('Tile', c_ushort),
        ('X', c_ushort),
        ('Y', c_ushort),
        ('Z', c_byte),
    ]


# Point
class TPoint(Structure):
    _pack_ = 1
    _fields_ = [
        ('X', c_int),
        ('Y', c_int),
    ]


# My Point
class TMyPoint(Structure):
    _pack_ = 1
    _fields_ = [
        ('X', c_ushort),
        ('Y', c_ushort),
        ('Z', c_byte),
    ]


# StaticCellXY
class TStaticItemRealXY(Structure):
    _pack_ = 1
    _fields_ = [
        ('Tile', c_ushort),
        ('X', c_ushort),
        ('Y', c_ushort),
        ('Z', c_byte),
        ('Color', c_ushort),
    ]


# Found Tile
class TFoundTile(Structure):
    _pack_ = 1
    _fields_ = [
        ('Tile', c_ushort),
        ('X', c_short),
        ('Y', c_short),
        ('Z', c_byte),
    ]


class TGroup(Structure):
    _pack_ = 1
    _fields_ = [
        ('groupnumber', c_int),
        ('Page', c_int),
        ('ElemNum', c_int),
    ]


class TEndGroup(Structure):
    _pack_ = 1
    _fields_ = [
        ('groupnumber', c_int),
        ('Page', c_int),
        ('ElemNum', c_int),
    ]


class TPage(Structure):
    _pack_ = 1
    _fields_ = [
        ('Page', c_int),
        ('ElemNum', c_int),
    ]


class TMasterGump(Structure):
    _pack_ = 1
    _fields_ = [
        ('ID', c_uint),
        ('ElemNum', c_int),
    ]


class TGumpButton(Structure):
    _pack_ = 1
    _fields_ = [
        ('x', c_int),
        ('y', c_int),
        ('released_id', c_int),
        ('pressed_id', c_int),
        ('quit', c_int),
        ('page_id', c_int),
        ('return_value', c_int),
        ('Page', c_int),
        ('ElemNum', c_int),
    ]


class TButtonTileArt(Structure):
    _pack_ = 1
    _fields_ = [
        ('x', c_int),
        ('y', c_int),
        ('released_id', c_int),
        ('pressed_id', c_int),
        ('quit', c_int),
        ('page_id', c_int),
        ('return_value', c_int),
        ('art_id', c_int),
        ('Hue', c_int),
        ('art_x', c_int),
        ('art_y', c_int),
        ('ElemNum', c_int),
    ]


class TCheckBox(Structure):
    _pack_ = 1
    _fields_ = [
        ('x', c_int),
        ('y', c_int),
        ('released_id', c_int),
        ('pressed_id', c_int),
        ('status', c_int),
        ('return_value', c_int),
        ('Page', c_int),
        ('ElemNum', c_int),
    ]


class TCheckerTrans(Structure):
    _pack_ = 1
    _fields_ = [
        ('x', c_int),
        ('y', c_int),
        ('width', c_int),
        ('height', c_int),
        ('Page', c_int),
        ('ElemNum', c_int),
    ]


class TCroppedText(Structure):
    _pack_ = 1
    _fields_ = [
        ('x', c_int),
        ('y', c_int),
        ('width', c_int),
        ('height', c_int),
        ('color', c_int),
        ('text_id', c_int),
        ('Page', c_int),
        ('ElemNum', c_int),
    ]


class TGumpPic(Structure):
    _pack_ = 1
    _fields_ = [
        ('x', c_int),
        ('y', c_int),
        ('id', c_int),
        ('Hue', c_int),
        ('Page', c_int),
        ('ElemNum', c_int),
    ]


class TGumpPicTiled(Structure):
    _pack_ = 1
    _fields_ = [
        ('x', c_int),
        ('y', c_int),
        ('width', c_int),
        ('height', c_int),
        ('gump_id', c_int),
        ('Page', c_int),
        ('ElemNum', c_int),
    ]


class TRadio(Structure):
    _pack_ = 1
    _fields_ = [
        ('x', c_int),
        ('y', c_int),
        ('released_id', c_int),
        ('pressed_id', c_int),
        ('status', c_int),
        ('return_value', c_int),
        ('Page', c_int),
        ('ElemNum', c_int),
    ]


class TResizePic(Structure):
    _pack_ = 1
    _fields_ = [
        ('x', c_int),
        ('y', c_int),
        ('gump_id', c_int),
        ('width', c_int),
        ('height', c_int),
        ('Page', c_int),
        ('ElemNum', c_int),
    ]


class TGumpText(Structure):
    _pack_ = 1
    _fields_ = [
        ('x', c_int),
        ('y', c_int),
        ('color', c_int),
        ('text_id', c_int),
        ('Page', c_int),
        ('ElemNum', c_int),
    ]


class TTextEntry(Structure):
    _pack_ = 1
    _fields_ = [
        ('x', c_int),
        ('y', c_int),
        ('width', c_int),
        ('height', c_int),
        ('color', c_int),
        ('return_value', c_int),
        ('default_text_id', c_int),
        ('Page', c_int),
        ('ElemNum', c_int),
    ]


class TTextEntryLimited(Structure):
    _pack_ = 1
    _fields_ = [
        ('x', c_int),
        ('y', c_int),
        ('width', c_int),
        ('height', c_int),
        ('color', c_int),
        ('return_value', c_int),
        ('default_text_id', c_int),
        ('Limit', c_int),
        ('Page', c_int),
        ('ElemNum', c_int),
    ]


class TTilePic(Structure):
    _pack_ = 1
    _fields_ = [
        ('x', c_int),
        ('y', c_int),
        ('id', c_int),
        ('Page', c_int),
        ('ElemNum', c_int),
    ]


class TTilePichue(Structure):
    _pack_ = 1
    _fields_ = [
        ('x', c_int),
        ('y', c_int),
        ('id', c_int),
        ('color', c_int),
        ('Page', c_int),
        ('ElemNum', c_int),
    ]


class TTooltip(Structure):
    _pack_ = 1
    _fields_ = [
        ('Cliloc_ID', c_uint),
        ('Page', c_int),
        ('ElemNum', c_int),
    ]


class THtmlGump(Structure):
    _pack_ = 1
    _fields_ = [
        ('x', c_int),
        ('y', c_int),
        ('width', c_int),
        ('height', c_int),
        ('text_id', c_int),
        ('background', c_int),
        ('scrollbar', c_int),
        ('Page', c_int),
        ('ElemNum', c_int),
    ]


class TXmfHTMLGump(Structure):
    _pack_ = 1
    _fields_ = [
        ('x', c_int),
        ('y', c_int),
        ('width', c_int),
        ('height', c_int),
        ('Cliloc_id', c_uint),
        ('background', c_int),
        ('scrollbar', c_int),
        ('Page', c_int),
        ('ElemNum', c_int),
    ]


class TXmfHTMLGumpColor(Structure):
    _pack_ = 1
    _fields_ = [
        ('x', c_int),
        ('y', c_int),
        ('width', c_int),
        ('height', c_int),
        ('Cliloc_id', c_uint),
        ('background', c_int),
        ('scrollbar', c_int),
        ('Hue', c_int),
        ('Page', c_int),
        ('ElemNum', c_int),
    ]


class TXmfHTMLTok(Structure):
    _pack_ = 1
    _fields_ = [
        ('x', c_int),
        ('y', c_int),
        ('width', c_int),
        ('height', c_int),
        ('background', c_int),
        ('scrollbar', c_int),
        ('Color', c_int),
        ('Cliloc_id', c_uint),
        ('Arguments', c_wchar_p),
        ('Page', c_int),
        ('ElemNum', c_int),
    ]


class TItemProperty(Structure):
    _pack_ = 1
    _fields_ = [
        ('Prop', c_uint),
        ('ElemNum', c_int),
    ]


class TUnknownItem(Structure):
    _pack_ = 1
    _fields_ = [
        ('CmdName', c_wchar_p),
        ('Arguments', c_wchar_p),
        ('ElemNum', c_int),
    ]


class TBuffIcon(Structure):
    _pack_ = 1
    _fields_ = [
        ('Attribute_ID', c_ushort),
        ('TimeStart', c_double),
        ('Seconds', c_ushort),
        ('ClilocID1', c_uint),
        ('ClilocID2', c_uint),
    ]


#######################################################################################

##################### TEMP PLACE HOLDERS TO BE IMPLEMNTED/REMOVED #####################

# json needed in Methods.pas    
class TTileDataFlagSet:
    def from_param(self):
        pass


#######################################################################################

def TDateTimeToPyDateTime(tdatetime):
    """Converts a TDateTime from Delphi to a datetime.datetime in Python.
    For more info see: http://docs.embarcadero.com/products/rad_studio/delphiAndcpp2009/HelpUpdate2/EN/html/delphivclwin32/System_TDateTime.html """
    from datetime import datetime as dt, timedelta as td

    # we ensure the we are dealing with a float
    tdatetime = float(tdatetime)

    startDate = dt(year=1899, month=12, day=30)
    days = int(tdatetime)
    hours = 24 * (abs(tdatetime - days))
    deltaDate = td(days=days, hours=hours)

    return startDate + deltaDate


def PyDateTimeTOTDateTime(pydatetime):
    """Converts a datetime.datetime from Python to a TDateTimein Delphi. For more info see:
    http://docs.embarcadero.com/products/rad_studio/delphiAndcpp2009/HelpUpdate2/EN/html/delphivclwin32
    /System_TDateTime.html """
    from datetime import datetime as dt, timedelta as td

    if not isinstance(pydatetime, dt):
        raise TypeError('PyDateTimeTOTDateTime only accepts datetime.datetime arguments')

    startDate = dt(year=1899, month=12, day=30)
    deltaDate = (pydatetime - startDate)

    days = deltaDate.days
    deltaDate -= td(days=days)

    hours = ((deltaDate.total_seconds()) / 3600.0) / 24

    return float(days) + float(hours)


def stringFormMemory(address):
    outLen = c_uint()
    memmove(addressof(outLen), address, sizeof(c_uint))
    if outLen.value > 0:
        return wstring_at(address + 4, outLen.value)
    else:
        return ''


def split_by_n(seq, n):
    """A generator to divide a sequence into chunks of n units."""
    while seq:
        yield seq[:n]
        seq = seq[n:]


class eventProc():
    """Class decorator to give persistance to EventProcs"""

    def __init__(self, setEventProc):
        """Called when the function is defined"""
        self.callbacks = {}
        self.funPTRs = {}

    def __call__(self, event, func):
        """Called when the function is called"""
        if event not in TPacketEvent:
            raise Exception('Unkwon Event: {}'.format(event))

        self.event_index = TPacketEvent.index(event)
        self.event = c_ubyte(self.event_index)

        # evItemInfo 
        if self.event_index == 0:
            self.callbacks[0] = WINFUNCTYPE(c_void_p, c_uint)
        # evItemDeleted 
        elif self.event_index == 1:
            self.callbacks[1] = WINFUNCTYPE(c_void_p, c_uint)
        # evSpeech 
        elif self.event_index == 2:
            self.callbacks[2] = WINFUNCTYPE(c_void_p, c_wchar_p, c_wchar_p, c_uint)
        # evDrawGamePlayer 
        elif self.event_index == 3:
            self.callbacks[3] = WINFUNCTYPE(c_void_p, c_uint)
        # evMoveRejection 
        elif self.event_index == 4:
            self.callbacks[4] = WINFUNCTYPE(c_void_p, c_ushort, c_ushort, c_ubyte, c_ushort, c_ushort)
        # evDrawContainer 
        elif self.event_index == 5:
            self.callbacks[5] = WINFUNCTYPE(c_void_p, c_uint, c_ushort)
        # evAddItemToContainer 
        elif self.event_index == 6:
            self.callbacks[6] = WINFUNCTYPE(c_void_p, c_uint, c_uint)
        # evAddMultipleItemsInCont 
        elif self.event_index == 7:
            self.callbacks[7] = WINFUNCTYPE(c_void_p, c_uint)
        # evRejectMoveItem 
        elif self.event_index == 8:
            self.callbacks[8] = WINFUNCTYPE(c_void_p, c_ubyte)
        # evUpdateChar 
        elif self.event_index == 9:
            self.callbacks[9] = WINFUNCTYPE(c_void_p, c_uint)
        # evDrawObject 
        elif self.event_index == 10:
            self.callbacks[10] = WINFUNCTYPE(c_void_p, c_uint)
        # evMenu 
        elif self.event_index == 11:
            self.callbacks[11] = WINFUNCTYPE(c_void_p, c_uint, c_ushort)
        # evMapMessage 
        elif self.event_index == 12:
            self.callbacks[12] = WINFUNCTYPE(c_void_p, c_uint, c_int, c_int)
        # evAllow_RefuseAttack 
        elif self.event_index == 13:
            self.callbacks[13] = WINFUNCTYPE(c_void_p, c_uint, c_bool)
        # evClilocSpeech 
        elif self.event_index == 14:
            self.callbacks[14] = WINFUNCTYPE(c_void_p, c_uint, c_wchar_p, c_uint, c_wchar_p)
        # evClilocSpeechAffix 
        elif self.event_index == 15:
            self.callbacks[15] = WINFUNCTYPE(c_void_p, c_uint, c_wchar_p, c_uint, c_wchar_p, c_wchar_p)
        # evUnicodeSpeech 
        elif self.event_index == 16:
            self.callbacks[16] = WINFUNCTYPE(c_void_p, c_wchar_p, c_wchar_p, c_uint)
        # evBuff_DebuffSystem 
        elif self.event_index == 17:
            self.callbacks[17] = WINFUNCTYPE(c_void_p, c_uint, c_ushort, c_bool)
        # evClientSendResync 
        elif self.event_index == 18:
            self.callbacks[18] = WINFUNCTYPE(c_void_p)
        # evCharAnimation 
        elif self.event_index == 19:
            self.callbacks[19] = WINFUNCTYPE(c_void_p, c_uint, c_ushort)
        # evICQDisconnect 
        elif self.event_index == 20:
            self.callbacks[20] = WINFUNCTYPE(c_void_p)
        # evICQConnect 
        elif self.event_index == 21:
            self.callbacks[21] = WINFUNCTYPE(c_void_p)
        # evICQIncomingText 
        elif self.event_index == 22:
            self.callbacks[22] = WINFUNCTYPE(c_void_p, c_uint, c_wchar_p)
        # evICQError 
        elif self.event_index == 23:
            self.callbacks[23] = WINFUNCTYPE(c_void_p, c_wchar_p)
        # evIncomingGump 
        elif self.event_index == 24:
            self.callbacks[24] = WINFUNCTYPE(c_void_p, c_uint, c_uint, c_uint, c_uint)
        # evTimer1 
        elif self.event_index == 25:
            self.callbacks[25] = WINFUNCTYPE(c_void_p)
        # evTimer2 
        elif self.event_index == 26:
            self.callbacks[26] = WINFUNCTYPE(c_void_p)
        # evWindowsMessage 
        elif self.event_index == 27:
            self.callbacks[27] = WINFUNCTYPE(c_void_p, c_uint)
        # evSound 
        elif self.event_index == 28:
            self.callbacks[28] = WINFUNCTYPE(c_void_p, c_ushort, c_ushort, c_ushort, c_ushort)
        # evDeath 
        elif self.event_index == 29:
            self.callbacks[29] = WINFUNCTYPE(c_void_p, c_bool)
        # evQuestArrow 
        elif self.event_index == 30:
            self.callbacks[30] = WINFUNCTYPE(c_void_p, c_ushort, c_ushort, c_bool)
        # evPartyInvite 
        elif self.event_index == 31:
            self.callbacks[31] = WINFUNCTYPE(c_void_p, c_uint)
        # evMapPin 
        elif self.event_index == 32:
            self.callbacks[32] = WINFUNCTYPE(c_void_p, c_uint, c_ubyte, c_ubyte, c_ushort, c_ushort)
        # evGumpTextEntry
        elif self.event_index == 33:
            self.callbacks[33] = WINFUNCTYPE(c_void_p, c_uint, c_wchar_p, c_ubyte, c_uint, c_wchar_p)
        # evGraphicalEffect
        elif self.event_index == 34:
            self.callbacks[34] = WINFUNCTYPE(c_void_p, c_uint, c_ushort, c_ushort, c_short, c_uint, c_ushort, c_ushort,
                                             c_short)
        # evIRCIncomingText
        elif self.event_index == 35:
            self.callbacks[35] = WINFUNCTYPE(c_void_p, c_wchar_p)
        # evSkypeEvent
        elif self.event_index == 36:
            self.callbacks[36] = WINFUNCTYPE(c_void_p, c_wchar_p, c_wchar_p, c_wchar_p, c_ubyte)
        # evSetGlobalVar
        elif self.event_index == 37:
            self.callbacks[37] = WINFUNCTYPE(c_void_p, c_wchar_p, c_wchar_p)
        # evUpdateObjStats
        elif self.event_index == 38:
            self.callbacks[38] = WINFUNCTYPE(c_void_p, c_uint, c_int, c_int, c_int, c_int, c_int, c_int)
        # undefined / not handled
        else:
            raise Exception("Event {} => {} not defined. Please check class eventProc.".format(self.event_index, (
                TPacketEvent[self.event_index] if TPacketEvent[self.event_index] else '')))

        self.funPTRs[self.event_index] = c_void_p()
        if func:
            self.funPTRs[self.event_index] = self.callbacks[self.event_index](func)

        stealth_dll.Script_SetEventProc(self.event, self.funPTRs[self.event_index])


# region pipe connection
stealth_dll.StartStealthSocketInstance.restype = c_void_p
stealth_dll.StartStealthSocketInstance.argtypes = [c_char_p]


def StartStealthSocketInstance(ExeFile):
    return stealth_dll.StartStealthSocketInstance(ExeFile)


def StartStealthPipeInstance(ExeFile):
    try:
        _StartStealthPipeInstance = stealth_dll.StartStealthPipeInstance
    except Exception as e:
        _StartStealthPipeInstance = StartStealthSocketInstance

    return _StartStealthPipeInstance(ExeFile)


stealth_dll.CorrectDisconnection.restype = c_void_p


def CorrectDisconnection():
    return stealth_dll.CorrectDisconnection()


# end region pipe connection

# region Ability
stealth_dll.Script_GetAbility.restype = c_wchar_p


def GetActiveAbility():
    return stealth_dll.Script_GetAbility()


stealth_dll.Script_ToggleFly.restype = c_void_p


def ToggleFly():
    return stealth_dll.Script_ToggleFly()


stealth_dll.Script_UsePrimaryAbility.restype = c_void_p


def UsePrimaryAbility():
    return stealth_dll.Script_UsePrimaryAbility()


stealth_dll.Script_UseSecondaryAbility.restype = c_void_p


def UseSecondaryAbility():
    return stealth_dll.Script_UseSecondaryAbility()


# end region Ability

# region Actions
stealth_dll.Script_Bow.restype = c_void_p


def Bow():
    return stealth_dll.Script_Bow()


stealth_dll.Script_OpenDoor.restype = c_void_p


def OpenDoor():
    return stealth_dll.Script_OpenDoor()


stealth_dll.Script_Salute.restype = c_void_p


def Salute():
    return stealth_dll.Script_Salute()


# end region Actions

# region AddToSystemJournal
stealth_dll.Script_AddToSystemJournal.argtypes = [c_wchar_p]
stealth_dll.Script_AddToSystemJournal.restype = c_void_p


def AddToSystemJournal(*args, **kargs):
    # default arguments
    sep = kargs.get('sep', ' ')
    end = kargs.get('end', '')
    file = kargs.get('file', False)

    Text = ''
    first = True

    max_lex = 30000

    for arg in args:
        Text += ('' if first else sep) + str(arg)
        Text = Text.strip('\r\n\t')
        first = False

    if not file:
        if len(Text) <= max_lex:
            return stealth_dll.Script_AddToSystemJournal(Text)
        else:
            stealth_dll.Script_AddToSystemJournal(
                '*********** WARNING YOU ARE TRYING TO PRINT SOMETHING LONG {} CHARACTERS, MAX LENGTH IS {}: TEXT IS GOING TO BE SPLITTED! ***********'.format(
                    len(Text), max_lex))
            for token in split_by_n(Text, max_lex):
                stealth_dll.Script_AddToSystemJournal(token)
                Wait(2000)
    else:
        Text += '\n'
        file.write(Text)

    return None


# end region AddToSystemJournal

# region Attack and WarMode
stealth_dll.Script_Attack.argtypes = [c_uint]
stealth_dll.Script_Attack.restype = c_void_p


def Attack(AttackedID):
    return stealth_dll.Script_Attack(AttackedID)


stealth_dll.Script_GetWarModeStatus.restype = c_bool


def WarMode():
    return stealth_dll.Script_GetWarModeStatus()


stealth_dll.Script_GetWarTarget.restype = c_uint


def WarTargetID():
    return stealth_dll.Script_GetWarTarget()


stealth_dll.Script_SetWarMode.argtypes = [c_bool]
stealth_dll.Script_SetWarMode.restype = c_void_p


def SetWarMode(Value):
    return stealth_dll.Script_SetWarMode(Value)


# end region Attack and WarMode

# region Auto Reconnector
stealth_dll.Script_GetARStatus.restype = c_bool


def GetARStatus():
    return stealth_dll.Script_GetARStatus()


stealth_dll.Script_SetARStatus.argtypes = [c_bool]
stealth_dll.Script_SetARStatus.restype = c_void_p


def SetARStatus(Value):
    return stealth_dll.Script_SetARStatus(Value)


# end region Auto Reconnector

# region Backpack ID
stealth_dll.Script_GetBackpackID.restype = c_uint


def Backpack():
    return stealth_dll.Script_GetBackpackID()


# end region Backpack ID

# region Cast Spell
stealth_dll.Script_CastSpell.argtypes = [c_wchar_p]
stealth_dll.Script_CastSpell.restype = c_bool


def Cast(SpellName):
    return stealth_dll.Script_CastSpell(SpellName)


stealth_dll.Script_CastSpellToObj.argtypes = [c_wchar_p, c_uint]
stealth_dll.Script_CastSpellToObj.restype = c_bool


def CastToObj(SpellName, ObjId):
    return stealth_dll.Script_CastSpellToObj(SpellName, ObjId)


stealth_dll.Script_IsActiveSpellAbility.argtypes = [c_wchar_p]
stealth_dll.Script_IsActiveSpellAbility.restype = c_bool


def IsActiveSpellAbility(SpellName):
    return stealth_dll.Script_IsActiveSpellAbility(SpellName)


# end region Cast Spell

# region ChangeSkillLockState
stealth_dll.Script_ChangeSkillLockState.argtypes = [c_wchar_p, c_ubyte]
stealth_dll.Script_ChangeSkillLockState.restype = c_void_p


def SkillLockState(SkillName, skillState):
    return stealth_dll.Script_ChangeSkillLockState(SkillName, skillState)


# end region ChangeSkillLockState

# region Char Name
stealth_dll.Script_GetCharName.restype = c_wchar_p


def CharName():
    return stealth_dll.Script_GetCharName()


# end region Char Name

# region Char Stats
stealth_dll.Script_GetExtInfo.restype = TExtendedInfo


def ExtendedInfo():
    return stealth_dll.Script_GetExtInfo()


stealth_dll.Script_GetSelfDex.restype = c_int


def Dex():
    return stealth_dll.Script_GetSelfDex()


stealth_dll.Script_GetSelfInt.restype = c_int


def Int():
    return stealth_dll.Script_GetSelfInt()


stealth_dll.Script_GetSelfLife.restype = c_int


def HP():
    return stealth_dll.Script_GetSelfLife()


def Life():
    return stealth_dll.Script_GetSelfLife()


stealth_dll.Script_GetSelfLuck.restype = c_int


def Luck():
    return stealth_dll.Script_GetSelfLuck()


stealth_dll.Script_GetSelfMana.restype = c_int


def Mana():
    return stealth_dll.Script_GetSelfMana()


stealth_dll.Script_GetSelfMaxLife.restype = c_int


def MaxHP():
    return stealth_dll.Script_GetSelfMaxLife()


def MaxLife():
    return stealth_dll.Script_GetSelfMaxLife()


stealth_dll.Script_GetSelfMaxMana.restype = c_int


def MaxMana():
    return stealth_dll.Script_GetSelfMaxMana()


stealth_dll.Script_GetSelfMaxStam.restype = c_int


def MaxStam():
    return stealth_dll.Script_GetSelfMaxStam()


stealth_dll.Script_GetSelfStam.restype = c_int


def Stam():
    return stealth_dll.Script_GetSelfStam()


stealth_dll.Script_GetSelfStr.restype = c_int


def Str():
    return stealth_dll.Script_GetSelfStr()


# end region Char Stats

# region ClickOnObject
stealth_dll.Script_ClickOnObject.argtypes = [c_uint]
stealth_dll.Script_ClickOnObject.restype = c_void_p


def ClickOnObject(ObjectID):
    return stealth_dll.Script_ClickOnObject(ObjectID)


# end region ClickOnObject

# region Client work
stealth_dll.Script_ClientPrint.argtypes = [c_wchar_p]
stealth_dll.Script_ClientPrint.restype = c_void_p


def ClientPrint(Text):
    return stealth_dll.Script_ClientPrint(Text)


stealth_dll.Script_ClientPrintEx.argtypes = [c_uint, c_ushort, c_ushort, c_wchar_p]
stealth_dll.Script_ClientPrintEx.restype = c_void_p


def ClientPrintEx(SenderID, Color, Font, Text):
    return stealth_dll.Script_ClientPrintEx(SenderID, Color, Font, Text)


stealth_dll.Script_ClientRequestObjectTarget.restype = c_void_p


def ClientRequestObjectTarget():
    return stealth_dll.Script_ClientRequestObjectTarget()


stealth_dll.Script_ClientRequestTileTarget.restype = c_void_p


def ClientRequestTileTarget():
    return stealth_dll.Script_ClientRequestTileTarget()


stealth_dll.Script_ClientTargetResponse.restype = TTargetInfo


def ClientTargetResponse():
    return stealth_dll.Script_ClientTargetResponse()


stealth_dll.Script_ClientTargetResponsePresent.restype = c_bool


def ClientTargetResponsePresent():
    return stealth_dll.Script_ClientTargetResponsePresent()


stealth_dll.Script_CloseClientUIWindow.argtypes = [c_ubyte, c_uint]
stealth_dll.Script_CloseClientUIWindow.restype = c_void_p


def CloseClientUIWindow(UIWindowType, ID):
    if UIWindowType not in [0, 'wtPaperdoll', 1, 'wtStatus', 2, 'wtCharProfile', 3, 'wtContainer']:
        raise ValueError('UIWindowType can only have one of this values {}'.format(
            [0, 'wtPaperdoll', 1, 'wtStatus', 2, 'wtCharProfile', 3, 'wtContainer']))

    if UIWindowType == 'wtPaperdoll':
        UIWindowType = 0
    elif UIWindowType == 'wtStatus':
        UIWindowType = 1
    elif UIWindowType == 'wtCharProfile':
        UIWindowType = 2
    elif UIWindowType == 'wtContainer':
        UIWindowType = 3

    return stealth_dll.Script_CloseClientUIWindow(UIWindowType, ID)


stealth_dll.Script_WaitForClientTargetResponse.argtypes = [c_int]
stealth_dll.Script_WaitForClientTargetResponse.restype = c_bool


def WaitForClientTargetResponse(MaxWaitTimeMS):
    return stealth_dll.Script_WaitForClientTargetResponse(MaxWaitTimeMS)


# end region Client work

# region Connect - Disconnect
stealth_dll.Script_Connect.restype = c_void_p


def Connect():
    return stealth_dll.Script_Connect()


stealth_dll.Script_Disconnect.restype = c_void_p


def Disconnect():
    return stealth_dll.Script_Disconnect()


# end region Connect - Disconnect

# region Connected
stealth_dll.Script_GetConnectedStatus.restype = c_bool


def Connected():
    return stealth_dll.Script_GetConnectedStatus()


# end region Connected

# region ContextMenus
stealth_dll.Script_ClearContextMenu.restype = c_void_p


def ClearContextMenu():
    return stealth_dll.Script_ClearContextMenu()


stealth_dll.Script_GetContextMenu.restype = c_wchar_p


def GetContextMenu():
    return stealth_dll.Script_GetContextMenu().splitlines()


stealth_dll.Script_RequestContextMenu.argtypes = [c_uint]
stealth_dll.Script_RequestContextMenu.restype = c_void_p


def RequestContextMenu(ID):
    return stealth_dll.Script_RequestContextMenu(ID)


stealth_dll.Script_SetContextMenuHook.argtypes = [c_uint, c_ubyte]
stealth_dll.Script_SetContextMenuHook.restype = c_void_p


def SetContextMenuHook(MenuID, EntryNumber):
    return stealth_dll.Script_SetContextMenuHook(MenuID, EntryNumber)


# end region ContextMenus

# region Count/CountGround
stealth_dll.Script_Count.argtypes = [c_ushort]
stealth_dll.Script_Count.restype = c_int


def Count(ObjType):
    return stealth_dll.Script_Count(ObjType)


stealth_dll.Script_CountEx.argtypes = [c_ushort, c_ushort, c_uint]
stealth_dll.Script_CountEx.restype = c_int


def CountEx(ObjType, Color, Container):
    return stealth_dll.Script_CountEx(ObjType, Color, Container)


stealth_dll.Script_CountGround.argtypes = [c_ushort]
stealth_dll.Script_CountGround.restype = c_int


def CountGround(ObjType):
    return stealth_dll.Script_CountGround(ObjType)


# end region Count/CountGround

# region Dead
stealth_dll.Script_GetDeadStatus.restype = c_bool


def Dead():
    return stealth_dll.Script_GetDeadStatus()


# end region Dead

# region EasyUO Working
stealth_dll.Script_EUO2StealthID.argtypes = [c_wchar_p]
stealth_dll.Script_EUO2StealthID.restype = c_uint


def EUO2ID(EUO):
    return stealth_dll.Script_EUO2StealthID(EUO)


stealth_dll.Script_EUO2StealthType.argtypes = [c_wchar_p]
stealth_dll.Script_EUO2StealthType.restype = c_ushort


def EUO2Type(EUO):
    return stealth_dll.Script_EUO2StealthType(EUO)


stealth_dll.Script_GetEasyUO.argtypes = [c_int]
stealth_dll.Script_GetEasyUO.restype = c_wchar_p


def GetEasyUO(num):
    return stealth_dll.Script_GetEasyUO(num)


stealth_dll.Script_SetEasyUO.argtypes = [c_int, c_wchar_p]
stealth_dll.Script_SetEasyUO.restype = c_void_p


def SetEasyUO(num, Regvalue):
    return stealth_dll.Script_SetEasyUO(num, Regvalue)


# end region EasyUO Working

# region Event Handling
# stealth_dll.Script_SetEventProc.argtypes = [c_ubyte, POINTER]
stealth_dll.Script_SetEventProc.restype = c_void_p


@eventProc
def SetEventProc(event, func=None):
    pass


# end region Event Handling

# region FillNewWindow
stealth_dll.Script_ClearInfoWindow.restype = c_void_p


def ClearInfoWindow():
    return stealth_dll.Script_ClearInfoWindow()


stealth_dll.Script_FillInfoWindow.argtypes = [c_wchar_p]
stealth_dll.Script_FillInfoWindow.restype = c_void_p


def FillInfoWindow(s):
    return stealth_dll.Script_FillInfoWindow(s)


stealth_dll.Script_GetSilentMode.restype = c_bool


def GetSilentMode():
    return stealth_dll.Script_GetSilentMode()


stealth_dll.Script_SetSilentMode.argtypes = [c_bool]
stealth_dll.Script_SetSilentMode.restype = c_void_p


def SetSilentMode(Value):
    return stealth_dll.Script_SetSilentMode(Value)


# end region FillNewWindow

# region GetSkillCap
stealth_dll.Script_GetSkillCap.argtypes = [c_wchar_p]
stealth_dll.Script_GetSkillCap.restype = c_double


def GetSkillCap(SkillName):
    return stealth_dll.Script_GetSkillCap(SkillName)


# end region GetSkillCap

# region GetSkillValue
stealth_dll.Script_GetSkillValue.argtypes = [c_wchar_p]
stealth_dll.Script_GetSkillValue.restype = c_double


def GetSkillValue(SkillName):
    return stealth_dll.Script_GetSkillValue(SkillName)


stealth_dll.Script_GetSkillCurrentValue.argtypes = [c_wchar_p]
stealth_dll.Script_GetSkillCurrentValue.restype = c_double


def GetCurrentSkillValue(SkillName):
    return stealth_dll.Script_GetSkillCurrentValue(SkillName)


# end region GetSkillValue

# region Ground ID
stealth_dll.Script_GetGroundID.restype = c_uint


def Ground():
    return stealth_dll.Script_GetGroundID()


# end region Ground ID

# region Gumps
stealth_dll.Script_AddGumpIgnoreByID.argtypes = [c_uint]
stealth_dll.Script_AddGumpIgnoreByID.restype = c_void_p


def AddGumpIgnoreByID(ID):
    return stealth_dll.Script_AddGumpIgnoreByID(ID)


stealth_dll.Script_AddGumpIgnoreBySerial.argtypes = [c_uint]
stealth_dll.Script_AddGumpIgnoreBySerial.restype = c_void_p


def AddGumpIgnoreBySerial(Serial):
    return stealth_dll.Script_AddGumpIgnoreBySerial(Serial)


stealth_dll.Script_ClearGumpsIgnore.restype = c_void_p


def ClearGumpsIgnore():
    return stealth_dll.Script_ClearGumpsIgnore()


stealth_dll.Script_CloseSimpleGump.argtypes = [c_ushort]
stealth_dll.Script_CloseSimpleGump.restype = c_void_p


def CloseSimpleGump(GumpIndex):
    return stealth_dll.Script_CloseSimpleGump(GumpIndex)


stealth_dll.Script_GetGumpButtonsDescription.argtypes = [c_ushort]
stealth_dll.Script_GetGumpButtonsDescription.restype = c_wchar_p


def GetGumpButtonsDescription(GumpIndex):
    return stealth_dll.Script_GetGumpButtonsDescription(GumpIndex).splitlines()


stealth_dll.Script_GetGumpFullLines.argtypes = [c_ushort]
stealth_dll.Script_GetGumpFullLines.restype = c_wchar_p


def GetGumpFullLines(GumpIndex):
    return stealth_dll.Script_GetGumpFullLines(GumpIndex).splitlines()


stealth_dll.Script_GetGumpID.argtypes = [c_ushort]
stealth_dll.Script_GetGumpID.restype = c_uint


def GetGumpID(GumpIndex):
    return stealth_dll.Script_GetGumpID(GumpIndex)


# stealth_dll.Script_GetGumpInfo.argtypes = [c_ushort, Pointer, c_uint]
stealth_dll.Script_GetGumpInfo.restype = c_void_p


def GetGumpInfo(GumpIndex):
    outLen = c_uint()
    stealth_dll.Script_GetGumpInfo(GumpIndex, None, byref(outLen))

    if outLen.value > 0:
        byte_array = (c_ubyte * (outLen.value))()
        stealth_dll.Script_GetGumpInfo(GumpIndex, byref(byte_array), byref(outLen))
        stream_position = 0

        Result = {}
        tmp = c_uint()

        # Serial : Cardinal
        memmove(addressof(tmp), addressof(byte_array), sizeof(c_uint))
        Result['Serial'] = tmp.value
        stream_position += sizeof(c_uint)

        # GumpID : Cardinal
        memmove(addressof(tmp), addressof(byte_array) + stream_position, sizeof(c_uint))
        Result['GumpID'] = tmp.value
        stream_position += sizeof(c_uint)

        # X : Word
        tmp = c_ushort()
        memmove(addressof(tmp), addressof(byte_array) + stream_position, sizeof(c_ushort))
        Result['X'] = tmp.value
        stream_position += sizeof(c_ushort)

        # Y : Word
        memmove(addressof(tmp), addressof(byte_array) + stream_position, sizeof(c_ushort))
        Result['Y'] = tmp.value
        stream_position += sizeof(c_ushort)

        # Pages : Word
        tmp = c_int()
        memmove(addressof(tmp), addressof(byte_array) + stream_position, sizeof(c_int))
        Result['Pages'] = tmp.value
        stream_position += sizeof(c_int)

        # NoMove : Boolean
        tmp = c_bool()
        memmove(addressof(tmp), addressof(byte_array) + stream_position, sizeof(c_bool))
        Result['NoMove'] = tmp.value
        stream_position += sizeof(c_bool)

        # NoResize : Boolean
        memmove(addressof(tmp), addressof(byte_array) + stream_position, sizeof(c_bool))
        Result['NoResize'] = tmp.value
        stream_position += sizeof(c_bool)

        # NoDispose : Boolean
        memmove(addressof(tmp), addressof(byte_array) + stream_position, sizeof(c_bool))
        Result['NoDispose'] = tmp.value
        stream_position += sizeof(c_bool)

        # NoClose : Boolean
        memmove(addressof(tmp), addressof(byte_array) + stream_position, sizeof(c_bool))
        Result['NoClose'] = tmp.value
        stream_position += sizeof(c_bool)

        # Groups Length
        tmp = c_ushort()
        memmove(addressof(tmp), addressof(byte_array) + stream_position, sizeof(c_ushort))
        stream_position += sizeof(c_ushort)
        # Groups : array of TGroup
        if tmp.value > 0:
            gump_elements = (TGroup * tmp.value)()
            memmove(addressof(gump_elements), addressof(byte_array) + stream_position, (sizeof(TGroup) * tmp.value))
            Result['Groups'] = [{'groupnumber': tgroup.groupnumber, 'Page': tgroup.Page, 'ElemNum': tgroup.ElemNum, }
                                for tgroup in gump_elements]
            stream_position += sizeof(TGroup) * tmp.value

        # EndGroups Length
        memmove(addressof(tmp), addressof(byte_array) + stream_position, sizeof(c_ushort))
        stream_position += sizeof(c_ushort)
        # EndGroups : array of TEndGroup
        if tmp.value > 0:
            gump_elements = (TEndGroup * tmp.value)()
            memmove(addressof(gump_elements), addressof(byte_array) + stream_position, (sizeof(TEndGroup) * tmp.value))
            Result['EndGroups'] = [
                {'groupnumber': tendgroup.groupnumber, 'Page': tendgroup.Page, 'ElemNum': tendgroup.ElemNum, } for
                tendgroup in gump_elements]
            stream_position += sizeof(TEndGroup) * tmp.value

        # GumpButtons Length
        memmove(addressof(tmp), addressof(byte_array) + stream_position, sizeof(c_ushort))
        stream_position += sizeof(c_ushort)
        # GumpButtons : array of TGumpButton
        if tmp.value > 0:
            gump_elements = (TGumpButton * tmp.value)()
            memmove(addressof(gump_elements), addressof(byte_array) + stream_position,
                    (sizeof(TGumpButton) * tmp.value))
            Result['GumpButtons'] = [
                {'x': gump_button.x, 'y': gump_button.y, 'released_id': gump_button.released_id,
                 'pressed_id': gump_button.pressed_id,
                 'quit': gump_button.quit, 'page_id': gump_button.page_id, 'return_value': gump_button.return_value,
                 'Page': gump_button.Page,
                 'ElemNum': gump_button.ElemNum, } for gump_button in gump_elements]
            stream_position += sizeof(TGumpButton) * tmp.value

        # ButtonTileArts Length
        memmove(addressof(tmp), addressof(byte_array) + stream_position, sizeof(c_ushort))
        stream_position += sizeof(c_ushort)
        # ButtonTileArts : array of TButtonTileArt
        if tmp.value > 0:
            gump_elements = (TButtonTileArt * tmp.value)()
            memmove(addressof(gump_elements), addressof(byte_array) + stream_position,
                    (sizeof(TButtonTileArt) * tmp.value))
            Result['ButtonTileArts'] = [
                {'x': tbuttontileart.x, 'y': tbuttontileart.y, 'released_id': tbuttontileart.released_id,
                 'pressed_id': tbuttontileart.pressed_id,
                 'quit': tbuttontileart.quit, 'page_id': tbuttontileart.page_id,
                 'return_value': tbuttontileart.return_value,
                 'art_id': tbuttontileart.art_id, 'Hue': tbuttontileart.Hue, 'art_x': tbuttontileart.art_x,
                 'art_y': tbuttontileart.art_y,
                 'ElemNum': tbuttontileart.ElemNum, } for tbuttontileart in gump_elements]
            stream_position += sizeof(TButtonTileArt) * tmp.value

        # CheckBoxes Length
        memmove(addressof(tmp), addressof(byte_array) + stream_position, sizeof(c_ushort))
        stream_position += sizeof(c_ushort)
        # CheckBoxes
        if tmp.value > 0:
            gump_elements = (TCheckBox * tmp.value)()
            memmove(addressof(gump_elements), addressof(byte_array) + stream_position, (sizeof(TCheckBox) * tmp.value))
            Result['CheckBoxes'] = [
                {'x': tcheckbox.x, 'y': tcheckbox.y, 'released_id': tcheckbox.released_id,
                 'pressed_id': tcheckbox.pressed_id,
                 'status': tcheckbox.status, 'return_value': tcheckbox.return_value, 'Page': tcheckbox.Page,
                 'ElemNum': tcheckbox.ElemNum, } for tcheckbox in gump_elements]
            stream_position += sizeof(TCheckBox) * tmp.value

        # CheckerTrans Length
        memmove(addressof(tmp), addressof(byte_array) + stream_position, sizeof(c_ushort))
        stream_position += sizeof(c_ushort)
        # CheckerTrans : array of TCheckerTrans
        if tmp.value > 0:
            gump_elements = (TCheckerTrans * tmp.value)()
            memmove(addressof(gump_elements), addressof(byte_array) + stream_position,
                    (sizeof(TCheckerTrans) * tmp.value))
            Result['CheckerTrans'] = [
                {'x': tcheckertrans.x, 'y': tcheckertrans.y, 'width': tcheckertrans.width,
                 'height': tcheckertrans.height,
                 'Page': tcheckertrans.Page, 'ElemNum': tcheckertrans.ElemNum, } for tcheckertrans in gump_elements]
            stream_position += sizeof(TCheckerTrans) * tmp.value

        # CroppedText Length
        memmove(addressof(tmp), addressof(byte_array) + stream_position, sizeof(c_ushort))
        stream_position += sizeof(c_ushort)
        # CroppedText : array of TCroppedText
        if tmp.value > 0:
            gump_elements = (TCroppedText * tmp.value)()
            memmove(addressof(gump_elements), addressof(byte_array) + stream_position,
                    (sizeof(TCroppedText) * tmp.value))
            Result['CroppedText'] = [
                {'x': tcroppedtext.x, 'y': tcroppedtext.y, 'width': tcroppedtext.width, 'height': tcroppedtext.height,
                 'color': tcroppedtext.color, 'text_id': tcroppedtext.text_id, 'Page': tcroppedtext.Page,
                 'ElemNum': tcroppedtext.ElemNum, } for tcroppedtext in gump_elements]
            stream_position += sizeof(TCroppedText) * tmp.value

        # GumpPics Length
        memmove(addressof(tmp), addressof(byte_array) + stream_position, sizeof(c_ushort))
        stream_position += sizeof(c_ushort)
        # GumpPics : array of TGumpPic
        if tmp.value > 0:
            gump_elements = (TGumpPic * tmp.value)()
            memmove(addressof(gump_elements), addressof(byte_array) + stream_position, (sizeof(TGumpPic) * tmp.value))
            Result['GumpPics'] = [
                {'x': tgumppic.x, 'y': tgumppic.y, 'id': tgumppic.id, 'Hue': tgumppic.Hue, 'Page': tgumppic.Page,
                 'ElemNum': tgumppic.ElemNum, } for tgumppic in gump_elements]
            stream_position += sizeof(TGumpPic) * tmp.value

        # GumpPicTiled Length
        memmove(addressof(tmp), addressof(byte_array) + stream_position, sizeof(c_ushort))
        stream_position += sizeof(c_ushort)
        # GumpPicTiled : array of TGumpPicTiled
        if tmp.value > 0:
            gump_elements = (TGumpPicTiled * tmp.value)()
            memmove(addressof(gump_elements), addressof(byte_array) + stream_position,
                    (sizeof(TGumpPicTiled) * tmp.value))
            Result['GumpPicTiled'] = [
                {'x': tgumppictiled.x, 'y': tgumppictiled.y, 'width': tgumppictiled.width,
                 'height': tgumppictiled.height,
                 'gump_id': tgumppictiled.gump_id, 'Page': tgumppictiled.Page, 'ElemNum': tgumppictiled.ElemNum, }
                for tgumppictiled in gump_elements]
            stream_position += sizeof(TGumpPicTiled) * tmp.value

        # RadioButtons Length
        memmove(addressof(tmp), addressof(byte_array) + stream_position, sizeof(c_ushort))
        stream_position += sizeof(c_ushort)
        # RadioButtons : array of TRadio
        if tmp.value > 0:
            gump_elements = (TRadio * tmp.value)()
            memmove(addressof(gump_elements), addressof(byte_array) + stream_position, (sizeof(TRadio) * tmp.value))
            Result['RadioButtons'] = [
                {'x': tradio.x, 'y': tradio.y, 'released_id': tradio.released_id,
                 'pressed_id': tradio.pressed_id, 'status': tradio.status, 'return_value': tradio.return_value,
                 'Page': tradio.Page, 'ElemNum': tradio.ElemNum, } for tradio in gump_elements]
            stream_position += sizeof(TRadio) * tmp.value

        # ResizePics Length
        memmove(addressof(tmp), addressof(byte_array) + stream_position, sizeof(c_ushort))
        stream_position += sizeof(c_ushort)
        # ResizePics : array of TResizePic
        if tmp.value > 0:
            gump_elements = (TResizePic * tmp.value)()
            memmove(addressof(gump_elements), addressof(byte_array) + stream_position, (sizeof(TResizePic) * tmp.value))
            Result['ResizePics'] = [
                {'x': tresizepic.x, 'y': tresizepic.y, 'gump_id': tresizepic.gump_id, 'width': tresizepic.width,
                 'height': tresizepic.height, 'Page': tresizepic.Page, 'ElemNum': tresizepic.ElemNum, } for tresizepic
                in gump_elements]
            stream_position += sizeof(TResizePic) * tmp.value

        # GumpText Length
        memmove(addressof(tmp), addressof(byte_array) + stream_position, sizeof(c_ushort))
        stream_position += sizeof(c_ushort)
        # GumpText : array of TGumpText
        if tmp.value > 0:
            gump_elements = (TGumpText * tmp.value)()
            memmove(addressof(gump_elements), addressof(byte_array) + stream_position, (sizeof(TGumpText) * tmp.value))
            Result['GumpText'] = [
                {'x': tgumptext.x, 'y': tgumptext.y, 'color': tgumptext.color, 'text_id': tgumptext.text_id,
                 'Page': tgumptext.Page, 'ElemNum': tgumptext.ElemNum, } for tgumptext in gump_elements]
            stream_position += sizeof(TGumpText) * tmp.value

        # TextEntries Length
        memmove(addressof(tmp), addressof(byte_array) + stream_position, sizeof(c_ushort))
        stream_position += sizeof(c_ushort)
        # TextEntries : array of TTextEntry
        if tmp.value > 0:
            gump_elements = (TTextEntry * tmp.value)()
            memmove(addressof(gump_elements), addressof(byte_array) + stream_position, (sizeof(TTextEntry) * tmp.value))
            Result['TextEntries'] = [
                {'x': ttextentry.x, 'y': ttextentry.y, 'width': ttextentry.width, 'height': ttextentry.height,
                 'color': ttextentry.color, 'return_value': ttextentry.return_value,
                 'default_text_id': ttextentry.default_text_id,
                 'Page': ttextentry.Page, 'ElemNum': ttextentry.ElemNum, } for ttextentry in gump_elements]
            stream_position += sizeof(TTextEntry) * tmp.value

        # Text Length
        memmove(addressof(tmp), addressof(byte_array) + stream_position, sizeof(c_ushort))
        stream_position += sizeof(c_ushort)
        # Text : array of String
        if tmp.value > 0:
            # print('Text : array of {} String'.format(tmp.value))
            Result['Text'] = []

            for i in range(0, tmp.value):
                tmp_str = stringFormMemory(addressof(byte_array) + stream_position)
                Result['Text'].append(tmp_str)
                stream_position += sizeof(c_uint) + (sizeof(c_wchar) * len(tmp_str))

        # TextEntriesLimited Length
        memmove(addressof(tmp), addressof(byte_array) + stream_position, sizeof(c_ushort))
        stream_position += sizeof(c_ushort)
        # TextEntriesLimited : array of TTextEntryLimited
        if tmp.value > 0:
            # print('TextEntriesLimited : array of {} TTextEntryLimited'.format(tmp.value))
            gump_elements = (TTextEntryLimited * tmp.value)()
            memmove(addressof(gump_elements), addressof(byte_array) + stream_position,
                    (sizeof(TTextEntryLimited) * tmp.value))
            Result['TextEntriesLimited'] = [
                {'x': ttextentrylimited.x, 'y': ttextentrylimited.y, 'width': ttextentrylimited.width,
                 'height': ttextentrylimited.height,
                 'color': ttextentrylimited.color, 'return_value': ttextentrylimited.return_value,
                 'default_text_id': ttextentrylimited.default_text_id, 'Limit': ttextentrylimited.Limit,
                 'Page': ttextentrylimited.Page,
                 'ElemNum': ttextentrylimited.ElemNum, } for ttextentrylimited in gump_elements]
            stream_position += sizeof(TTextEntryLimited) * tmp.value

        # TilePics Length
        memmove(addressof(tmp), addressof(byte_array) + stream_position, sizeof(c_ushort))
        stream_position += sizeof(c_ushort)
        # TilePics : array of TTilePic
        if tmp.value > 0:
            # print('TilePics : array of {} TTilePic'.format(tmp.value))
            gump_elements = (TTilePic * tmp.value)()
            memmove(addressof(gump_elements), addressof(byte_array) + stream_position, (sizeof(TTilePic) * tmp.value))
            Result['TilePics'] = [
                {'x': ttilepic.x, 'y': ttilepic.y, 'id': ttilepic.id, 'Page': ttilepic.Page,
                 'ElemNum': ttilepic.ElemNum, } for ttilepic in gump_elements]
            stream_position += sizeof(TTilePic) * tmp.value

        # TilePicHue Length
        memmove(addressof(tmp), addressof(byte_array) + stream_position, sizeof(c_ushort))
        stream_position += sizeof(c_ushort)
        # TilePicHue : array of TTilePichue
        if tmp.value > 0:
            # print('TilePicHue : array of {} TTilePichue'.format(tmp.value))
            gump_elements = (TTilePichue * tmp.value)()
            memmove(addressof(gump_elements), addressof(byte_array) + stream_position,
                    (sizeof(TTilePichue) * tmp.value))
            Result['TilePicHue'] = [
                {'x': ttilepichue.x, 'y': ttilepichue.y, 'id': ttilepichue.id, 'color': ttilepichue.color,
                 'Page': ttilepichue.Page, 'ElemNum': ttilepichue.ElemNum, } for ttilepichue in gump_elements]
            stream_position += sizeof(TTilePichue) * tmp.value

        # Tooltips Length
        memmove(addressof(tmp), addressof(byte_array) + stream_position, sizeof(c_ushort))
        stream_position += sizeof(c_ushort)
        # Tooltips : array of TTooltip
        if tmp.value > 0:
            # print('Tooltips : array of {} TTooltip'.format(tmp.value))
            gump_elements = (TTooltip * tmp.value)()
            memmove(addressof(gump_elements), addressof(byte_array) + stream_position, (sizeof(TTooltip) * tmp.value))
            Result['Tooltips'] = [
                {'Cliloc_ID': ttooltip.Cliloc_ID, 'Page': ttooltip.Page, 'ElemNum': ttooltip.ElemNum, } for ttooltip in
                gump_elements]
            stream_position += sizeof(TTooltip) * tmp.value

        # HtmlGump Length
        memmove(addressof(tmp), addressof(byte_array) + stream_position, sizeof(c_ushort))
        stream_position += sizeof(c_ushort)
        # HtmlGump : array of THtmlGump
        if tmp.value > 0:
            # print('HtmlGump : array of {} THtmlGump'.format(tmp.value))
            gump_elements = (THtmlGump * tmp.value)()
            memmove(addressof(gump_elements), addressof(byte_array) + stream_position, (sizeof(THtmlGump) * tmp.value))
            Result['HtmlGump'] = [
                {'x': thtmlgump.x, 'y': thtmlgump.y, 'width': thtmlgump.width, 'height': thtmlgump.height,
                 'text_id': thtmlgump.text_id, 'background': thtmlgump.background, 'scrollbar': thtmlgump.scrollbar,
                 'Page': thtmlgump.Page, 'ElemNum': thtmlgump.ElemNum, } for thtmlgump in gump_elements]
            stream_position += sizeof(THtmlGump) * tmp.value

        # XmfHtmlGump Length
        memmove(addressof(tmp), addressof(byte_array) + stream_position, sizeof(c_ushort))
        stream_position += sizeof(c_ushort)
        # XmfHtmlGump : array of TXmfHtmlGump
        if tmp.value > 0:
            # print('XmfHtmlGump : array of {} TXmfHtmlGump'.format(tmp.value))
            gump_elements = (TXmfHTMLGump * tmp.value)()
            memmove(addressof(gump_elements), addressof(byte_array) + stream_position,
                    (sizeof(TXmfHTMLGump) * tmp.value))
            Result['XmfHtmlGump'] = [
                {'x': txmfhtmlgump.x, 'y': txmfhtmlgump.y, 'width': txmfhtmlgump.width, 'height': txmfhtmlgump.height,
                 'Cliloc_id': txmfhtmlgump.Cliloc_id, 'background': txmfhtmlgump.background,
                 'scrollbar': txmfhtmlgump.scrollbar,
                 'Page': txmfhtmlgump.Page, 'ElemNum': txmfhtmlgump.ElemNum, } for txmfhtmlgump in gump_elements]
            stream_position += sizeof(TXmfHTMLGump) * tmp.value

        # XmfHTMLGumpColor Length
        memmove(addressof(tmp), addressof(byte_array) + stream_position, sizeof(c_ushort))
        stream_position += sizeof(c_ushort)
        # XmfHTMLGumpColor : array of TXmfHTMLGumpColor
        if tmp.value > 0:
            gump_elements = (TXmfHTMLGumpColor * tmp.value)()
            memmove(addressof(gump_elements), addressof(byte_array) + stream_position,
                    (sizeof(TXmfHTMLGumpColor) * tmp.value))
            Result['XmfHTMLGumpColor'] = [
                {'x': txmfhtmlgumpcolor.x, 'y': txmfhtmlgumpcolor.y, 'width': txmfhtmlgumpcolor.width,
                 'height': txmfhtmlgumpcolor.height, 'Cliloc_id': txmfhtmlgumpcolor.Cliloc_id,
                 'background': txmfhtmlgumpcolor.background,
                 'scrollbar': txmfhtmlgumpcolor.scrollbar, 'Hue': txmfhtmlgumpcolor.Hue, 'Page': txmfhtmlgumpcolor.Page,
                 'ElemNum': txmfhtmlgumpcolor.ElemNum, } for txmfhtmlgumpcolor in gump_elements]
            stream_position += sizeof(TXmfHTMLGumpColor) * tmp.value

        # XmfHTMLTok Length
        memmove(addressof(tmp), addressof(byte_array) + stream_position, sizeof(c_ushort))
        stream_position += sizeof(c_ushort)
        # XmfHTMLTok : array of TXmfHTMLTok
        if tmp.value > 0:
            Result['XmfHTMLTok'] = []
            for i in range(0, tmp.value):
                txmfhtmltok = TXmfHTMLTok()

                # x : Integer
                # memmove(addressof(txmfhtmltok.x),  addressof(byte_array) + stream_position, sizeof(c_int))
                # stream_position += sizeof(c_int)

                tmp = c_int()
                memmove(addressof(tmp), addressof(byte_array) + stream_position, sizeof(c_int))
                txmfhtmltok.x = tmp.value
                stream_position += sizeof(c_int)

                # y : Integer
                # memmove(addressof(txmfhtmltok.y),  addressof(byte_array) + stream_position, sizeof(c_int))
                # stream_position += sizeof(c_int)

                tmp = c_int()
                memmove(addressof(tmp), addressof(byte_array) + stream_position, sizeof(c_int))
                txmfhtmltok.y = tmp.value
                stream_position += sizeof(c_int)

                # width : Integer
                # memmove(addressof(txmfhtmltok.width),  addressof(byte_array) + stream_position, sizeof(c_int))
                # stream_position += sizeof(c_int)

                tmp = c_int()
                memmove(addressof(tmp), addressof(byte_array) + stream_position, sizeof(c_int))
                txmfhtmltok.width = tmp.value
                stream_position += sizeof(c_int)

                # height : Integer
                # memmove(addressof(txmfhtmltok.height),  addressof(byte_array) + stream_position, sizeof(c_int))
                # stream_position += sizeof(c_int)

                tmp = c_int()
                memmove(addressof(tmp), addressof(byte_array) + stream_position, sizeof(c_int))
                txmfhtmltok.height = tmp.value
                stream_position += sizeof(c_int)

                # background : Integer
                # memmove(addressof(txmfhtmltok.background),  addressof(byte_array) + stream_position, sizeof(c_int))
                # stream_position += sizeof(c_int)

                tmp = c_int()
                memmove(addressof(tmp), addressof(byte_array) + stream_position, sizeof(c_int))
                txmfhtmltok.background = tmp.value
                stream_position += sizeof(c_int)

                # scrollbar : Integer
                # memmove(addressof(txmfhtmltok.scrollbar),  addressof(byte_array) + stream_position, sizeof(c_int))
                # stream_position += sizeof(c_int)

                tmp = c_int()
                memmove(addressof(tmp), addressof(byte_array) + stream_position, sizeof(c_int))
                txmfhtmltok.scrollbar = tmp.value
                stream_position += sizeof(c_int)

                # Color : Integer
                # memmove(addressof(txmfhtmltok.Color),  addressof(byte_array) + stream_position, sizeof(c_int))
                # stream_position += sizeof(c_int)

                tmp = c_int()
                memmove(addressof(tmp), addressof(byte_array) + stream_position, sizeof(c_int))
                txmfhtmltok.Color = tmp.value
                stream_position += sizeof(c_int)

                # Cliloc_id : Cardinal
                # memmove(addressof(txmfhtmltok.Cliloc_id),  addressof(byte_array) + stream_position, sizeof(c_uint))
                # stream_position += sizeof(c_uint)

                tmp = c_int()
                memmove(addressof(tmp), addressof(byte_array) + stream_position, sizeof(c_int))
                txmfhtmltok.Cliloc_id = tmp.value
                stream_position += sizeof(c_int)

                # Arguments : TPCharStr
                tmp_str = stringFormMemory(addressof(byte_array) + stream_position)
                stream_position += sizeof(c_uint) + (sizeof(c_wchar) * len(tmp_str))
                txmfhtmltok.Arguments = c_wchar_p(tmp_str)

                # Page : Integer
                # memmove(addressof(txmfhtmltok.Page),  addressof(byte_array) + stream_position, sizeof(c_int))
                # stream_position += sizeof(c_int)

                tmp = c_int()
                memmove(addressof(tmp), addressof(byte_array) + stream_position, sizeof(c_int))
                txmfhtmltok.Page = tmp.value
                stream_position += sizeof(c_int)

                # ElemNum : Integer
                # memmove(addressof(txmfhtmltok.ElemNum),  addressof(byte_array) + stream_position, sizeof(c_int))
                # stream_position += sizeof(c_int)

                tmp = c_int()
                memmove(addressof(tmp), addressof(byte_array) + stream_position, sizeof(c_int))
                txmfhtmltok.ElemNum = tmp.value
                stream_position += sizeof(c_int)

                Result['XmfHTMLTok'].append(
                    {'x': txmfhtmltok.x, 'y': txmfhtmltok.y, 'width': txmfhtmltok.width, 'height': txmfhtmltok.height,
                     'background': txmfhtmltok.background, 'scrollbar': txmfhtmltok.scrollbar,
                     'Color': txmfhtmltok.Color,
                     'Cliloc_id': txmfhtmltok.Cliloc_id, 'Arguments': txmfhtmltok.Arguments, 'Page': txmfhtmltok.Page,
                     'ElemNum': txmfhtmltok.ElemNum, }
                )

        # ItemProperties Length
        memmove(addressof(tmp), addressof(byte_array) + stream_position, sizeof(c_ushort))
        stream_position += sizeof(c_ushort)
        # ItemProperties : array of TItemProperty
        if tmp.value > 0:
            gump_elements = (TItemProperty * tmp.value)()
            memmove(addressof(gump_elements), addressof(byte_array) + stream_position,
                    (sizeof(TItemProperty) * tmp.value))
            Result['ItemProperties'] = [{'Prop': titemproperty.Prop, 'ElemNum': titemproperty.ElemNum, } for
                                        titemproperty in gump_elements]

        # print(Result)
        return Result


stealth_dll.Script_GetGumpNoClose.argtypes = [c_ushort]
stealth_dll.Script_GetGumpNoClose.restype = c_bool


def IsGumpCanBeClosed(GumpIndex):
    return stealth_dll.Script_GetGumpNoClose(GumpIndex)


stealth_dll.Script_GetGumpSerial.argtypes = [c_ushort]
stealth_dll.Script_GetGumpSerial.restype = c_uint


def GetGumpSerial(GumpIndex):
    return stealth_dll.Script_GetGumpSerial(GumpIndex)


stealth_dll.Script_GetGumpShortLines.argtypes = [c_ushort]
stealth_dll.Script_GetGumpShortLines.restype = c_wchar_p


def GetGumpShortLines(GumpIndex):
    return stealth_dll.Script_GetGumpShortLines(GumpIndex).splitlines()


stealth_dll.Script_GetGumpTextLines.argtypes = [c_ushort]
stealth_dll.Script_GetGumpTextLines.restype = c_wchar_p


def GetGumpTextLines(GumpIndex):
    return stealth_dll.Script_GetGumpTextLines(GumpIndex).splitlines()


stealth_dll.Script_GetGumpsCount.restype = c_int


def GetGumpsCount():
    return stealth_dll.Script_GetGumpsCount()


stealth_dll.Script_GumpAutoCheckBox.argtypes = [c_int, c_int]
stealth_dll.Script_GumpAutoCheckBox.restype = c_void_p


def GumpAutoCheckBox(CBID, Value):
    return stealth_dll.Script_GumpAutoCheckBox(CBID, Value)


stealth_dll.Script_GumpAutoRadiobutton.argtypes = [c_int, c_int]
stealth_dll.Script_GumpAutoRadiobutton.restype = c_void_p


def GumpAutoRadiobutton(RadiobuttonID, Value):
    return stealth_dll.Script_GumpAutoRadiobutton(RadiobuttonID, Value)


stealth_dll.Script_GumpAutoTextEntry.argtypes = [c_int, c_wchar_p]
stealth_dll.Script_GumpAutoTextEntry.restype = c_void_p


def GumpAutoTextEntry(TextEntryID, Value):
    return stealth_dll.Script_GumpAutoTextEntry(TextEntryID, Value)


stealth_dll.Script_IsGump.restype = c_bool


def IsGump():
    return stealth_dll.Script_IsGump()


stealth_dll.Script_NumGumpButton.argtypes = [c_ushort, c_int]
stealth_dll.Script_NumGumpButton.restype = c_bool


def NumGumpButton(GumpIndex, Value):
    return stealth_dll.Script_NumGumpButton(GumpIndex, Value)


stealth_dll.Script_NumGumpCheckBox.argtypes = [c_ushort, c_int, c_int]
stealth_dll.Script_NumGumpCheckBox.restype = c_bool


def NumGumpCheckBox(GumpIndex, CBID, Value):
    return stealth_dll.Script_NumGumpCheckBox(GumpIndex, CBID, Value)


stealth_dll.Script_NumGumpRadiobutton.argtypes = [c_ushort, c_int, c_int]
stealth_dll.Script_NumGumpRadiobutton.restype = c_bool


def NumGumpRadiobutton(GumpIndex, RadiobuttonID, Value):
    return stealth_dll.Script_NumGumpRadiobutton(GumpIndex, RadiobuttonID, Value)


stealth_dll.Script_NumGumpTextEntry.argtypes = [c_ushort, c_int, c_wchar_p]
stealth_dll.Script_NumGumpTextEntry.restype = c_bool


def NumGumpTextEntry(GumpIndex, TextEntryID, Value):
    return stealth_dll.Script_NumGumpTextEntry(GumpIndex, TextEntryID, Value)


stealth_dll.Script_WaitGump.argtypes = [c_wchar_p]
stealth_dll.Script_WaitGump.restype = c_void_p


def WaitGump(Value):
    return stealth_dll.Script_WaitGump(Value)


stealth_dll.Script_WaitGumpTextEntry.argtypes = [c_wchar_p]
stealth_dll.Script_WaitGumpTextEntry.restype = c_void_p


def WaitTextEntry(Value):
    return stealth_dll.Script_WaitGumpTextEntry(Value)


# end region Gumps

# region Hidden
stealth_dll.Script_GetHiddenStatus.restype = c_bool


def Hidden():
    return stealth_dll.Script_GetHiddenStatus()


# end region Hidden

# region HttpWorking
stealth_dll.Script_HTTP_Body.restype = c_wchar_p


def HTTP_Body():
    return stealth_dll.Script_HTTP_Body()


stealth_dll.Script_HTTP_Get.argtypes = [c_wchar_p]
stealth_dll.Script_HTTP_Get.restype = c_void_p


def HTTP_Get(URL):
    return stealth_dll.Script_HTTP_Get(URL)


stealth_dll.Script_HTTP_Header.restype = c_wchar_p


def HTTP_Header():
    return stealth_dll.Script_HTTP_Header()


stealth_dll.Script_HTTP_Post.argtypes = [c_wchar_p, c_wchar_p]
stealth_dll.Script_HTTP_Post.restype = c_wchar_p


def HTTP_Post(URL, PostData):
    return stealth_dll.Script_HTTP_Post(URL, PostData)


# end region HttpWorking

# region ICQ
stealth_dll.Script_ICQ_Connect.argtypes = [c_uint, c_wchar_p]
stealth_dll.Script_ICQ_Connect.restype = c_void_p


def ICQConnect(UIN, Password):
    return stealth_dll.Script_ICQ_Connect(UIN, Password)


stealth_dll.Script_ICQ_Disconnect.restype = c_void_p


def ICQDisconnect():
    return stealth_dll.Script_ICQ_Disconnect()


stealth_dll.Script_ICQ_GetConnectedStatus.restype = c_bool


def ICQConnected():
    return stealth_dll.Script_ICQ_GetConnectedStatus()


stealth_dll.Script_ICQ_SendText.argtypes = [c_uint, c_wchar_p]
stealth_dll.Script_ICQ_SendText.restype = c_void_p


def ICQSendText(DestinationUIN, Text):
    return stealth_dll.Script_ICQ_SendText(DestinationUIN, Text)


stealth_dll.Script_ICQ_SetStatus.argtypes = [c_ubyte]
stealth_dll.Script_ICQ_SetStatus.restype = c_void_p


def ICQSetStatus(Num):
    return stealth_dll.Script_ICQ_SetStatus(Num)


stealth_dll.Script_ICQ_SetXStatus.argtypes = [c_ubyte]
stealth_dll.Script_ICQ_SetXStatus.restype = c_void_p


def ICQSetXStatus(Num):
    return stealth_dll.Script_ICQ_SetXStatus(Num)


# end region ICQ

# region Journal
stealth_dll.Script_AddChatUserIgnore.argtypes = [c_wchar_p]
stealth_dll.Script_AddChatUserIgnore.restype = c_void_p


def AddChatUserIgnore(User):
    return stealth_dll.Script_AddChatUserIgnore(User)


stealth_dll.Script_AddJournalIgnore.argtypes = [c_wchar_p]
stealth_dll.Script_AddJournalIgnore.restype = c_void_p


def AddJournalIgnore(Str):
    return stealth_dll.Script_AddJournalIgnore(Str)


stealth_dll.Script_AddToJournal.argtypes = [c_wchar_p]
stealth_dll.Script_AddToJournal.restype = c_void_p


def AddToJournal(Msg):
    return stealth_dll.Script_AddToJournal(Msg)


stealth_dll.Script_ClearChatUserIgnore.restype = c_void_p


def ClearChatUserIgnore():
    return stealth_dll.Script_ClearChatUserIgnore()


stealth_dll.Script_ClearJournal.restype = c_void_p


def ClearJournal():
    return stealth_dll.Script_ClearJournal()


stealth_dll.Script_ClearJournalIgnore.restype = c_void_p


def ClearJournalIgnore():
    return stealth_dll.Script_ClearJournalIgnore()


stealth_dll.Script_ClearSystemJournal.restype = c_void_p


def ClearSystemJournal():
    return stealth_dll.Script_ClearSystemJournal()


stealth_dll.Script_HighJournal.restype = c_int


def HighJournal():
    return stealth_dll.Script_HighJournal()


stealth_dll.Script_InJournal.argtypes = [c_wchar_p]
stealth_dll.Script_InJournal.restype = c_int


def InJournal(Str):
    return stealth_dll.Script_InJournal(Str)


stealth_dll.Script_InJournalBetweenTimes.argtypes = [c_wchar_p, c_double, c_double]
stealth_dll.Script_InJournalBetweenTimes.restype = c_int


def InJournalBetweenTimes(Str, TimeBegin, TimeEnd):
    return stealth_dll.Script_InJournalBetweenTimes(Str, PyDateTimeTOTDateTime(TimeBegin),
                                                    PyDateTimeTOTDateTime(TimeEnd))


stealth_dll.Script_Journal.argtypes = [c_uint]
stealth_dll.Script_Journal.restype = c_wchar_p


def Journal(StringIndex):
    return stealth_dll.Script_Journal(StringIndex)


stealth_dll.Script_LastJournalMessage.restype = c_wchar_p


def LastJournalMessage():
    return stealth_dll.Script_LastJournalMessage()


stealth_dll.Script_LowJournal.restype = c_int


def LowJournal():
    return stealth_dll.Script_LowJournal()


stealth_dll.Script_SetJournalLine.argtypes = [c_uint, c_wchar_p]
stealth_dll.Script_SetJournalLine.restype = c_void_p


def SetJournalLine(StringIndex, Text):
    return stealth_dll.Script_SetJournalLine(StringIndex, Text)


stealth_dll.Script_WaitJournalLine.argtypes = [c_double, c_wchar_p, c_int]
stealth_dll.Script_WaitJournalLine.restype = c_bool


def WaitJournalLine(StartTime, Str, MaxWaitTimeMS):
    return stealth_dll.Script_WaitJournalLine(PyDateTimeTOTDateTime(StartTime), Str, MaxWaitTimeMS)


stealth_dll.Script_WaitJournalLineSystem.argtypes = [c_double, c_wchar_p, c_int]
stealth_dll.Script_WaitJournalLineSystem.restype = c_bool


def WaitJournalLineSystem(StartTime, Str, MaxWaitTimeMS):
    return stealth_dll.Script_WaitJournalLineSystem(PyDateTimeTOTDateTime(StartTime), Str, MaxWaitTimeMS)


# end region Journal

# region Layer dress/undress
stealth_dll.Script_GetDressSpeed.restype = c_ushort


def GetDressSpeed():
    return stealth_dll.Script_GetDressSpeed()


stealth_dll.Script_SetDress.restype = c_void_p


def SetDress():
    return stealth_dll.Script_SetDress()


stealth_dll.Script_SetDressSpeed.argtypes = [c_ushort]
stealth_dll.Script_SetDressSpeed.restype = c_void_p


def SetDressSpeed(Value):
    return stealth_dll.Script_SetDressSpeed(Value)


stealth_dll.Script_Undress.restype = c_bool


def UnDress():
    return stealth_dll.Script_Undress()


stealth_dll.Script_disarm.restype = c_bool


def Disarm():
    return stealth_dll.Script_disarm()


stealth_dll.Script_equip.argtypes = [c_ubyte, c_uint]
stealth_dll.Script_equip.restype = c_bool


def Equip(Layer, Obj):
    return stealth_dll.Script_equip(Layer, Obj)


stealth_dll.Script_equipt.argtypes = [c_ubyte, c_ushort]
stealth_dll.Script_equipt.restype = c_bool


def Equipt(Layer, ObjType):
    return stealth_dll.Script_equipt(Layer, ObjType)


stealth_dll.Script_unequip.argtypes = [c_ubyte]
stealth_dll.Script_unequip.restype = c_bool


def Unequip(Layer):
    return stealth_dll.Script_unequip(Layer)


stealth_dll.Script_EquipDressSet.restype = c_bool


def DressSavedSet():
    return stealth_dll.Script_EquipDressSet()


# end region Layer dress/undress

# region LayerInfo
stealth_dll.Script_GetLayer.argtypes = [c_uint]
stealth_dll.Script_GetLayer.restype = c_ubyte


def GetLayer(Obj):
    return stealth_dll.Script_GetLayer(Obj)


stealth_dll.Script_ObjAtLayer.argtypes = [c_ubyte]
stealth_dll.Script_ObjAtLayer.restype = c_uint


def ObjAtLayer(LayerType):
    return stealth_dll.Script_ObjAtLayer(LayerType)


stealth_dll.Script_ObjAtLayerEx.argtypes = [c_ubyte, c_uint]
stealth_dll.Script_ObjAtLayerEx.restype = c_uint


def ObjAtLayerEx(LayerType, PlayerID):
    return stealth_dll.Script_ObjAtLayerEx(LayerType, PlayerID)


# end region LayerInfo

# region Layers Names
stealth_dll.Script_GetArmsLayer.restype = c_ubyte


def ArmsLayer():
    return stealth_dll.Script_GetArmsLayer()


stealth_dll.Script_GetBankLayer.restype = c_ubyte


def BankLayer():
    return stealth_dll.Script_GetBankLayer()


stealth_dll.Script_GetBeardLayer.restype = c_ubyte


def BeardLayer():
    return stealth_dll.Script_GetBeardLayer()


stealth_dll.Script_GetBpackLayer.restype = c_ubyte


def BpackLayer():
    return stealth_dll.Script_GetBpackLayer()


stealth_dll.Script_GetBraceLayer.restype = c_ubyte


def BraceLayer():
    return stealth_dll.Script_GetBraceLayer()


stealth_dll.Script_GetCloakLayer.restype = c_ubyte


def CloakLayer():
    return stealth_dll.Script_GetCloakLayer()


stealth_dll.Script_GetEarLayer.restype = c_ubyte


def EarLayer():
    return stealth_dll.Script_GetEarLayer()


stealth_dll.Script_GetEggsLayer.restype = c_ubyte


def EggsLayer():
    return stealth_dll.Script_GetEggsLayer()


stealth_dll.Script_GetGlovesLayer.restype = c_ubyte


def GlovesLayer():
    return stealth_dll.Script_GetGlovesLayer()


stealth_dll.Script_GetHairLayer.restype = c_ubyte


def HairLayer():
    return stealth_dll.Script_GetHairLayer()


stealth_dll.Script_GetHatLayer.restype = c_ubyte


def HatLayer():
    return stealth_dll.Script_GetHatLayer()


stealth_dll.Script_GetHorseLayer.restype = c_ubyte


def HorseLayer():
    return stealth_dll.Script_GetHorseLayer()


stealth_dll.Script_GetLegsLayer.restype = c_ubyte


def LegsLayer():
    return stealth_dll.Script_GetLegsLayer()


stealth_dll.Script_GetLhandLayer.restype = c_ubyte


def LhandLayer():
    return stealth_dll.Script_GetLhandLayer()


stealth_dll.Script_GetNRstkLayer.restype = c_ubyte


def NRstkLayer():
    return stealth_dll.Script_GetNRstkLayer()


stealth_dll.Script_GetNeckLayer.restype = c_ubyte


def NeckLayer():
    return stealth_dll.Script_GetNeckLayer()


stealth_dll.Script_GetPantsLayer.restype = c_ubyte


def PantsLayer():
    return stealth_dll.Script_GetPantsLayer()


stealth_dll.Script_GetRhandLayer.restype = c_ubyte


def RhandLayer():
    return stealth_dll.Script_GetRhandLayer()


stealth_dll.Script_GetRingLayer.restype = c_ubyte


def RingLayer():
    return stealth_dll.Script_GetRingLayer()


stealth_dll.Script_GetRobeLayer.restype = c_ubyte


def RobeLayer():
    return stealth_dll.Script_GetRobeLayer()


stealth_dll.Script_GetRstkLayer.restype = c_ubyte


def RstkLayer():
    return stealth_dll.Script_GetRstkLayer()


stealth_dll.Script_GetSellLayer.restype = c_ubyte


def SellLayer():
    return stealth_dll.Script_GetSellLayer()


stealth_dll.Script_GetShirtLayer.restype = c_ubyte


def ShirtLayer():
    return stealth_dll.Script_GetShirtLayer()


stealth_dll.Script_GetShoesLayer.restype = c_ubyte


def ShoesLayer():
    return stealth_dll.Script_GetShoesLayer()


stealth_dll.Script_GetTalismanLayer.restype = c_ubyte


def TalismanLayer():
    return stealth_dll.Script_GetTalismanLayer()


stealth_dll.Script_GetTorsoHLayer.restype = c_ubyte


def TorsoHLayer():
    return stealth_dll.Script_GetTorsoHLayer()


stealth_dll.Script_GetTorsoLayer.restype = c_ubyte


def TorsoLayer():
    return stealth_dll.Script_GetTorsoLayer()


stealth_dll.Script_GetWaistLayer.restype = c_ubyte


def WaistLayer():
    return stealth_dll.Script_GetWaistLayer()


# end region Layers Names

# region Line Fields
stealth_dll.Script_GetFoundedParamID.restype = c_int


def FoundedParamID():
    return stealth_dll.Script_GetFoundedParamID()


stealth_dll.Script_GetLineCount.restype = c_int


def LineCount():
    return stealth_dll.Script_GetLineCount()


stealth_dll.Script_GetLineID.restype = c_uint


def LineID():
    return stealth_dll.Script_GetLineID()


stealth_dll.Script_GetLineIndex.restype = c_int


def LineIndex():
    return stealth_dll.Script_GetLineIndex()


stealth_dll.Script_GetLineMsgType.restype = c_ubyte


def LineMsgType():
    return stealth_dll.Script_GetLineMsgType()


stealth_dll.Script_GetLineName.restype = c_wchar_p


def LineName():
    return stealth_dll.Script_GetLineName()


stealth_dll.Script_GetLineTextColor.restype = c_ushort


def LineTextColor():
    return stealth_dll.Script_GetLineTextColor()


stealth_dll.Script_GetLineTextFont.restype = c_ushort


def LineTextFont():
    return stealth_dll.Script_GetLineTextFont()


stealth_dll.Script_GetLineTime.restype = c_double


def LineTime():
    return TDateTimeToPyDateTime(stealth_dll.Script_GetLineTime())


stealth_dll.Script_GetLineType.restype = c_ushort


def LineType():
    return stealth_dll.Script_GetLineType()


# end region Line Fields

# region Menus
stealth_dll.Script_AutoMenu.argtypes = [c_wchar_p, c_wchar_p]
stealth_dll.Script_AutoMenu.restype = c_void_p


def AutoMenu(MenuCaption, ElementCaption):
    return stealth_dll.Script_AutoMenu(MenuCaption, ElementCaption)


stealth_dll.Script_CancelMenu.restype = c_void_p


def CancelMenu():
    return stealth_dll.Script_CancelMenu()


stealth_dll.Script_CloseMenu.restype = c_void_p


def CloseMenu():
    return stealth_dll.Script_CloseMenu()


stealth_dll.Script_GetLastMenuItems.restype = c_wchar_p


def GetLastMenuItems():
    return stealth_dll.Script_GetLastMenuItems().splitlines()


stealth_dll.Script_GetMenuItems.argtypes = [c_wchar_p]
stealth_dll.Script_GetMenuItems.restype = c_wchar_p


def GetMenuItems(MenuCaption):
    return stealth_dll.Script_GetMenuItems(MenuCaption).splitlines()


stealth_dll.Script_MenuHookPresent.restype = c_bool


def MenuHookPresent():
    return stealth_dll.Script_MenuHookPresent()


stealth_dll.Script_MenuPresent.restype = c_bool


def MenuPresent():
    return stealth_dll.Script_MenuPresent()


stealth_dll.Script_WaitMenu.argtypes = [c_wchar_p, c_wchar_p]
stealth_dll.Script_WaitMenu.restype = c_void_p


def WaitMenu(MenuCaption, ElementCaption):
    return stealth_dll.Script_WaitMenu(MenuCaption, ElementCaption)


# end region Menus

# region Move Items
stealth_dll.Script_DragItem.argtypes = [c_uint, c_int]
stealth_dll.Script_DragItem.restype = c_bool


def DragItem(ItemID, Count):
    return stealth_dll.Script_DragItem(ItemID, Count)


stealth_dll.Script_Drop.argtypes = [c_uint, c_int, c_ushort, c_ushort, c_byte]
stealth_dll.Script_Drop.restype = c_bool


def Drop(ItemID, Count, X, Y, Z):
    return stealth_dll.Script_Drop(ItemID, Count, X, Y, Z)


stealth_dll.Script_DropHere.argtypes = [c_uint]
stealth_dll.Script_DropHere.restype = c_bool


def DropHere(ItemID):
    return stealth_dll.Script_DropHere(ItemID)


stealth_dll.Script_DropItem.argtypes = [c_uint, c_int, c_int, c_int]
stealth_dll.Script_DropItem.restype = c_bool


def DropItem(MoveIntoID, X, Y, Z):
    return stealth_dll.Script_DropItem(MoveIntoID, X, Y, Z)


stealth_dll.Script_EmptyContainer.argtypes = [c_uint, c_uint, c_ushort]
stealth_dll.Script_EmptyContainer.restype = c_bool


def EmptyContainer(Container, DestContainer, delay_ms):
    return stealth_dll.Script_EmptyContainer(Container, DestContainer, delay_ms)


stealth_dll.Script_GetDropCheckCoord.restype = c_bool


def GetDropCheckCoord():
    return stealth_dll.Script_GetDropCheckCoord()


stealth_dll.Script_GetDropDelay.restype = c_uint


def GetDropDelay():
    return stealth_dll.Script_GetDropDelay()


stealth_dll.Script_Grab.argtypes = [c_uint, c_int]
stealth_dll.Script_Grab.restype = c_bool


def Grab(ItemID, Count):
    return stealth_dll.Script_Grab(ItemID, Count)


stealth_dll.Script_MoveItem.argtypes = [c_uint, c_int, c_uint, c_ushort, c_ushort, c_byte]
stealth_dll.Script_MoveItem.restype = c_bool


def MoveItem(ItemID, Count, MoveIntoID, X, Y, Z):
    return stealth_dll.Script_MoveItem(ItemID, Count, MoveIntoID, X, Y, Z)


stealth_dll.Script_MoveItems.argtypes = [c_uint, c_ushort, c_ushort, c_uint, c_ushort, c_ushort, c_byte, c_int]
stealth_dll.Script_MoveItems.restype = c_bool


def MoveItems(Container, ItemsType, ItemsColor, MoveIntoID, X, Y, Z, DelayMS):
    return stealth_dll.Script_MoveItems(Container, ItemsType, ItemsColor, MoveIntoID, X, Y, Z, DelayMS)


stealth_dll.Script_SetDropCheckCoord.argtypes = [c_bool]
stealth_dll.Script_SetDropCheckCoord.restype = c_void_p


def SetDropCheckCoord(Value):
    return stealth_dll.Script_SetDropCheckCoord(Value)


stealth_dll.Script_SetDropDelay.argtypes = [c_uint]
stealth_dll.Script_SetDropDelay.restype = c_void_p


def SetDropDelay(Value):
    return stealth_dll.Script_SetDropDelay(Value)


# end region Move Items

# region MoveVars
stealth_dll.Script_GetMoveOpenDoor.restype = c_bool


def GetMoveOpenDoor():
    return stealth_dll.Script_GetMoveOpenDoor()


stealth_dll.Script_GetMoveThroughNPC.restype = c_ushort


def Script_GetMoveThroughNPC():
    return stealth_dll.Script_GetMoveThroughNPC()


stealth_dll.Script_SetMoveOpenDoor.argtypes = [c_bool]
stealth_dll.Script_SetMoveOpenDoor.restype = c_void_p


def SetMoveOpenDoor(Value):
    return stealth_dll.Script_SetMoveOpenDoor(Value)


stealth_dll.Script_SetMoveThroughNPC.argtypes = [c_ushort]
stealth_dll.Script_SetMoveThroughNPC.restype = c_void_p


def SetMoveThroughNPC(Value):
    return stealth_dll.Script_SetMoveThroughNPC(Value)


# end region MoveVars

# region Mover
stealth_dll.Script_CalcCoord.argtypes = [c_ushort, c_ushort, c_ubyte, c_ushort, c_ushort]
stealth_dll.Script_CalcCoord.restype = c_void_p


def CalcCoord(x, y, Dir, varx2, y2):
    return stealth_dll.Script_CalcCoord(x, y, Dir, varx2, y2)


stealth_dll.Script_CalcDir.argtypes = [c_int, c_int, c_int, c_int]
stealth_dll.Script_CalcDir.restype = c_ubyte


def CalcDir(Xfrom, Yfrom, Xto, Yto):
    return stealth_dll.Script_CalcDir(Xfrom, Yfrom, Xto, Yto)


stealth_dll.Script_CheckLOS.argtypes = [c_ushort, c_ushort, c_byte, c_ushort, c_ushort, c_byte, c_ubyte, c_ubyte,
                                        c_uint]
stealth_dll.Script_CheckLOS.restype = c_bool


def CheckLOS(xf, yf, zf, xt, yt, zt, WorldNum, LOSCheckType, LOSOptions):
    return stealth_dll.Script_CheckLOS(xf, yf, zf, xt, yt, zt, WorldNum, LOSCheckType, LOSOptions)


stealth_dll.Script_ClearBadLocationList.restype = c_void_p


def ClearBadLocationList():
    return stealth_dll.Script_ClearBadLocationList()


stealth_dll.Script_ClearBadObjectList.restype = c_void_p


def ClearBadObjectList():
    return stealth_dll.Script_ClearBadObjectList()


stealth_dll.Script_Dist.argtypes = [c_ushort, c_ushort, c_ushort, c_ushort]
stealth_dll.Script_Dist.restype = c_ushort


def Dist(x1, y1, x2, y2):
    return stealth_dll.Script_Dist(x1, y1, x2, y2)


stealth_dll.Script_GetLastStepQUsedDoor.restype = c_uint


def GetLastStepQUsedDoor():
    return stealth_dll.Script_GetLastStepQUsedDoor()


# stealth_dll.Script_GetPathArray.argtypes = [c_ushort, c_ushort, c_bool, c_int, Pointer, c_uint]
stealth_dll.Script_GetPathArray.restype = c_void_p


def GetPathArray(DestX, DestY, Optimized, Accuracy):
    outLen = c_int()

    stealth_dll.Script_GetPathArray(DestX, DestY, Optimized, Accuracy, None, byref(outLen))

    if outLen.value > 0:
        Result = (TMyPoint * (outLen.value // 4))()
        stealth_dll.Script_GetPathArray(DestX, DestY, Optimized, Accuracy, Result, byref(outLen))

        return [(point.X, point.Y, point.Z) for point in Result]
    else:
        return []


# stealth_dll.Script_GetPathArray3D.argtypes = [c_ushort, c_ushort, c_byte, c_ushort, c_ushort, c_byte, c_ubyte, c_int, c_int, c_bool, POINTER(TMyPoint), c_uint]
stealth_dll.Script_GetPathArray3D.restype = c_void_p


def GetPathArray3D(StartX, StartY, StartZ, FinishX, FinishY, FinishZ, WorldNum, AccuracyXY, AccuracyZ, Run):
    outLen = c_uint()

    stealth_dll.Script_GetPathArray3D(StartX, StartY, StartZ, FinishX, FinishY, FinishZ, WorldNum, AccuracyXY,
                                      AccuracyZ, Run, None, byref(outLen))

    if outLen.value > 0:
        Result = (TMyPoint * (outLen.value // 4))()
        stealth_dll.Script_GetPathArray3D(StartX, StartY, StartZ, FinishX, FinishY, FinishZ, WorldNum, AccuracyXY,
                                          AccuracyZ, Run, Result, byref(outLen))

        return [(point.X, point.Y, point.Z) for point in Result]
    else:
        return []


stealth_dll.Script_GetRunMountTimer.restype = c_ushort


def GetRunMountTimer():
    return stealth_dll.Script_GetRunMountTimer()


stealth_dll.Script_GetRunUnmountTimer.restype = c_ushort


def GetRunUnMountTimer():
    return stealth_dll.Script_GetRunUnmountTimer()


stealth_dll.Script_GetWalkMountTimer.restype = c_ushort


def GetWalkMountTimer():
    return stealth_dll.Script_GetWalkMountTimer()


stealth_dll.Script_GetWalkUnmountTimer.restype = c_ushort


def GetWalkUnmountTimer():
    return stealth_dll.Script_GetWalkUnmountTimer()


stealth_dll.Script_MoveXY.argtypes = [c_ushort, c_ushort, c_bool, c_int, c_bool]
stealth_dll.Script_MoveXY.restype = c_bool


def MoveXY(Xdst, Ydst, Optimized, Accuracy, Running):
    return stealth_dll.Script_MoveXY(Xdst, Ydst, Optimized, Accuracy, Running)


stealth_dll.Script_MoveXYZ.argtypes = [c_ushort, c_ushort, c_byte, c_int, c_int, c_bool]
stealth_dll.Script_MoveXYZ.restype = c_bool


def MoveXYZ(Xdst, Ydst, Zdst, AccuracyXY, AccuracyZ, Running):
    return stealth_dll.Script_MoveXYZ(Xdst, Ydst, Zdst, AccuracyXY, AccuracyZ, Running)


stealth_dll.Script_SetBadLocation.argtypes = [c_ushort, c_ushort]
stealth_dll.Script_SetBadLocation.restype = c_void_p


def SetBadLocation(X, Y):
    return stealth_dll.Script_SetBadLocation(X, Y)


stealth_dll.Script_SetBadObject.argtypes = [c_ushort, c_ushort, c_ubyte]
stealth_dll.Script_SetBadObject.restype = c_void_p


def SetBadObject(ObjType, Color, Radius):
    return stealth_dll.Script_SetBadObject(ObjType, Color, Radius)


stealth_dll.Script_SetGoodLocation.argtypes = [c_ushort, c_ushort]
stealth_dll.Script_SetGoodLocation.restype = c_void_p


def SetGoodLocation(X, Y):
    return stealth_dll.Script_SetGoodLocation(X, Y)


stealth_dll.Script_SetRunMountTimer.argtypes = [c_ushort]
stealth_dll.Script_SetRunMountTimer.restype = c_void_p


def SetRunMountTimer(Value):
    return stealth_dll.Script_SetRunMountTimer(Value)


stealth_dll.Script_SetRunUnmountTimer.argtypes = [c_ushort]
stealth_dll.Script_SetRunUnmountTimer.restype = c_void_p


def SetRunUnmountTimer(Value):
    return stealth_dll.Script_SetRunUnmountTimer(Value)


stealth_dll.Script_SetWalkMountTimer.argtypes = [c_ushort]
stealth_dll.Script_SetWalkMountTimer.restype = c_void_p


def SetWalkMountTimer(Value):
    return stealth_dll.Script_SetWalkMountTimer(Value)


stealth_dll.Script_SetWalkUnmountTimer.argtypes = [c_ushort]
stealth_dll.Script_SetWalkUnmountTimer.restype = c_void_p


def SetWalkUnmountTimer(Value):
    return stealth_dll.Script_SetWalkUnmountTimer(Value)


stealth_dll.Script_Step.argtypes = [c_ubyte, c_bool]
stealth_dll.Script_Step.restype = c_ubyte


def Step(Direction, Running):
    return stealth_dll.Script_Step(Direction, Running)


stealth_dll.Script_StepQ.argtypes = [c_ubyte, c_bool]
stealth_dll.Script_StepQ.restype = c_int


def StepQ(Direction, Running):
    return stealth_dll.Script_StepQ(Direction, Running)


stealth_dll.Script_newMoveXY.argtypes = [c_ushort, c_ushort, c_bool, c_int, c_bool]
stealth_dll.Script_newMoveXY.restype = c_bool


def NewMoveXY(Xdst, Ydst, Optimized, Accuracy, Running):
    return stealth_dll.Script_newMoveXY(Xdst, Ydst, Optimized, Accuracy, Running)


# end region Mover

# region MsToDateTime
stealth_dll.Script_MsToDateTime.argtypes = [c_uint]
stealth_dll.Script_MsToDateTime.restype = c_double


def MsToDateTime(TimeMS):
    dt = (stealth_dll.Script_MsToDateTime(TimeMS) / 1000) / (1440 * 60)
    return TDateTimeToPyDateTime(dt)


# end region MsToDateTime

# region Objects
stealth_dll.Script_FindAtCoord.argtypes = [c_ushort, c_ushort]
stealth_dll.Script_FindAtCoord.restype = c_uint


def FindAtCord(X, Y):
    return stealth_dll.Script_FindAtCoord(X, Y)


stealth_dll.Script_FindNotoriety.argtypes = [c_ushort, c_ubyte]
stealth_dll.Script_FindNotoriety.restype = c_uint


def FindNotoriety(ObjType, Notoriety):
    return stealth_dll.Script_FindNotoriety(ObjType, Notoriety)


stealth_dll.Script_FindType.argtypes = [c_ushort, c_uint]
stealth_dll.Script_FindType.restype = c_uint


def FindType(ObjType, Container):
    return stealth_dll.Script_FindType(ObjType, Container)


stealth_dll.Script_FindTypeEx.argtypes = [c_ushort, c_ushort, c_uint, c_bool]
stealth_dll.Script_FindTypeEx.restype = c_uint


def FindTypeEx(ObjType, Color, Container, InSub):
    return stealth_dll.Script_FindTypeEx(ObjType, Color, Container, InSub)


stealth_dll.Script_FindTypesArrayEx.restype = c_uint


def FindTypeArrayEx(ObjTypes, Colors, Containers, InSub):
    if not isinstance(ObjTypes, list):
        raise TypeError('ObjTypes must be a list while it is {}'.format(type(ObjTypes)))

    if not isinstance(Colors, list):
        raise TypeError('Colors must be a list while it is {}'.format(type(Colors)))

    if not isinstance(Containers, list):
        raise TypeError('Containers must be a list while it is {}'.format(type(Containers)))

    pyObjTypes = (c_ushort * len(ObjTypes))(*ObjTypes)
    pyColors = (c_ushort * len(Colors))(*Colors)
    pyContainers = (c_uint * len(Containers))(*Containers)
    pyInSub = c_bool(InSub)
    return stealth_dll.Script_FindTypesArrayEx(byref(pyObjTypes), len(ObjTypes) * 2,
                                               byref(pyColors), len(Colors) * 2,
                                               byref(pyContainers), len(Containers) * 4,
                                               pyInSub
                                               )


stealth_dll.Script_GetAltName.argtypes = [c_uint]
stealth_dll.Script_GetAltName.restype = c_wchar_p


def GetAltName(ObjID):
    return stealth_dll.Script_GetAltName(ObjID)


stealth_dll.Script_GetClilocByID.argtypes = [c_uint]
stealth_dll.Script_GetClilocByID.restype = c_wchar_p


def GetCliloc(ClilocID):
    return stealth_dll.Script_GetClilocByID(ClilocID)


'''stealth_dll.Script_GetClilocRecJson.argtypes = [c_uint]
stealth_dll.Script_GetClilocRecJson.restype = c_wchar_p
def GetToolTipRec(ObjID):
    ugly_json = loads(stealth_dll.Script_GetClilocRecJson(ObjID))
    if ugly_json.get('Items', False):
        nice_list = {item['ClilocID'] : item['Params'] for item in ugly_json['Items']}
        return nice_list
    else:
        return {}'''


def GetToolTipRec(serial):
    func = stealth_dll.Script_GetClilocRec

    buff_size = c_uint()
    func(c_uint(serial), c_void_p(None), byref(buff_size))
    if not buff_size.value:
        return {}

    buffer = (c_ubyte * buff_size.value)()
    func(c_uint(serial), byref(buffer), byref(buff_size))

    res = {}
    data = bytes(buffer)
    count = c_uint.from_buffer_copy(data[:4]).value
    data = data[4:]
    for i in range(count):
        cliloc_id = c_uint.from_buffer_copy(data[:4]).value
        array_len = c_uint.from_buffer_copy(data[4:8]).value
        data = data[8:]
        tmp = []
        for j in range(array_len):
            str_len = c_uint.from_buffer_copy(data[:4]).value
            string = data[4:4 + str_len * 2].decode('UTF-16LE')
            data = data[4 + str_len * 2:]
            tmp.append(string)
        res[cliloc_id] = tmp
    return res


stealth_dll.Script_GetColor.argtypes = [c_uint]
stealth_dll.Script_GetColor.restype = c_ushort


def GetColor(ObjID):
    return stealth_dll.Script_GetColor(ObjID)


stealth_dll.Script_GetDex.argtypes = [c_uint]
stealth_dll.Script_GetDex.restype = c_int


def GetDex(ObjID):
    return stealth_dll.Script_GetDex(ObjID)


stealth_dll.Script_GetDirection.argtypes = [c_uint]
stealth_dll.Script_GetDirection.restype = c_ubyte


def GetDirection(ObjID):
    return stealth_dll.Script_GetDirection(ObjID)


stealth_dll.Script_GetDistance.argtypes = [c_uint]
stealth_dll.Script_GetDistance.restype = c_int


def GetDistance(ObjID):
    return stealth_dll.Script_GetDistance(ObjID)


stealth_dll.Script_GetFindCount.restype = c_int


def FindCount():
    return stealth_dll.Script_GetFindCount()


stealth_dll.Script_GetFindDistance.restype = c_uint


def GetFindDistance():
    return stealth_dll.Script_GetFindDistance()


stealth_dll.Script_GetFindFullQuantity.restype = c_int


def FindFullQuantity():
    return stealth_dll.Script_GetFindFullQuantity()


stealth_dll.Script_GetFindInNulPoint.restype = c_bool


def GetFindInNulPoint():
    return stealth_dll.Script_GetFindInNulPoint()


stealth_dll.Script_GetFindItem.restype = c_uint


def FindItem():
    return stealth_dll.Script_GetFindItem()


stealth_dll.Script_GetFindQuantity.restype = c_int


def FindQuantity():
    return stealth_dll.Script_GetFindQuantity()


stealth_dll.Script_GetFindVertical.restype = c_uint


def GetFindVertical():
    return stealth_dll.Script_GetFindVertical()


stealth_dll.Script_GetFindedList.restype = c_void_p


def GetFindedList():
    BufLen = c_uint()

    stealth_dll.Script_GetFindedList(None, byref(BufLen))
    if BufLen.value > 0:
        Result = (c_uint * (BufLen.value // 4))()
        stealth_dll.Script_GetFindedList(byref(Result), byref(BufLen))

        return list(Result)
    else:
        return []


stealth_dll.Script_GetHP.argtypes = [c_uint]
stealth_dll.Script_GetHP.restype = c_int


def GetHP(ObjID):
    return stealth_dll.Script_GetHP(ObjID)


stealth_dll.Script_GetIgnoreList.restype = c_void_p


def GetIgnoreList():
    BufLen = c_uint()

    stealth_dll.Script_GetIgnoreList(None, byref(BufLen))
    if BufLen.value > 0:
        Result = (c_uint * (BufLen.value // 4))()
        stealth_dll.Script_GetIgnoreList(byref(Result), byref(BufLen))

        return list(Result)
    else:
        return []


stealth_dll.Script_GetInt.argtypes = [c_uint]
stealth_dll.Script_GetInt.restype = c_int


def GetInt(ObjID):
    return stealth_dll.Script_GetInt(ObjID)


stealth_dll.Script_GetMana.argtypes = [c_uint]
stealth_dll.Script_GetMana.restype = c_int


def GetMana(ObjID):
    return stealth_dll.Script_GetMana(ObjID)


stealth_dll.Script_GetMaxHP.argtypes = [c_uint]
stealth_dll.Script_GetMaxHP.restype = c_int


def GetMaxHP(ObjID):
    return stealth_dll.Script_GetMaxHP(ObjID)


stealth_dll.Script_GetMaxMana.argtypes = [c_uint]
stealth_dll.Script_GetMaxMana.restype = c_int


def GetMaxMana(ObjID):
    return stealth_dll.Script_GetMaxMana(ObjID)


stealth_dll.Script_GetMaxStam.argtypes = [c_uint]
stealth_dll.Script_GetMaxStam.restype = c_int


def GetMaxStam(ObjID):
    return stealth_dll.Script_GetMaxStam(ObjID)


stealth_dll.Script_GetName.argtypes = [c_uint]
stealth_dll.Script_GetName.restype = c_wchar_p


def GetName(ObjID):
    return stealth_dll.Script_GetName(ObjID)


stealth_dll.Script_GetNotoriety.argtypes = [c_uint]
stealth_dll.Script_GetNotoriety.restype = c_ubyte


def GetNotoriety(ObjID):
    return stealth_dll.Script_GetNotoriety(ObjID)


stealth_dll.Script_GetParent.argtypes = [c_uint]
stealth_dll.Script_GetParent.restype = c_uint


def GetParent(ObjID):
    return stealth_dll.Script_GetParent(ObjID)


stealth_dll.Script_GetPrice.argtypes = [c_uint]
stealth_dll.Script_GetPrice.restype = c_uint


def GetPrice(ObjID):
    return stealth_dll.Script_GetPrice(ObjID)


stealth_dll.Script_GetQuantity.argtypes = [c_uint]
stealth_dll.Script_GetQuantity.restype = c_int


def GetQuantity(ObjID):
    return stealth_dll.Script_GetQuantity(ObjID)


stealth_dll.Script_GetStam.argtypes = [c_uint]
stealth_dll.Script_GetStam.restype = c_int


def GetStam(ObjID):
    return stealth_dll.Script_GetStam(ObjID)


stealth_dll.Script_GetStr.argtypes = [c_uint]
stealth_dll.Script_GetStr.restype = c_int


def GetStr(ObjID):
    return stealth_dll.Script_GetStr(ObjID)


stealth_dll.Script_GetTitle.argtypes = [c_uint]
stealth_dll.Script_GetTitle.restype = c_wchar_p


def GetTitle(ObjID):
    return stealth_dll.Script_GetTitle(ObjID)


stealth_dll.Script_GetTooltip.argtypes = [c_uint]
stealth_dll.Script_GetTooltip.restype = c_wchar_p


def GetTooltip(ObjID):
    return stealth_dll.Script_GetTooltip(ObjID)


stealth_dll.Script_GetType.argtypes = [c_uint]
stealth_dll.Script_GetType.restype = c_ushort


def GetType(ObjID):
    return stealth_dll.Script_GetType(ObjID)


stealth_dll.Script_GetX.argtypes = [c_uint]
stealth_dll.Script_GetX.restype = c_int


def GetX(ObjID):
    return stealth_dll.Script_GetX(ObjID)


stealth_dll.Script_GetY.argtypes = [c_uint]
stealth_dll.Script_GetY.restype = c_int


def GetY(ObjID):
    return stealth_dll.Script_GetY(ObjID)


stealth_dll.Script_GetZ.argtypes = [c_uint]
stealth_dll.Script_GetZ.restype = c_byte


def GetZ(ObjID):
    return stealth_dll.Script_GetZ(ObjID)


stealth_dll.Script_Ignore.argtypes = [c_uint]
stealth_dll.Script_Ignore.restype = c_void_p


def Ignore(ObjID):
    return stealth_dll.Script_Ignore(ObjID)


stealth_dll.Script_IgnoreOff.argtypes = [c_uint]
stealth_dll.Script_IgnoreOff.restype = c_void_p


def IgnoreOff(ObjID):
    return stealth_dll.Script_IgnoreOff(ObjID)


stealth_dll.Script_IgnoreReset.restype = c_void_p


def IgnoreReset():
    return stealth_dll.Script_IgnoreReset()


stealth_dll.Script_IsContainer.argtypes = [c_uint]
stealth_dll.Script_IsContainer.restype = c_bool


def IsContainer(ObjID):
    return stealth_dll.Script_IsContainer(ObjID)


stealth_dll.Script_IsDead.argtypes = [c_uint]
stealth_dll.Script_IsDead.restype = c_bool


def IsDead(ObjID):
    return stealth_dll.Script_IsDead(ObjID)


stealth_dll.Script_IsFemale.argtypes = [c_uint]
stealth_dll.Script_IsFemale.restype = c_bool


def IsFemale(ObjID):
    return stealth_dll.Script_IsFemale(ObjID)


stealth_dll.Script_IsHidden.argtypes = [c_uint]
stealth_dll.Script_IsHidden.restype = c_bool


def IsHidden(ObjID):
    return stealth_dll.Script_IsHidden(ObjID)


stealth_dll.Script_IsMovable.argtypes = [c_uint]
stealth_dll.Script_IsMovable.restype = c_bool


def IsMovable(ObjID):
    return stealth_dll.Script_IsMovable(ObjID)


stealth_dll.Script_IsNPC.argtypes = [c_uint]
stealth_dll.Script_IsNPC.restype = c_bool


def IsNPC(ObjID):
    return stealth_dll.Script_IsNPC(ObjID)


stealth_dll.Script_IsObjectExists.argtypes = [c_uint]
stealth_dll.Script_IsObjectExists.restype = c_bool


def IsObjectExists(ObjID):
    return stealth_dll.Script_IsObjectExists(ObjID)


stealth_dll.Script_IsParalyzed.argtypes = [c_uint]
stealth_dll.Script_IsParalyzed.restype = c_bool


def IsParalyzed(ObjID):
    return stealth_dll.Script_IsParalyzed(ObjID)


stealth_dll.Script_IsPoisoned.argtypes = [c_uint]
stealth_dll.Script_IsPoisoned.restype = c_bool


def IsPoisoned(ObjID):
    return stealth_dll.Script_IsPoisoned(ObjID)


stealth_dll.Script_IsRunning.argtypes = [c_uint]
stealth_dll.Script_IsRunning.restype = c_bool


def IsRunning(ObjID):
    return stealth_dll.Script_IsRunning(ObjID)


stealth_dll.Script_IsWarMode.argtypes = [c_uint]
stealth_dll.Script_IsWarMode.restype = c_bool


def IsWarMode(ObjID):
    return stealth_dll.Script_IsWarMode(ObjID)


stealth_dll.Script_IsYellowHits.argtypes = [c_uint]
stealth_dll.Script_IsYellowHits.restype = c_bool


def IsYellowHits(ObjID):
    return stealth_dll.Script_IsYellowHits(ObjID)


stealth_dll.Script_PredictedDirection.restype = c_ubyte


def PredictedDirection():
    return stealth_dll.Script_PredictedDirection()


stealth_dll.Script_PredictedX.restype = c_ushort


def PredictedX():
    return stealth_dll.Script_PredictedX()


stealth_dll.Script_PredictedY.restype = c_ushort


def PredictedY():
    return stealth_dll.Script_PredictedY()


stealth_dll.Script_PredictedZ.restype = c_byte


def PredictedZ():
    return stealth_dll.Script_PredictedZ()


stealth_dll.Script_SetFindDistance.argtypes = [c_uint]
stealth_dll.Script_SetFindDistance.restype = c_void_p


def SetFindDistance(Value):
    return stealth_dll.Script_SetFindDistance(Value)


stealth_dll.Script_SetFindInNulPoint.argtypes = [c_bool]
stealth_dll.Script_SetFindInNulPoint.restype = c_void_p


def SetFindInNulPoint(Value):
    return stealth_dll.Script_SetFindInNulPoint(Value)


stealth_dll.Script_SetFindVertical.argtypes = [c_uint]
stealth_dll.Script_SetFindVertical.restype = c_void_p


def SetFindVertical(Value):
    return stealth_dll.Script_SetFindVertical(Value)


# end region Objects

# region Other
stealth_dll.Script_ChangeStatLockState.argtypes = [c_ubyte, c_ubyte]
stealth_dll.Script_ChangeStatLockState.restype = c_void_p


def SetStatState(statNum, statState):
    return stealth_dll.Script_ChangeStatLockState(statNum, statState)


stealth_dll.Script_CheckLag.argtypes = [c_int]
stealth_dll.Script_CheckLag.restype = c_bool


def CheckLag(timeoutMS):
    return stealth_dll.Script_CheckLag(timeoutMS)


stealth_dll.Script_ConsoleEntryReply.argtypes = [c_wchar_p]
stealth_dll.Script_ConsoleEntryReply.restype = c_void_p


def ConsoleEntryReply(Text):
    return stealth_dll.Script_ConsoleEntryReply(Text)


stealth_dll.Script_ConsoleEntryUnicodeReply.argtypes = [c_wchar_p]
stealth_dll.Script_ConsoleEntryUnicodeReply.restype = c_void_p


def ConsoleEntryUnicodeReply(Text):
    return stealth_dll.Script_ConsoleEntryUnicodeReply(Text)


stealth_dll.Script_GameServerIPString.restype = c_wchar_p


def GameServerIPString():
    return stealth_dll.Script_GameServerIPString()


stealth_dll.Script_GetGlobal.argtypes = [c_ubyte, c_wchar_p]
stealth_dll.Script_GetGlobal.restype = c_wchar_p


def GetGlobal(GlobalRegion, VarName):
    if GlobalRegion not in [0, 'reg_stealth', 1, 'reg_char']:
        raise ValueError('GlobalRegion can only have one of this values {}'.format([0, 'reg_stealth', 1, 'reg_char']))

    if GlobalRegion == 'reg_stealth':
        GlobalRegion = 0
    elif GlobalRegion == 'reg_char':
        GlobalRegion = 1

    return stealth_dll.Script_GetGlobal(GlobalRegion, VarName)


# stealth_dll.Script_GetStaticArtBitmap.argtypes = [c_uint, c_ushort, POINTER, c_uint]
stealth_dll.Script_GetStaticArtBitmap.restype = c_void_p


def GetStaticArtBitmap(Id, Hue, ImgPath="imageToSave.bmp"):
    Result = None
    outLen = c_uint()
    stealth_dll.Script_GetStaticArtBitmap(Id, Hue, None, byref(outLen))

    if outLen.value > 0:
        Result = (c_ubyte * (outLen.value))()
        stealth_dll.Script_GetStaticArtBitmap(Id, Hue, byref(Result), byref(outLen))
        Result = bytes(byte for byte in Result)
        fh = open(ImgPath, 'wb')
        fh.write(Result)

    return None


stealth_dll.Script_HelpRequest.restype = c_void_p


def HelpRequest():
    return stealth_dll.Script_HelpRequest()


stealth_dll.Script_MobileCanBeRenamed.argtypes = [c_uint]
stealth_dll.Script_MobileCanBeRenamed.restype = c_bool


def MobileCanBeRenamed(Mob_ID):
    return stealth_dll.Script_MobileCanBeRenamed(Mob_ID)


stealth_dll.Script_PlayWav.argtypes = [c_wchar_p]
stealth_dll.Script_PlayWav.restype = c_bool


def PlayWav(FileName):
    return stealth_dll.Script_PlayWav(FileName)


stealth_dll.Script_PrintScriptMethodsList.argtypes = [c_wchar_p, c_bool]
stealth_dll.Script_PrintScriptMethodsList.restype = c_void_p


def PrintScriptMethodsList(FileName, SortedList):
    return stealth_dll.Script_PrintScriptMethodsList(FileName, SortedList)


stealth_dll.Script_QuestRequest.restype = c_void_p


def QuestRequest():
    return stealth_dll.Script_QuestRequest()


stealth_dll.Script_RenameMobile.argtypes = [c_uint, c_wchar_p]
stealth_dll.Script_RenameMobile.restype = c_void_p


def RenameMobile(Mob_ID, NewName):
    return stealth_dll.Script_RenameMobile(Mob_ID, NewName)


stealth_dll.Script_RequestStats.argtypes = [c_uint]
stealth_dll.Script_RequestStats.restype = c_void_p


def RequestStats(ObjID):
    return stealth_dll.Script_RequestStats(ObjID)


stealth_dll.Script_SendTextToUO.argtypes = [c_wchar_p]
stealth_dll.Script_SendTextToUO.restype = c_void_p


def UOSay(Text):
    return stealth_dll.Script_SendTextToUO(Text)


stealth_dll.Script_SendTextToUOColor.argtypes = [c_wchar_p, c_ushort]
stealth_dll.Script_SendTextToUOColor.restype = c_void_p


def UOSayColor(Text, Color):
    return stealth_dll.Script_SendTextToUOColor(Text, Color)


stealth_dll.Script_SetAlarm.restype = c_void_p


def Alarm():
    return stealth_dll.Script_SetAlarm()


stealth_dll.Script_SetCOMEnabled.argtypes = [c_bool]
stealth_dll.Script_SetCOMEnabled.restype = c_void_p


def SetCOMEnabled(Value):
    return stealth_dll.Script_SetCOMEnabled(Value)


stealth_dll.Script_SetGlobal.argtypes = [c_ubyte, c_wchar_p, c_wchar_p]
stealth_dll.Script_SetGlobal.restype = c_void_p


def SetGlobal(GlobalRegion, VarName, VarValue):
    if GlobalRegion not in [0, 'reg_stealth', 1, 'reg_char']:
        raise ValueError('GlobalRegion can only have one of this values {}'.format([0, 'reg_stealth', 1, 'reg_char']))

    if GlobalRegion == 'reg_stealth':
        GlobalRegion = 0
    elif GlobalRegion == 'reg_char':
        GlobalRegion = 1

    return stealth_dll.Script_SetGlobal(GlobalRegion, VarName, VarValue)


# end region Other

# region Paralyzed
stealth_dll.Script_GetParalyzedStatus.restype = c_bool


def Paralyzed():
    return stealth_dll.Script_GetParalyzedStatus()


# end region Paralyzed

# region Party
stealth_dll.Script_InParty.restype = c_bool


def InParty():
    return stealth_dll.Script_InParty()


stealth_dll.Script_InviteToParty.argtypes = [c_uint]
stealth_dll.Script_InviteToParty.restype = c_void_p


def InviteToParty(ID):
    return stealth_dll.Script_InviteToParty(ID)


stealth_dll.Script_PartyAcceptInvite.restype = c_void_p


def PartyAcceptInvite():
    return stealth_dll.Script_PartyAcceptInvite()


stealth_dll.Script_PartyCanLootMe.argtypes = [c_bool]
stealth_dll.Script_PartyCanLootMe.restype = c_void_p


def PartyCanLootMe(Value):
    return stealth_dll.Script_PartyCanLootMe(Value)


stealth_dll.Script_PartyDeclineInvite.restype = c_void_p


def PartyDeclineInvite():
    return stealth_dll.Script_PartyDeclineInvite()


stealth_dll.Script_PartyLeave.restype = c_void_p


def PartyLeave():
    return stealth_dll.Script_PartyLeave()


stealth_dll.Script_PartyMembersList.restype = c_void_p


def PartyMembersList():
    BufLen = c_uint()

    stealth_dll.Script_PartyMembersList(None, byref(BufLen))
    if BufLen.value > 0:
        Result = (c_uint * (BufLen.value // 4))()
        stealth_dll.Script_PartyMembersList(byref(Result), byref(BufLen))

        return list(Result)
    else:
        return []


stealth_dll.Script_PartyMessageTo.argtypes = [c_uint, c_wchar_p]
stealth_dll.Script_PartyMessageTo.restype = c_void_p


def PartyMessageTo(ID, Msg):
    return stealth_dll.Script_PartyMessageTo(ID, Msg)


stealth_dll.Script_PartySay.argtypes = [c_wchar_p]
stealth_dll.Script_PartySay.restype = c_void_p


def PartySay(Msg):
    return stealth_dll.Script_PartySay(Msg)


stealth_dll.Script_RemoveFromParty.argtypes = [c_uint]
stealth_dll.Script_RemoveFromParty.restype = c_void_p


def RemoveFromParty(ID):
    return stealth_dll.Script_RemoveFromParty(ID)


# end region Party

# region Path
stealth_dll.Script_GetStealthPath.restype = c_wchar_p


def StealthPath():
    return stealth_dll.Script_GetStealthPath()


# end region Path

# region Pause Script on disconnect
stealth_dll.Script_GetPauseScriptOnDisconnectStatus.restype = c_bool


def GetPauseScriptOnDisconnectStatus():
    return stealth_dll.Script_GetPauseScriptOnDisconnectStatus()


stealth_dll.Script_SetPauseScriptOnDisconnectStatus.argtypes = [c_bool]
stealth_dll.Script_SetPauseScriptOnDisconnectStatus.restype = c_void_p


def SetPauseScriptOnDisconnectStatus(Value):
    return stealth_dll.Script_SetPauseScriptOnDisconnectStatus(Value)


# end region Pause Script on disconnect

# region Poisoned
stealth_dll.Script_GetPoisonedStatus.restype = c_bool


def Poisoned():
    return stealth_dll.Script_GetPoisonedStatus()


# end region Poisoned

# region Profile Name
stealth_dll.Script_ChangeProfile.argtypes = [c_wchar_p]
stealth_dll.Script_ChangeProfile.restype = c_int


def ChangeProfile(PName):
    return stealth_dll.Script_ChangeProfile(PName)


stealth_dll.Script_ProfileName.restype = c_wchar_p


def ProfileName():
    return stealth_dll.Script_ProfileName()


# end region Profile Name

# region Proxy
stealth_dll.Script_GetProxyIP.restype = c_wchar_p


def ProxyIP():
    return stealth_dll.Script_GetProxyIP()


stealth_dll.Script_GetProxyPort.restype = c_ushort


def ProxyPort():
    return stealth_dll.Script_GetProxyPort()


stealth_dll.Script_GetUseProxy.restype = c_bool


def UseProxy():
    return stealth_dll.Script_GetUseProxy()


# end region Proxy

# region QuestArrow
stealth_dll.Script_GetQuestArrow.restype = TPoint


def GetQuestArrow():
    return stealth_dll.Script_GetQuestArrow()


# end region QuestArrow

# region Reagents
stealth_dll.Script_ConstBM.restype = c_ushort


def BM():
    return stealth_dll.Script_ConstBM()


stealth_dll.Script_ConstBMCount.restype = c_ushort


def BMCount():
    return stealth_dll.Script_ConstBMCount()


stealth_dll.Script_ConstBP.restype = c_ushort


def BP():
    return stealth_dll.Script_ConstBP()


stealth_dll.Script_ConstBPCount.restype = c_ushort


def BPCount():
    return stealth_dll.Script_ConstBPCount()


stealth_dll.Script_ConstGA.restype = c_ushort


def GA():
    return stealth_dll.Script_ConstGA()


stealth_dll.Script_ConstGACount.restype = c_ushort


def GACount():
    return stealth_dll.Script_ConstGACount()


stealth_dll.Script_ConstGS.restype = c_ushort


def GS():
    return stealth_dll.Script_ConstGS()


stealth_dll.Script_ConstGSCount.restype = c_ushort


def GSCount():
    return stealth_dll.Script_ConstGSCount()


stealth_dll.Script_ConstMR.restype = c_ushort


def MR():
    return stealth_dll.Script_ConstMR()


stealth_dll.Script_ConstMRCount.restype = c_ushort


def MRCount():
    return stealth_dll.Script_ConstMRCount()


stealth_dll.Script_ConstNS.restype = c_ushort


def NS():
    return stealth_dll.Script_ConstNS()


stealth_dll.Script_ConstNSCount.restype = c_ushort


def NSCount():
    return stealth_dll.Script_ConstNSCount()


stealth_dll.Script_ConstSA.restype = c_ushort


def SA():
    return stealth_dll.Script_ConstSA()


stealth_dll.Script_ConstSACount.restype = c_ushort


def SACount():
    return stealth_dll.Script_ConstSACount()


stealth_dll.Script_ConstSS.restype = c_ushort


def SS():
    return stealth_dll.Script_ConstSS()


stealth_dll.Script_ConstSSCount.restype = c_ushort


def SSCount():
    return stealth_dll.Script_ConstSSCount()


# end region Reagents

# region Secure Trade
stealth_dll.Script_CancelTrade.argtypes = [c_ubyte]
stealth_dll.Script_CancelTrade.restype = c_bool


def CancelTrade(TradeNum):
    return stealth_dll.Script_CancelTrade(TradeNum)


stealth_dll.Script_CheckTradeState.restype = c_bool


def IsTrade():
    return stealth_dll.Script_CheckTradeState()


stealth_dll.Script_ConfirmTrade.argtypes = [c_ubyte]
stealth_dll.Script_ConfirmTrade.restype = c_void_p


def ConfirmTrade(TradeNum):
    return stealth_dll.Script_ConfirmTrade(TradeNum)


stealth_dll.Script_GetTradeContainer.argtypes = [c_ubyte, c_ubyte]
stealth_dll.Script_GetTradeContainer.restype = c_uint


def GetTradeContainer(TradeNum, Num):
    return stealth_dll.Script_GetTradeContainer(TradeNum, Num)


stealth_dll.Script_GetTradeCount.restype = c_ubyte


def TradeCount():
    return stealth_dll.Script_GetTradeCount()


stealth_dll.Script_GetTradeOpponent.argtypes = [c_ubyte]
stealth_dll.Script_GetTradeOpponent.restype = c_uint


def GetTradeOpponent(TradeNum):
    return stealth_dll.Script_GetTradeOpponent(TradeNum)


stealth_dll.Script_GetTradeOpponentName.argtypes = [c_ubyte]
stealth_dll.Script_GetTradeOpponentName.restype = c_wchar_p


def GetTradeOpponentName(TradeNum):
    return stealth_dll.Script_GetTradeOpponentName(TradeNum)


stealth_dll.Script_TradeCheck.argtypes = [c_ubyte, c_ubyte]
stealth_dll.Script_TradeCheck.restype = c_bool


def TradeCheck(TradeNum, Num):
    return stealth_dll.Script_TradeCheck(TradeNum, Num)


# end region Secure Trade

# region Self
# stealth_dll.Script_GetBuffBarInfo.argtypes = [Pointer, c_uint]
stealth_dll.Script_GetBuffBarInfo.restype = c_void_p


def GetBuffBarInfo():
    outLen = c_uint()
    stealth_dll.Script_GetBuffBarInfo(None, byref(outLen))

    if outLen.value > 0:
        byte_array = (c_ubyte * (outLen.value))()
        stealth_dll.Script_GetBuffBarInfo(byref(byte_array), byref(outLen))
        stream_position = 0

        Result = []
        tmp = c_ubyte()

        # Count : Byte
        memmove(addressof(tmp), addressof(byte_array), sizeof(c_ubyte))
        stream_position += sizeof(c_ubyte)

        # Buffs : array of TBuffIcon
        if tmp.value > 0:
            buff_icons = (TBuffIcon * tmp.value)()

            memmove(addressof(buff_icons), addressof(byte_array) + stream_position, (sizeof(TBuffIcon) * tmp.value))
            Result = [
                {'Attribute_ID': icon.Attribute_ID, 'TimeStart': TDateTimeToPyDateTime(icon.TimeStart),
                 'Seconds': icon.Seconds, 'ClilocID1': icon.ClilocID1,
                 'ClilocID2': icon.ClilocID1, } for icon in buff_icons]

    return Result


stealth_dll.Script_GetCharTitle.restype = c_wchar_p


def CharTitle():
    return stealth_dll.Script_GetCharTitle()


stealth_dll.Script_GetConnectedTime.restype = c_double


def ConnectedTime():
    return TDateTimeToPyDateTime(stealth_dll.Script_GetConnectedTime())


stealth_dll.Script_GetDisconnectedTime.restype = c_double


def DisconnectedTime():
    return TDateTimeToPyDateTime(stealth_dll.Script_GetDisconnectedTime())


stealth_dll.Script_GetLastAttack.restype = c_uint


def LastAttack():
    return stealth_dll.Script_GetLastAttack()


stealth_dll.Script_GetLastContainer.restype = c_uint


def LastContainer():
    return stealth_dll.Script_GetLastContainer()


stealth_dll.Script_GetLastObject.restype = c_uint


def LastObject():
    return stealth_dll.Script_GetLastObject()


stealth_dll.Script_GetLastStatus.restype = c_uint


def LastStatus():
    return stealth_dll.Script_GetLastStatus()


stealth_dll.Script_GetLastTarget.restype = c_uint


def LastTarget():
    return stealth_dll.Script_GetLastTarget()


stealth_dll.Script_GetSelfArmor.restype = c_ushort


def Armor():
    return stealth_dll.Script_GetSelfArmor()


stealth_dll.Script_GetSelfColdResist.restype = c_ushort


def ColdResist():
    return stealth_dll.Script_GetSelfColdResist()


stealth_dll.Script_GetSelfEnergyResist.restype = c_ushort


def EnergyResist():
    return stealth_dll.Script_GetSelfEnergyResist()


stealth_dll.Script_GetSelfFireResist.restype = c_ushort


def FireResist():
    return stealth_dll.Script_GetSelfFireResist()


stealth_dll.Script_GetSelfGold.restype = c_uint


def Gold():
    return stealth_dll.Script_GetSelfGold()


stealth_dll.Script_GetSelfID.restype = c_uint


def Self():
    return stealth_dll.Script_GetSelfID()


stealth_dll.Script_GetSelfMaxWeight.restype = c_ushort


def MaxWeight():
    return stealth_dll.Script_GetSelfMaxWeight()


stealth_dll.Script_GetSelfPetsCurrent.restype = c_ubyte


def PetsCurrent():
    return stealth_dll.Script_GetSelfPetsCurrent()


stealth_dll.Script_GetSelfPetsMax.restype = c_ubyte


def PetsMax():
    return stealth_dll.Script_GetSelfPetsMax()


stealth_dll.Script_GetSelfPoisonResist.restype = c_ushort


def PoisonResist():
    return stealth_dll.Script_GetSelfPoisonResist()


stealth_dll.Script_GetSelfRace.restype = c_ubyte


def Race():
    return stealth_dll.Script_GetSelfRace()


stealth_dll.Script_GetSelfSex.restype = c_ubyte


def Sex():
    return stealth_dll.Script_GetSelfSex()


stealth_dll.Script_GetSelfWeight.restype = c_ushort


def Weight():
    return stealth_dll.Script_GetSelfWeight()


stealth_dll.Script_GetWorldNum.restype = c_ubyte


def WorldNum():
    return stealth_dll.Script_GetWorldNum()


# end region Self

# region SetCatchBag
stealth_dll.Script_SetCatchBag.argtypes = [c_uint]
stealth_dll.Script_SetCatchBag.restype = c_ubyte


def SetCatchBag(ObjectID):
    return stealth_dll.Script_SetCatchBag(ObjectID)


stealth_dll.Script_UnsetCatchBag.restype = c_void_p


def UnsetCatchBag():
    return stealth_dll.Script_UnsetCatchBag()


# end region SetCatchBag

# region Shard Names
stealth_dll.Script_GetProfileShardName.restype = c_wchar_p


def ProfileShardName():
    return stealth_dll.Script_GetProfileShardName()


stealth_dll.Script_GetShardName.restype = c_wchar_p


def ShardName():
    return stealth_dll.Script_GetShardName()


# end region Shard Names

# region Shop
stealth_dll.Script_AutoBuy.argtypes = [c_ushort, c_ushort, c_ushort]
stealth_dll.Script_AutoBuy.restype = c_void_p


def AutoBuy(ItemType, ItemColor, Quantity):
    return stealth_dll.Script_AutoBuy(ItemType, ItemColor, Quantity)


stealth_dll.Script_AutoBuyEx.argtypes = [c_ushort, c_ushort, c_ushort, c_uint, c_wchar_p]
stealth_dll.Script_AutoBuyEx.restype = c_void_p


def AutoBuyEx(ItemType, ItemColor, Quantity, Price, ItemName):
    return stealth_dll.Script_AutoBuyEx(ItemType, ItemColor, Quantity, Price, ItemName)


stealth_dll.Script_AutoSell.argtypes = [c_ushort, c_ushort, c_ushort]
stealth_dll.Script_AutoSell.restype = c_void_p


def AutoSell(ItemType, ItemColor, Quantity):
    return stealth_dll.Script_AutoSell(ItemType, ItemColor, Quantity)


stealth_dll.Script_ClearShopList.restype = c_void_p


def ClearShopList():
    return stealth_dll.Script_ClearShopList()


stealth_dll.Script_GetAutoBuyDelay.restype = c_ushort


def GetAutoBuyDelay():
    return stealth_dll.Script_GetAutoBuyDelay()


stealth_dll.Script_GetAutoSellDelay.restype = c_ushort


def GetAutoSellDelay():
    return stealth_dll.Script_GetAutoSellDelay()


stealth_dll.Script_GetShopList.restype = c_wchar_p


def GetShopList():
    return stealth_dll.Script_GetShopList().splitlines()


stealth_dll.Script_SetAutoBuyDelay.argtypes = [c_ushort]
stealth_dll.Script_SetAutoBuyDelay.restype = c_void_p


def SetAutoBuyDelay(Value):
    return stealth_dll.Script_SetAutoBuyDelay(Value)


stealth_dll.Script_SetAutoSellDelay.argtypes = [c_ushort]
stealth_dll.Script_SetAutoSellDelay.restype = c_void_p


def SetAutoSellDelay(Value):
    return stealth_dll.Script_SetAutoSellDelay(Value)


# end region Shop

# region Stealth Info
stealth_dll.Script_GetStealthInfo.restype = TAboutData


def GetStealthInfo():
    AboutData = TAboutData()
    AboutData = stealth_dll.Script_GetStealthInfo()

    return {"StealthVersion": tuple(AboutData.StealthVersion),
            "Build": int(AboutData.Build),
            "BuildDate": TDateTimeToPyDateTime(AboutData.BuildDate),
            "SVNChangeset": int(AboutData.SVNChangeset)}


# end region Stealth Info

# region Target
stealth_dll.Script_CancelTarget.restype = c_void_p


def CancelTarget():
    return stealth_dll.Script_CancelTarget()


stealth_dll.Script_GetTargetID.restype = c_uint


def TargetID():
    return stealth_dll.Script_GetTargetID()


stealth_dll.Script_GetTargetStatus.restype = c_bool


def TargetPresent():
    return stealth_dll.Script_GetTargetStatus()


stealth_dll.Script_TargetToObject.argtypes = [c_uint]
stealth_dll.Script_TargetToObject.restype = c_void_p


def TargetToObject(ObjectID):
    return stealth_dll.Script_TargetToObject(ObjectID)


stealth_dll.Script_TargetToTile.argtypes = [c_ushort, c_ushort, c_ushort, c_byte]
stealth_dll.Script_TargetToTile.restype = c_void_p


def TargetToTile(TileModel, X, Y, Z):
    return stealth_dll.Script_TargetToTile(TileModel, X, Y, Z)


stealth_dll.Script_TargetToXYZ.argtypes = [c_ushort, c_ushort, c_byte]
stealth_dll.Script_TargetToXYZ.restype = c_void_p


def TargetToXYZ(X, Y, Z):
    return stealth_dll.Script_TargetToXYZ(X, Y, Z)


stealth_dll.Script_WaitForTarget.argtypes = [c_int]
stealth_dll.Script_WaitForTarget.restype = c_bool


def WaitForTarget(MaxWaitTimeMS):
    return stealth_dll.Script_WaitForTarget(MaxWaitTimeMS)


# end region Target

# region Tile Working
stealth_dll.Script_ConvertIntegerToFlags.argtypes = [c_ubyte, c_uint]
stealth_dll.Script_ConvertIntegerToFlags.restype = c_wchar_p


def ConvertIntegerToFlags(Group, Flags):
    return stealth_dll.Script_ConvertIntegerToFlags(Group, Flags).splitlines()

    # Map Cell


class TMapCell(Structure):
    _pack_ = 1
    _fields_ = [
        ('Tile', c_ushort),
        ('Z', c_byte),
    ]


# stealth_dll.Script_GetCell.argtypes = [c_ushort, c_ushort, c_ubyte]
stealth_dll.Script_GetCell.restype = TMapCell


def GetMapCell(X, Y, WorldNum):
    s = TMapCell()
    stealth_dll.Script_GetCell(byref(s), X, Y, WorldNum)
    return s


stealth_dll.Script_GetLandTileData.argtypes = [c_ushort]
stealth_dll.Script_GetLandTileData.restype = TLandTileData


def GetLandTileData(Tile):
    return stealth_dll.Script_GetLandTileData(Tile)


# stealth_dll.Script_GetLandTilesArray.argtypes = [c_ushort, c_ushort, c_ushort, c_ushort, c_ubyte, Pointer, c_uint,
# Pointer]
stealth_dll.Script_GetLandTilesArray.restype = c_ushort


def GetLandTilesArray(Xmin, Ymin, Xmax, Ymax, WorldNum, TileType):
    cnt = c_ushort(0)

    # we suppose TileType is iterable
    try:
        ArrayBytes = (c_ushort * len(TileType))()
        for cnt, tile in enumerate(TileType):
            ArrayBytes[cnt] = c_ushort(tile)
            # print(cnt, tile, ArrayBytes[cnt])
        cnt = stealth_dll.Script_GetLandTilesArray(Xmin, Ymin, Xmax, Ymax, WorldNum, byref(ArrayBytes),
                                                   2 * len(TileType), None)
    except TypeError:
        ArrayBytes = (c_ushort * 1)()
        ArrayBytes[0] = c_ushort(int(TileType))
        cnt = stealth_dll.Script_GetLandTilesArray(Xmin, Ymin, Xmax, Ymax, WorldNum, byref(ArrayBytes), 2, None)

    if cnt > 0:
        Result = (TFoundTile * cnt)()
        cnt = stealth_dll.Script_GetLandTilesArray(Xmin, Ymin, Xmax, Ymax, WorldNum, ArrayBytes, 2 * len(ArrayBytes),
                                                   byref(Result))
        return [(tile.Tile, tile.X, tile.Y, tile.Z) for tile in list(Result)]
    else:
        return []


stealth_dll.Script_GetLayerCount.argtypes = [c_ushort, c_ushort, c_ubyte]
stealth_dll.Script_GetLayerCount.restype = c_ubyte


def GetLayerCount(X, Y, WorldNum):
    return stealth_dll.Script_GetLayerCount(X, Y, WorldNum)


stealth_dll.Script_GetStaticTileData.argtypes = [c_ushort]
stealth_dll.Script_GetStaticTileData.restype = TStaticTileDataNew


def GetStaticTileData(Tile):
    return stealth_dll.Script_GetStaticTileData(Tile)


# stealth_dll.Script_GetStaticTilesArray.argtypes = [c_ushort, c_ushort, c_ushort, c_ushort, c_ubyte, Pointer, c_uint, Pointer]
stealth_dll.Script_GetStaticTilesArray.restype = c_ushort


def GetStaticTilesArray(Xmin, Ymin, Xmax, Ymax, WorldNum, TileType):
    cnt = c_ushort(0)

    # we suppose TileType is iterable
    try:
        ArrayBytes = (c_ushort * len(TileType))()
        for cnt, tile in enumerate(TileType):
            ArrayBytes[cnt] = c_ushort(tile)
            # print(cnt, tile, ArrayBytes[cnt])
        cnt = stealth_dll.Script_GetStaticTilesArray(Xmin, Ymin, Xmax, Ymax, WorldNum, byref(ArrayBytes),
                                                     2 * len(TileType), None)
    except TypeError:
        ArrayBytes = (c_ushort * 1)()
        ArrayBytes[0] = c_ushort(int(TileType))
        cnt = stealth_dll.Script_GetStaticTilesArray(Xmin, Ymin, Xmax, Ymax, WorldNum, byref(ArrayBytes), 2, None)

    if cnt > 0:
        Result = (TFoundTile * cnt)()
        cnt = stealth_dll.Script_GetStaticTilesArray(Xmin, Ymin, Xmax, Ymax, WorldNum, ArrayBytes, 2 * len(ArrayBytes),
                                                     byref(Result))
        return [(tile.Tile, tile.X, tile.Y, tile.Z) for tile in list(Result)]
    else:
        return []


stealth_dll.Script_GetSurfaceZ.argtypes = [c_ushort, c_ushort, c_ubyte]
stealth_dll.Script_GetSurfaceZ.restype = c_byte


def GetSurfaceZ(X, Y, WorldNum):
    return stealth_dll.Script_GetSurfaceZ(X, Y, WorldNum)


stealth_dll.Script_GetTileFlags.argtypes = [c_ubyte, c_ushort]
stealth_dll.Script_GetTileFlags.restype = c_uint


def GetTileFlags(TileGroup, Tile):
    if TileGroup not in [0, 'tfLand', 1, 'tfStatic']:
        raise ValueError('TileGroup can only have one of this values {}'.format([0, 'tfLand', 1, 'tfStatic']))

    if TileGroup == 'tfLand':
        TileGroup = 0
    elif TileGroup == 'tfStatic':
        TileGroup = 1

    return stealth_dll.Script_GetTileFlags(TileGroup, Tile)


stealth_dll.Script_IsWorldCellPassable.argtypes = [c_ushort, c_ushort, c_byte, c_ushort, c_ushort, c_byte, c_ubyte]
stealth_dll.Script_IsWorldCellPassable.restype = c_bool


def IsWorldCellPassable(CurrX, CurrY, CurrZ, DestX, DestY, varDestZ, WorldNum):
    return stealth_dll.Script_IsWorldCellPassable(CurrX, CurrY, CurrZ, DestX, DestY, varDestZ, WorldNum)


stealth_dll.Script_ReadStaticsXY.argtypes = [c_ushort, c_ushort, c_ubyte, c_void_p, c_void_p]
stealth_dll.Script_ReadStaticsXY.restype = c_void_p


def ReadStaticsXY(X, Y, WorldNum):
    outLen = c_uint()
    stealth_dll.Script_ReadStaticsXY(X, Y, WorldNum, None, byref(outLen))
    if outLen.value > 0:
        Result = (TStaticItemRealXY * (outLen.value // sizeof(TStaticItemRealXY)))()
        stealth_dll.Script_ReadStaticsXY(X, Y, WorldNum, byref(Result), byref(outLen))
        return list(Result)
    else:
        return []


# end region Tile Working

# region UseObject
stealth_dll.Script_UseFromGround.argtypes = [c_ushort, c_ushort]
stealth_dll.Script_UseFromGround.restype = c_uint


def UseFromGround(ObjType, Color):
    return stealth_dll.Script_UseFromGround(ObjType, Color)


stealth_dll.Script_UseObject.argtypes = [c_uint]
stealth_dll.Script_UseObject.restype = c_void_p


def UseObject(ObjectID):
    return stealth_dll.Script_UseObject(ObjectID)


stealth_dll.Script_UseType.argtypes = [c_ushort, c_ushort]
stealth_dll.Script_UseType.restype = c_uint


def UseType(ObjType, Color):
    return stealth_dll.Script_UseType(ObjType, Color)


# end region UseObject

# region UseSkill
stealth_dll.Script_UseSkill.argtypes = [c_wchar_p]
stealth_dll.Script_UseSkill.restype = c_bool


def UseSkill(SkillName):
    return stealth_dll.Script_UseSkill(SkillName)


# end region UseSkill

# region Virtues
stealth_dll.Script_ReqVirtuesGump.restype = c_void_p


def ReqVirtuesGump():
    return stealth_dll.Script_ReqVirtuesGump()


stealth_dll.Script_UseVirtue.argtypes = [c_wchar_p]
stealth_dll.Script_UseVirtue.restype = c_void_p


def UseVirtue(VirtueName):
    return stealth_dll.Script_UseVirtue(VirtueName)


# end region Virtues

# region Wait
stealth_dll.Script_Wait.argtypes = [c_int]
stealth_dll.Script_Wait.restype = c_void_p


def Wait(WaitTimeMS):
    return stealth_dll.Script_Wait(WaitTimeMS)


# end region Wait

# region WaitTarget
stealth_dll.Script_CancelWaitTarget.restype = c_void_p


def CancelWaitTarget():
    return stealth_dll.Script_CancelWaitTarget()


stealth_dll.Script_WaitTargetGround.argtypes = [c_ushort]
stealth_dll.Script_WaitTargetGround.restype = c_void_p


def WaitTargetGround(ObjType):
    return stealth_dll.Script_WaitTargetGround(ObjType)


stealth_dll.Script_WaitTargetLast.restype = c_void_p


def WaitTargetLast():
    return stealth_dll.Script_WaitTargetLast()


stealth_dll.Script_WaitTargetObject.argtypes = [c_uint]
stealth_dll.Script_WaitTargetObject.restype = c_void_p


def WaitTargetObject(ObjID):
    return stealth_dll.Script_WaitTargetObject(ObjID)


stealth_dll.Script_WaitTargetSelf.restype = c_void_p


def WaitTargetSelf():
    return stealth_dll.Script_WaitTargetSelf()


stealth_dll.Script_WaitTargetTile.argtypes = [c_ushort, c_ushort, c_ushort, c_byte]
stealth_dll.Script_WaitTargetTile.restype = c_void_p


def WaitTargetTile(Tile, X, Y, Z):
    return stealth_dll.Script_WaitTargetTile(Tile, X, Y, Z)


stealth_dll.Script_WaitTargetType.argtypes = [c_ushort]
stealth_dll.Script_WaitTargetType.restype = c_void_p


def WaitTargetType(ObjType):
    return stealth_dll.Script_WaitTargetType(ObjType)


stealth_dll.Script_WaitTargetXYZ.argtypes = [c_ushort, c_ushort, c_byte]
stealth_dll.Script_WaitTargetXYZ.restype = c_void_p


def WaitTargetXYZ(X, Y, Z):
    return stealth_dll.Script_WaitTargetXYZ(X, Y, Z)


# end region WaitTarget

# region Work with paperdoll scrolls
stealth_dll.Script_UseOtherPaperdollScroll.argtypes = [c_uint]
stealth_dll.Script_UseOtherPaperdollScroll.restype = c_void_p


def UseOtherPaperdollScroll(ID):
    return stealth_dll.Script_UseOtherPaperdollScroll(ID)


stealth_dll.Script_UseSelfPaperdollScroll.restype = c_void_p


def UseSelfPaperdollScroll():
    return stealth_dll.Script_UseSelfPaperdollScroll()


# end region Work with paperdoll scrolls

# region Skype
stealth_dll.Script_Skype_Connected.restype = c_bool


def Skype_Connected():
    return stealth_dll.Script_Skype_Connected()


stealth_dll.Script_Skype_Connect.argtypes = [c_wchar_p, c_wchar_p]
stealth_dll.Script_Skype_Connect.restype = c_void_p


def Skype_Connect(login, password):
    return stealth_dll.Script_Skype_Connect(login, password)


stealth_dll.Script_Skype_Disconnect.restype = c_void_p


def Skype_Disconnect():
    return stealth_dll.Script_Skype_Disconnect()


stealth_dll.Script_Skype_SendMessage.argtypes = [c_wchar_p, c_wchar_p]
stealth_dll.Script_Skype_SendMessage.restype = c_void_p


def Skype_SendMessage(msg, user_id):
    return stealth_dll.Script_Skype_SendMessage(msg, user_id)


stealth_dll.Script_Skype_GetNicknameByID.argtypes = [c_wchar_p]
stealth_dll.Script_Skype_GetNicknameByID.restype = c_wchar_p


def Skype_GetNicknameByID(user_id):
    return stealth_dll.Script_Skype_GetNicknameByID(user_id)


stealth_dll.Script_Skype_GetIDByNickname.argtypes = [c_wchar_p]
stealth_dll.Script_Skype_GetIDByNickname.restype = c_wchar_p


def Skype_GetIDByNickname(user_name):
    return stealth_dll.Script_Skype_GetIDByNickname(user_name)
