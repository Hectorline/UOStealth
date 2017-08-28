// v 1.0
// First maker is Grin (inject)
// adaptation AdmiR

unit AbyssAntiMacro; 
interface 

function return_value(gi :TGumpInfo) : integer;
procedure AntimacroAbyss(Serial,GumpID,X,Y : Cardinal);


implementation

const
  AntiMacroGumpSerial = $1832044;   

function return_value(gi :TGumpInfo) : integer;

var 
  a : array of array of integer;
  i ,j , k , VariantReply , F: integer;  
  dx,dy : array [0..1] of integer; 
  cos : longint;
begin
  SetLength(a, 10); 
  a[2]:=[8,9,10,8,5,6,8,1,2];
  a[3]:=[4,7,6,6,7,8,5,7,11];
  a[5]:=[4,5,6,6,7,8,5,7,11];
  a[6]:=[7,9,10,5,6,8,8,11,10];
  a[8]:=[3,5,6,6,7,9,4,9,8];
  a[9]:=[4,6,7,5,8,7,2,1,4];    
  F := 10000;
                            
  for i := 0 to 2 do
  begin  
    VariantReply := StrToInt(gi.Text[i+1]);  
    cos := 0; 
    for k := 0 to 2 do
    begin
      for j := 0 to 1 do 
      begin 
        dx[j] := gi.GumpPics[a[VariantReply][j+k*3]].x-gi.GumpPics[a[VariantReply][j+1+k*3]].x; 
        dy[j] := gi.GumpPics[a[VariantReply][j+k*3]].y-gi.GumpPics[a[VariantReply][j+1+k*3]].y;
      end; 
      cos := cos + Abs(round(1000*(dx[0]*dx[1]+dy[0]*dy[1])/sqrt((dx[0]*dx[0]+dy[0]*dy[0])*(dx[1]*dx[1]+dy[1]*dy[1]))));    
    end;  
    if cos < F then 
    begin
      F := cos;
      result := i+1;
    end;
  end;
end;    

procedure AntimacroAbyss(Serial,GumpID,X,Y : Cardinal);
  var
    gi :TGumpInfo;
  begin 
    if Serial = AntiMacroGumpSerial then
      begin
        GetGumpInfo(GetGumpsCount-1,gi);    
        NumGumpButton(GetGumpsCount-1,return_value(gi));        
      end;  
  end;     

Begin
  SetEventProc(evIncomingGump,'AntimacroAbyss');  
end.