 unit stealth_script;

interface
uses
  windows,
  UITypes,
  Classes,
  Vcl.Forms,
  Vcl.Graphics,
  Rtti,TypInfo,
  SysUtils;

const
  ConstScriptDLL = 'Script.dll';

{$Region 'Script consts'}
Const
//Layers
RhandLayer = $01;
LhandLayer = $02;
ShoesLayer = $03;
PantsLayer = $04;
ShirtLayer = $05;
HatLayer   = $06;
GlovesLayer= $07;
RingLayer  = $08;
TalismanLayer= $09;
NeckLayer  = $0A;
HairLayer  = $0B;
WaistLayer = $0C;
TorsoLayer = $0D;
BraceLayer = $0E;
BeardLayer = $10;
TorsoHLayer= $11;
EarLayer   = $12;
ArmsLayer  = $13;
CloakLayer = $14;
BpackLayer = $15;
RobeLayer  = $16;
EggsLayer  = $17;
LegsLayer  = $18;
HorseLayer = $19;
RstkLayer  = $1A;
NRstkLayer = $1B;
SellLayer  = $1C;
BankLayer  = $1D;
//Regs
BP = $F7A;
BM = $F7B;
GA = $F84;
GS = $F85;
MR = $F86;
NS = $F88;
SA = $F8C;
SS = $F8D;

//Skype
  evCode_Connected = 0;
  evCode_ClientDisconnected = 1;
  evCode_ServerDisconnected = 2;
  evCode_MsgReceived = 3;
  evCode_Error = 4;

{$Endregion}

{$Region 'Events types'}
type
  TPacketEvent =  (evItemInfo=0, evItemDeleted=1, evSpeech=2, evDrawGamePlayer=3,
                  evMoveRejection=4, evDrawContainer=5, evAddItemToContainer=6,
                  evAddMultipleItemsInCont = 7, evRejectMoveItem = 8, evUpdateChar = 9,

                  evDrawObject = 10, evMenu = 11, evMapMessage = 12, evAllow_RefuseAttack = 13,
                  evClilocSpeech = 14, evClilocSpeechAffix = 15, evUnicodeSpeech = 16,
                  evBuff_DebuffSystem = 17, evClientSendResync = 18, evCharAnimation = 19,

                  evICQDisconnect = 20, evICQConnect = 21, evICQIncomingText = 22, evICQError = 23,
                  evIncomingGump = 24, evTimer1 = 25, evTimer2 = 26,
                  evWindowsMessage = 27, evSound = 28, evDeath = 29,

                  evQuestArrow = 30, evPartyInvite = 31, evMapPin = 32, evGumpTextEntry = 33,
                  evGraphicalEffect = 34, evIRCIncomingText = 35, evSkypeEvent = 36,
                  evSetGlobalVar = 37, evUpdateObjStats = 38);

  TEvItemInfoCallBack = procedure (ItemID:Cardinal);stdcall;
  TEvItemDeletedCallBack = procedure (ItemID:Cardinal);stdcall;
  TEvSpeechCallBack = procedure (Text, SenderName : String; SenderID:Cardinal);stdcall;
  TEvDrawGamePlayerCallBack = procedure (ID:Cardinal);stdcall;
  TEvMoveRejectionCallBack = procedure (Xorig, Yorig : Word; Dir : Byte; X, Y : Word);stdcall;
  TEvDrawContainerCallBack = procedure (ContainerID:Cardinal; ModelGump : Word);stdcall;
  TEvAddItemToContainerCallBack = procedure (ItemID, ContainerID:Cardinal);stdcall;
  TEvAddMultipleItemsInContCallBack = procedure (ContainerID:Cardinal);stdcall;
  TEvRejectMoveItemCallBack = procedure (Reason : Byte);stdcall;
  TEvUpdateCharCallBack = procedure (ID:Cardinal);stdcall;
  TEvDrawObjectCallBack = procedure (ContainerID:Cardinal);stdcall;
  TEvMenuCallBack = procedure (DialogID : Cardinal; MenuID : Word);stdcall;
  TEvMapMessageCallBack = procedure (ID:Cardinal; centerx, centery : Integer);stdcall;
  TEvAllow_RefuseAttackCallBack = procedure (ID:Cardinal; AttackAllowed : Boolean);stdcall;
  TEvClilocSpeechCallBack = procedure (SenderID : Cardinal; SenderName : String; ClilocID : Cardinal;ClilocText : String);stdcall;
  TEvClilocSpeechAffixCallBack = procedure (SenderID : Cardinal; SenderName : String; ClilocID : Cardinal;Affix, ClilocText : String);stdcall;
  TEvUnicodeSpeechCallBack = procedure (Text, SenderName : String; SenderID:Cardinal);stdcall;
  TEvBuff_DebuffSystemCallBack = procedure (ID:Cardinal; Attribute_ID : Word; IsEnabled : Boolean);stdcall;
  TEvClientSendResyncCallBack = procedure ();stdcall;
  TEvCharAnimationCallBack = procedure (ID:Cardinal; Action : Word);stdcall;
  TEvICQDisconnectCallBack = procedure();stdcall;
  TEvICQConnectCallBack = procedure();stdcall;
  TEvICQIncomingTextCallBack = procedure (UIN : Cardinal; Text : String);stdcall;
  TEvICQErrorCallBack = procedure (Text : String);stdcall;
  TEvIncomingGumpCallBack = procedure (GumpSerial, GumpID, X, Y:Cardinal);stdcall;
  TEvTimerCallBack = procedure ();stdcall;
  TEvWindowsMessageCallBack = procedure (lParam:Cardinal);stdcall;
  TEvSoundCallBack = procedure(Sound_ID, X, Y, Z : Word);stdcall;
  TEvDeathCallBack = procedure(IsDead : Boolean);stdcall;
  TEvQuestArrowCallBack = procedure(fQuestArrowX, fQuestArrowY : Word; fQuestArrowActive : Boolean);stdcall;
  TEvPartyInviteCallBack = procedure(Inviter_ID : Cardinal);stdcall;
  TEvMapPinCallBack = procedure(ID : Cardinal; Action, PinID : Byte; X, Y : Word);stdcall;
  TEvGumpTextEntryCallBack = procedure(ID : Cardinal; Title : String; InputStyle : Byte; MaxValue : Cardinal; Title2 : String);
  TEvGraphicalEffectCallBack = procedure(srcID : Cardinal; srcX, srcY : Word; srcZ : Smallint;
                                 destID : Cardinal; destX, destY : Word; destZ : Smallint;
                                 _type : Byte; itemID : Word; fixedDir : Byte); stdcall;
  TEvIRCIncomingTextCallBack = procedure(IRCMessage : String); stdcall;
  TEvSkypeEventCallBack = procedure(SenderNickName : String; SenderId : String; EventMsg : String; EventCode : Byte); stdcall;
  TEvSetGlobalVarCallBack = procedure(VarName : String; VarValue : String); stdcall;
  TEvUpdateObjStatsCallBack = procedure(ID : Cardinal; CurLife,MaxLife,CurMana,MaxMana,CurStam,MaxStam : Integer); stdcall;
 {$EndRegion}

{$Region 'Script types'}
type
  TStepResult = (srError, srResync,srBufferFull,srNotPassable,srTimeOut,
                 srServReject,srSendStep, srStepAccepted);
  // 0 - Unknown Error
  // 1 - Mover: Resync is pending, ignoring.
  // 2 - Mover: Step buffer overflow, Ignoring
  // 3 - Mover: Client Canceled. Point not Passable.
  // 4 - Mover: Move timeout.
  // 5 - Mover: MoveReject
  // 6 - Mover: Client Check OK, send move request
  // 7 - Mover: Server Check OK, move request accepted

  TVarRegion = (reg_stealth, reg_char);
  TUIWindowType = (wtPaperdoll, wtStatus, wtCharProfile, wtContainer);

  cararr = TArray<Cardinal>;
  PCarArray = ^cararr;

  TSkillState = (ssUp, ssDown, ssLock);
  TLOSCheckType = (losSphere = 1, losSphereAdv = 2, losPOL = 3, losRunUO = 4);
  TLOSCheckOption = (losSphereCheckCorners,losPolUseNoShoot,losPolLOSThroughWindow);
  TLOSCheckOptions = set of TLOSCheckOption;

  TAboutData = record
    StealthVersion : array[0..2] of Word;
    Build : Word;
    BuildDate : TDateTime;
    SVNChangeset : Word;
  end;

  TBuffIcon = packed record
    Attribute_ID : Word;
    TimeStart : TDateTime;
    Seconds : Word;
    ClilocID1 : Cardinal;
    ClilocID2 : Cardinal;
  end;
  PBuffIcon = ^TBuffIcon;

  TBuffBarInfo = packed record
    Count : Byte;
    Buffs : array of TBuffIcon;
  end;
  PBuffBarInfo = ^TBuffBarInfo;



 {$EndRegion}

{$Region 'TExtendedInfo'}
type
  TExtendedInfo = record
    MaxWeight : Word;
    Race : Byte;
    StatCap : Word;
    PetsCurrent : Byte;
    PetsMax : Byte;
    FireResist : Word;
    ColdResist : Word;
    PoisonResist : Word;
    EnergyResist : Word;
    Luck : Smallint;
    DamageMin : Word;
    DamageMax : Word;
    Tithing_points : Cardinal; //Tithing points (Paladin Books)
    Hit_Chance_Incr,
    Swing_Speed_Incr,
    Damage_Incr,
    Lower_Reagent_Cost,
    HP_Regen,
    Stam_Regen,
    Mana_Regen,
    Reflect_Phys_Damage,
    Enhance_Potions,
    Defense_Chance_Incr,
    Spell_Damage_Incr,
    Faster_Cast_Recovery,
    Faster_Casting,
    Lower_Mana_Cost,
    Strength_Incr,
    Dext_Incr,
    Int_Incr,
    HP_Incr,
    Stam_Incr,
    Mana_Incr,
    Max_HP_Incr,
    Max_Stam_Incr,
    Max_Mana_Increase : Word;
  end;
{$EndRegion}

{$Region 'Gumpinfo'}
type
  TGroup = packed record
    groupnumber : Integer;
    Page : Integer;
    ElemNum : Integer;
  end;

  TEndGroup = packed record
    groupnumber : Integer;
    Page : Integer;
    ElemNum : Integer;
  end;

  TPage = packed record
    Page : Integer;
    ElemNum : Integer;
  end;

  TMasterGump = packed record
    ID : Cardinal;
    ElemNum : Integer;
 end;

  TGumpButton = packed record
    x, y : Integer;
    released_id : Integer;
    pressed_id : Integer;
    quit : Integer;
    page_id : Integer;
    return_value : Integer;
    Page : Integer;
    ElemNum : Integer;
  end;

  TButtonTileArt = packed record
    x, y : Integer;
    released_id : Integer;
    pressed_id : Integer;
    quit : Integer;
    page_id : Integer;
    return_value : Integer;
    art_id : Integer;
    Hue :  Integer;
    art_x, art_y : Integer;
    ElemNum : Integer;
  end;

  TCheckBox = packed record
    x, y : Integer;
    released_id : Integer;
    pressed_id : Integer;
    status : Integer;
    return_value : Integer;
    Page : Integer;
    ElemNum : Integer;
  end;

  TCheckerTrans = packed record   //transparent rectangle
    x, y : Integer;
    width, height : Integer;
    Page : Integer;
    ElemNum : Integer;
  end;

  TCroppedText = packed record  //text is cropped to the defined area
    x, y,width, height,color,text_id : Integer;
    Page : Integer;
    ElemNum : Integer;
  end;

  TGumpPic = packed record
    x, y : Integer;
    id : Integer;
    Hue : Integer;
    Page : Integer;
    ElemNum : Integer;
  end;

  TGumpPicTiled = packed record   //tiled by images
    x, y : Integer;
    width, height : Integer;
    gump_id : Integer;
    Page : Integer;
    ElemNum : Integer;
  end;

  TRadio = packed record
    x, y : Integer;
    released_id : Integer;
    pressed_id : Integer;
    status : Integer;
    return_value : Integer;
    Page : Integer;
    ElemNum : Integer;
  end;

  TResizePic = packed record
    x, y : Integer;
    gump_id : Integer;
    width, height : Integer;
    Page : Integer;
    ElemNum : Integer;
  end;

  TGumpText = packed record
    x, y, color : Integer;
    text_id : Integer;
    Page : Integer;
    ElemNum : Integer;
  end;

  TTextEntry = packed record
    x, y, width, height, color : Integer;
    return_value : Integer;
    default_text_id : Integer;
    Page : Integer;
    ElemNum : Integer;
  end;

  TTextEntryLimited = packed record
    x, y, width, height, color : Integer;
    return_value : Integer;
    default_text_id : Integer;
    Limit : Integer;
    Page : Integer;
    ElemNum : Integer;
  end;

  TTilePic = packed record
    x, y : Integer;
    id : Integer;
    Page : Integer;
    ElemNum : Integer;
  end;

  TTilePichue = packed record
    x, y : Integer;
    id : Integer;
    color : Integer;
    Page : Integer;
    ElemNum : Integer;
  end;

  TTooltip = packed record
    Cliloc_ID : Cardinal;
    Page : Integer;
    ElemNum : Integer;
  end;

  THtmlGump = packed record
    x, y : Integer;
    width, height : Integer;
    text_id : Integer;
    background : Integer;
    scrollbar : Integer;
    Page : Integer;
    ElemNum : Integer;
  end;

  TXmfHTMLGump = packed record
    x, y : Integer;
    width, height : Integer;
    Cliloc_id : Cardinal;
    background : Integer;
    scrollbar : Integer;
    Page : Integer;
    ElemNum : Integer;
  end;

  TXmfHTMLGumpColor = packed record
    x, y : Integer;
    width, height : Integer;
    Cliloc_id : Cardinal;
    background : Integer;
    scrollbar : Integer;
    Hue :  Integer;
    Page : Integer;
    ElemNum : Integer;
  end;

  TXmfHTMLTok =  packed record
    x, y : Integer;
    width, height : Integer;
    background : Integer;
    scrollbar : Integer;
    Color : Integer;
    Cliloc_id : Cardinal;
    Arguments : String;
    Page : Integer;
    ElemNum : Integer;
  end;

  type
  TItemProperty = packed record
    Prop : Cardinal;
    ElemNum : Integer;
  end;

type
  TUnknownItem = packed record
    CmdName : String;
    Arguments : String;
    ElemNum : Integer;
  end;

type
	TGumpInfo = packed record
    Serial : Cardinal;
    GumpID : Cardinal;
    X : Word;
    Y : Word;
    Pages : Integer;
    NoMove : Boolean;
    NoResize : Boolean;
    NoDispose : Boolean;
    NoClose : Boolean;


    Groups : array of TGroup;
    EndGroups : array of TEndGroup;
    GumpButtons : array of TGumpButton;
    ButtonTileArts : array of TButtonTileArt;
    CheckBoxes : array of TCheckBox;
    CheckerTrans : array of TCheckerTrans;
    CroppedText : array of TCroppedText;
    GumpPics : array of TGumpPic;
    GumpPicTiled : array of TGumpPicTiled;
    RadioButtons : array of TRadio;
    ResizePics : array of TResizePic;
    GumpText : array of TGumpText;
    TextEntries : array of TTextEntry;
    Text : array of string;
    TextEntriesLimited : array of TTextEntryLimited;
    TilePics : array of TTilePic;
    TilePicHue : array of TTilePicHue;
    Tooltips : array of TTooltip;
    HtmlGump : array of THtmlGump;
    XmfHtmlGump : array of TXmfHtmlGump;
    XmfHTMLGumpColor : array of TXmfHTMLGumpColor;
    XmfHTMLTok : array of TXmfHTMLTok;
    ItemProperties : array of TItemProperty;
	end;

{$Endregion}

{$Region 'UO-files types'}
  TileFlagsType = (tfLand, tfStatic);

  TTileDataFlags = (
    tsfBackground,
    tsfWeapon,
    tsfTransparent,
    tsfTranslucent,
    tsfWall,
    tsfDamaging,
    tsfImpassable,
    tsfWet,
    tsfUnknown,
    tsfSurface,
    tsfBridge,
    tsfGeneric,
    tsfWindow,
    tsfNoShoot,
    tsfPrefixA,
    tsfPrefixAn,
    tsfInternal,
    tsfFoliage,
    tsfPartialHue,
    tsfUnknown1,
    tsfMap,
    tsfContainer,
    tsfWearable,
    tsfLightSource,
    tsfAnimated,
    tsfNoDiagonal,
    tsfUnknown2,
    tsfArmor,
    tsfRoof,
    tsfDoor,
    tsfStairBack,
    tsfStairRight,
    tlfTranslucent,
    tlfWall,
    tlfDamaging,
    tlfImpassable,
    tlfWet,
    tlfSurface,
    tlfBridge,
    tlfPrefixA,
    tlfPrefixAn,
    tlfInternal,
    tlfMap,
    tlfUnknown3);
  TTileDataFlagSet = set of TTileDataFlags;

  TLandTileData = record   //HS
    Flags : Cardinal;
    Flags2 : Cardinal;
    TextureID : word;
    Name :  array[0..19] of AnsiChar;
  end;

  TStaticData = record
    Graphic : word;
    X : byte;
    Y : byte;
    Z : shortint;
    Tag : word;
  end;

  TStaticTileData = record
    Flags : UInt64;
    Weight,
    Height : Integer;
    RadarColorRGBA : array[0..3] of Byte;
    Name : array[0..19] of AnsiChar;
    //end
  end;


  TStaticItemRealXY = record
    Tile : Word;
    X : Word;
    Y : Word;
    Z : shortint;
    Color : Word;
  end;

  TMapCell = packed record
    Tile : Word;
    Z : Shortint;
  end;

  TStaticCellRealXY = packed record
    Statics : array of TStaticItemRealXY;
    StaticCount : Byte;
  end;

  TFoundTile = packed record
    Tile : Word;
    X : SmallInt;
    Y : SmallInt;
    Z : ShortInt;
  end;

  {$A+}

  TFoundTilesArray = array of TFoundTile;

  Ttargetinfo = packed record
    ID : Cardinal;
    Tile : Word;
    X, Y : Word;
    Z :  ShortInt;
  end;

  TMsgDlgType = UITypes.TMsgDlgType;

  TMsgDlgBtn = UITypes.TMsgDlgBtn;

  TMsgDlgButtons = UITypes.TMsgDlgButtons;

{$Region 'MapFigures types'}
  TFigureCoord = (fcWorld, fcScreen);
  TFigureKind  = (fkLine, fkEllipse, fkRectangle, fkDirection, fkText);

  TMapFigure = packed record
    kind : TFigureKind;
    coord : TFigureCoord;

    x1, y1 : Integer;
    x2, y2 : Integer;

    brushColor : TColor;
    brushStyle : TBrushStyle;
    color : TColor;
    text :  String;
  end;
  TMapFiguresArray = TArray<TMapFigure>;
 {$EndRegion}

{$EndRegion}

{$Region'Other'}
type TClilocItemRec = record
  ClilocID : Cardinal;
  Params : array of String;
end;

type TClilocRec = record
  Count : Cardinal;
  Items : array of TClilocItemRec;
end;

  TContextMenuRec = record
    Tag: Word;
    Flags: Word;
    ClilocStr : String;
  end;


  TMyPoint = packed record
    X : Word;
    Y : Word;
    Z : ShortInt;
  end;
TPathArray = array[0..999] of TMyPoint;


TScriptExecMethod = reference to procedure;
{$Endregion}



{$TYPEINFO ON}
{$Region 'Script classes(records)'}
  TMyChar = record
    private
      function GetCharName : String;
      function GetSelfID : Cardinal;
      function GetSelfSex : Byte;
      function GetCharTitle : String;
      function GetSelfGold : Cardinal;
      function GetSelfArmor : Word;
      function GetSelfWeight : Word;
      function GetSelfMaxWeight : Word;
      function GetSelfRace : Byte;
      function GetSelfPetsMax : Byte;
      function GetSelfPetsCurrent : Byte;
      function GetSelfFireResist : Word;
      function GetSelfColdResist : Word;
      function GetSelfPoisonResist : Word;
      function GetSelfEnergyResist : Word;
      function GetBackpackID : Cardinal;
      function GetSelfStr : Integer;
      function GetSelfInt : Integer;
      function GetSelfDex : Integer;
      function GetSelfLife : Integer;
      function GetSelfMana : Integer;
      function GetSelfStam : Integer;
      function GetSelfMaxLife : Integer;
      function GetSelfMaxMana : Integer;
      function GetSelfMaxStam : Integer;
      function GetSelfLuck : Integer;
      function GetExtInfo : TExtendedInfo;
      function GetHiddenStatus : Boolean;
      function GetPoisonedStatus : Boolean;
      function GetParalyzedStatus : Boolean;
      function GetDeadStatus : Boolean;
      function GetWarModeStatus : Boolean;
      procedure SetWarMode(Value : Boolean);
      function GetBuffBarInfo : TBuffBarInfo;
    public
      function WarTargetID : Cardinal;
      procedure Attack(AttackedID : Cardinal);
      procedure UseSelfPaperdollScroll;
      procedure UseOtherPaperdollScroll(ID : Cardinal);
      function ObjAtLayer(LayerType : Byte) : Cardinal;

      property CharName : String read GetCharName;
      property Self : Cardinal read GetSelfID;
      property ID : Cardinal read GetSelfID;
      property Sex : Byte read GetSelfSex;
      property CharTitle : String read GetCharTitle;
      property Gold : Cardinal read GetSelfGold;
      property Armor : Word read GetSelfArmor;
      property Weight : Word read GetSelfWeight;
      property MaxWeight : Word read GetSelfMaxWeight;
      property Race : Byte read GetSelfRace;
      property PetsMax : Byte read GetSelfPetsMax;
      property PetsCurrent : Byte read GetSelfPetsCurrent;
      property Luck : Integer read GetSelfLuck;
      property FireResist : Word read GetSelfFireResist;
      property ColdResist : Word read GetSelfColdResist;
      property PoisonResist : Word read GetSelfPoisonResist;
      property EnergyResist : Word read GetSelfEnergyResist;
      property Backpack : Cardinal read GetBackpackID;

      property Str : Integer read GetSelfStr;
      property Int : Integer read GetSelfInt;
      property Dex : Integer read GetSelfDex;
      property Life : Integer read GetSelfLife;
      property Mana : Integer read GetSelfMana;
      property Stam : Integer read GetSelfStam;
      property MaxLife : Integer read GetSelfMaxLife;
      property MaxMana : Integer read GetSelfMaxMana;
      property MaxStam : Integer read GetSelfMaxStam;
      property ExtInfo : TExtendedInfo read GetExtInfo;
      property Hidden : Boolean read GetHiddenStatus;
      property Poisoned : Boolean read GetPoisonedStatus;
      property Paralyzed : Boolean read GetParalyzedStatus;
      property Dead : Boolean read GetDeadStatus;
      property WarMode : Boolean read GetWarModeStatus write SetWarMode;
      property BuffBarInfo : TBuffBarInfo read GetBuffBarInfo;
   end;

  TUOObject = class
    private
      fObjID : Cardinal;
    public
      constructor Create(ObjID : Cardinal);
      function X : Integer;
      class function GetX(ObjID : Cardinal) : Integer;
      function Y : Integer;
      class function GetY(ObjID : Cardinal) : Integer;
      function Z : ShortInt;
      class function GetZ(ObjID : Cardinal) : ShortInt;
      function Name : String;
      class function GetName(ObjID : Cardinal) : String;
      function AltName : String;
      class function GetAltName(ObjID : Cardinal) : String;
      function Title : String;
      class function GetTitle(ObjID : Cardinal) : String;
      function GetClilocRec : TClilocRec; overload;
      class function GetClilocRec(ObjID : Cardinal) : TClilocRec; overload;
      function GetTooltip : String; overload;
      class function GetTooltip(ObjID : Cardinal) : String; overload;
      function ObjType : Word;
      class function GetType(ObjID : Cardinal) : Word;
      function GetQuantity : Integer; overload;
      class function GetQuantity(ObjID : Cardinal) : Integer; overload;
      function IsObjectExists : Boolean; overload;
      class function IsObjectExists(ObjID : Cardinal) : Boolean; overload;
      function IsNPC : Boolean; overload;
      class function IsNPC(ObjID : Cardinal) : Boolean; overload;
      function GetPrice : Cardinal; overload;
      class function GetPrice(ObjID : Cardinal) : Cardinal; overload;
      function GetDirection : Byte; overload;
      class function GetDirection(ObjID : Cardinal) : Byte; overload;
      function GetDistance : Integer; overload;
      class function GetDistance(ObjID : Cardinal) : Integer; overload;
      function GetColor : Word; overload;
      class function GetColor(ObjID : Cardinal) : Word; overload;
      function GetStr : Integer; overload;
      class function GetStr(ObjID : Cardinal) : Integer; overload;
      function GetInt : Integer; overload;
      class function GetInt(ObjID : Cardinal) : Integer; overload;
      function GetDex : Integer; overload;
      class function GetDex(ObjID : Cardinal) : Integer; overload;
      function GetHP : Integer; overload;
      class function GetHP(ObjID : Cardinal) : Integer; overload;
      class function GetHP(ObjID,TimeOutMS : Cardinal) : Integer; overload;
      function GetMaxHP : Integer; overload;
      class function GetMaxHP(ObjID : Cardinal) : Integer; overload;
      class function GetMaxHP(ObjID,TimeOutMS : Cardinal) : Integer;overload;
      function GetMana : Integer; overload;
      class function GetMana(ObjID : Cardinal) : Integer; overload;
      function GetMaxMana : Integer; overload;
      class function GetMaxMana(ObjID : Cardinal) : Integer; overload;
      function GetStam : Integer; overload;
      class function GetStam(ObjID : Cardinal) : Integer; overload;
      function GetMaxStam : Integer; overload;
      class function GetMaxStam(ObjID : Cardinal) : Integer; overload;
      function GetNotoriety : Byte; overload;
      class function GetNotoriety(ObjID : Cardinal) : Byte; overload;
      function GetParent : Cardinal; overload;
      class function GetParent(ObjID : Cardinal) : Cardinal; overload;
      function IsWarMode : Boolean; overload;
      class function IsWarMode(ObjID : Cardinal) : Boolean; overload;
      function IsDead : Boolean; overload;
      class function IsDead(ObjID : Cardinal) : Boolean; overload;
      function IsRunning : Boolean; overload;
      class function IsRunning(ObjID : Cardinal) : Boolean; overload;
      function IsContainer : Boolean; overload;
      class function IsContainer(ObjID : Cardinal) : Boolean; overload;
      function IsHidden : Boolean; overload;
      class function IsHidden(ObjID : Cardinal) : Boolean; overload;
      function IsMovable : Boolean; overload;
      class function IsMovable(ObjID : Cardinal) : Boolean; overload;
      function IsYellowHits : Boolean; overload;
      class function IsYellowHits(ObjID : Cardinal) : Boolean; overload;
      function IsPoisoned : Boolean; overload;
      class function IsPoisoned(ObjID : Cardinal) : Boolean; overload;
      function IsParalyzed : Boolean; overload;
      class function IsParalyzed(ObjID : Cardinal) : Boolean; overload;
      function IsFemale : Boolean; overload;
      class function IsFemale(ObjID : Cardinal) : Boolean; overload;
      function ObjAtLayerEx(LayerType : Byte) : Cardinal; overload;
      class function ObjAtLayerEx(LayerType : Byte; PlayerID : Cardinal) : Cardinal; overload;
      function GetLayer : Byte; overload;
      class function GetLayer(ObjID : Cardinal) : Byte; overload;
      procedure RequestStats; overload;
      class procedure RequestStats(ObjID : Cardinal); overload;
   end;

  TFindEngine = record
    private
      procedure SetFindDistance(Value : Cardinal);
      function GetFindDistance : Cardinal;
      procedure SetFindVertical(Value : Cardinal);
      function GetFindVertical : Cardinal;
      procedure SetFindInNulPoint(Value : Boolean);
      function GetFindInNulPoint : Boolean;
    public
      function FindTypeEx(ObjType : Word; Color : Word; Container : Cardinal; InSub : Boolean) : Cardinal;
      function FindType(ObjType : Word; Container : Cardinal) : Cardinal;
      function FindTypesArrayEx(ObjTypes, Colors : Array of word; Containers : Array of Cardinal; InSub : Boolean) : Cardinal;
      function FindNotoriety(ObjType : Word; Notoriety : Byte) : Cardinal;
      function FindAtCoord(X, Y : Word) : Cardinal;
      procedure Ignore(ObjID : Cardinal);
      procedure IgnoreRemove(ObjID : Cardinal);
      procedure IgnoreReset;
      function GetIgnoreList : TArray<Cardinal>;
      function GetFindedList : TArray<Cardinal>;
      function FindItem : Cardinal;
      function FindCount : Integer;
      function FindQuantity : Integer;
      function FindFullQuantity : Integer;
      property FindDistance : Cardinal read GetFindDistance write SetFindDistance;
      property FindVertical : Cardinal read GetFindVertical write SetFindVertical;
      property FindInNulPoint : Boolean read GetFindInNulPoint write SetFindInNulPoint;
    end;

  TMoveItemEngine = record
    private
      function GetDropCheckCoord : Boolean;
      procedure SetDropCheckCoord(Value : Boolean);
      function GetDropDelay : Cardinal;
      procedure SetDropDelay(Value : Cardinal);
    public
      function DragItem(ItemID : Cardinal; Count : Integer) : Boolean;
      function DropItem(MoveIntoID : Cardinal; X, Y : Word; Z : ShortInt) : Boolean;
      function MoveItem(ItemID : Cardinal; Count : Integer; MoveIntoID : Cardinal; X, Y : Word; Z : ShortInt) : Boolean;
      function Grab(ItemID : Cardinal; Count : Integer) : Boolean;
      function Drop(ItemID : Cardinal; Count : Integer; X, Y : Smallint; Z : ShortInt) : Boolean;
      function DropHere(ItemID : Cardinal) : Boolean;
      function MoveItems(Container : Cardinal; ItemsType : Word; ItemsColor : Word; MoveIntoID : Cardinal; X, Y : Word; Z : ShortInt; DelayMS : Integer) : Boolean;
      function EmptyContainer(Container, DestContainer : Cardinal; delay_ms : Word) : Boolean;
      property DropCheckCoord : Boolean read GetDropCheckCoord write SetDropCheckCoord;
      property DropDelay : Cardinal read GetDropDelay write SetDropDelay;
  end;

  TSecureTrade = record
    public
      function CheckTradeState : Boolean;
      function GetTradeContainer(TradeNum, Num : Byte) : Cardinal;
      function GetTradeOpponent(TradeNum : Byte) : Cardinal;
      function GetTradeCount : Byte;
      function GetTradeOpponentName(TradeNum : Byte) : String;
      function TradeCheck(TradeNum, Num : Byte) : Boolean;
      procedure ConfirmTrade(TradeNum : Byte);
      function CancelTrade(TradeNum : Byte) : Boolean;
  end;

  TTargetWork = record
    private
      function GetTargetID : Cardinal;
      function GetTargetStatus : Boolean;
    public
      function WaitForTarget(MaxWaitTimeMS : Integer) : Boolean;
      procedure CancelTarget;
      procedure TargetToObject(ObjectID : Cardinal);
      procedure TargetToXYZ(X, Y : Word; Z : ShortInt);
      procedure TargetToTile(TileModel,X,Y : Word; Z : ShortInt);
      procedure WaitTargetObject(ObjID : Cardinal);
      procedure WaitTargetTile(Tile,X, Y : Word;  Z : ShortInt);
      procedure WaitTargetXYZ(X, Y : Word; Z : ShortInt);
      procedure WaitTargetSelf;
      procedure WaitTargetType(ObjType : Word);
      procedure CancelWaitTarget;
      procedure WaitTargetGround(ObjType : Word);
      procedure WaitTargetLast;

      property TargetID : Cardinal read GetTargetID;
      property TargetPresent : Boolean read GetTargetStatus;
   end;

  TLineFields = record
    private
      function GetFoundedParamID : Integer;
      function GetLineID : Cardinal;
      function GetLineType : Word;
      function GetLineName : String;
      function GetLineTime : TDateTime;
      function GetLineMsgType : Byte;
      function GetLineTextColor : Word;
      function GetLineTextFont : Word;
      function GetLineIndex : Integer;
      function GetLineCount : Integer;
    public
      property FoundedParamID : Integer read GetFoundedParamID;
      property LineID : Cardinal read GetLineID;
      property LineType : Word read GetLineType;
      property LineName : String read GetLineName;
      property LineTime : TDateTime read GetLineTime;
      property LineMsgType : Byte read GetLineMsgType;
      property LineTextColor : Word read GetLineTextColor;
      property LineTextFont : Word read GetLineTextFont;
      property LineIndex : Integer read GetLineIndex;
      property LineCount : Integer read GetLineCount;
  end;

  TJournal = record
    private
      function GetJournalLine(StringIndex : Cardinal) : String;
      procedure SetJournalLine(StringIndex : Cardinal; Text : String);
      function GetLowJournal : Integer;
      function GetHighJournal : Integer;
      function GetLastJournalMessage : String;

    public
      procedure AddToJournal(Value : String);
      procedure AddJournalIgnore(Str : String);
      procedure ClearJournalIgnore;
      procedure AddChatUserIgnore(User : String);
      procedure ClearChatUserIgnore;
      procedure ClearJournal;
      function InJournal(Str : String) : Integer;
      function InJournalBetweenTimes(Str : String; TimeBegin, TimeEnd : TDateTime) : Integer;
      function WaitJournalLine(StartTime : TDateTime; Str : String; MaxWaitTimeMS : Integer) : Boolean;
      function WaitJournalLineSystem(StartTime : TDateTime; Str : String; MaxWaitTimeMS : Integer) : Boolean;

      property Low : Integer read GetLowJournal;
      property High : Integer read GetHighJournal;
      property Lines[Index: Cardinal] : String read GetJournalLine write SetJournalLine; default;
      property LastJournalMessage : String read GetLastJournalMessage;
  end;

  TContextMenu = record
    public
      procedure RequestContextMenu(ObjectID : Cardinal);
      procedure SetContextMenuHook(MenuID : Cardinal; EntryNumber : Byte);
      function GetContextMenu : TArray<String>;
      function GetContextMenuRec : TContextMenuRec;
      procedure ClearContextMenu;
  end;

  TMenu = record
    public
      procedure WaitMenu(MenuCaption, ElementCaption : String);
      procedure AutoMenu(MenuCaption, ElementCaption : String);
      function MenuHookPresent : Boolean;
      function MenuPresent : Boolean;
      procedure CancelMenu;
      procedure CloseMenu;
      function GetMenuItems(MenuCaption : String) : TArray<String>;
      function GetLastMenuItems : TArray<String>;
  end;

  TGump = record
    private
      function GetGumpsCount : Cardinal;
    public
      procedure WaitGump(Value : Integer);
      procedure WaitGumpStr(Value : String);
      procedure GumpAutoTextEntry(TextEntryID : Integer; Value : String);
      procedure GumpAutoRadiobutton(RadiobuttonID, Value : Integer);
      procedure GumpAutoCheckBox(CBID, Value : Integer);
      function NumGumpButton(GumpIndex : Word; Value : Integer) : Boolean;
      function NumGumpTextEntry(GumpIndex : Word; TextEntryID : Integer; Value : String) : Boolean;
      function NumGumpRadiobutton(GumpIndex : Word; RadiobuttonID, Value : Integer) : Boolean;
      function NumGumpCheckBox(GumpIndex : Word; CBID, Value : Integer) : Boolean;
      procedure CloseSimpleGump(GumpIndex : Word);
      function IsGump : Boolean;
      function GetGumpSerial(GumpIndex : Word) : Cardinal;
      function GetGumpID(GumpIndex : Word) : Cardinal;
      function GetGumpNoClose(GumpIndex : Word) : Boolean;
      function GetGumpTextLines(GumpIndex : Word) : TArray<String>;
      function GetGumpFullLines(GumpIndex : Word) : TArray<String>;
      function GetGumpShortLines(GumpIndex : Word) : TArray<String>;
      function GetGumpButtonsDescription(GumpIndex : Word) : TArray<String>;
      function GetGumpInfo(GumpIndex : Word) : TGumpInfo;
      procedure AddGumpIgnoreByID(GumpID : Cardinal);
      procedure AddGumpIgnoreBySerial(GumpSerial : Cardinal);
      procedure ClearGumpsIgnore;
      property Count : Cardinal read GetGumpsCount;
  end;

  TShop = record
    private
      function GetAutoBuyDelay : Word;
      procedure SetAutoBuyDelay(Value : Word);
      function GetAutoSellDelay : Word;
      procedure SetAutoSellDelay(Value : Word);
    public
      procedure AutoBuy(ItemType, ItemColor, Quantity : Word);
      function GetShopList : TArray<String>;
      procedure ClearShopList;
      procedure AutoBuyEx(ItemType : Word; ItemColor : Word; Quantity : Word; Price : Cardinal; Name : String);
      procedure AutoSell(ItemType, ItemColor, Quantity : Word);
      property AutoBuyDelay : Word read GetAutoBuyDelay write SetAutoBuyDelay;
      property AutoSellDelay : Word read GetAutoSellDelay write SetAutoSellDelay;
  end;

  TParty = record
    public
      procedure InviteToParty(ObjectID : Cardinal);
      procedure RemoveFromParty(ObjectID : Cardinal);
      procedure PartyMessageTo(ObjectID : Cardinal; Msg : String);
      procedure PartySay(Msg : String);
      procedure PartyCanLootMe(Value : Boolean);
      procedure PartyAcceptInvite;
      procedure PartyDeclineInvite;
      procedure PartyLeave;
      function InParty : Boolean;
      function PartyMembersList : TArray<Cardinal>;
  end;

  THTTP = record
    private
      function GetBody : String;
      function GetHeader : String;
    public
      procedure Get(URL : String);
      function Post(URL, PostData : String) : String;
      property Body : String read GetBody;
      property Header : String read GetHeader;
  end;

  TICQ = record
    private
      function GetConnectedStatus : Boolean;
    public
      procedure Connect(UIN : Cardinal; Password : String);
      procedure Disconnect;
      procedure SetStatus(Num : Byte);
      procedure SetXStatus(Num : Byte);
      procedure SendText(DestinationUIN : Cardinal; Text : String);
      property Connected : Boolean read GetConnectedStatus;
  end;

  TSkype = record
    private
      function GetConnected : Boolean;
    public
      procedure Connect(Login : String; Password : String);
      procedure Disconnect;
      procedure SendMessage(Msg : String; UserID : String);
      function GetNicknameByID(ID : String) : String;
      function GetIDByNickname(Nickname : String) : String;
      property Connected : Boolean read GetConnected;
  end;

  TClient = record
    public
      procedure Print(Msg : String);
      procedure PrintEx(SenderID : Cardinal; Color, Font : Word; Msg : String);
      procedure CloseUIWindow(UIWindowType : TUIWindowType; ID : Cardinal);
      procedure RequestObjectTarget;
      procedure RequestTileTarget;
      function TargetResponsePresent : Boolean;
      function TargetResponse : TTargetInfo;
      function WaitForTargetResponse(MaxWaitTimeMS : Integer) : Boolean;
  end;

  TSkill = class
    private
      fSkillName : String;
    public
      constructor Create(SkillName : String);
      function Use : Boolean; overload;
      class function Use(SkillName : String) : Boolean; overload;
      procedure ChangeLockState(skillState : TSkillState);overload;
      class procedure ChangeLockState(SkillName : String; skillState : TSkillState); overload;
      function GetCap : Double;overload;
      class function GetCap(SkillName : String) : Double; overload;
      function GetValue : Double; overload;
      class function GetValue(SkillName : String) : Double;overload;
      function GetCurrentValue : Double; overload;
      class function GetCurrentValue(SkillName : String) : Double;overload;
  end;

  TTileWork = record
    public
      function GetTileFlags(TileGroup : TileFlagsType; Tile : Word) : Cardinal;
      function ConvertFlagsToFlagSet(TileGroup : TileFlagsType; Flags : LongWord) : TTileDataFlagSet;
      function GetLandTileData(Tile : Word) : TLandTileData;
      function GetStaticTileData(Tile : Word) : TStaticTileData;
      function GetCell(X, Y : Word; WorldNum : Byte) : TMapCell;
      function GetLayerCount(X, Y : word; WorldNum : byte) : Byte;
      function ReadStaticsXY(X, Y : word; WorldNum : byte) : TStaticCellRealXY;
      function GetSurfaceZ(X, Y : word; WorldNum : Byte) : ShortInt;
      function IsWorldCellPassable(CurrX, CurrY : Word; CurrZ : ShortInt; DestX, DestY : Word; var DestZ : ShortInt; WorldNum : byte) : Boolean;
      function GetStaticTilesArray(Xmin, Ymin, Xmax, Ymax : Word; WorldNum: Byte; TileTypes: Array of Word) : TFoundTilesArray;
      function GetLandTilesArray(Xmin, Ymin, Xmax, Ymax : Word; WorldNum : byte; TileTypes : Array of Word) : TFoundTilesArray;
  end;

  TEasyUO = record
    private
      procedure SetEUOVar(VarNum : Byte; VarValue : String);
      function GetEUOVar(VarNum : Byte) : String;
    public
      function EUO2StealthType(EUO : String) : Word;
      function EUO2StealthID(EUO : String) : Cardinal;
      property EUOVar[VarNum : Byte] : String read GetEUOVar write SetEUOVar;
  end;

  TPath = record
    private
      function GetStealthPath : String;
      function GetCurrentScriptPath : String;
      function GetStealthProfilePath : String;
      function GetShardPath : String;
    public
      property StealthPath : String read GetStealthPath;
      property CurrentScriptPath : String read GetCurrentScriptPath;
      property StealthProfilePath : String read GetStealthProfilePath;
      property ShardPath : String read GetShardPath;
  end;

  TMover = record
    private
      procedure SetRunUnmountTimer(Value : Word);
      procedure SetWalkMountTimer(Value : Word);
      procedure SetRunMountTimer(Value : Word);
      procedure SetWalkUnmountTimer(Value : Word);
      function GetRunMountTimer : Word;
      function GetWalkMountTimer : Word;
      function GetRunUnmountTimer : Word;
      function GetWalkUnmountTimer : Word;
      function GetLastStepQUsedDoor : Cardinal;
      procedure SetMoveOpenDoor(Value : Boolean);
      function GetMoveOpenDoor : Boolean;
      procedure SetMoveThroughNPC(Value : Word);
      function GetMoveThroughNPC : Word;
      procedure SetMoveThroughCorner(Value : Boolean);
      function GetMoveThroughCorner : Boolean;
      procedure SetMoveHeuristicMult(Value : Integer);
      function GetMoveHeuristicMult : Integer;
    public
      function Step(Direction : Byte; Running : Boolean) : TStepResult;
      function StepQ(Direction : Byte; Running : Boolean) : Integer;
      function MoveXYZ(Xdst, Ydst : Word; Zdst : ShortInt; AccuracyXY, AccuracyZ : Integer; Running : Boolean) : Boolean;
      function newMoveXY(Xdst, Ydst : Word; Optimized : Boolean; Accuracy : Integer; Running : Boolean) : Boolean;
      procedure SetBadLocation(X, Y : Word);
      procedure SetGoodLocation(X, Y : Word);
      procedure ClearBadLocationList;
      procedure SetBadObject(ObjType, Color : Word; Radius : Byte);
      procedure ClearBadObjectList;
      function CheckLOS(xf, yf : Word; zf : ShortInt; xt, yt : Word; zt : ShortInt; WorldNum : Byte; LOSCheckType : TLOSCheckType; LOSCheckOptions : TLOSCheckOptions) : Boolean;
      function GetPathArray(DestX, DestY : Word; Optimized : Boolean; Accuracy : Integer): TArray<TMyPoint>;
      function GetPathArray3D(StartX, StartY : Word; StartZ : Shortint; FinishX, FinishY : Word; FinishZ : Shortint; WorldNum : Byte; AccuracyXY, AccuracyZ : Integer; Run : Boolean): TArray<TMyPoint>;
      function Dist(x1, y1, x2, y2 : word) : word;
      procedure CalcCoord(x, y : word; Dir : byte; var x2, y2 : word);
      function CalcDir(Xfrom, Yfrom, Xto, Yto : integer) : byte;
      function PredictedX : Word;
      function PredictedY : Word;
      function PredictedZ : ShortInt;
      function PredictedDirection : Byte;

      property RunUnmountTimer : Word read GetRunUnmountTimer write SetRunUnmountTimer;
      property WalkMountTimer : Word read GetWalkMountTimer write SetWalkMountTimer;
      property RunMountTimer : Word read GetRunMountTimer write SetRunMountTimer;
      property WalkUnmountTimer : Word read GetWalkUnmountTimer write SetWalkUnmountTimer;
      property LastStepQUsedDoor : Cardinal read GetLastStepQUsedDoor;
      property MoveOpenDoor : Boolean read GetMoveOpenDoor write SetMoveOpenDoor;
      property MoveThroughNPC : Word read GetMoveThroughNPC write SetMoveThroughNPC;
      property MoveThroughCorner : Boolean read GetMoveThroughCorner write SetMoveThroughCorner;
      property MoveHeuristicMult : Integer read GetMoveHeuristicMult write SetMoveHeuristicMult;
  end;

  TConnection = record
    private
      procedure SetARStatus(Value : Boolean);
      function GetARStatus : Boolean;
      function GetConnectedStatus : Boolean;
      function GetConnectedTime : TDateTime;
      function GetDisconnectedTime : TDateTime;
      function GetShardName : String;
      function GetProfileShardName : String;
      function GetProxyIP : String;
      function GetProxyPort : Word;
      function GetUseProxy : Boolean;
      procedure SetPauseScriptOnDisconnectStatus(Value : Boolean);
      function GetPauseScriptOnDisconnectStatus : Boolean;
    public
      procedure Connect;
      procedure Disconnect;
      function ChangeProfile(Name : String) : Integer;
      function ChangeProfileEx(Name : String; ShardName : String = ''; CharName : String = '') : Integer;
      function ProfileName : String;
      property ARStatus : Boolean read GetARStatus write SetARStatus;
      property Connected : Boolean read GetConnectedStatus;
      property ConnectedTime : TDateTime read GetConnectedTime;
      property DisconnectedTime : TDateTime read GetDisconnectedTime;
      property ShardName : String read GetShardName;
      property ProfileShardName : String read GetProfileShardName;
      property ProxyIP : String read GetProxyIP;
      property ProxyPort : Word read GetProxyPort;
      property ProxyUsed : Boolean read GetUseProxy;
      property PauseScriptOnDisconnectStatus : Boolean read GetPauseScriptOnDisconnectStatus write SetPauseScriptOnDisconnectStatus;
    end;

  TScript = record
    private
      function GetDressSpeed : Word;
      procedure SetDressSpeed(Value : Word);
      function GetLastContainer : Cardinal;
      function GetLastTarget : Cardinal;
      function GetLastAttack : Cardinal;
      function GetLastStatus : Cardinal;
      function GetLastObject : Cardinal;
      function GetWorldNum : Byte;
      function GetBackpackID : Cardinal;
      function GetGroundID : Cardinal;
      function GetSilentMode : Boolean;
      procedure SetSilentMode(Value : Boolean);
      function GetGlobalCharVar(VarName : String) : String;
      procedure SetGlobalCharVar(VarName, Value : String);
      function GetGlobalStealthVar(VarName : String) : String;
      procedure SetGlobalStealthVar(VarName, Value : String);
    public
      { public declarations }
      MyChar : TMyChar;       //Character
      Target : TTargetWork;
      LineFields : TLineFields;
      Journal : TJournal;
      FindEngine : TFindEngine;
      UOObject : TUOObject;
      MoveItemEngine : TMoveItemEngine;
      Menu : TMenu;
      Gump : TGump;
      Shop : TShop;
      Party : TParty;
      HTTP : THTTP;
      ICQ : TICQ;
      Skype : TSkype;
      Client : TClient;
      Skill : TSkill;
      Mover : TMover;
      Connection : TConnection;
      TileWork : TTileWork;
      ContextMenu : TContextMenu;

      procedure AddToSystemJournal(Text : String); overload;
      procedure AddToSystemJournal(Text : Cardinal); overload;
      function StealthInfo : TAboutData;
      function MsToDateTime(TimeMS : Cardinal) : TDateTime;
      procedure Wait(WaitTimeMS : Integer);

      procedure WaitTextEntry(Value : String);

//maybe move to class "Ability" ?
//maybe move to class "TMyChar" ?
      procedure UsePrimaryAbility;
      procedure UseSecondaryAbility;
      function GetActiveAbility : String;

      procedure ToggleFly;
      procedure ReqVirtuesGump;
      procedure UseVirtue(VirtueName : String);

//maybe move to class "TSpell" ?
      function CastSpell(SpellName : String) : Boolean;
      function CastSpellToObj(SpellName : String; ObjId : Cardinal) : Boolean;
      function IsActiveSpellAbility(SpellName : String) : Boolean;

      procedure UnsetCatchBag;
      function SetCatchBag(ObjectID : Cardinal) : Byte;
      procedure UseObject(ObjectID : Cardinal);
      function UseType(ObjType : Word; Color : Word = $FFFF) : Cardinal;
      function UseFromGround(ObjType : Word; Color : Word) : Cardinal;
      procedure ClickOnObject(ObjectID : Cardinal);
      function GetClilocByID(ClilocID : Cardinal) : String;
      procedure OpenDoor;
      procedure Bow;
      procedure Salute;
      function GetQuestArrow : TPoint;
      function PlayWav(FileName : String) : Boolean;
      procedure HelpRequest;
      procedure QuestRequest;
      procedure RenameMobile(Mob_ID : Cardinal; NewName : String);
      function MobileCanBeRenamed(Mob_ID : Cardinal) : Boolean;
      procedure ChangeStatLockState(statNum, statState : Byte);
      function GetStaticArtBitmap(Id : LongWord; Hue : Word) : TBitmap;
      procedure SetAlarm;
      function CheckLag(timeoutMS : Integer) : Boolean;
      procedure UOSay(Text : String);
      procedure SendTextToUOColor(Text : String; Color : Word);
      procedure SetEventProc(const eventname : TPacketEvent; const method : Pointer);
      procedure ConsoleEntryReply(Text : String);
      procedure ConsoleEntryUnicodeReply(Text : String);
      procedure FillInfoWindow(s : String); overload;
      procedure FillInfoWindow(SA : TArray<String>); overload;
      procedure ClearInfoWindow;

      function PrintScriptMethodsList(Sorted : Boolean = False; Filename : String = '') : TArray<String>;
      procedure SetCOMEnabled(Value : Boolean);

      property DressSpeed : Word read GetDressSpeed write SetDressSpeed;
      property WorldNum : Byte read GetWorldNum;
      property LastContainer : Cardinal read GetLastContainer;
      property LastTarget : Cardinal read GetLastTarget;
      property LastAttack : Cardinal read GetLastAttack;
      property LastStatus : Cardinal read GetLastStatus;
      property LastObject : Cardinal read GetLastObject;
      property Backpack : Cardinal read GetBackpackID;
      property Ground : Cardinal read GetGroundID;
      property SilentMode : Boolean read GetSilentMode write SetSilentMode;
      property GlobalCharVar[VarName : String]  : String read GetGlobalCharVar write SetGlobalCharVar;
      property GlobalStealthVar[VarName : String]  : String read GetGlobalStealthVar write SetGlobalStealthVar;
   end;
 {$Endregion}
{$TYPEINFO OFF}

threadvar Script : TScript;

procedure StartScriptInThread(Method : TScriptExecMethod);

implementation

function ReadStringParam( ParamStream : TMemoryStream): String;
var
  Len : Cardinal;
begin
  ParamStream.Read(Len, 4);
  SetLength(Result,Len);
  ParamStream.Read(Result[1], Len * sizeOf(Char));
end;

{$Region 'Finished'}
{$Region 'AddToSystemJournal'}
procedure Script_AddToSystemJournal(Text : PChar); stdcall; external ConstScriptDLL name 'Script_AddToSystemJournal';
{$EndRegion}
{$Region 'Connect - Disconnect'}
procedure Script_Connect; stdcall; external ConstScriptDLL name 'Script_Connect';
procedure Script_Disconnect; stdcall; external ConstScriptDLL name 'Script_Disconnect';
{$EndRegion}
{$Region 'Stealth Info'}
function Script_GetStealthInfo : TAboutData; stdcall; external ConstScriptDLL name 'Script_GetStealthInfo';
{$EndRegion}
{$Region 'Pause Script on disconnect'}
procedure Script_SetPauseScriptOnDisconnectStatus(Value : Boolean); stdcall; external ConstScriptDLL name 'Script_SetPauseScriptOnDisconnectStatus';
function Script_GetPauseScriptOnDisconnectStatus : Boolean; stdcall; external ConstScriptDLL name 'Script_GetPauseScriptOnDisconnectStatus';
{$EndRegion}
{$Region 'Auto Reconnector'}
procedure Script_SetARStatus(Value : Boolean); stdcall; external ConstScriptDLL name 'Script_SetARStatus';
function Script_GetARStatus : Boolean; stdcall; external ConstScriptDLL name 'Script_GetARStatus';
{$EndRegion}
{$Region 'MsToDateTime'}
function Script_MsToDateTime(TimeMS : Cardinal) : TDateTime; stdcall; external ConstScriptDLL name 'Script_MsToDateTime';
{$EndRegion}
{$Region 'Connected'}
function Script_GetConnectedStatus : Boolean;  stdcall; external ConstScriptDLL name 'Script_GetConnectedStatus';
{$EndRegion}
{$Region 'Char Name'}
function Script_GetCharName : PChar; stdcall; external ConstScriptDLL name 'Script_GetCharName';
{$EndRegion}
{$Region 'Profile Name'}
function Script_ChangeProfile(Name : PChar) : Integer; stdcall; external ConstScriptDLL name 'Script_ChangeProfile';
function Script_ChangeProfileEx(Name : PChar;ShardName : PChar; CharName : PChar) : Integer; stdcall; external ConstScriptDLL name 'Script_ChangeProfileEx';
function Script_ProfileName : PChar; stdcall; external ConstScriptDLL name 'Script_ProfileName';
{$EndRegion}
{$Region 'Self'}
function Script_GetSelfID : Cardinal; stdcall; external ConstScriptDLL name 'Script_GetSelfID';
function Script_GetSelfSex : Byte; stdcall; external ConstScriptDLL name 'Script_GetSelfSex';
function Script_GetCharTitle : PChar; stdcall; external ConstScriptDLL name 'Script_GetCharTitle';
function Script_GetSelfGold : Cardinal; stdcall; external ConstScriptDLL name 'Script_GetSelfGold';
function Script_GetSelfArmor : Word; stdcall; external ConstScriptDLL name 'Script_GetSelfArmor';
function Script_GetSelfWeight : Word; stdcall; external ConstScriptDLL name 'Script_GetSelfWeight';
function Script_GetSelfMaxWeight : Word; stdcall; external ConstScriptDLL name 'Script_GetSelfMaxWeight';
function Script_GetWorldNum : Byte; stdcall; external ConstScriptDLL name 'Script_GetWorldNum';
function Script_GetSelfRace : Byte; stdcall; external ConstScriptDLL name 'Script_GetSelfRace';
function Script_GetSelfPetsMax : Byte; stdcall; external ConstScriptDLL name 'Script_GetSelfPetsMax';
function Script_GetSelfPetsCurrent : Byte; stdcall; external ConstScriptDLL name 'Script_GetSelfPetsCurrent';
function Script_GetSelfFireResist : Word; stdcall; external ConstScriptDLL name 'Script_GetSelfFireResist';
function Script_GetSelfColdResist : Word; stdcall; external ConstScriptDLL name 'Script_GetSelfColdResist';
function Script_GetSelfPoisonResist : Word; stdcall; external ConstScriptDLL name 'Script_GetSelfPoisonResist';
function Script_GetSelfEnergyResist : Word; stdcall; external ConstScriptDLL name 'Script_GetSelfEnergyResist';
function Script_GetConnectedTime : TDateTime; stdcall; external ConstScriptDLL name 'Script_GetConnectedTime';
function Script_GetDisconnectedTime : TDateTime; stdcall; external ConstScriptDLL name 'Script_GetDisconnectedTime';
function Script_GetLastContainer : Cardinal; stdcall; external ConstScriptDLL name 'Script_GetLastContainer';
function Script_GetLastTarget : Cardinal; stdcall; external ConstScriptDLL name 'Script_GetLastTarget';
function Script_GetLastAttack : Cardinal; stdcall; external ConstScriptDLL name 'Script_GetLastAttack';
function Script_GetLastStatus : Cardinal; stdcall; external ConstScriptDLL name 'Script_GetLastStatus';
function Script_GetLastObject : Cardinal; stdcall; external ConstScriptDLL name 'Script_GetLastObject';
{$EndRegion}
{$Region 'Shard Name'}
function Script_GetShardName : PChar; stdcall; external ConstScriptDLL name 'Script_GetShardName';
function Script_GetProfileShardName : PChar; stdcall; external ConstScriptDLL name 'Script_GetProfileShardName';
{$EndRegion}
{$Region 'Proxy'}
function Script_GetProxyIP : PChar; stdcall; external ConstScriptDLL name 'Script_GetProxyIP';
function Script_GetProxyPort : Word; stdcall; external ConstScriptDLL name 'Script_GetProxyPort';
function Script_GetUseProxy : Boolean; stdcall; external ConstScriptDLL name 'Script_GetUseProxy';
{$EndRegion}
{$Region 'Backpack ID'}
function Script_GetBackpackID : Cardinal; stdcall; external ConstScriptDLL name 'Script_GetBackpackID';
{$EndRegion}
{$Region 'Ground ID'}
function Script_GetGroundID : Cardinal; stdcall; external ConstScriptDLL name 'Script_GetGroundID';
{$EndRegion}
{$Region 'Char Stats'}
function Script_GetSelfStr : Integer; stdcall; external ConstScriptDLL name 'Script_GetSelfStr';
function Script_GetSelfInt : Integer; stdcall; external ConstScriptDLL name 'Script_GetSelfInt';
function Script_GetSelfDex : Integer; stdcall; external ConstScriptDLL name 'Script_GetSelfDex';
function Script_GetSelfLife : Integer; stdcall; external ConstScriptDLL name 'Script_GetSelfLife';
function Script_GetSelfMana : Integer; stdcall; external ConstScriptDLL name 'Script_GetSelfMana';
function Script_GetSelfStam : Integer; stdcall; external ConstScriptDLL name 'Script_GetSelfStam';
function Script_GetSelfMaxLife : Integer; stdcall; external ConstScriptDLL name 'Script_GetSelfMaxLife';
function Script_GetSelfMaxMana : Integer; stdcall; external ConstScriptDLL name 'Script_GetSelfMaxMana';
function Script_GetSelfMaxStam : Integer; stdcall; external ConstScriptDLL name 'Script_GetSelfMaxStam';
function Script_GetSelfLuck : Integer; stdcall; external ConstScriptDLL name 'Script_GetSelfLuck';
function Script_GetExtInfo : TExtendedInfo; stdcall; external ConstScriptDLL name 'Script_GetExtInfo';
{$EndRegion}
{$Region 'Hidden'}
function Script_GetHiddenStatus : Boolean; stdcall; external ConstScriptDLL name 'Script_GetHiddenStatus';
{$EndRegion}
{$Region 'Poisoned'}
function Script_GetPoisonedStatus : Boolean; stdcall; external ConstScriptDLL name 'Script_GetPoisonedStatus';
{$EndRegion}
{$Region 'Paralyzed'}
function Script_GetParalyzedStatus : Boolean; stdcall; external ConstScriptDLL name 'Script_GetParalyzedStatus';
{$EndRegion}
{$Region 'Dead'}
function Script_GetDeadStatus : Boolean; stdcall; external ConstScriptDLL name 'Script_GetDeadStatus';
{$EndRegion}
{$Region 'Attack and WarMode'}
function Script_GetWarModeStatus : Boolean; stdcall; external ConstScriptDLL name 'Script_GetWarModeStatus';
procedure Script_SetWarMode(Value : Boolean); stdcall; external ConstScriptDLL name 'Script_SetWarMode';
function Script_GetWarTarget : Cardinal; stdcall; external ConstScriptDLL name 'Script_GetWarTarget';
procedure Script_Attack(AttackedID : Cardinal); stdcall; external ConstScriptDLL name 'Script_Attack';
{$EndRegion}
{$Region 'Work with paperdoll scrolls'}
procedure Script_UseSelfPaperdollScroll; stdcall; external ConstScriptDLL name 'Script_UseSelfPaperdollScroll';
procedure Script_UseOtherPaperdollScroll(ID : Cardinal); stdcall; external ConstScriptDLL name 'Script_UseOtherPaperdollScroll';
{$EndRegion}
{$Region 'Target'}
function Script_GetTargetID : Cardinal; stdcall; external ConstScriptDLL name 'Script_GetTargetID';
function Script_GetTargetStatus : Boolean; stdcall; external ConstScriptDLL name 'Script_GetTargetStatus';
function Script_WaitForTarget(MaxWaitTimeMS : Integer) : Boolean; stdcall; external ConstScriptDLL name 'Script_WaitForTarget';
procedure Script_CancelTarget; stdcall; external ConstScriptDLL name 'Script_CancelTarget';
procedure Script_TargetToObject(ObjectID : Cardinal); stdcall; external ConstScriptDLL name 'Script_TargetToObject';
procedure Script_TargetToXYZ(X, Y : Word; Z : ShortInt); stdcall; external ConstScriptDLL name 'Script_TargetToXYZ';
procedure Script_TargetToTile(TileModel,X,Y : Word; Z : ShortInt); stdcall; external ConstScriptDLL name 'Script_TargetToTile';
{$EndRegion}
{$Region 'WaitTarget'}
procedure Script_WaitTargetObject(ObjID : Cardinal); stdcall; external ConstScriptDLL name 'Script_WaitTargetObject';
procedure Script_WaitTargetTile(Tile,X, Y : Word;  Z : ShortInt); stdcall; external ConstScriptDLL name 'Script_WaitTargetTile';
procedure Script_WaitTargetXYZ(X, Y : Word; Z : ShortInt); stdcall; external ConstScriptDLL name 'Script_WaitTargetXYZ';
procedure Script_WaitTargetSelf; stdcall; external ConstScriptDLL name 'Script_WaitTargetSelf';
procedure Script_WaitTargetType(ObjType : Word); stdcall; external ConstScriptDLL name 'Script_WaitTargetType';
procedure Script_CancelWaitTarget; stdcall; external ConstScriptDLL name 'Script_CancelWaitTarget';
procedure Script_WaitTargetGround(ObjType : Word); stdcall; external ConstScriptDLL name 'Script_WaitTargetGround';
procedure Script_WaitTargetLast; stdcall; external ConstScriptDLL name 'Script_WaitTargetLast';
{$EndRegion}
{$Region 'Wait'}
procedure Script_Wait(WaitTimeMS : Integer); stdcall; external ConstScriptDLL name 'Script_Wait';
{$EndRegion}
{$Region 'Ability'}
procedure Script_UsePrimaryAbility; stdcall; external ConstScriptDLL name 'Script_UsePrimaryAbility';
procedure Script_UseSecondaryAbility; stdcall; external ConstScriptDLL name 'Script_UseSecondaryAbility';
function Script_GetAbility : PChar; stdcall; external ConstScriptDLL name 'Script_GetAbility';
procedure Script_ToggleFly; stdcall; external ConstScriptDLL name 'Script_ToggleFly';
{$EndRegion}
{$Region 'Skills Func'}
function Script_UseSkill(SkillName : PChar) : Boolean; stdcall; external ConstScriptDLL name 'Script_UseSkill';
procedure Script_ChangeSkillLockState(SkillName : PChar; skillState : Byte); stdcall; external ConstScriptDLL name 'Script_ChangeSkillLockState';
function Script_GetSkillCap(SkillName : PChar) : Double; stdcall; external ConstScriptDLL name 'Script_GetSkillCap';
function Script_GetSkillValue(SkillName : PChar) : Double; stdcall; external ConstScriptDLL name 'Script_GetSkillValue';
function Script_GetSkillCurrentValue(SkillName : PChar) : Double; stdcall; external ConstScriptDLL name 'Script_GetSkillCurrentValue';
{$EndRegion}
{$Region 'Virtues'}
procedure Script_ReqVirtuesGump; stdcall; external ConstScriptDLL name 'Script_ReqVirtuesGump';
procedure Script_UseVirtue(VirtueName : PChar); stdcall; external ConstScriptDLL name 'Script_UseVirtue';
{$EndRegion}
{$Region 'Cast Spell'}
function Script_CastSpell(SpellName : PChar) : Boolean; stdcall; external ConstScriptDLL name 'Script_CastSpell';
function Script_CastSpellToObj(SpellName : PChar; ObjId : Cardinal) : Boolean; stdcall; external ConstScriptDLL name 'Script_CastSpellToObj';
function Script_IsActiveSpellAbility(SpellName : PChar) : Boolean; stdcall; external ConstScriptDLL name 'Script_IsActiveSpellAbility';
{$EndRegion}
{$Region 'SetCatchBag'}
procedure Script_UnsetCatchBag; stdcall; external ConstScriptDLL name 'Script_UnsetCatchBag';
function Script_SetCatchBag(ObjectID : Cardinal) : Byte; stdcall; external ConstScriptDLL name 'Script_SetCatchBag';
{$EndRegion}
{$Region 'UseObject'}
procedure Script_UseObject(ObjectID : Cardinal); stdcall; external ConstScriptDLL name 'Script_UseObject';
function Script_UseType(ObjType : Word; Color : Word) : Cardinal; stdcall; external ConstScriptDLL name 'Script_UseType';
function Script_UseType2(ObjType : Word) : Cardinal; stdcall; external ConstScriptDLL name 'Script_UseType2';
function Script_UseFromGround(ObjType : Word; Color : Word) : Cardinal; stdcall; external ConstScriptDLL name 'Script_UseFromGround';
{$EndRegion}
{$Region 'ClickOnObject'}
procedure Script_ClickOnObject(ObjectID : Cardinal); stdcall; external ConstScriptDLL name 'Script_ClickOnObject';
{$EndRegion}
{$Region 'Line Fields'}
function Script_GetFoundedParamID : Integer; stdcall; external ConstScriptDLL name 'Script_GetFoundedParamID';
function Script_GetLineID : Cardinal; stdcall; external ConstScriptDLL name 'Script_GetLineID';
function Script_GetLineType : Word; stdcall; external ConstScriptDLL name 'Script_GetLineType';
function Script_GetLineName : PChar; stdcall; external ConstScriptDLL name 'Script_GetLineName';
function Script_GetLineTime : TDateTime; stdcall; external ConstScriptDLL name 'Script_GetLineTime';
function Script_GetLineMsgType : Byte; stdcall; external ConstScriptDLL name 'Script_GetLineMsgType';
function Script_GetLineTextColor : Word; stdcall; external ConstScriptDLL name 'Script_GetLineTextColor';
function Script_GetLineTextFont : Word; stdcall; external ConstScriptDLL name 'Script_GetLineTextFont';
function Script_GetLineIndex : Integer; stdcall; external ConstScriptDLL name 'Script_GetLineIndex';
function Script_GetLineCount : Integer; stdcall; external ConstScriptDLL name 'Script_GetLineCount';
{$EndRegion}
{$Region 'Journal'}
procedure Script_AddJournalIgnore(Str : PChar); stdcall; external ConstScriptDLL name 'Script_AddJournalIgnore';
procedure Script_ClearJournalIgnore; stdcall; external ConstScriptDLL name 'Script_ClearJournalIgnore';
procedure Script_AddChatUserIgnore(User : PChar); stdcall; external ConstScriptDLL name 'Script_AddChatUserIgnore';
procedure Script_ClearChatUserIgnore; stdcall; external ConstScriptDLL name 'Script_ClearChatUserIgnore';
procedure Script_ClearJournal; stdcall; external ConstScriptDLL name 'Script_ClearJournal';
function Script_LastJournalMessage : PChar; stdcall; external ConstScriptDLL name 'Script_LastJournalMessage';
function Script_InJournal(Str : PChar) : Integer; stdcall; external ConstScriptDLL name 'Script_InJournal';
function Script_InJournalBetweenTimes(Str : PChar; TimeBegin, TimeEnd : TDateTime) : Integer; stdcall; external ConstScriptDLL name 'Script_InJournalBetweenTimes';
function Script_Journal(StringIndex : Cardinal) : PChar; stdcall; external ConstScriptDLL name 'Script_Journal';
procedure Script_SetJournalLine(StringIndex : Cardinal; Text : PChar); stdcall; external ConstScriptDLL name 'Script_SetJournalLine';
function Script_LowJournal : Integer; stdcall; external ConstScriptDLL name 'Script_LowJournal';
function Script_HighJournal : Integer; stdcall; external ConstScriptDLL name 'Script_HighJournal';
function Script_WaitJournalLine(StartTime : TDateTime; Str : PChar; MaxWaitTimeMS : Integer) : Boolean; stdcall; external ConstScriptDLL name 'Script_WaitJournalLine';
function Script_WaitJournalLineSystem(StartTime : TDateTime; Str : PChar; MaxWaitTimeMS : Integer) : Boolean; stdcall; external ConstScriptDLL name 'Script_WaitJournalLineSystem';
procedure Script_AddToJournal(Msg : PChar); stdcall; external ConstScriptDLL name 'Script_AddToJournal';
{$EndRegion}
{$Region 'Objects'}
procedure Script_SetFindDistance(Value : Cardinal); stdcall; external ConstScriptDLL name 'Script_SetFindDistance';
function Script_GetFindDistance : Cardinal; stdcall; external ConstScriptDLL name 'Script_GetFindDistance';
procedure Script_SetFindVertical(Value : Cardinal); stdcall; external ConstScriptDLL name 'Script_SetFindVertical';
function Script_GetFindVertical : Cardinal; stdcall; external ConstScriptDLL name 'Script_GetFindVertical';
procedure Script_SetFindInNulPoint(Value : Boolean); stdcall; external ConstScriptDLL name 'Script_SetFindInNulPoint';
function Script_GetFindInNulPoint : Boolean; stdcall; external ConstScriptDLL name 'Script_GetFindInNulPoint';
function Script_FindTypeEx(ObjType : Word; Color : Word; Container : Cardinal; InSub : Boolean) : Cardinal; stdcall; external ConstScriptDLL name 'Script_FindTypeEx';
function Script_FindType(ObjType : Word; Container : Cardinal) : Cardinal; stdcall; external ConstScriptDLL name 'Script_FindType';
function Script_FindTypesArrayEx(ArrayBytes : Pointer; const Len : Cardinal; ArrayBytes2 : Pointer; const Len2 : Cardinal; ArrayBytes3 : Pointer; const Len3 : Cardinal;  InSub : Boolean) : Cardinal; stdcall; external ConstScriptDLL name 'Script_FindTypesArrayEx';
function Script_FindNotoriety(ObjType : Word; Notoriety : Byte) : Cardinal; stdcall; external ConstScriptDLL name 'Script_FindNotoriety';
function Script_FindAtCoord(X, Y : Word) : Cardinal; stdcall; external ConstScriptDLL name 'Script_FindAtCoord';
procedure Script_Ignore(ObjID : Cardinal); stdcall; external ConstScriptDLL name 'Script_Ignore';
procedure Script_IgnoreOff(ObjID : Cardinal); stdcall; external ConstScriptDLL name 'Script_IgnoreOff';
procedure Script_IgnoreReset; stdcall; external ConstScriptDLL name 'Script_IgnoreReset';
procedure Script_GetIgnoreList(List : Pointer; out Len : Cardinal); stdcall; external ConstScriptDLL name 'Script_GetIgnoreList';
procedure Script_GetFindedList(List : Pointer; out Len : Cardinal); stdcall; external ConstScriptDLL name 'Script_GetFindedList';
function Script_GetFindItem : Cardinal; stdcall; external ConstScriptDLL name 'Script_GetFindItem';
function Script_GetFindCount : Integer; stdcall; external ConstScriptDLL name 'Script_GetFindCount';
function Script_GetFindQuantity : Integer; stdcall; external ConstScriptDLL name 'Script_GetFindQuantity';
function Script_GetFindFullQuantity : Integer; stdcall; external ConstScriptDLL name 'Script_GetFindFullQuantity';

function Script_GetX(ObjID : Cardinal) : Integer; stdcall; external ConstScriptDLL name 'Script_GetX';
function Script_GetY(ObjID : Cardinal) : Integer; stdcall; external ConstScriptDLL name 'Script_GetY';
function Script_GetZ(ObjID : Cardinal) : ShortInt; stdcall; external ConstScriptDLL name 'Script_GetZ';
function Script_GetName(ObjID : Cardinal) : PChar; stdcall; external ConstScriptDLL name 'Script_GetName';
function Script_GetAltName(ObjID : Cardinal) : PChar; stdcall; external ConstScriptDLL name 'Script_GetAltName';
function Script_GetTitle(ObjID : Cardinal) : PChar; stdcall; external ConstScriptDLL name 'Script_GetTitle';
function Script_GetTooltip(ObjID : Cardinal) : PChar; stdcall; external ConstScriptDLL name 'Script_GetTooltip';
function Script_GetType(ObjID : Cardinal) : Word; stdcall; external ConstScriptDLL name 'Script_GetType';
procedure Script_GetClilocRec(ObjID : Cardinal; List : Pointer; out Len : Cardinal); stdcall; external ConstScriptDLL name 'Script_GetClilocRec';
function Script_GetClilocByID(ClilocID : Cardinal) : PChar; stdcall; external ConstScriptDLL name 'Script_GetClilocByID';
function Script_GetQuantity(ObjID : Cardinal) : Integer; stdcall; external ConstScriptDLL name 'Script_GetQuantity';
function Script_IsObjectExists(ObjID : Cardinal) : Boolean; stdcall; external ConstScriptDLL name 'Script_IsObjectExists';
function Script_IsNPC(ObjID : Cardinal) : Boolean; stdcall; external ConstScriptDLL name 'Script_IsNPC';
function Script_GetPrice(ObjID : Cardinal) : Cardinal; stdcall; external ConstScriptDLL name 'Script_GetPrice';
function Script_GetDirection(ObjID : Cardinal) : Byte; stdcall; external ConstScriptDLL name 'Script_GetDirection';
function Script_GetDistance(ObjID : Cardinal) : Integer; stdcall; external ConstScriptDLL name 'Script_GetDistance';
function Script_GetColor(ObjID : Cardinal) : Word; stdcall; external ConstScriptDLL name 'Script_GetColor';
function Script_GetStr(ObjID : Cardinal) : Integer; stdcall; external ConstScriptDLL name 'Script_GetStr';
function Script_GetInt(ObjID : Cardinal) : Integer; stdcall; external ConstScriptDLL name 'Script_GetInt';
function Script_GetDex(ObjID : Cardinal) : Integer; stdcall; external ConstScriptDLL name 'Script_GetDex';
function Script_GetHP(ObjID : Cardinal) : Integer; stdcall; external ConstScriptDLL name 'Script_GetHP';
function Script_GetMaxHP(ObjID : Cardinal) : Integer; stdcall; external ConstScriptDLL name 'Script_GetMaxHP';
function Script_GetMana(ObjID : Cardinal) : Integer; stdcall; external ConstScriptDLL name 'Script_GetMana';
function Script_GetMaxMana(ObjID : Cardinal) : Integer; stdcall; external ConstScriptDLL name 'Script_GetMaxMana';
function Script_GetStam(ObjID : Cardinal) : Integer; stdcall; external ConstScriptDLL name 'Script_GetStam';
function Script_GetMaxStam(ObjID : Cardinal) : Integer; stdcall; external ConstScriptDLL name 'Script_GetMaxStam';
function Script_GetNotoriety(ObjID : Cardinal) : Byte; stdcall; external ConstScriptDLL name 'Script_GetNotoriety';
function Script_GetParent(ObjID : Cardinal) : Cardinal; stdcall; external ConstScriptDLL name 'Script_GetParent';
function Script_IsWarMode(ObjID : Cardinal) : Boolean; stdcall; external ConstScriptDLL name 'Script_IsWarMode';
function Script_IsDead(ObjID : Cardinal) : Boolean; stdcall; external ConstScriptDLL name 'Script_IsDead';
function Script_IsRunning(ObjID : Cardinal) : Boolean; stdcall; external ConstScriptDLL name 'Script_IsRunning';
function Script_IsContainer(ObjID : Cardinal) : Boolean; stdcall; external ConstScriptDLL name 'Script_IsContainer';
function Script_IsHidden(ObjID : Cardinal) : Boolean; stdcall; external ConstScriptDLL name 'Script_IsHidden';
function Script_IsMovable(ObjID : Cardinal) : Boolean; stdcall; external ConstScriptDLL name 'Script_IsMovable';
function Script_IsYellowHits(ObjID : Cardinal) : Boolean; stdcall; external ConstScriptDLL name 'Script_IsYellowHits';
function Script_IsPoisoned(ObjID : Cardinal) : Boolean; stdcall; external ConstScriptDLL name 'Script_IsPoisoned';
function Script_IsParalyzed(ObjID : Cardinal) : Boolean; stdcall; external ConstScriptDLL name 'Script_IsParalyzed';
function Script_IsFemale(ObjID : Cardinal) : Boolean; stdcall; external ConstScriptDLL name 'Script_IsFemale';
procedure Script_RequestStats(ObjID : Cardinal); stdcall; external ConstScriptDLL name 'Script_RequestStats';

{$EndRegion}
{$Region 'Actions'}
procedure Script_OpenDoor; stdcall; external ConstScriptDLL name 'Script_OpenDoor';
procedure Script_Bow; stdcall; external ConstScriptDLL name 'Script_Bow';
procedure Script_Salute; stdcall; external ConstScriptDLL name 'Script_Salute';
{$EndRegion}
{$Region 'Move Items'}
function Script_GetDropCheckCoord : Boolean; stdcall; external ConstScriptDLL name 'Script_GetDropCheckCoord';
procedure Script_SetDropCheckCoord(Value : Boolean); stdcall; external ConstScriptDLL name 'Script_SetDropCheckCoord';
function Script_GetDropDelay : Cardinal; stdcall; external ConstScriptDLL name 'Script_GetDropDelay';
procedure Script_SetDropDelay(Value : Cardinal); stdcall; external ConstScriptDLL name 'Script_SetDropDelay';
function Script_DragItem(ItemID : Cardinal; Count : Integer) : Boolean; stdcall; external ConstScriptDLL name 'Script_DragItem';
function Script_DropItem(MoveIntoID : Cardinal; X, Y : Word; Z : ShortInt) : Boolean; stdcall; external ConstScriptDLL name 'Script_DropItem';
function Script_MoveItem(ItemID : Cardinal; Count : Integer; MoveIntoID : Cardinal; X, Y : Word; Z : ShortInt) : Boolean; stdcall; external ConstScriptDLL name 'Script_MoveItem';
function Script_Grab(ItemID : Cardinal; Count : Integer) : Boolean; stdcall; external ConstScriptDLL name 'Script_Grab';
function Script_Drop(ItemID : Cardinal; Count : Integer; X, Y : Smallint; Z : ShortInt) : Boolean; stdcall; external ConstScriptDLL name 'Script_Drop';
function Script_DropHere(ItemID : Cardinal) : Boolean; stdcall; external ConstScriptDLL name 'Script_DropHere';
function Script_MoveItems(Container : Cardinal; ItemsType : Word; ItemsColor : Word; MoveIntoID : Cardinal; X, Y : Word; Z : ShortInt; DelayMS : Integer) : Boolean; stdcall; external ConstScriptDLL name 'Script_MoveItems';
function Script_EmptyContainer(Container, DestContainer : Cardinal; delay_ms : Word) : Boolean; stdcall; external ConstScriptDLL name 'Script_EmptyContainer';
{$EndRegion}
{$Region 'Secure Trade'}
function Script_CheckTradeState : Boolean; stdcall; external ConstScriptDLL name 'Script_CheckTradeState';
function Script_GetTradeContainer(TradeNum, Num : Byte) : Cardinal; stdcall; external ConstScriptDLL name 'Script_GetTradeContainer';
function Script_GetTradeOpponent(TradeNum : Byte) : Cardinal; stdcall; external ConstScriptDLL name 'Script_GetTradeOpponent';
function Script_GetTradeCount : Byte; stdcall; external ConstScriptDLL name 'Script_GetTradeCount';
function Script_GetTradeOpponentName(TradeNum : Byte) : PChar; stdcall; external ConstScriptDLL name 'Script_GetTradeOpponentName';
function Script_TradeCheck(TradeNum, Num : Byte) : Boolean; stdcall; external ConstScriptDLL name 'Script_TradeCheck';
procedure Script_ConfirmTrade(TradeNum : Byte); stdcall; external ConstScriptDLL name 'Script_ConfirmTrade';
function Script_CancelTrade(TradeNum : Byte) : Boolean; stdcall; external ConstScriptDLL name 'Script_CancelTrade';
{$EndRegion}
{$Region 'Menus'}
procedure Script_WaitMenu(MenuCaption, ElementCaption : PChar); stdcall; external ConstScriptDLL name 'Script_WaitMenu';
procedure Script_AutoMenu(MenuCaption, ElementCaption : PChar); stdcall; external ConstScriptDLL name 'Script_AutoMenu';
function Script_MenuHookPresent : Boolean; stdcall; external ConstScriptDLL name 'Script_MenuHookPresent';
function Script_MenuPresent : Boolean; stdcall; external ConstScriptDLL name 'Script_MenuPresent';
procedure Script_CancelMenu; stdcall; external ConstScriptDLL name 'Script_CancelMenu';
procedure Script_CloseMenu; stdcall; external ConstScriptDLL name 'Script_CloseMenu';
function Script_GetMenuItems(MenuCaption : PChar) : PChar; stdcall; external ConstScriptDLL name 'Script_GetMenuItems';
function Script_GetLastMenuItems : PChar; stdcall; external ConstScriptDLL name 'Script_GetLastMenuItems';
{$EndRegion}
{$Region 'Gumps'}
procedure Script_WaitGumpInt(Value : Integer); stdcall; external ConstScriptDLL name 'Script_WaitGumpInt';
procedure Script_WaitGump(Value : PChar); stdcall; external ConstScriptDLL name 'Script_WaitGump';
procedure Script_WaitGumpTextEntry(Value : PChar); stdcall; external ConstScriptDLL name 'Script_WaitGumpTextEntry';
procedure Script_GumpAutoTextEntry(TextEntryID : Integer; Value : PChar); stdcall; external ConstScriptDLL name 'Script_GumpAutoTextEntry';
procedure Script_GumpAutoRadiobutton(RadiobuttonID, Value : Integer); stdcall; external ConstScriptDLL name 'Script_GumpAutoRadiobutton';
procedure Script_GumpAutoCheckBox(CBID, Value : Integer); stdcall; external ConstScriptDLL name 'Script_GumpAutoCheckBox';
function Script_NumGumpButton(GumpIndex : Word; Value : Integer) : Boolean; stdcall; external ConstScriptDLL name 'Script_NumGumpButton';
function Script_NumGumpTextEntry(GumpIndex : Word; TextEntryID : Integer; Value : PChar) : Boolean; stdcall; external ConstScriptDLL name 'Script_NumGumpTextEntry';
function Script_NumGumpRadiobutton(GumpIndex : Word; RadiobuttonID, Value : Integer) : Boolean; stdcall; external ConstScriptDLL name 'Script_NumGumpRadiobutton';
function Script_NumGumpCheckBox(GumpIndex : Word; CBID, Value : Integer) : Boolean; stdcall; external ConstScriptDLL name 'Script_NumGumpCheckBox';
function Script_GetGumpsCount : Integer; stdcall; external ConstScriptDLL name 'Script_GetGumpsCount';
procedure Script_CloseSimpleGump(GumpIndex : Word); stdcall; external ConstScriptDLL name 'Script_CloseSimpleGump';
function Script_IsGump : Boolean; stdcall; external ConstScriptDLL name 'Script_IsGump';
function Script_GetGumpSerial(GumpIndex : Word) : Cardinal; stdcall; external ConstScriptDLL name 'Script_GetGumpSerial';
function Script_GetGumpID(GumpIndex : Word) : Cardinal; stdcall; external ConstScriptDLL name 'Script_GetGumpID';
function Script_GetGumpNoClose(GumpIndex : Word) : Boolean; stdcall; external ConstScriptDLL name 'Script_GetGumpNoClose';
function Script_GetGumpTextLines(GumpIndex : Word) : PChar; stdcall; external ConstScriptDLL name 'Script_GetGumpTextLines';
function Script_GetGumpFullLines(GumpIndex : Word) : PChar; stdcall; external ConstScriptDLL name 'Script_GetGumpFullLines';
function Script_GetGumpShortLines(GumpIndex : Word) : PChar; stdcall; external ConstScriptDLL name 'Script_GetGumpShortLines';
function Script_GetGumpButtonsDescription(GumpIndex : Word) : PChar; stdcall; external ConstScriptDLL name 'Script_GetGumpButtonsDescription';
procedure Script_GetGumpInfo(GumpIndex : Word; List : Pointer; out Len : Cardinal); stdcall; external ConstScriptDLL name 'Script_GetGumpInfo';
procedure Script_AddGumpIgnoreByID(ID : Cardinal); stdcall; external ConstScriptDLL name 'Script_AddGumpIgnoreByID';
procedure Script_AddGumpIgnoreBySerial(Serial : Cardinal); stdcall; external ConstScriptDLL name 'Script_AddGumpIgnoreBySerial';
procedure Script_ClearGumpsIgnore; stdcall; external ConstScriptDLL name 'Script_ClearGumpsIgnore';
{$EndRegion}
{$Region 'ContextMenus'}
procedure Script_RequestContextMenu(ID : Cardinal); stdcall; external ConstScriptDLL name 'Script_RequestContextMenu';
procedure Script_SetContextMenuHook(MenuID : Cardinal; EntryNumber : Byte); stdcall; external ConstScriptDLL name 'Script_SetContextMenuHook';
function Script_GetContextMenu : PChar; stdcall; external ConstScriptDLL name 'Script_GetContextMenu';
function Script_GetContextMenuRec(var Tag : Word; var Flags : Word) : PChar; stdcall; external ConstScriptDLL name 'Script_GetContextMenuRec';
procedure Script_ClearContextMenu; stdcall; external ConstScriptDLL name 'Script_ClearContextMenu';
{$EndRegion}
{$Region 'Layers Names'}
{function GetRhandLayer : Byte; stdcall; external ConstScriptDLL name 'Script_GetRhandLayer';
function GetLhandLayer : Byte; stdcall; external ConstScriptDLL name 'Script_GetLhandLayer';
function GetShoesLayer : Byte; stdcall; external ConstScriptDLL name 'Script_GetShoesLayer';
function GetPantsLayer : Byte; stdcall; external ConstScriptDLL name 'Script_GetPantsLayer';
function GetShirtLayer : Byte; stdcall; external ConstScriptDLL name 'Script_GetShirtLayer';
function GetHatLayer : Byte; stdcall; external ConstScriptDLL name 'Script_GetHatLayer';
function GetGlovesLayer : Byte; stdcall; external ConstScriptDLL name 'Script_GetGlovesLayer';
function GetRingLayer : Byte; stdcall; external ConstScriptDLL name 'Script_GetRingLayer';
function GetTalismanLayer : Byte; stdcall; external ConstScriptDLL name 'Script_GetTalismanLayer';
function GetNeckLayer : Byte; stdcall; external ConstScriptDLL name 'Script_GetNeckLayer';
function GetHairLayer : Byte; stdcall; external ConstScriptDLL name 'Script_GetHairLayer';
function GetWaistLayer : Byte; stdcall; external ConstScriptDLL name 'Script_GetWaistLayer';
function GetTorsoLayer : Byte; stdcall; external ConstScriptDLL name 'Script_GetTorsoLayer';
function GetBraceLayer : Byte; stdcall; external ConstScriptDLL name 'Script_GetBraceLayer';
function GetBeardLayer : Byte; stdcall; external ConstScriptDLL name 'Script_GetBeardLayer';
function GetTorsoHLayer : Byte; stdcall; external ConstScriptDLL name 'Script_GetTorsoHLayer';
function GetEarLayer : Byte; stdcall; external ConstScriptDLL name 'Script_GetEarLayer';
function GetArmsLayer : Byte; stdcall; external ConstScriptDLL name 'Script_GetArmsLayer';
function GetCloakLayer : Byte; stdcall; external ConstScriptDLL name 'Script_GetCloakLayer';
function GetBpackLayer : Byte; stdcall; external ConstScriptDLL name 'Script_GetBpackLayer';
function GetRobeLayer : Byte; stdcall; external ConstScriptDLL name 'Script_GetRobeLayer';
function GetEggsLayer : Byte; stdcall; external ConstScriptDLL name 'Script_GetEggsLayer';
function GetLegsLayer : Byte; stdcall; external ConstScriptDLL name 'Script_GetLegsLayer';
function GetHorseLayer : Byte; stdcall; external ConstScriptDLL name 'Script_GetHorseLayer';
function GetRstkLayer : Byte; stdcall; external ConstScriptDLL name 'Script_GetRstkLayer';
function GetNRstkLayer : Byte; stdcall; external ConstScriptDLL name 'Script_GetNRstkLayer';
function GetSellLayer : Byte; stdcall; external ConstScriptDLL name 'Script_GetSellLayer';
function GetBankLayer : Byte; stdcall; external ConstScriptDLL name 'Script_GetBankLayer';    }
{$EndRegion}
{$Region 'LayerInfo'}
function Script_ObjAtLayerEx(LayerType : Byte; PlayerID : Cardinal) : Cardinal; stdcall; external ConstScriptDLL name 'Script_ObjAtLayerEx';
function Script_ObjAtLayer(LayerType : Byte) : Cardinal; stdcall; external ConstScriptDLL name 'Script_ObjAtLayer';
function Script_GetLayer(Obj : Cardinal) : Byte; stdcall; external ConstScriptDLL name 'Script_GetLayer';
{$EndRegion}
{$Region 'Shop'}
procedure Script_AutoBuy(ItemType, ItemColor, Quantity : Word); stdcall; external ConstScriptDLL name 'Script_AutoBuy';
function Script_GetShopList : PChar; stdcall; external ConstScriptDLL name 'Script_GetShopList';
procedure Script_ClearShopList; stdcall; external ConstScriptDLL name 'Script_ClearShopList';
procedure Script_AutoBuyEx(ItemType : Word; ItemColor : Word; Quantity : Word; Price : Cardinal; Name : PChar); stdcall; external ConstScriptDLL name 'Script_AutoBuyEx';
function Script_GetAutoBuyDelay : Word; stdcall; external ConstScriptDLL name 'Script_GetAutoBuyDelay';
procedure Script_SetAutoBuyDelay(Value : Word); stdcall; external ConstScriptDLL name 'Script_SetAutoBuyDelay';
function Script_GetAutoSellDelay : Word; stdcall; external ConstScriptDLL name 'Script_GetAutoSellDelay';
procedure Script_SetAutoSellDelay(Value : Word); stdcall; external ConstScriptDLL name 'Script_SetAutoSellDelay';
procedure Script_AutoSell(ItemType, ItemColor, Quantity : Word); stdcall; external ConstScriptDLL name 'Script_AutoSell';
{$EndRegion}
{$Region 'Party'}
procedure Script_InviteToParty(ID : Cardinal); stdcall; external ConstScriptDLL name 'Script_InviteToParty';
procedure Script_RemoveFromParty(ID : Cardinal); stdcall; external ConstScriptDLL name 'Script_RemoveFromParty';
procedure Script_PartyMessageTo(ID : Cardinal; Msg : PChar); stdcall; external ConstScriptDLL name 'Script_PartyMessageTo';
procedure Script_PartySay(Msg : PChar); stdcall; external ConstScriptDLL name 'Script_PartySay';
procedure Script_PartyCanLootMe(Value : Boolean); stdcall; external ConstScriptDLL name 'Script_PartyCanLootMe';
procedure Script_PartyAcceptInvite; stdcall; external ConstScriptDLL name 'Script_PartyAcceptInvite';
procedure Script_PartyDeclineInvite; stdcall; external ConstScriptDLL name 'Script_PartyDeclineInvite';
procedure Script_PartyLeave; stdcall; external ConstScriptDLL name 'Script_PartyLeave';
function Script_InParty : Boolean; stdcall; external ConstScriptDLL name 'Script_InParty';
procedure Script_PartyMembersList(List : Pointer; out Len : Cardinal); stdcall; external ConstScriptDLL name 'Script_PartyMembersList';
{$EndRegion}
{$Region 'HttpWorking'}
procedure Script_HTTP_Get(URL : PChar); stdcall; external ConstScriptDLL name 'Script_HTTP_Get';
function Script_HTTP_Post(URL : PChar; PostData : PChar) : PChar; stdcall; external ConstScriptDLL name 'Script_HTTP_Post';
function Script_HTTP_Body : PChar; stdcall; external ConstScriptDLL name 'Script_HTTP_Body';
function Script_HTTP_Header : PChar; stdcall; external ConstScriptDLL name 'Script_HTTP_Header';
{$EndRegion}
{$Region 'ICQ'}
function Script_ICQ_GetConnectedStatus : Boolean; stdcall; external ConstScriptDLL name 'Script_ICQ_GetConnectedStatus';
procedure Script_ICQ_Connect(UIN : Cardinal; Password : PChar); stdcall; external ConstScriptDLL name 'Script_ICQ_Connect';
procedure Script_ICQ_Disconnect; stdcall; external ConstScriptDLL name 'Script_ICQ_Disconnect';
procedure Script_ICQ_SetStatus(Num : Byte); stdcall; external ConstScriptDLL name 'Script_ICQ_SetStatus';
procedure Script_ICQ_SetXStatus(Num : Byte); stdcall; external ConstScriptDLL name 'Script_ICQ_SetXStatus';
procedure Script_ICQ_SendText(DestinationUIN : Cardinal; Text : PChar); stdcall; external ConstScriptDLL name 'Script_ICQ_SendText';
{$EndRegion}
{$Region 'Skype'}
function Script_Skype_Connected : Boolean; stdcall; external ConstScriptDLL name 'Script_Skype_Connected';
procedure Script_Skype_Connect(Login : PChar; Password : PChar); stdcall; external ConstScriptDLL name 'Script_Skype_Connect';
procedure Script_Skype_Disconnect; stdcall; external ConstScriptDLL name 'Script_Skype_Disconnect';
procedure Script_Skype_SendMessage(Msg : PChar; UserID : PChar); stdcall; external ConstScriptDLL name 'Script_Skype_SendMessage';
function Script_Skype_GetNicknameByID(ID : PChar) : PChar; stdcall; external ConstScriptDLL name 'Script_Skype_GetNicknameByID';
function Script_Skype_GetIDByNickname(Nickname : PChar) : PChar; stdcall; external ConstScriptDLL name 'Script_Skype_GetIDByNickname';
{$EndRegion}
{$Region 'Client work'}
procedure Script_ClientPrint(Text : PChar); stdcall; external ConstScriptDLL name 'Script_ClientPrint';
procedure Script_ClientPrintEx(SenderID : Cardinal; Color, Font : Word; Text : PChar); stdcall; external ConstScriptDLL name 'Script_ClientPrintEx';
procedure Script_CloseClientUIWindow(UIWindowType : TUIWindowType; ID : Cardinal); stdcall; external ConstScriptDLL name 'Script_CloseClientUIWindow';
procedure Script_ClientRequestObjectTarget; stdcall; external ConstScriptDLL name 'Script_ClientRequestObjectTarget';
procedure Script_ClientRequestTileTarget; stdcall; external ConstScriptDLL name 'Script_ClientRequestTileTarget';
function Script_ClientTargetResponsePresent : Boolean; stdcall; external ConstScriptDLL name 'Script_ClientTargetResponsePresent';
function Script_ClientTargetResponse : TTargetInfo; stdcall; external ConstScriptDLL name 'Script_ClientTargetResponse';
function Script_WaitForClientTargetResponse(MaxWaitTimeMS : Integer) : Boolean; stdcall; external ConstScriptDLL name 'Script_WaitForClientTargetResponse';
{$EndRegion}
{$Region 'EasyUO Working'}
procedure Script_SetEasyUO(num : Integer; Regvalue : PChar); stdcall; external ConstScriptDLL name 'Script_SetEasyUO';
function Script_GetEasyUO(num : Integer) : PChar; stdcall; external ConstScriptDLL name 'Script_GetEasyUO';
function Script_EUO2StealthType(EUO : PChar) : Word; stdcall; external ConstScriptDLL name 'Script_EUO2StealthType';
function Script_EUO2StealthID(EUO : PChar) : Cardinal; stdcall; external ConstScriptDLL name 'Script_EUO2StealthID';
{$EndRegion}
{$Region 'Tile Working'}
function Script_GetTileFlags(TileGroup : TileFlagsType; Tile : Word) : Cardinal; stdcall; external ConstScriptDLL name 'Script_GetTileFlags';
function Script_ConvertFlagsToFlagSet(TileGroup : TileFlagsType; Flags : LongWord) : TTileDataFlagSet; stdcall; external ConstScriptDLL name 'Script_ConvertFlagsToFlagSet';
function Script_GetLandTileData(Tile : Word) : TLandTileData; stdcall; external ConstScriptDLL name 'Script_GetLandTileData';
function Script_GetStaticTileData(Tile : Word) : TStaticTileData; stdcall; external ConstScriptDLL name 'Script_GetStaticTileData';
function Script_GetCell(X, Y : Word; WorldNum : Byte) : TMapCell; stdcall; external ConstScriptDLL name 'Script_GetCell';
function Script_GetLayerCount(X, Y : word; WorldNum : byte) : Byte; stdcall; external ConstScriptDLL name 'Script_GetLayerCount';
procedure Script_ReadStaticsXY(X, Y : word; WorldNum : byte; List : Pointer; out Len : Cardinal); stdcall; external ConstScriptDLL name 'Script_ReadStaticsXY';
function Script_GetSurfaceZ(X, Y : word; WorldNum : Byte) : ShortInt; stdcall; external ConstScriptDLL name 'Script_GetSurfaceZ';
function Script_IsWorldCellPassable(CurrX, CurrY : Word; CurrZ : ShortInt; DestX, DestY : Word; var DestZ : ShortInt; WorldNum : byte) : Boolean; stdcall; external ConstScriptDLL name 'Script_IsWorldCellPassable';
function Script_GetStaticTilesArray(Xmin, Ymin, Xmax, Ymax : Word; WorldNum : byte; ArrayBytes : Pointer; const Len : Cardinal; List : Pointer) : Word; stdcall; external ConstScriptDLL name 'Script_GetStaticTilesArray';
function Script_GetLandTilesArray(Xmin, Ymin, Xmax, Ymax : Word; WorldNum : byte; ArrayBytes : Pointer; const Len : Cardinal; List : Pointer) : Word; stdcall; external ConstScriptDLL name 'Script_GetLandTilesArray';
{$EndRegion}
{$Region 'Path'}
function Script_GetStealthPath : PChar; stdcall; external ConstScriptDLL name 'Script_GetStealthPath';
function Script_GetCurrentScriptPath : PChar; stdcall; external ConstScriptDLL name 'Script_GetCurrentScriptPath';
function Script_GetStealthProfilePath : PChar; stdcall; external ConstScriptDLL name 'Script_GetStealthProfilePath';
function Script_GetShardPath : PChar; stdcall; external ConstScriptDLL name 'Script_GetShardPath';
{$EndRegion}
{$Region 'Event Handling'}
procedure Script_SetEventProc(const eventname : TPacketEvent; const method : Pointer); stdcall; external ConstScriptDLL name 'Script_SetEventProc';
{$Endregion}
{$Region 'Mover'}
function Script_Step(Direction : Byte; Running : Boolean) : Byte; stdcall; external ConstScriptDLL name 'Script_Step';
function Script_StepQ(Direction : Byte; Running : Boolean) : Integer; stdcall; external ConstScriptDLL name 'Script_StepQ';
function Script_MoveXYZ(Xdst, Ydst : Word; Zdst : ShortInt; AccuracyXY, AccuracyZ : Integer; Running : Boolean) : Boolean; stdcall; external ConstScriptDLL name 'Script_MoveXYZ';
function Script_newMoveXY(Xdst, Ydst : Word; Optimized : Boolean; Accuracy : Integer; Running : Boolean) : Boolean; stdcall; external ConstScriptDLL name 'Script_newMoveXY';
function Script_MoveXY(Xdst, Ydst : Word; Optimized : Boolean; Accuracy : Integer; Running : Boolean) : Boolean; stdcall; external ConstScriptDLL name 'Script_MoveXY';
procedure Script_SetBadLocation(X, Y : Word); stdcall; external ConstScriptDLL name 'Script_SetBadLocation';
procedure Script_SetGoodLocation(X, Y : Word); stdcall; external ConstScriptDLL name 'Script_SetGoodLocation';
procedure Script_ClearBadLocationList; stdcall; external ConstScriptDLL name 'Script_ClearBadLocationList';
procedure Script_SetBadObject(ObjType, Color : Word; Radius : Byte); stdcall; external ConstScriptDLL name 'Script_SetBadObject';
procedure Script_ClearBadObjectList; stdcall; external ConstScriptDLL name 'Script_ClearBadObjectList';
function Script_CheckLOS(xf, yf : Word; zf : ShortInt; xt, yt : Word; zt : ShortInt; WorldNum : Byte; LOSCheckType : Byte; LOSOptions : Cardinal) : Boolean; stdcall; external ConstScriptDLL name 'Script_CheckLOS';
procedure Script_GetPathArray(DestX, DestY : Word; Optimized : Boolean; Accuracy : Integer; List : Pointer; out Len : Cardinal); stdcall; external ConstScriptDLL name 'Script_GetPathArray';
procedure Script_GetPathArray3D(StartX, StartY : Word; StartZ : Shortint; FinishX, FinishY : Word; FinishZ : Shortint; WorldNum : Byte; AccuracyXY, AccuracyZ : Integer; Run : Boolean; List : Pointer; out Len : Cardinal); stdcall; external ConstScriptDLL name 'Script_GetPathArray3D';
function Script_Dist(x1, y1, x2, y2 : word) : word; stdcall; external ConstScriptDLL name 'Script_Dist';
procedure Script_CalcCoord(x, y : word; Dir : byte; var x2, y2 : word); stdcall; external ConstScriptDLL name 'Script_CalcCoord';
function Script_CalcDir(Xfrom, Yfrom, Xto, Yto : integer) : byte; stdcall; external ConstScriptDLL name 'Script_CalcDir';
procedure Script_SetRunUnmountTimer(Value : Word); stdcall; external ConstScriptDLL name 'Script_SetRunUnmountTimer';
procedure Script_SetWalkMountTimer(Value : Word); stdcall; external ConstScriptDLL name 'Script_SetWalkMountTimer';
procedure Script_SetRunMountTimer(Value : Word); stdcall; external ConstScriptDLL name 'Script_SetRunMountTimer';
procedure Script_SetWalkUnmountTimer(Value : Word); stdcall; external ConstScriptDLL name 'Script_SetWalkUnmountTimer';
function Script_GetRunMountTimer : Word; stdcall; external ConstScriptDLL name 'Script_GetRunMountTimer';
function Script_GetWalkMountTimer : Word; stdcall; external ConstScriptDLL name 'Script_GetWalkMountTimer';
function Script_GetRunUnmountTimer : Word; stdcall; external ConstScriptDLL name 'Script_GetRunUnmountTimer';
function Script_GetWalkUnmountTimer : Word; stdcall; external ConstScriptDLL name 'Script_GetWalkUnmountTimer';
function Script_GetLastStepQUsedDoor : Cardinal; stdcall; external ConstScriptDLL name 'Script_GetLastStepQUsedDoor';

function Script_PredictedX : Word; stdcall; external ConstScriptDLL name 'Script_PredictedX';
function Script_PredictedY : Word; stdcall; external ConstScriptDLL name 'Script_PredictedY';
function Script_PredictedZ : ShortInt; stdcall; external ConstScriptDLL name 'Script_PredictedZ';
function Script_PredictedDirection : Byte; stdcall; external ConstScriptDLL name 'Script_PredictedDirection';
procedure Script_SetMoveOpenDoor(Value : Boolean); stdcall; external ConstScriptDLL name 'Script_SetMoveOpenDoor';
function Script_GetMoveOpenDoor : Boolean; stdcall; external ConstScriptDLL name 'Script_GetMoveOpenDoor';
procedure Script_SetMoveThroughNPC(Value : Word); stdcall; external ConstScriptDLL name 'Script_SetMoveThroughNPC';
function Script_GetMoveThroughNPC : Word; stdcall; external ConstScriptDLL name 'Script_GetMoveThroughNPC';
procedure Script_SetMoveThroughCorner(Value : Boolean); stdcall; external ConstScriptDLL name 'Script_SetMoveThroughCorner';
function Script_GetMoveThroughCorner : Boolean; stdcall; external ConstScriptDLL name 'Script_GetMoveThroughCorner';
procedure Script_SetMoveHeuristicMult(Value : Integer); stdcall; external ConstScriptDLL name 'Script_SetMoveHeuristicMult';
function Script_GetMoveHeuristicMult : Integer; stdcall; external ConstScriptDLL name 'Script_GetMoveHeuristicMult';

{$EndRegion}
{$Region 'FillNewWindow'}
function Script_GetSilentMode : Boolean; stdcall; external ConstScriptDLL name 'Script_GetSilentMode';
procedure Script_SetSilentMode(Value : Boolean); stdcall; external ConstScriptDLL name 'Script_SetSilentMode';
procedure Script_FillInfoWindow(s : PChar); stdcall; external ConstScriptDLL name 'Script_FillInfoWindow';
procedure Script_ClearInfoWindow; stdcall; external ConstScriptDLL name 'Script_ClearInfoWindow';
{$EndRegion}
{$Region 'BuffBarInfo'}
procedure Script_GetBuffBarInfo(List : Pointer; out Len : Cardinal); stdcall; external ConstScriptDLL name 'Script_GetBuffBarInfo';
{$EndRegion}
{$EndRegion}

{$Region 'Import from dll'}
{$Region 'Layer dress/undress'}
function disarm : Boolean; stdcall; external ConstScriptDLL name 'Script_disarm';
function equip(Layer : Byte; Obj : Cardinal) : Boolean; stdcall; external ConstScriptDLL name 'Script_equip';
function equipt(Layer : Byte; ObjType : Word) : Boolean; stdcall; external ConstScriptDLL name 'Script_equipt';
function unequip(Layer : Byte) : Boolean; stdcall; external ConstScriptDLL name 'Script_unequip';
function Script_GetDressSpeed : Word; stdcall; external ConstScriptDLL name 'Script_GetDressSpeed';
procedure Script_SetDressSpeed(Value : Word); stdcall; external ConstScriptDLL name 'Script_SetDressSpeed';
function Undress : Boolean; stdcall; external ConstScriptDLL name 'Script_undress';
procedure SetDress; stdcall; external ConstScriptDLL name 'Script_SetDress';
{$EndRegion}

{$Region 'Count/CountGround'}
function Count(ObjType : Word) : Integer; stdcall; external ConstScriptDLL name 'Script_Count';
function Script_CountGround(ObjType : Word) : Integer; stdcall; external ConstScriptDLL name 'Script_CountGround';
function Script_CountEx(ObjType, Color : Word; Container : Cardinal) : Integer; stdcall; external ConstScriptDLL name 'Script_CountEx';
{$EndRegion}

{$Region 'Reagents'}
function Script_ConstBPCount : Word; stdcall; external ConstScriptDLL name 'Script_ConstBPCount';
function Script_ConstBMCount : Word; stdcall; external ConstScriptDLL name 'Script_ConstBMCount';
function Script_ConstGACount : Word; stdcall; external ConstScriptDLL name 'Script_ConstGACount';
function Script_ConstGSCount : Word; stdcall; external ConstScriptDLL name 'Script_ConstGSCount';
function Script_ConstMRCount : Word; stdcall; external ConstScriptDLL name 'Script_ConstMRCount';
function Script_ConstNSCount : Word; stdcall; external ConstScriptDLL name 'Script_ConstNSCount';
function Script_ConstSACount : Word; stdcall; external ConstScriptDLL name 'Script_ConstSACount';
function Script_ConstSSCount : Word; stdcall; external ConstScriptDLL name 'Script_ConstSSCount';
{$EndRegion}

{$Region 'Other'}
function Script_GetQuestArrow : TPoint; stdcall; external ConstScriptDLL name 'Script_GetQuestArrow';
function Script_PlayWav(FileName : PChar) : Boolean; stdcall; external ConstScriptDLL name 'Script_PlayWav';
procedure Script_HelpRequest; stdcall; external ConstScriptDLL name 'Script_HelpRequest';
procedure Script_QuestRequest; stdcall; external ConstScriptDLL name 'Script_QuestRequest';
procedure Script_RenameMobile(Mob_ID : Cardinal; NewName : PChar); stdcall; external ConstScriptDLL name 'Script_RenameMobile';
function Script_MobileCanBeRenamed(Mob_ID : Cardinal) : Boolean; stdcall; external ConstScriptDLL name 'Script_MobileCanBeRenamed';
procedure Script_ChangeStatLockState(statNum, statState : Byte); stdcall; external ConstScriptDLL name 'Script_ChangeStatLockState';
procedure Script_GetStaticArtBitmap(Id : LongWord; Hue : Word; ByteArray : Pointer; out Len : Cardinal); stdcall; external ConstScriptDLL name 'Script_GetStaticArtBitmap';
procedure Script_SetAlarm; stdcall; external ConstScriptDLL name 'Script_SetAlarm';
function Script_CheckLag(timeoutMS : Integer) : Boolean; stdcall; external ConstScriptDLL name 'Script_CheckLag';
procedure Script_SendTextToUO(Text : PChar); stdcall; external ConstScriptDLL name 'Script_SendTextToUO';
procedure Script_SendTextToUOColor(Text : PChar; Color : Word); stdcall; external ConstScriptDLL name 'Script_SendTextToUOColor';
procedure Script_ConsoleEntryReply(Text : PChar); stdcall; external ConstScriptDLL name 'Script_ConsoleEntryReply';
procedure Script_ConsoleEntryUnicodeReply(Text : PChar); stdcall; external ConstScriptDLL name 'Script_ConsoleEntryUnicodeReply';
procedure Script_SetGlobal(GlobalRegion : TVarRegion; VarName : PChar; VarValue : PChar); stdcall; external ConstScriptDLL name 'Script_SetGlobal';
function Script_GetGlobal(GlobalRegion : TVarRegion; VarName : PChar) : PChar; stdcall; external ConstScriptDLL name 'Script_GetGlobal';
procedure Script_SetCOMEnabled(Value : Boolean); stdcall; external ConstScriptDLL name 'Script_SetCOMEnabled';
procedure StartStealthSocketInstance(ExeFile : PAnsiChar);stdcall; external ConstScriptDLL name 'StartStealthSocketInstance';
procedure InitNewThread; stdcall; external ConstScriptDLL name 'InitNewThread';

function Script_GameServerIPString : PChar; stdcall;  external ConstScriptDLL name 'Script_GameServerIPString';
procedure Script_PrintScriptMethodsList(FileName : PChar; SortedList : Boolean = False); stdcall; external ConstScriptDLL name 'Script_PrintScriptMethodsList';
procedure CorrectDisconnection; stdcall; external ConstScriptDLL name 'CorrectDisconnection';
{$EndRegion}





{$EndRegion}


{$Region 'TScript'}
function TScript.GetDressSpeed : Word;
begin
  Result := Script_GetDressSpeed;
end;

procedure TScript.SetDressSpeed(Value : Word);
begin
  Script_SetDressSpeed(Value);
end;

procedure TScript.AddToSystemJournal(Text : String);
begin
  Script_AddToSystemJournal(PChar(Text));
end;

procedure TScript.AddToSystemJournal(Text : Cardinal);
begin
  Script_AddToSystemJournal(PChar(IntToStr(Text)));
end;

function TScript.StealthInfo : TAboutData;
begin
  Result := Script_GetStealthInfo;
end;

function TScript.MsToDateTime(TimeMS : Cardinal) : TDateTime;
begin
  Result := Script_MsToDateTime(TimeMS);
end;

function TScript.GetWorldNum : Byte;
begin
  Result := Script_GetWorldNum;
end;

function TScript.GetLastContainer : Cardinal;
begin
  Result := Script_GetLastContainer;
end;

function TScript.GetLastTarget : Cardinal;
begin
  Result := Script_GetLastTarget;
end;

function TScript.GetLastAttack : Cardinal;
begin
  Result := Script_GetLastAttack;
end;

function TScript.GetLastStatus : Cardinal;
begin
  Result := Script_GetLastStatus;
end;

function TScript.GetLastObject : Cardinal;
begin
  Result := Script_GetLastObject;
end;

function TScript.GetBackpackID : Cardinal;
begin
  Result := Script_GetBackpackID;
end;

function TScript.GetGroundID : Cardinal;
begin
  Result := Script_GetGroundID;
end;

function TScript.GetSilentMode : Boolean;
begin
  Result := Script_GetSilentMode;
end;

procedure TScript.SetSilentMode(Value : Boolean);
begin
  Script_SetSilentMode(Value);
end;

function TScript.GetGlobalCharVar(VarName : String) : String;
begin
  Result := String(Script_GetGlobal(reg_char,PChar(VarName)));
end;

procedure TScript.SetGlobalCharVar(VarName, Value : String);
begin
  Script_SetGlobal(reg_char,PChar(VarName),PChar(Value));
end;

function TScript.GetGlobalStealthVar(VarName : String) : String;
begin
  Result := String(Script_GetGlobal(reg_stealth,PChar(VarName)));
end;

procedure TScript.SetGlobalStealthVar(VarName, Value : String);
begin
  Script_SetGlobal(reg_stealth,PChar(VarName),PChar(Value));
end;


procedure TScript.Wait(WaitTimeMS : Integer);
begin
  Script_Wait(WaitTimeMS);
end;

procedure TScript.UsePrimaryAbility;
begin
  Script_UsePrimaryAbility;
end;

procedure TScript.UseSecondaryAbility;
begin
  Script_UseSecondaryAbility;
end;

function TScript.GetActiveAbility : String;
begin
  Result := String(Script_GetAbility);
end;

procedure TScript.ToggleFly;
begin
  Script_ToggleFly;
end;

procedure TScript.UseVirtue(VirtueName : String);
begin
  Script_UseVirtue(PChar(VirtueName));
end;

procedure TScript.ReqVirtuesGump;
begin
  Script_ReqVirtuesGump;
end;

function TScript.CastSpell(SpellName : String) : Boolean;
begin
  Result := Script_CastSpell(PChar(SpellName));
end;

function TScript.CastSpellToObj(SpellName : String; ObjId : Cardinal) : Boolean;
begin
  Result := Script_CastSpellToObj(PChar(SpellName),ObjId);
end;

function TScript.IsActiveSpellAbility(SpellName : String) : Boolean;
begin
  Result := Script_IsActiveSpellAbility(PChar(SpellName));
end;

procedure TScript.UnsetCatchBag;
begin
  Script_UnsetCatchBag;
end;

function TScript.SetCatchBag(ObjectID : Cardinal) : Byte;
begin
  Result := Script_SetCatchBag(ObjectID);
end;

procedure TScript.UseObject(ObjectID : Cardinal);
begin
  Script_UseObject(ObjectID);
end;

function TScript.UseType(ObjType : Word; Color : Word) : Cardinal;
begin
  Result := Script_UseType(ObjType, Color);
end;

function TScript.UseFromGround(ObjType : Word; Color : Word) : Cardinal;
begin
  Result := Script_UseFromGround(ObjType, Color);
end;

procedure TScript.ClickOnObject(ObjectID : Cardinal);
begin
  Script_ClickOnObject(ObjectID);
end;

function TScript.GetClilocByID(ClilocID : Cardinal) : String;
begin
  Result := String(Script_GetClilocByID(ClilocID));
end;

procedure TScript.OpenDoor;
begin
  Script_OpenDoor;
end;

procedure TScript.Bow;
begin
  Script_Bow;
end;

procedure TScript.Salute;
begin
  Script_Salute;
end;

function TScript.GetQuestArrow : TPoint;
begin
  Result := Script_GetQuestArrow;
end;

function TScript.PlayWav(FileName : String) : Boolean;
begin
  Result := Script_PlayWav(PChar(FileName));
end;

procedure TScript.HelpRequest;
begin
  Script_HelpRequest;
end;

procedure TScript.QuestRequest;
begin
  Script_QuestRequest;
end;

procedure TScript.RenameMobile(Mob_ID : Cardinal; NewName : String);
begin
  Script_RenameMobile(Mob_ID, PChar(NewName));
end;

function TScript.MobileCanBeRenamed(Mob_ID : Cardinal) : Boolean;
begin
  Result := Script_MobileCanBeRenamed(Mob_ID);
end;

procedure TScript.ChangeStatLockState(statNum, statState : Byte);
begin
  Script_ChangeStatLockState(statNum, statState);
end;

function TScript.GetStaticArtBitmap(Id : LongWord; Hue : Word) : TBitmap;
var BufLen : Cardinal;
    Buf : Pointer;
    Stream : TMemoryStream;
begin
  Result := nil;
  Script_GetStaticArtBitmap(Id, Hue, nil, BufLen);
  if BufLen = 0 then Exit;
  GetMem(Buf, BufLen);
  Script_GetStaticArtBitmap(Id, Hue, Buf, BufLen);
  Stream := TMemoryStream.Create;
  Stream.Write(Buf^,BufLen);
  Stream.Position := 0;
  FreeMem(Buf);
  Result := TBitmap.Create;
  if Stream.Size > 4 then
    Result.LoadFromStream(Stream);
  Stream.Free;
end;

procedure TScript.SetAlarm;
begin
  Script_SetAlarm;
end;

function TScript.CheckLag(timeoutMS : Integer) : Boolean;
begin
  Result := Script_CheckLag(timeoutMS);
end;

procedure TScript.UOSay(Text : String);
begin
  Script_SendTextToUO(PChar(Text));
end;

procedure TScript.SendTextToUOColor(Text : String; Color : Word);
begin
  Script_SendTextToUOColor(PChar(Text), Color);
end;

procedure TScript.SetEventProc(const eventname : TPacketEvent; const method : Pointer);
begin
//  if method is TEvItemInfoCallBack then
{  case eventname of

  end;  }
  Script_SetEventProc(eventname, method);
end;

procedure TScript.ConsoleEntryReply(Text : String);
begin
  Script_ConsoleEntryReply(PChar(Text));
end;

procedure TScript.ConsoleEntryUnicodeReply(Text : String);
begin
  Script_ConsoleEntryUnicodeReply(PChar(Text));
end;

procedure TScript.FillInfoWindow(s : String);
begin
  Script_FillInfoWindow(PChar(s));
end;

procedure TScript.ClearInfoWindow;
begin
  Script_ClearInfoWindow;
end;

procedure TScript.FillInfoWindow(SA : TArray<String>);
var TempStr : String;
begin
  if Length(SA) > 0 then
    for TempStr in SA do
      Script_FillInfoWindow(PChar(TempStr));
end;

procedure TScript.WaitTextEntry(Value : String);
begin
  Script_WaitGumpTextEntry(PChar(Value));
end;


procedure TScript.SetCOMEnabled(Value : Boolean);
begin
  Script_SetCOMEnabled(Value);
end;

function TScript.PrintScriptMethodsList(Sorted : Boolean = False; Filename : String = '') : TArray<String>;
{var
  FContext : TRttiContext ;
  FType    : TRttiType ;
  FProp    : TRttiProperty ;
  FRecord  : TRttiRecordType ;
  Value    : TValue ;
  Data     : TValue ;
  ResStrList,ScriptStrList : TList<String>;}
begin
{ScriptStrList := TList<String>.Create;
ResStrList := TList<String>.Create;
FContext := TRttiContext.Create ;
  FType := FContext.GetType(TypeInfo(TScript));
  Result := DumpTypeDefinition(TypeInfo(TStringList));
  Result := DumpTypeDefinition(TypeInfo(TMyChar));
}//  GetInfo(FType.AsRecord, ScriptStrList,ResStrList);

end ;

{$EndRegion}

{$Region 'TConnection'}
procedure TConnection.SetARStatus(Value : Boolean);
begin
  Script_SetARStatus(Value);
end;

function TConnection.GetARStatus : Boolean;
begin
  Result := Script_GetARStatus;
end;

function TConnection.GetConnectedStatus : Boolean;
begin
  Result := Script_GetConnectedStatus;
end;

function TConnection.ChangeProfile(Name : String) : Integer;
begin
  Result := Script_ChangeProfile(PChar(Name));
end;

function TConnection.ChangeProfileEx(Name : String; ShardName : String = ''; CharName : String = '') : Integer;
begin
  Result := Script_ChangeProfileEx(PChar(Name),PChar(ShardName),PChar(CharName));
end;

function TConnection.ProfileName : String;
begin
  Result := String(Script_ProfileName);
end;

function TConnection.GetConnectedTime : TDateTime;
begin
  Result := Script_GetConnectedTime;
end;

function TConnection.GetDisconnectedTime : TDateTime;
begin
  Result := Script_GetDisconnectedTime;
end;

function TConnection.GetProfileShardName : String;
begin
  Result := String(Script_GetProfileShardName);
end;

function TConnection.GetShardName : String;
begin
  Result := String(Script_GetShardName);
end;

function TConnection.GetProxyIP : String;
begin
  Result := String(Script_GetProxyIP);
end;

function TConnection.GetProxyPort : Word;
begin
  Result := Script_GetProxyPort;
end;

function TConnection.GetUseProxy : Boolean;
begin
  Result := Script_GetUseProxy;
end;

procedure TConnection.Connect;
begin
  Script_Connect;
end;

procedure TConnection.Disconnect;
begin
  Script_Disconnect;
end;

procedure TConnection.SetPauseScriptOnDisconnectStatus(Value : Boolean);
begin
  Script_SetPauseScriptOnDisconnectStatus(Value);
end;

function TConnection.GetPauseScriptOnDisconnectStatus : Boolean;
begin
  Result := Script_GetPauseScriptOnDisconnectStatus;
end;
{$EndRegion}

{$Region 'TJournal'}
procedure TJournal.AddToJournal(Value : String);
begin
  Script_AddToJournal(PChar(Value));
end;

procedure TJournal.AddJournalIgnore(Str : String);
begin
  Script_AddJournalIgnore(PChar(Str));
end;

procedure TJournal.ClearJournalIgnore;
begin
  Script_ClearJournalIgnore;
end;

procedure TJournal.AddChatUserIgnore(User : String);
begin
  Script_AddChatUserIgnore(PChar(User));
end;

procedure TJournal.ClearChatUserIgnore;
begin
  Script_ClearChatUserIgnore;
end;

procedure TJournal.ClearJournal;
begin
  Script_ClearJournal;
end;

function TJournal.GetLastJournalMessage : String;
begin
  Result := String(Script_LastJournalMessage);
end;

function TJournal.InJournal(Str : String) : Integer;
begin
  Result := Script_InJournal(PChar(Str));
end;

function TJournal.InJournalBetweenTimes(Str : String; TimeBegin, TimeEnd : TDateTime) : Integer;
begin
  Result := Script_InJournalBetweenTimes(PChar(Str), TimeBegin, TimeEnd);
end;

function TJournal.GetJournalLine(StringIndex : Cardinal) : String;
begin
  Result := String(Script_Journal(StringIndex));
end;

procedure TJournal.SetJournalLine(StringIndex : Cardinal; Text : String);
begin
  Script_SetJournalLine(StringIndex,PChar(Text));
end;

function TJournal.WaitJournalLine(StartTime : TDateTime; Str : String; MaxWaitTimeMS : Integer) : Boolean;
begin
  Result := Script_WaitJournalLine(StartTime,PChar(Str), MaxWaitTimeMS);
end;

function TJournal.WaitJournalLineSystem(StartTime : TDateTime; Str : String; MaxWaitTimeMS : Integer) : Boolean;
begin
  Result := Script_WaitJournalLineSystem(StartTime,PChar(Str), MaxWaitTimeMS);
end;

function TJournal.GetLowJournal : Integer;
begin
  Result := Script_LowJournal;
end;

function TJournal.GetHighJournal : Integer;
begin
  Result := Script_HighJournal;
end;

{$EndRegion}

{$Region 'TLineFields'}
function TLineFields.GetFoundedParamID : Integer;
begin
  Result := Script_GetFoundedParamID;
end;

function TLineFields.GetLineID : Cardinal;
begin
  Result := Script_GetLineID;
end;

function TLineFields.GetLineType : Word;
begin
  Result := Script_GetLineType;
end;


function TLineFields.GetLineName : String;
begin
  Result := String(Script_GetLineName);
end;

function TLineFields.GetLineTime : TDateTime;
begin
  Result := Script_GetLineTime;
end;

function TLineFields.GetLineMsgType : Byte;
begin
  Result := Script_GetLineMsgType;
end;

function TLineFields.GetLineTextColor : Word;
begin
  Result := Script_GetLineTextColor;
end;

function TLineFields.GetLineTextFont : Word;
begin
  Result := Script_GetLineTextFont;
end;

function TLineFields.GetLineIndex : Integer;
begin
  Result := Script_GetLineIndex;
end;

function TLineFields.GetLineCount : Integer;
begin
  Result := Script_GetLineCount;
end;
{$EndRegion}

{$Region 'TMyChar'}
function TMyChar.GetSelfID : Cardinal;
begin
  Result := Script_GetSelfID;
end;

function TMyChar.GetSelfSex : Byte;
begin
  Result := Script_GetSelfSex;
end;

function TMyChar.GetCharTitle : String;
begin
  Result := String(Script_GetCharTitle);
end;

function TMyChar.GetCharName : String;
begin
  Result := String(Script_GetCharName);
end;

function TMyChar.GetSelfGold : Cardinal;
begin
  Result := Script_GetSelfGold;
end;

function TMyChar.GetSelfArmor : Word;
begin
  Result := Script_GetSelfArmor;
end;

function TMyChar.GetSelfWeight : Word;
begin
  Result := Script_GetSelfWeight;
end;

function TMyChar.GetSelfMaxWeight : Word;
begin
  Result := Script_GetSelfMaxWeight;
end;

function TMyChar.GetSelfRace : Byte;
begin
  Result := Script_GetSelfRace;
end;

function TMyChar.GetSelfPetsMax : Byte;
begin
  Result := Script_GetSelfPetsMax;
end;

function TMyChar.GetSelfPetsCurrent : Byte;
begin
  Result := Script_GetSelfPetsCurrent;
end;

function TMyChar.GetSelfFireResist : Word;
begin
  Result := Script_GetSelfFireResist;
end;

function TMyChar.GetSelfColdResist : Word;
begin
  Result := Script_GetSelfColdResist;
end;

function TMyChar.GetSelfPoisonResist : Word;
begin
  Result := Script_GetSelfPoisonResist;
end;

function TMyChar.GetSelfEnergyResist : Word;
begin
  Result := Script_GetSelfEnergyResist;
end;

function TMyChar.GetBackpackID : Cardinal;
begin
  Result := Script_GetBackpackID;
end;


function TMyChar.GetSelfStr : Integer;
begin
  Result := Script_GetSelfStr;
end;

function TMyChar.GetSelfInt : Integer;
begin
  Result := Script_GetSelfInt;
end;

function TMyChar.GetSelfDex : Integer;
begin
  Result := Script_GetSelfDex;
end;

function TMyChar.GetSelfLife : Integer;
begin
  Result := Script_GetSelfLife;
end;

function TMyChar.GetSelfMana : Integer;
begin
  Result := Script_GetSelfMana;
end;

function TMyChar.GetSelfStam : Integer;
begin
  Result := Script_GetSelfStam;
end;

function TMyChar.GetSelfMaxLife : Integer;
begin
  Result := Script_GetSelfMaxLife;
end;

function TMyChar.GetSelfMaxMana : Integer;
begin
  Result := Script_GetSelfMaxMana;
end;

function TMyChar.GetSelfMaxStam : Integer;
begin
  Result := Script_GetSelfMaxStam;
end;

function TMyChar.GetSelfLuck : Integer;
begin
  Result := Script_GetSelfLuck;
end;

function TMyChar.GetExtInfo : TExtendedInfo;
begin
  Result := Script_GetExtInfo;
end;

function TMyChar.GetHiddenStatus : Boolean;
begin
  Result := Script_GetHiddenStatus;
end;

function TMyChar.GetPoisonedStatus : Boolean;
begin
  Result := Script_GetPoisonedStatus;
end;

function TMyChar.GetParalyzedStatus : Boolean;
begin
  Result := Script_GetParalyzedStatus;
end;

function TMyChar.GetDeadStatus : Boolean;
begin
  Result := Script_GetDeadStatus;
end;

function TMyChar.GetWarModeStatus : Boolean;
begin
  Result := Script_GetWarModeStatus;
end;

procedure TMyChar.SetWarMode(Value : Boolean);
begin
  Script_SetWarMode(Value);
end;

function TMyChar.WarTargetID : Cardinal;
begin
  Result := Script_GetWarTarget;
end;

procedure TMyChar.Attack(AttackedID : Cardinal);
begin
  Script_Attack(AttackedID);
end;

procedure TMyChar.UseSelfPaperdollScroll;
begin
  Script_UseSelfPaperdollScroll;
end;

procedure TMyChar.UseOtherPaperdollScroll(ID : Cardinal);
begin
  Script_UseSelfPaperdollScroll;
end;

function TMyChar.ObjAtLayer(LayerType : Byte) : Cardinal;
begin
  Result := Script_ObjAtLayer(LayerType);
end;

function TMyChar.GetBuffBarInfo : TBuffBarInfo;
var BufLen : Cardinal;
    Buf : Pointer;
begin
  Result.Count := 0;
  Script_GetBuffBarInfo(nil, BufLen);
  if BufLen = 0 then Exit;
  SetLength(Result.Buffs, (BufLen - 1) div SizeOf(TBuffIcon));
  GetMem(Buf, BufLen);
  Script_GetBuffBarInfo(Buf, BufLen);
  Result.Count := BufLen div sizeof(TBuffIcon);
  SetLength(Result.Buffs, Result.Count);
  Move(Buf^,Result.Buffs[0],BufLen);
end;
{$EndRegion}

{$Region 'TUOObject'}
constructor TUOObject.Create(ObjID : Cardinal);
begin
  inherited Create;
  fObjID := ObjID;
  if Script_IsObjectExists(ObjID) and Script_IsNPC(ObjID) then
    Script_RequestStats(ObjID);
end;

function TUOObject.X : Integer;
begin
  Result := Script_GetX(fObjID);
end;

class function TUOObject.GetX(ObjID : Cardinal) : Integer;
begin
  Result := Script_GetX(ObjID);
end;

function TUOObject.Y : Integer;
begin
  Result := Script_GetY(fObjID);
end;

class function TUOObject.GetY(ObjID : Cardinal) : Integer;
begin
  Result := Script_GetY(ObjID);
end;

function TUOObject.Z : ShortInt;
begin
  Result := Script_GetZ(fObjID);
end;

class function TUOObject.GetZ(ObjID : Cardinal) : ShortInt;
begin
  Result := Script_GetZ(ObjID);
end;

function TUOObject.Name : String;
begin
  Result := String(Script_GetName(fObjID));
end;

class function TUOObject.GetName(ObjID : Cardinal) : String;
begin
  Result := String(Script_GetName(ObjID));
end;

function TUOObject.AltName : String;
begin
  Result := String(Script_GetAltName(fObjID));
end;

class function TUOObject.GetAltName(ObjID : Cardinal) : String;
begin
  Result := String(Script_GetAltName(ObjID));
end;

function TUOObject.Title : String;
begin
  Result := String(Script_GetTitle(fObjID));
end;

class function TUOObject.GetTitle(ObjID : Cardinal) : String;
begin
  Result := String(Script_GetTitle(ObjID));
end;

function TUOObject.GetClilocRec : TClilocRec;
begin
  Result := TUOObject.GetClilocRec(fObjID);
end;

class function TUOObject.GetClilocRec(ObjID : Cardinal) : TClilocRec;
var Res : TArray<Byte>;
    Len : Cardinal;
var i,k,m : Integer;
    ClilocRecStream : TMemoryStream;
begin
  Script_GetClilocRec(ObjID,nil,Len);
  SetLength(Res,Len);
  Script_GetClilocRec(ObjID,@res[0],Len);

  ClilocRecStream := TMemoryStream.Create;
  ClilocRecStream.Write(res[0], Len);
  ClilocRecStream.Position := 0;
  ClilocRecStream.Read(Result.Count,4);
  SetLength(Result.Items,Result.Count);
  for I := 0 to Result.Count - 1 do
  begin
    ClilocRecStream.Read(Result.Items[i].ClilocID,4);
    ClilocRecStream.Read(k,4);
    SetLength(Result.Items[i].Params,k);
    for m := 0 to k - 1 do
      Result.Items[i].Params[m] := ReadStringParam(ClilocRecStream);
  end;
  ClilocRecStream.Free;
end;

function TUOObject.GetTooltip : String;
begin
  Result := String(Script_GetTooltip(fObjID));
end;

class function TUOObject.GetTooltip(ObjID : Cardinal) : String;
begin
  Result := String(Script_GetTooltip(ObjID));
end;

function TUOObject.ObjType : Word;
begin
  Result := Script_GetType(fObjID);
end;

class function TUOObject.GetType(ObjID : Cardinal) : Word;
begin
  Result := Script_GetType(ObjID);
end;

function TUOObject.GetQuantity : Integer;
begin
  Result := Script_GetQuantity(fObjID);
end;

class function TUOObject.GetQuantity(ObjID : Cardinal) : Integer;
begin
  Result := Script_GetQuantity(ObjID);
end;

function TUOObject.IsObjectExists : Boolean;
begin
  Result := Script_IsObjectExists(fObjID);
end;

class function TUOObject.IsObjectExists(ObjID : Cardinal) : Boolean;
begin
  Result := Script_IsObjectExists(ObjID);
end;

function TUOObject.IsNPC : Boolean;
begin
  Result := Script_IsNPC(fObjID);
end;

class function TUOObject.IsNPC(ObjID : Cardinal) : Boolean;
begin
  Result := Script_IsNPC(ObjID);
end;

function TUOObject.GetPrice : Cardinal;
begin
  Result := Script_GetPrice(fObjID);
end;

class function TUOObject.GetPrice(ObjID : Cardinal) : Cardinal;
begin
  Result := Script_GetPrice(ObjID);
end;

function TUOObject.GetDirection : Byte;
begin
  Result := Script_GetDirection(fObjID);
end;

class function TUOObject.GetDirection(ObjID : Cardinal) : Byte;
begin
  Result := Script_GetDirection(ObjID);
end;

function TUOObject.GetDistance : Integer;
begin
  Result := Script_GetDistance(fObjID);
end;

class function TUOObject.GetDistance(ObjID : Cardinal) : Integer;
begin
  Result := Script_GetDistance(ObjID);
end;

function TUOObject.GetColor : Word;
begin
  Result := Script_GetColor(fObjID);
end;

class function TUOObject.GetColor(ObjID : Cardinal) : Word;
begin
  Result := Script_GetColor(ObjID);
end;

function TUOObject.GetStr : Integer;
begin
  Result := Script_GetStr(fObjID);
end;

class function TUOObject.GetStr(ObjID : Cardinal) : Integer;
begin
  Result := Script_GetStr(ObjID);
end;

function TUOObject.GetInt : Integer;
begin
  Result := Script_GetInt(fObjID);
end;

class function TUOObject.GetInt(ObjID : Cardinal) : Integer;
begin
  Result := Script_GetInt(ObjID);
end;

function TUOObject.GetDex : Integer;
begin
  Result := Script_GetDex(fObjID);
end;

class function TUOObject.GetDex(ObjID : Cardinal) : Integer;
begin
  Result := Script_GetDex(ObjID);
end;

function TUOObject.GetHP : Integer;
begin
  Result := Script_GetHP(fObjID);
end;

class function TUOObject.GetHP(ObjID : Cardinal) : Integer;
begin
  Result := Script_GetHP(ObjID);
end;

class function TUOObject.GetHP(ObjID,TimeOutMS : Cardinal) : Integer;
var STime : TDateTime;
begin
  STime := Now;
  repeat
  until (GetHP(ObjID) <> 0) and (Now > STime + (TimeOutMS/(1440*60*1000)));
  Result := GetHP(ObjID);
end;

function TUOObject.GetMaxHP : Integer;
begin
  Result := Script_GetMaxHP(fObjID);
end;

class function TUOObject.GetMaxHP(ObjID,TimeOutMS : Cardinal) : Integer;
var STime : TDateTime;
begin
  STime := Now;
  repeat
  until (GetMaxHP(ObjID) <> 0) and (Now > STime + (TimeOutMS/(1440*60*1000)));
  Result := GetMaxHP(ObjID);
end;

class function TUOObject.GetMaxHP(ObjID : Cardinal) : Integer;
begin
  Result := Script_GetMaxHP(ObjID);
end;

function TUOObject.GetMana : Integer;
begin
  Result := Script_GetMana(fObjID);
end;

class function TUOObject.GetMana(ObjID : Cardinal) : Integer;
begin
  Result := Script_GetMana(ObjID);
end;

function TUOObject.GetMaxMana : Integer;
begin
  Result := Script_GetMaxMana(fObjID);
end;

class function TUOObject.GetMaxMana(ObjID : Cardinal) : Integer;
begin
  Result := Script_GetMaxMana(ObjID);
end;

function TUOObject.GetStam : Integer;
begin
  Result := Script_GetStam(fObjID);
end;

class function TUOObject.GetStam(ObjID : Cardinal) : Integer;
begin
  Result := Script_GetStam(ObjID);
end;

function TUOObject.GetMaxStam : Integer;
begin
  Result := Script_GetMaxStam(fObjID);
end;

class function TUOObject.GetMaxStam(ObjID : Cardinal) : Integer;
begin
  Result := Script_GetMaxStam(ObjID);
end;

function TUOObject.GetNotoriety : Byte;
begin
  Result := Script_GetNotoriety(fObjID);
end;

class function TUOObject.GetNotoriety(ObjID : Cardinal) : Byte;
begin
  Result := Script_GetNotoriety(ObjID);
end;

function TUOObject.GetParent : Cardinal;
begin
  Result := Script_GetParent(fObjID);
end;

class function TUOObject.GetParent(ObjID : Cardinal) : Cardinal;
begin
  Result := Script_GetParent(ObjID);
end;

function TUOObject.IsWarMode : Boolean;
begin
  Result := Script_IsWarMode(fObjID);
end;

class function TUOObject.IsWarMode(ObjID : Cardinal) : Boolean;
begin
  Result := Script_IsWarMode(ObjID);
end;

function TUOObject.IsDead : Boolean;
begin
  Result := Script_IsDead(fObjID);
end;

class function TUOObject.IsDead(ObjID : Cardinal) : Boolean;
begin
  Result := Script_IsDead(ObjID);
end;

function TUOObject.IsRunning : Boolean;
begin
  Result := Script_IsRunning(fObjID);
end;

class function TUOObject.IsRunning(ObjID : Cardinal) : Boolean;
begin
  Result := Script_IsRunning(ObjID);
end;

function TUOObject.IsContainer : Boolean;
begin
  Result := Script_IsContainer(fObjID);
end;

class function TUOObject.IsContainer(ObjID : Cardinal) : Boolean;
begin
  Result := Script_IsContainer(ObjID);
end;

function TUOObject.IsHidden : Boolean;
begin
  Result := Script_IsHidden(fObjID);
end;

class function TUOObject.IsHidden(ObjID : Cardinal) : Boolean;
begin
  Result := Script_IsHidden(ObjID);
end;

function TUOObject.IsMovable : Boolean;
begin
  Result := Script_IsMovable(fObjID);
end;

class function TUOObject.IsMovable(ObjID : Cardinal) : Boolean;
begin
  Result := Script_IsMovable(ObjID);
end;

function TUOObject.IsYellowHits : Boolean;
begin
  Result := Script_IsYellowHits(fObjID);
end;

class function TUOObject.IsYellowHits(ObjID : Cardinal) : Boolean;
begin
  Result := Script_IsYellowHits(ObjID);
end;

function TUOObject.IsPoisoned : Boolean;
begin
  Result := Script_IsPoisoned(fObjID);
end;

class function TUOObject.IsPoisoned(ObjID : Cardinal) : Boolean;
begin
  Result := Script_IsPoisoned(ObjID);
end;

function TUOObject.IsParalyzed : Boolean;
begin
  Result := Script_IsParalyzed(fObjID);
end;

class function TUOObject.IsParalyzed(ObjID : Cardinal) : Boolean;
begin
  Result := Script_IsParalyzed(ObjID);
end;

function TUOObject.IsFemale : Boolean;
begin
  Result := Script_IsFemale(fObjID);
end;

class function TUOObject.IsFemale(ObjID : Cardinal) : Boolean;
begin
  Result := Script_IsFemale(ObjID);
end;

function TUOObject.ObjAtLayerEx(LayerType : Byte) : Cardinal;
begin
  Result := Script_ObjAtLayerEx(LayerType, fObjID);
end;

class function TUOObject.ObjAtLayerEx(LayerType : Byte; PlayerID : Cardinal) : Cardinal;
begin
  Result := Script_ObjAtLayerEx(LayerType, PlayerID);
end;

function TUOObject.GetLayer : Byte;
begin
  Result := Script_GetLayer(fObjID);
end;

class function TUOObject.GetLayer(ObjID : Cardinal) : Byte;
begin
  Result := Script_GetLayer(ObjID);
end;

procedure TUOObject.RequestStats;
begin
  Script_RequestStats(fObjID);
end;

class procedure TUOObject.RequestStats(ObjID : Cardinal);
begin
  Script_RequestStats(ObjID);
end;


{$EndRegion}

{$Region 'TFindEngine'}
procedure TFindEngine.SetFindDistance(Value : Cardinal);
begin
  Script_SetFindDistance(Value);
end;

function TFindEngine.GetFindDistance : Cardinal;
begin
  Result := Script_GetFindDistance;
end;

procedure TFindEngine.SetFindVertical(Value : Cardinal);
begin
  Script_SetFindVertical(Value);
end;

function TFindEngine.GetFindVertical : Cardinal;
begin
  Result := Script_GetFindVertical;
end;

procedure TFindEngine.SetFindInNulPoint(Value : Boolean);
begin
  Script_SetFindInNulPoint(Value);
end;

function TFindEngine.GetFindInNulPoint : Boolean;
begin
  Result := Script_GetFindInNulPoint;
end;

function TFindEngine.FindTypeEx(ObjType : Word; Color : Word; Container : Cardinal; InSub : Boolean) : Cardinal;
begin
  Result := Script_FindTypeEx(ObjType, Color, Container, InSub);
end;

function TFindEngine.FindType(ObjType : Word; Container : Cardinal) : Cardinal;
begin
  Result := Script_FindType(ObjType, Container);
end;

function TFindEngine.FindTypesArrayEx(ObjTypes, Colors : Array of word; Containers : Array of Cardinal; InSub : Boolean) : Cardinal;
begin
  Result := Script_FindTypesArrayEx(@(ObjTypes[0]), Length(ObjTypes) * 2,
                                    @(Colors[0]), Length(Colors) * 2,
                                    @(Containers[0]), Length(Containers) * 4,
                                    InSub);
end;

function TFindEngine.FindNotoriety(ObjType : Word; Notoriety : Byte) : Cardinal;
begin
  Result := Script_FindNotoriety(ObjType, Notoriety);
end;

function TFindEngine.FindAtCoord(X, Y : Word) : Cardinal;
begin
  Result := Script_FindNotoriety(X, Y);
end;

procedure TFindEngine.Ignore(ObjID : Cardinal);
begin
  Script_Ignore(ObjID);
end;

procedure TFindEngine.IgnoreRemove(ObjID : Cardinal);
begin
  Script_IgnoreOff(ObjID);
end;

procedure TFindEngine.IgnoreReset;
begin
  Script_IgnoreReset;
end;

function TFindEngine.GetIgnoreList : TArray<Cardinal>;
var BufLen : Cardinal;
begin
  Script_GetIgnoreList(nil, BufLen);
  if BufLen = 0 then Exit;
  SetLength(Result,BufLen div 4);
  Script_GetIgnoreList(Result, BufLen);
end;

function TFindEngine.GetFindedList : TArray<Cardinal>;
var BufLen : Cardinal;
begin
  Script_GetFindedList(nil, BufLen);
  if BufLen = 0 then Exit;
  SetLength(Result,BufLen div 4);
  Script_GetFindedList(Result, BufLen);
end;

function TFindEngine.FindItem : Cardinal;
begin
  Result := Script_GetFindItem;
end;

function TFindEngine.FindCount : Integer;
begin
  Result := Script_GetFindCount;
end;

function TFindEngine.FindQuantity : Integer;
begin
  Result := Script_GetFindQuantity;
end;

function TFindEngine.FindFullQuantity : Integer;
begin
  Result := Script_GetFindFullQuantity;
end;
{$EndRegion}

{$Region 'TMoveItemEngine'}
function TMoveItemEngine.GetDropCheckCoord : Boolean;
begin
  Result := Script_GetDropCheckCoord;
end;

procedure TMoveItemEngine.SetDropCheckCoord(Value : Boolean);
begin
  Script_SetDropCheckCoord(Value);
end;

function TMoveItemEngine.GetDropDelay : Cardinal;
begin
  Result := Script_GetDropDelay;
end;

procedure TMoveItemEngine.SetDropDelay(Value : Cardinal);
begin
  Script_SetDropDelay(Value);
end;

function TMoveItemEngine.DragItem(ItemID : Cardinal; Count : Integer) : Boolean;
begin
  Result := Script_DragItem(ItemID,Count);
end;

function TMoveItemEngine.DropItem(MoveIntoID : Cardinal; X, Y : Word; Z : ShortInt) : Boolean;
begin
  Result := Script_DropItem(MoveIntoID, X, Y, Z);
end;

function TMoveItemEngine.MoveItem(ItemID : Cardinal; Count : Integer; MoveIntoID : Cardinal; X, Y : Word; Z : ShortInt) : Boolean;
begin
  Result := Script_MoveItem(ItemID, Count, MoveIntoID, X, Y, Z);
end;

function TMoveItemEngine.Grab(ItemID : Cardinal; Count : Integer) : Boolean;
begin
  Result := Script_Grab(ItemID,Count);
end;

function TMoveItemEngine.Drop(ItemID : Cardinal; Count : Integer; X, Y : Smallint; Z : ShortInt) : Boolean;
begin
  Result := Script_Drop(ItemID, Count, X, Y, Z);
end;

function TMoveItemEngine.DropHere(ItemID : Cardinal) : Boolean;
begin
  Result := Script_DropHere(ItemID);
end;

function TMoveItemEngine.MoveItems(Container : Cardinal; ItemsType : Word; ItemsColor : Word; MoveIntoID : Cardinal; X, Y : Word; Z : ShortInt; DelayMS : Integer) : Boolean;
begin
  Result := Script_MoveItems(Container, ItemsType, ItemsColor, MoveIntoID, X, Y, Z, DelayMS);
end;

function TMoveItemEngine.EmptyContainer(Container, DestContainer : Cardinal; delay_ms : Word) : Boolean;
begin
  Result := Script_EmptyContainer(Container, DestContainer,delay_ms);
end;

{$EndRegion}

{$Region 'TSecureTrade'}

function TSecureTrade.CheckTradeState : Boolean;
begin
  Result := Script_CheckTradeState;
end;

function TSecureTrade.GetTradeContainer(TradeNum, Num : Byte) : Cardinal;
begin
  Result := Script_GetTradeContainer(TradeNum, Num);
end;

function TSecureTrade.GetTradeOpponent(TradeNum : Byte) : Cardinal;
begin
  Result := Script_GetTradeOpponent(TradeNum);
end;

function TSecureTrade.GetTradeCount : Byte;
begin
  Result := Script_GetTradeCount;
end;

function TSecureTrade.GetTradeOpponentName(TradeNum : Byte) : String;
begin
  Result := String(Script_GetTradeOpponentName(TradeNum));
end;

function TSecureTrade.TradeCheck(TradeNum, Num : Byte) : Boolean;
begin
  Result := Script_TradeCheck(TradeNum, Num);
end;

procedure TSecureTrade.ConfirmTrade(TradeNum : Byte);
begin
  Script_ConfirmTrade(TradeNum);
end;

function TSecureTrade.CancelTrade(TradeNum : Byte) : Boolean;
begin
  Result := Script_CancelTrade(TradeNum);
end;


{$EndRegion}

{$Region 'TMenu'}
procedure TMenu.WaitMenu(MenuCaption, ElementCaption : String);
begin
  Script_WaitMenu(PChar(MenuCaption),PChar(ElementCaption));
end;

procedure TMenu.AutoMenu(MenuCaption, ElementCaption : String);
begin
  Script_AutoMenu(PChar(MenuCaption),PChar(ElementCaption));
end;

function TMenu.MenuHookPresent : Boolean;
begin
  Result := Script_MenuHookPresent;
end;

function TMenu.MenuPresent : Boolean;
begin
  Result := Script_MenuPresent;
end;

procedure TMenu.CancelMenu;
begin
  Script_CancelMenu;
end;

procedure TMenu.CloseMenu;
begin
  Script_CloseMenu;
end;

function TMenu.GetMenuItems(MenuCaption : String) : TArray<String>;
begin
  Result := String(Script_GetMenuItems(PChar(MenuCaption))).Replace(#10,'').Split([#13]);
end;

function TMenu.GetLastMenuItems : TArray<String>;
begin
  Result := String(Script_GetLastMenuItems).Replace(#10,'').Split([#13]);
end;

{$EndRegion}

{$Region 'TContextMenu'}
procedure TContextMenu.RequestContextMenu(ObjectID : Cardinal);
begin
  Script_RequestContextMenu(ObjectID);
end;

procedure TContextMenu.SetContextMenuHook(MenuID : Cardinal; EntryNumber : Byte);
begin
  Script_SetContextMenuHook(MenuID,EntryNumber);
end;

function TContextMenu.GetContextMenu : TArray<String>;
begin
  Result := String(Script_GetContextMenu).Replace(#10,'').Split([#13]);
end;

function TContextMenu.GetContextMenuRec : TContextMenuRec;
begin
//  Result.ClilocStr := String(Script_GetContextMenuRec(Result.Tag, Result.Flags));
end;



procedure TContextMenu.ClearContextMenu;
begin
  Script_ClearContextMenu;
end;

{$EndRegion}

{$Region 'TShop'}
function TShop.GetAutoBuyDelay : Word;
begin
  Result := Script_GetAutoBuyDelay;
end;

procedure TShop.SetAutoBuyDelay(Value : Word);
begin
  Script_SetAutoBuyDelay(Value);
end;

function TShop.GetAutoSellDelay : Word;
begin
  Result := Script_GetAutoSellDelay;
end;

procedure TShop.SetAutoSellDelay(Value : Word);
begin
  Script_SetAutoSellDelay(Value);
end;

procedure TShop.AutoBuy(ItemType, ItemColor, Quantity : Word);
begin
  Script_AutoBuy(ItemType, ItemColor, Quantity);
end;

function TShop.GetShopList : TArray<String>;
begin
  Result := String(Script_GetShopList).Replace(#10,'').Split([#13]);
end;

procedure TShop.ClearShopList;
begin
  Script_ClearShopList;
end;

procedure TShop.AutoBuyEx(ItemType : Word; ItemColor : Word; Quantity : Word; Price : Cardinal; Name : String);
begin
  Script_AutoBuyEx(ItemType, ItemColor, Quantity,Price, PChar(Name));
end;

procedure TShop.AutoSell(ItemType, ItemColor, Quantity : Word);
begin
  Script_AutoSell(ItemType, ItemColor, Quantity);
end;

{$EndRegion}

{$Region 'TParty'}
procedure TParty.InviteToParty(ObjectID : Cardinal);
begin
  Script_InviteToParty(ObjectID);
end;

procedure TParty.RemoveFromParty(ObjectID : Cardinal);
begin
  Script_RemoveFromParty(ObjectID);
end;

procedure TParty.PartyMessageTo(ObjectID : Cardinal; Msg : String);
begin
  Script_PartyMessageTo(ObjectID,PChar(Msg));
end;

procedure TParty.PartySay(Msg : String);
begin
  Script_PartySay(PChar(Msg));
end;

procedure TParty.PartyCanLootMe(Value : Boolean);
begin
  Script_PartyCanLootMe(Value);
end;

procedure TParty.PartyAcceptInvite;
begin
  Script_PartyAcceptInvite;
end;

procedure TParty.PartyDeclineInvite;
begin
  Script_PartyDeclineInvite;
end;

procedure TParty.PartyLeave;
begin
  Script_PartyLeave;
end;

function TParty.InParty : Boolean;
begin
  Result := Script_InParty;
end;

function TParty.PartyMembersList : TArray<Cardinal>;
var BufLen : Cardinal;
    Buf : Pointer;
begin
  Script_PartyMembersList(nil, BufLen);
  if BufLen > 3 then
  begin
    GetMem(Buf, BufLen);
    Script_PartyMembersList(Buf, BufLen);
    SetLength(Result,BufLen div 4);
    Move(Buf^,Result,BufLen);
    FreeMem(Buf);
  end;
end;
{$EndRegion}

{$Region 'THTTP'}
procedure THTTP.Get(URL : String);
begin
  Script_HTTP_Get(PChar(URL));
end;

function THTTP.Post(URL, PostData : String) : String;
begin
  Result := String(Script_HTTP_Post(PChar(URL),PChar(PostData)));
end;

function THTTP.GetBody : String;
begin
  Result := String(Script_HTTP_Body);
end;

function THTTP.GetHeader : String;
begin
  Result := String(Script_HTTP_Header);
end;

{$EndRegion}

{$Region 'TICQ'}
function TICQ.GetConnectedStatus : Boolean;
begin
  Result := Script_ICQ_GetConnectedStatus;
end;

procedure TICQ.Connect(UIN : Cardinal; Password : String);
begin
  Script_ICQ_Connect(UIN, PChar(Password));
end;

procedure TICQ.Disconnect;
begin
  Script_ICQ_Disconnect;
end;

procedure TICQ.SetStatus(Num : Byte);
begin
  Script_ICQ_SetStatus(Num);
end;

procedure TICQ.SetXStatus(Num : Byte);
begin
  Script_ICQ_SetXStatus(Num);
end;

procedure TICQ.SendText(DestinationUIN : Cardinal; Text : String);
begin
  Script_ICQ_SendText(DestinationUIN,PChar(Text));
end;

{$EndRegion}

{$Region 'TSkype'}
function TSkype.GetConnected : Boolean;
begin
  Result := Script_Skype_Connected;
end;

procedure TSkype.Connect(Login : String; Password : String);
begin
  Script_Skype_Connect(PChar(Login), PChar(Password));
end;

procedure TSkype.Disconnect;
begin
  Script_Skype_Disconnect;
end;

procedure TSkype.SendMessage(Msg : String; UserID : String);
begin
  Script_Skype_SendMessage(PChar(Msg), PChar(UserID));
end;

function TSkype.GetNicknameByID(ID : String) : String;
begin
  Script_Skype_GetNicknameByID(PChar(ID));
end;

function TSkype.GetIDByNickname(Nickname : String) : String;
begin
  Script_Skype_GetIDByNickname(PChar(Nickname));
end;

{$EndRegion}

{$Region 'TClient'}

procedure TClient.Print(Msg : String);
begin
  Script_ClientPrint(PChar(Msg));
end;

procedure TClient.PrintEx(SenderID : Cardinal; Color, Font : Word; Msg : String);
begin
  Script_ClientPrintEx(SenderID,Color, Font, PChar(Msg));
end;

procedure TClient.CloseUIWindow(UIWindowType : TUIWindowType; ID : Cardinal);
begin
  Script_CloseClientUIWindow(UIWindowType,ID);
end;

procedure TClient.RequestObjectTarget;
begin
  Script_ClientRequestObjectTarget;
end;

procedure TClient.RequestTileTarget;
begin
  Script_ClientRequestTileTarget;
end;

function TClient.TargetResponsePresent : Boolean;
begin
  Result := Script_ClientTargetResponsePresent;
end;

function TClient.TargetResponse : TTargetInfo;
begin
  Result := Script_ClientTargetResponse;
end;

function TClient.WaitForTargetResponse(MaxWaitTimeMS : Integer) : Boolean;
begin
  Result := Script_WaitForClientTargetResponse(MaxWaitTimeMS);
end;

{$EndRegion}

{$Region 'TSkill'}
constructor TSkill.Create(SkillName : String);
begin
  inherited Create;
  fSkillName := SkillName;
end;

function TSkill.Use : Boolean;
begin
  Result := Script_UseSkill(PChar(fSkillName));
end;

class function TSkill.Use(SkillName : String) : Boolean;
begin
  Result := Script_UseSkill(PChar(SkillName));
end;

procedure TSkill.ChangeLockState(skillState : TSkillState);
begin
  Script_ChangeSkillLockState(PChar(fSkillName),Byte(skillState));
end;

class procedure TSkill.ChangeLockState(SkillName : String; skillState : TSkillState);
begin
  Script_ChangeSkillLockState(PChar(SkillName),Byte(skillState));
end;

function TSkill.GetCap : Double;
begin
  Result := Script_GetSkillCap(PChar(fSkillName));
end;

class function TSkill.GetCap(SkillName : String) : Double;
begin
  Result := Script_GetSkillCap(PChar(SkillName));
end;

function TSkill.GetValue : Double;
begin
  Result := Script_GetSkillValue(PChar(fSkillName));
end;

class function TSkill.GetValue(SkillName : String) : Double;
begin
  Result := Script_GetSkillValue(PChar(SkillName));
end;

function TSkill.GetCurrentValue : Double;
begin
  Result := Script_GetSkillCurrentValue(PChar(fSkillName));
end;

class function TSkill.GetCurrentValue(SkillName : String) : Double;
begin
  Result := Script_GetSkillCurrentValue(PChar(SkillName));
end;
{$EndRegion}

{$Region 'TEasyUO'}
procedure TEasyUO.SetEUOVar(VarNum : Byte; VarValue : String);
begin
  Script_SetEasyUO(VarNum, PChar(VarValue));
end;

function TEasyUO.GetEUOVar(VarNum : Byte) : String;
begin
  Result := String(Script_GetEasyUO(VarNum));
end;

function TEasyUO.EUO2StealthType(EUO : String) : Word;
begin
  Result := Script_EUO2StealthType(PChar(EUO));
end;

function TEasyUO.EUO2StealthID(EUO : String) : Cardinal;
begin
  Result := Script_EUO2StealthID(PChar(EUO));
end;

{$EndRegion}

{$Region 'TPath'}
function TPath.GetStealthPath : String;
begin
Result := String(Script_GetStealthPath);
end;

function TPath.GetCurrentScriptPath : String;
begin
Result := String(Script_GetCurrentScriptPath);
end;

function TPath.GetStealthProfilePath : String;
begin
Result := String(Script_GetStealthProfilePath);
end;

function TPath.GetShardPath : String;
begin
Result := String(Script_GetShardPath);
end;

{$EndRegion}

{$Region 'TMover'}
procedure TMover.SetRunUnmountTimer(Value : Word);
begin
  Script_SetRunUnmountTimer(Value);
end;

procedure TMover.SetWalkMountTimer(Value : Word);
begin
  Script_SetWalkMountTimer(Value);
end;

procedure TMover.SetRunMountTimer(Value : Word);
begin
  Script_SetRunMountTimer(Value);
end;

procedure TMover.SetWalkUnmountTimer(Value : Word);
begin
  Script_SetWalkUnmountTimer(Value);
end;

function TMover.GetRunMountTimer : Word;
begin
  Result := Script_GetRunMountTimer;
end;

function TMover.GetWalkMountTimer : Word;
begin
  Result := Script_GetWalkMountTimer;
end;

function TMover.GetRunUnmountTimer : Word;
begin
  Result := Script_GetRunUnmountTimer;
end;

function TMover.GetWalkUnmountTimer : Word;
begin
  Result := Script_GetWalkUnmountTimer;
end;

function TMover.GetLastStepQUsedDoor : Cardinal;
begin
  Result := Script_GetLastStepQUsedDoor;
end;

function TMover.Step(Direction : Byte; Running : Boolean) : TStepResult;
begin
  Result := TStepResult(Script_Step(Direction, Running));
end;

function TMover.StepQ(Direction : Byte; Running : Boolean) : Integer;
begin
  Result := Script_StepQ(Direction, Running);
end;

function TMover.MoveXYZ(Xdst, Ydst : Word; Zdst : ShortInt; AccuracyXY, AccuracyZ : Integer; Running : Boolean) : Boolean;
begin
  Result := Script_MoveXYZ(Xdst, Ydst, Zdst, AccuracyXY, AccuracyZ, Running);
end;

function TMover.newMoveXY(Xdst, Ydst : Word; Optimized : Boolean; Accuracy : Integer; Running : Boolean) : Boolean;
begin
  Result := Script_newMoveXY(Xdst, Ydst, Optimized, Accuracy, Running);
end;

procedure TMover.SetBadLocation(X, Y : Word);
begin
  Script_SetBadLocation(X, Y);
end;

procedure TMover.SetGoodLocation(X, Y : Word);
begin
  Script_SetGoodLocation(X, Y);
end;

procedure TMover.ClearBadLocationList;
begin
  Script_ClearBadLocationList;
end;

procedure TMover.SetBadObject(ObjType, Color : Word; Radius : Byte);
begin
  Script_SetBadObject(ObjType, Color, Radius);
end;

procedure TMover.ClearBadObjectList;
begin
  Script_ClearBadObjectList;
end;

function TMover.CheckLOS(xf, yf : Word; zf : ShortInt; xt, yt : Word; zt : ShortInt; WorldNum : Byte; LOSCheckType : TLOSCheckType; LOSCheckOptions : TLOSCheckOptions) : Boolean;
var LOSOptions : Cardinal;
begin
LOSOptions := 0;
if losSphereCheckCorners in LOSCheckOptions then
  LOSOptions := $100;
if losPolUseNoShoot in LOSCheckOptions then
  LOSOptions := LOSOptions OR $200;
if losPolLOSThroughWindow in LOSCheckOptions then
  LOSOptions := LOSOptions OR $400;
  Result := Script_CheckLOS(xf, yf, zf, xt, yt, zt, WorldNum,Byte(LOSCheckType),LOSOptions);
end;

function TMover.GetPathArray(DestX, DestY : Word; Optimized : Boolean; Accuracy : Integer): TArray<TMyPoint>;
var BufLen : Cardinal;
begin
  Script_GetPathArray(DestX, DestY, Optimized, Accuracy, nil, BufLen);
  if BufLen = 0 then Exit;
  SetLength(Result,BufLen div SizeOf(TMyPoint));
  Script_GetPathArray(DestX, DestY, Optimized, Accuracy, Result, BufLen);
end;

function TMover.GetPathArray3D(StartX, StartY : Word; StartZ : Shortint; FinishX, FinishY : Word; FinishZ : Shortint; WorldNum : Byte; AccuracyXY, AccuracyZ : Integer; Run : Boolean): TArray<TMyPoint>;
var BufLen : Cardinal;
begin
  Script_GetPathArray3D(StartX, StartY, StartZ, FinishX, FinishY, FinishZ, WorldNum, AccuracyXY, AccuracyZ, Run, nil, BufLen);
  if BufLen = 0 then Exit;
  SetLength(Result,BufLen div SizeOf(TMyPoint));
  Script_GetPathArray3D(StartX, StartY, StartZ, FinishX, FinishY, FinishZ, WorldNum, AccuracyXY, AccuracyZ, Run, Result, BufLen);
end;

function TMover.Dist(x1, y1, x2, y2 : word) : word;
begin
  Result := Script_Dist(x1, y1, x2, y2);
end;

procedure TMover.CalcCoord(x, y : word; Dir : byte; var x2, y2 : word);
begin
  Script_CalcCoord(x, y, Dir, x2, y2);
end;

function TMover.CalcDir(Xfrom, Yfrom, Xto, Yto : integer) : byte;
begin
  Result := Script_CalcDir(Xfrom, Yfrom, Xto, Yto);
end;

function TMover.PredictedX : Word;
begin
  Result := Script_PredictedX;
end;

function TMover.PredictedY : Word;
begin
  Result := Script_PredictedY;
end;

function TMover.PredictedZ : ShortInt;
begin
  Result := Script_PredictedZ;
end;

function TMover.PredictedDirection : Byte;
begin
  Result := Script_PredictedDirection;
end;

procedure TMover.SetMoveOpenDoor(Value : Boolean);
begin
  Script_SetMoveOpenDoor(Value);
end;

function TMover.GetMoveOpenDoor : Boolean;
begin
  Result := Script_GetMoveOpenDoor;
end;

procedure TMover.SetMoveThroughNPC(Value : Word);
begin
  Script_SetMoveThroughNPC(Value);
end;

function TMover.GetMoveThroughNPC : Word;
begin
  Result := Script_GetMoveThroughNPC;
end;

procedure TMover.SetMoveThroughCorner(Value : Boolean);
begin
  Script_SetMoveThroughCorner(Value);
end;

function TMover.GetMoveThroughCorner : Boolean;
begin
  Result := Script_GetMoveThroughCorner;
end;

procedure TMover.SetMoveHeuristicMult(Value : Integer);
begin
  Script_SetMoveHeuristicMult(Value);
end;

function TMover.GetMoveHeuristicMult : Integer;
begin
  Result := Script_GetMoveHeuristicMult;
end;

{$EndRegion}

{$Region 'TTileWork'}
function TTileWork.GetTileFlags(TileGroup : TileFlagsType; Tile : Word) : Cardinal;
begin
  Result := Script_GetTileFlags(TileGroup, Tile);
end;

function TTileWork.ConvertFlagsToFlagSet(TileGroup : TileFlagsType; Flags : LongWord) : TTileDataFlagSet;
begin
  Result := Script_ConvertFlagsToFlagSet(TileGroup, Flags);
end;

function TTileWork.GetLandTileData(Tile : Word) : TLandTileData;
begin
  Result := Script_GetLandTileData(Tile);
end;

function TTileWork.GetStaticTileData(Tile : Word) : TStaticTileData;
begin
  Result := Script_GetStaticTileData(Tile);
end;

function TTileWork.GetCell(X, Y : Word; WorldNum : Byte) : TMapCell;
begin
  Result := Script_GetCell(X, Y, WorldNum);
end;

function TTileWork.GetLayerCount(X, Y : word; WorldNum : byte) : Byte;
begin
  Result := Script_GetLayerCount(X, Y, WorldNum);
end;

function TTileWork.ReadStaticsXY(X, Y : word; WorldNum : byte) : TStaticCellRealXY;
var BufLen : Cardinal;
begin
  Script_ReadStaticsXY(X, Y, WorldNum, nil, BufLen);
  if BufLen = 0 then Exit;
  SetLength(Result.Statics,BufLen div SizeOf(TStaticItemRealXY));
  Script_ReadStaticsXY(X, Y, WorldNum, Result.Statics, BufLen);
  Result.StaticCount := Length(Result.Statics);
end;

function TTileWork.GetSurfaceZ(X, Y : word; WorldNum : Byte) : ShortInt;
begin
  Result := Script_GetSurfaceZ(X, Y, WorldNum);
end;

function TTileWork.IsWorldCellPassable(CurrX, CurrY : Word; CurrZ : ShortInt; DestX, DestY : Word; var DestZ : ShortInt; WorldNum : byte) : Boolean;
begin
  Result := Script_IsWorldCellPassable(CurrX, CurrY, CurrZ, DestX, DestY, DestZ, WorldNum);
end;

function TTileWork.GetStaticTilesArray(Xmin, Ymin, Xmax, Ymax : Word; WorldNum: Byte; TileTypes: Array of Word) : TFoundTilesArray;
var Buf : Pointer;
    ArrLen : Word;
begin
  ArrLen := Script_GetStaticTilesArray(Xmin, Ymin, Xmax, Ymax, WorldNum, @(TileTypes[0]), Length(TileTypes) * 2, nil);
  if ArrLen > 0 then
  begin
    GetMem(Buf, ArrLen * SizeOf(TFoundTile));
    ArrLen := Script_GetStaticTilesArray(Xmin, Ymin, Xmax, Ymax, WorldNum, @(TileTypes[0]), Length(TileTypes) * 2, Buf);
    SetLength(Result,ArrLen);
    Move(Buf^,Result[0],ArrLen * SizeOf(TFoundTile));
    FreeMem(Buf);
  end;
end;

function TTileWork.GetLandTilesArray(Xmin, Ymin, Xmax, Ymax : Word; WorldNum: Byte; TileTypes: Array of Word) : TFoundTilesArray;
var Buf : Pointer;
    ArrLen : Word;
begin
  ArrLen := Script_GetLandTilesArray(Xmin, Ymin, Xmax, Ymax, WorldNum, @(TileTypes[0]), Length(TileTypes) * 2, nil);
  if ArrLen > 0 then
  begin
    GetMem(Buf, ArrLen * SizeOf(TFoundTile));
    ArrLen := Script_GetLandTilesArray(Xmin, Ymin, Xmax, Ymax, WorldNum, @(TileTypes[0]), Length(TileTypes) * 2, Buf);
    SetLength(Result,ArrLen);
    Move(Buf^,Result[0],ArrLen * SizeOf(TFoundTile));
    FreeMem(Buf);
  end;
end;

{$EndRegion}

{$Region 'TGump'}
procedure TGump.WaitGump(Value : Integer);
begin
  Script_WaitGumpInt(Value);
end;

procedure TGump.WaitGumpStr(Value : String);
begin
  Script_WaitGump(PChar(Value));
end;


procedure TGump.GumpAutoTextEntry(TextEntryID : Integer; Value : String);
begin
  Script_GumpAutoTextEntry(TextEntryID, PChar(Value));
end;

procedure TGump.GumpAutoRadiobutton(RadiobuttonID, Value : Integer);
begin
  Script_GumpAutoRadiobutton(RadiobuttonID, Value);
end;

procedure TGump.GumpAutoCheckBox(CBID, Value : Integer);
begin
  Script_GumpAutoCheckBox(CBID, Value);
end;

function TGump.NumGumpButton(GumpIndex : Word; Value : Integer) : Boolean;
begin
  Result := Script_NumGumpButton(GumpIndex, Value);
end;

function TGump.NumGumpTextEntry(GumpIndex : Word; TextEntryID : Integer; Value : String) : Boolean;
begin
  Result := Script_NumGumpTextEntry(GumpIndex, TextEntryID, PChar(Value));
end;

function TGump.NumGumpRadiobutton(GumpIndex : Word; RadiobuttonID, Value : Integer) : Boolean;
begin
  Result := Script_NumGumpRadiobutton(GumpIndex, RadiobuttonID, Value);
end;

function TGump.NumGumpCheckBox(GumpIndex : Word; CBID, Value : Integer) : Boolean;
begin
  Result := Script_NumGumpCheckBox(GumpIndex, CBID, Value);
end;

function TGump.GetGumpsCount : Cardinal;
begin
  Result := Script_GetGumpsCount;
end;

procedure TGump.CloseSimpleGump(GumpIndex : Word);
begin
  Script_CloseSimpleGump(GumpIndex);
end;

function TGump.IsGump : Boolean;
begin
  Result := Script_IsGump;
end;

function TGump.GetGumpSerial(GumpIndex : Word) : Cardinal;
begin
  Result := Script_GetGumpSerial(GumpIndex);
end;

function TGump.GetGumpID(GumpIndex : Word) : Cardinal;
begin
  Result := Script_GetGumpID(GumpIndex);
end;

function TGump.GetGumpNoClose(GumpIndex : Word) : Boolean;
begin
  Result := Script_GetGumpNoClose(GumpIndex);
end;

function TGump.GetGumpTextLines(GumpIndex : Word) : TArray<String>;
begin
  Result := String(Script_GetGumpTextLines(GumpIndex)).Replace(#10,'').Split([#13]);
end;

function TGump.GetGumpFullLines(GumpIndex : Word) : TArray<String>;
begin
  Result := String(Script_GetGumpFullLines(GumpIndex)).Replace(#10,'').Split([#13]);
end;

function TGump.GetGumpShortLines(GumpIndex : Word) : TArray<String>;
begin
  Result := String(Script_GetGumpShortLines(GumpIndex)).Replace(#10,'').Split([#13]);
end;

function TGump.GetGumpButtonsDescription(GumpIndex : Word) : TArray<String>;
begin
  Result := String(Script_GetGumpButtonsDescription(GumpIndex)).Replace(#10,'').Split([#13]);
end;

function TGump.GetGumpInfo(GumpIndex : Word) : TGumpInfo;
var Res : TArray<Byte>;
    GumpInfoStream : TMemoryStream;
    i : Integer;
    ArrLen : Word;
    Len : Cardinal;
begin
  Script_GetGumpInfo(GumpIndex,nil,Len);
  SetLength(Res,Len);
  Script_GetGumpInfo(GumpIndex,@res[0],Len);

  GumpInfoStream := TMemoryStream.Create;
  GumpInfoStream.Write(Res[0],Length(Res));
  GumpInfoStream.Position := 0;
//  Move(GumpInfoStream.Memory^,n,20);
  GumpInfoStream.Read(Result.Serial,20);  //first 20 bytes of common props
  GumpInfoStream.Read(ArrLen,2);
  SetLength(Result.Groups,ArrLen);
  if ArrLen > 0 then
    GumpInfoStream.Read(Result.Groups[0],SizeOF(TGroup) * ArrLen);

  GumpInfoStream.Read(ArrLen,2);
  SetLength(Result.EndGroups,ArrLen);
  if ArrLen > 0 then
    GumpInfoStream.Read(Result.EndGroups[0],SizeOF(TEndGroup) * ArrLen);

  GumpInfoStream.Read(ArrLen,2);
  SetLength(Result.GumpButtons,ArrLen);
  if ArrLen > 0 then
    GumpInfoStream.Read(Result.GumpButtons[0],SizeOF(TGumpButton) * ArrLen);

  GumpInfoStream.Read(ArrLen,2);
  SetLength(Result.ButtonTileArts,ArrLen);
  if ArrLen > 0 then
    GumpInfoStream.Read(Result.ButtonTileArts[0],SizeOF(TButtonTileArt) * ArrLen);

  GumpInfoStream.Read(ArrLen,2);
  SetLength(Result.CheckBoxes,ArrLen);
  if ArrLen > 0 then
    GumpInfoStream.Read(Result.CheckBoxes[0],SizeOF(TCheckBox) * ArrLen);

  GumpInfoStream.Read(ArrLen,2);
  SetLength(Result.CheckerTrans,ArrLen);
  if ArrLen > 0 then
    GumpInfoStream.Read(Result.CheckerTrans[0],SizeOF(TCheckerTrans) * ArrLen);

  GumpInfoStream.Read(ArrLen,2);
  SetLength(Result.CroppedText,ArrLen);
  if ArrLen > 0 then
    GumpInfoStream.Read(Result.CroppedText[0],SizeOF(TCroppedText) * ArrLen);

  GumpInfoStream.Read(ArrLen,2);
  SetLength(Result.GumpPics,ArrLen);
  if ArrLen > 0 then
    GumpInfoStream.Read(Result.GumpPics[0],SizeOF(TGumpPic) * ArrLen);

  GumpInfoStream.Read(ArrLen,2);
  SetLength(Result.GumpPicTiled,ArrLen);
  if ArrLen > 0 then
    GumpInfoStream.Read(Result.GumpPicTiled[0],SizeOF(TGumpPicTiled) * ArrLen);

  GumpInfoStream.Read(ArrLen,2);
  SetLength(Result.RadioButtons,ArrLen);
  if ArrLen > 0 then
    GumpInfoStream.Read(Result.RadioButtons[0],SizeOF(TRadio) * ArrLen);

  GumpInfoStream.Read(ArrLen,2);
  SetLength(Result.ResizePics,ArrLen);
  if ArrLen > 0 then
    GumpInfoStream.Read(Result.ResizePics[0],SizeOF(TResizePic) * ArrLen);

  GumpInfoStream.Read(ArrLen,2);
  SetLength(Result.GumpText,ArrLen);
  if ArrLen > 0 then
    GumpInfoStream.Read(Result.GumpText[0],SizeOF(TGumpText) * ArrLen);

  GumpInfoStream.Read(ArrLen,2);
  SetLength(Result.TextEntries,ArrLen);
  if ArrLen > 0 then
    GumpInfoStream.Read(Result.TextEntries[0],SizeOF(TTextEntry) * ArrLen);

  GumpInfoStream.Read(ArrLen,2);
  SetLength(Result.Text,ArrLen);
  if ArrLen > 0 then
  for I := 0 to ArrLen - 1 do
    Result.Text[i] := ReadStringParam(GumpInfoStream);

  GumpInfoStream.Read(ArrLen,2);
  SetLength(Result.TextEntriesLimited,ArrLen);
  if ArrLen > 0 then
    GumpInfoStream.Read(Result.TextEntriesLimited[0],SizeOF(TTextEntryLimited) * ArrLen);

  GumpInfoStream.Read(ArrLen,2);
  SetLength(Result.TilePics,ArrLen);
  if ArrLen > 0 then
    GumpInfoStream.Read(Result.TilePics[0],SizeOF(TTilePic) * ArrLen);

  GumpInfoStream.Read(ArrLen,2);
  SetLength(Result.TilePicHue,ArrLen);
  if ArrLen > 0 then
    GumpInfoStream.Read(Result.TilePicHue[0],SizeOF(TTilePicHue) * ArrLen);

  GumpInfoStream.Read(ArrLen,2);
  SetLength(Result.Tooltips,ArrLen);
  if ArrLen > 0 then
    GumpInfoStream.Read(Result.Tooltips[0],SizeOF(TTooltip) * ArrLen);

  GumpInfoStream.Read(ArrLen,2);
  SetLength(Result.HtmlGump,ArrLen);
  if ArrLen > 0 then
    GumpInfoStream.Read(Result.HtmlGump[0],SizeOF(THtmlGump) * ArrLen);

  GumpInfoStream.Read(ArrLen,2);
  SetLength(Result.XmfHtmlGump,ArrLen);
  if ArrLen > 0 then
    GumpInfoStream.Read(Result.XmfHtmlGump[0],SizeOF(TXmfHtmlGump) * ArrLen);

  GumpInfoStream.Read(ArrLen,2);
  SetLength(Result.XmfHTMLGumpColor,ArrLen);
  if ArrLen > 0 then
    GumpInfoStream.Read(Result.XmfHTMLGumpColor[0],SizeOF(TXmfHTMLGumpColor) * ArrLen);


  GumpInfoStream.Read(ArrLen,2);
  SetLength(Result.XmfHTMLTok,ArrLen);
  if ArrLen > 0 then
  for I := 0 to ArrLen - 1 do
  begin
    GumpInfoStream.Read(Result.XmfHTMLTok[i].x,32);
    Result.XmfHTMLTok[i].Arguments := ReadStringParam(GumpInfoStream);
    GumpInfoStream.Read(Result.XmfHTMLTok[i].Page,8);
  end;

  GumpInfoStream.Read(ArrLen,2);
  SetLength(Result.ItemProperties,ArrLen);
  if ArrLen > 0 then
    GumpInfoStream.Read(Result.ItemProperties[0],SizeOF(TItemProperty) * ArrLen);
  GumpInfoStream.Free;
end;

procedure TGump.AddGumpIgnoreByID(GumpID : Cardinal);
begin
  Script_AddGumpIgnoreByID(GumpID);
end;

procedure TGump.AddGumpIgnoreBySerial(GumpSerial : Cardinal);
begin
  Script_AddGumpIgnoreBySerial(GumpSerial);
end;

procedure TGump.ClearGumpsIgnore;
begin
  Script_ClearGumpsIgnore;
end;

{$EndRegion}

{$Region 'TTargetWork'}
function TTargetWork.GetTargetID : Cardinal;
begin
  Result := Script_GetTargetID;
end;

function TTargetWork.GetTargetStatus : Boolean;
begin
  Result := Script_GetTargetStatus;
end;

function TTargetWork.WaitForTarget(MaxWaitTimeMS : Integer) : Boolean;
begin
  Result := Script_WaitForTarget(MaxWaitTimeMS);
end;

procedure TTargetWork.CancelTarget;
begin
  Script_CancelTarget;
end;

procedure TTargetWork.TargetToObject(ObjectID : Cardinal);
begin
  Script_TargetToObject(ObjectID);
end;

procedure TTargetWork.TargetToXYZ(X, Y : Word; Z : ShortInt);
begin
  Script_TargetToXYZ(X, Y, Z);
end;

procedure TTargetWork.TargetToTile(TileModel,X,Y : Word; Z : ShortInt);
begin
  Script_TargetToTile(TileModel,X, Y, Z);
end;

procedure TTargetWork.WaitTargetObject(ObjID : Cardinal);
begin
  Script_WaitTargetObject(ObjID);
end;

procedure TTargetWork.WaitTargetTile(Tile,X, Y : Word;  Z : ShortInt);
begin
  Script_WaitTargetTile(Tile,X, Y, Z);
end;

procedure TTargetWork.WaitTargetXYZ(X, Y : Word; Z : ShortInt);
begin
  Script_WaitTargetXYZ(X, Y, Z);
end;

procedure TTargetWork.WaitTargetSelf;
begin
  Script_WaitTargetSelf;
end;

procedure TTargetWork.WaitTargetType(ObjType : Word);
begin
  Script_WaitTargetType(ObjType);
end;

procedure TTargetWork.CancelWaitTarget;
begin
  Script_CancelWaitTarget;
end;

procedure TTargetWork.WaitTargetGround(ObjType : Word);
begin
  Script_WaitTargetGround(ObjType);
end;

procedure TTargetWork.WaitTargetLast;
begin
  Script_WaitTargetLast;
end;


{$EndRegion}

var GUIScriptMethod : TScriptExecMethod;

type TScrThread = class(TThread)
  procedure Execute; override;
end;

procedure TScrThread.Execute;
begin
  NameThreadForDebugging('In-Script Thread');
  InitNewThread;
  try
    GUIScriptMethod;
  finally
    CorrectDisconnection;
  end;
end;

procedure StartScriptInThread(Method : TScriptExecMethod);
begin
  GUIScriptMethod := Method;
  TScrThread.Create;
end;

initialization
if (ParamCount = 0) or (ParamStr(1) <> 'Stealth') then
  StartStealthSocketInstance(PAnsiChar(AnsiString(ParamStr(0))));

finalization
sleep(300);
CorrectDisconnection; //disconnection of main script thread socket
end.

