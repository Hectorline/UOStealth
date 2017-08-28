program CrazyLumber;

const
GumpIgnore=0;
IngotsStorage = $4047B327; // Pecho en una casa en la que se plieguen picado.

HomeRuneBook = $446BE66A; // Runabuki ID srunkoy la casa.
HomeRuneIndex = 0; // Posicion runas a runabuke casa. 0 - la primera runa.
RuneBookShift = 5; // 7 - Chiva, 5 magia.
//HomeX = 1979; // Coordenada X delante del pecho en la casa.
//HomeY= 1213; // Coordenadas en frente del pecho en la casa.

Arm= 62; // Número armadura fizikal sin Protecta.
Protection= $1F3B; // Tipo pergaminos Protecta.

Axe = $41E0A2DE; // Hacha ID que Ruban.
Logtype = $1BDD; // Tipo troncos.
WaitTime=500;
RecalTime=3000;
LagWait=1000;
WaitCycles=7;

var
CurrentRune,CurrentBook:Integer;
Resourses,Killers:array of Word;
RuneBooks:array of Cardinal;
cTime,cTime2:TDateTime;

procedure Heal;
var
StartTime:TDateTime;
begin
  StartTime:=Now;
  if Poisoned then begin
    Cast('Cure');
    WaitForTarget(2000);
    TargetToObject(self);
  end;
  if (HP<>MaxHP) and (not Poisoned) then begin
    cast('Greater Heal');
    WaitForTarget(2000);
    TargetToObject(self);
  end;
  if (InJournalBetweenTimes('Your concentration is disturbed, thus ruining thy spell', StartTime, Now) > 0) or Poisoned or (HP<>MaxHP) then Heal;
  CancelWaitTarget;
  ClearJournal;
  Wait(500);
end;

procedure Move(Item:Array of Word);
var
j:Byte;
begin
  while FindType(LogType,Backpack)>0 do begin
    if Dead or not Connected then Exit;
    while ObjAtLayer(LhandLayer) = 0 do begin
      Equip(LhandLayer,Axe);
      wait(1000);
    end;
    UseObject(Axe);
    CheckLag(LagWait);
    WaitForTarget(LagWait);
    TargetToObject(FindItem);
  end;
  CheckLag(LagWait);
  for j:=0 to Length(Item)-1 do begin
    if Dead or not Connected then Exit;
    CheckLag(LagWait);
    While (FindType(Item[j], Backpack)>1) do begin
      if Dead or not Connected then Exit;
      MoveItem(Finditem,GetQuantity(Finditem),IngotsStorage,0,0,0);
      CheckLag(LagWait);
      Wait(WaitTime);
    end;
  end;
end;

function RecallRune(RuneBook: Cardinal; Rune: Byte):Boolean;
var
Counter: Byte;
X, Y: Word;
begin
  Result := False;
  X := GetX(Self);
  Y := GetY(Self);
  CheckLag(LagWait);
  Wait(WaitTime);
  if Dead or not Connected then Exit;
  cTime2:=Now;         
//   AddToSystemJournal('Runebook # '+IntToStr(CurrentBook+1));
//  AddToSystemJournal('Rune # '+IntToStr(CurrentRune+1));
  while (cTime2 < cTime)do begin
    cTime2:=Now;
    wait(100);
  end;
  UseObject(RuneBook);
  CheckLag(LagWait);
  cTime:=Now+0.00008;
  Counter := WaitCycles;
  while Counter > 0 do begin
    if IsGump then Break;
    Wait(WaitTime);
    CheckLag(LagWait);
    Inc(Counter);
  end;
  if IsGump then begin
    if NumGumpButton(GetGumpsCount-1, RuneBookShift + 6*Rune) then begin
      CheckLag(LagWait);
      Wait(RecalTime);
      CheckLag(LagWait);
      Result := (X <> GetX(Self)) or (Y <> GetY(Self));
    end else Result := False;
  end else Result := False;
end;
function GoBase: Boolean;
begin
  //if (GetX(self)=HomeX) and (GetY(self)=HomeY) then Exit;
  Result:=RecallRune(HomeRuneBook, HomeRuneIndex);
end;

function NextRune: Boolean;
var
Counter: Cardinal;
begin
  Inc(CurrentRune);
  if CurrentRune > 15 then begin
    CurrentRune := 0
    Inc(CurrentBook);
    if CurrentBook >= Length(RuneBooks) then CurrentBook := 0;
  end;
  for Counter := 0 to WaitCycles do begin   //bucle de recall is blocked etc
    if Dead or not Connected then Exit;
    Result := RecallRune(RuneBooks[CurrentBook], CurrentRune);
    if Result then Break;
    Inc(CurrentRune);
    Result := RecallRune(RuneBooks[CurrentBook], CurrentRune);
    if Result then Break;
    GoBase;
    Wait(10000);
  end;
end;

procedure CheckState(X,Y:Integer);
begin
  if Dead or not Connected then Exit;
  if 477 < Weight + 70 then begin
    while True do begin
      if Dead or not Connected then Exit;
      if GoBase then Break;
      if not RecallRune(RuneBooks[CurrentBook], CurrentRune) then Wait(10000);
    end;
    Move(Resourses);
    while True do begin
      if Dead or not Connected then Exit;
      if RecallRune(RuneBooks[CurrentBook], CurrentRune) then Break;
    end;
  end;
  NewMoveXY(X,Y,True,1,True);  //moveee
end;

function CheckPK: boolean;
var
i,q:integer;
begin
  FindDistance:=25;
  for q:=0 to high(Killers) do
  for i:=3 to 6 do
  if FindNotoriety(Killers[q],i)>0 then begin
    Result:=True;
    AddToSystemJournal('Llegó el tío malo - ' + GetName(FindItem));
    AddToSystemJournal('Runebook # '+IntToStr(CurrentBook+1));
    AddToSystemJournal('Rune # '+IntToStr(CurrentRune+1));
    FindDistance:=2;
    Exit;
  end;
  FindDistance:=2;
  if (Poisoned) or (HP<>MaxHP) then Result:=True;
end;

procedure Mine(Tile,X,Y,Z:Integer);
var
StartTime:TDateTime;
begin
  while True do begin
    while ObjAtLayer(LhandLayer) = 0 do begin
      Equip(LhandLayer,Axe);
      wait(1000);
    end;
    if Dead or not Connected then Exit;
    if TargetPresent then CancelTarget;
    CheckState(x,y);
    CheckLag(LagWait);
    Wait(WaitTime);
    UseObject(Axe);
    CheckLag(LagWait);
    WaitForTarget(LagWait);
    if TargetPresent then begin
      StartTime := Now;
      TargetToTile(Tile, X, Y, Z);
      CheckLag(LagWait);
      if InJournalBetweenTimes('t use an axe |is too far away|cannot be seen|s not enough wood here to harvest', StartTime, Now) > 0 then Exit;
      Wait(200);
      CheckState(x,y);
      if CheckPK then begin
        cTime:=Now-0.00008;
        GoBase;
        Inc(CurrentRune);
        Heal;
        Wait(WaitTime*1200);
        RecallRune(RuneBooks[CurrentBook], CurrentRune);
        CheckLag(LagWait);
        Wait(WaitTime);
      end;
    end;
  end;
end;

function CheckTiles:Array of array of Integer;
var
X0,Y0,i,q:Integer;
StaticData:TStaticCell;
h:Byte;
TSTData:TStaticTileData;
Tiles:Array of array of Integer;
treeTiles:array of integer;
begin
      Y0 :=(GetY(Self)-1);  //Ricard
      X0 :=(GetX(Self));                                 
treeTiles := [3240,3242,3277,3283,3286,3288,3289,3290,3291,3294,3296,3299,3302,3393,3394,3395,3396,3415,3416,3417,3418,3419,3438,3439,3440,3441,3442,3460,3461,3462,3480,3482,3488];      

 for Y0:=(GetY(Self)-6) to (GetY(Self)+6) do begin    //asi se recorre un arraybidimesional
    for X0:=(GetX(Self)-6) to (GetX(Self)+6) do begin                          
    
      StaticData:=ReadStaticsXY(X0,Y0,WorldNum); //coje los datos del tile
      if GetLayerCount(X0,Y0,WorldNum)<1 then begin  //creo k esto es k no hay tiles o algo asi
          Continue;  //continue salta esta vuelta de bucle, desde aqui va al end.         
      end;                                                  
      
      TSTData:=GetStaticTileData(StaticData.Statics[0].Tile);
      h:=TSTData.Height;                                     
        
      for i:=0 to Length(treeTiles)-1 do begin    //recorro el array de los tipos de arbol
        if StaticData.Statics[0].Tile=treeTiles[i] then begin
           SetLength(Tiles, q+1);
           SetLength(Tiles[q], 4);
           Tiles[q][0]:=StaticData.Statics[0].Tile;
           Tiles[q][1]:=StaticData.Statics[0].X;
           Tiles[q][2]:=StaticData.Statics[0].Y;
           Tiles[q][3]:=StaticData.Statics[0].Z;
           Inc(q);  
        end;
      end;
 
    end; 
  end;   
  Result:=Tiles;
end;


procedure MinePoint;
var
i:Integer;
Tiles:Array of array of Integer;
begin
  if Dead or not Connected then Exit;
  Tiles:=CheckTiles;
  for i:=0 to Length(Tiles)-1 do begin
    NewMoveXY(Tiles[i][1],Tiles[i][2],True,1,True);     //moveee
    Mine(Tiles[i][0],Tiles[i][1],Tiles[i][2],Tiles[i][3]);
  end;
  Inc(CurrentRune);
end;

procedure CheckProtect;
begin
  if Dead or not Connected then Exit;
  if Arm-15=Armor then Exit;
  GoBase;
  UseObject(IngotsStorage);
  CheckLag(LagWait);
  Wait(RecalTime);
  if CountEx(Protection,$FFFF,backpack)<=0 then begin
    if FindType(Protection,IngotsStorage)<=0 then begin
      AddToSystemJournal('Rollos terminados Protecta');
      Halt;
    end;
    repeat
      Grab(FindItem,1);
      CheckLag(LagWait);
      Wait(RecalTime);
    until CountEx(Protection,$FFFF,backpack)>0;
  end;
  repeat
    UseObject(FindItem);
    CheckLag(LagWait);
    Wait(RecalTime);
  until(Arm-15=Armor);
  CheckProtect;
end;

begin

  if not Connected then begin
    Connect;
    Wait(10000);
  end;     
 
  //While IsGump do CloseSimpleGump(GetGumpsCount-1); 
   
  cTime:=Now;
  RuneBooks:=[$446E1286,$446EC7BF]; 
  Resourses:=[$1BD7,$318F,$3191,$2F5F,$3199,$3190];
  Killers:=[$0190,$0191,$025E,$025D,$0028,$009F];
  //CheckProtect;  
  
  while True do begin
    if Dead then begin
      AddToSystemJournal('You Dead.');
      AddToSystemJournal('Runebook # '+IntToStr(CurrentBook+1));            
      AddToSystemJournal('Rune # '+IntToStr(CurrentRune+1));
      Halt;
    end;
    if not Connected then begin
      Connect;
      Wait(10000);
      //While IsGump do CloseSimpleGump(GetGumpsCount-1);
      //CheckProtect;
      //Continue;
    end;    

    NextRune;
    MinePoint;
  end;
end.

