Unit ScriptHelpers;

interface

type
 {$Region 'TileHelper'}
 
 //TTypeSpot can contain Tile or Id of animal;    
 TFarmingSpot = record
  X, Y : Integer;
  SpotType : Cardinal;  
 end;  
                                     
 TFarmingSpots = Array of TFarmingSpot;
 
 //TFarmingArea = TDictionary<String, TFarmingSpots>;
 TFarmingArea = record
  Title : String;
  FarmingSpots : TFarmingSpots;
 end;
                  
 TFarmingAreas = Array of TFarmingArea;
        
 function FarmingSpotsScanner(var Types : Array of Word) : TFarmingAreas; 
 {$EndRegion}
 
implementation

(*
    Function to gain all the farming spots we can in some range;
    ScannerType : 
    0 = animals,
    1 = tiles;
*)
function FarmingSpotsScanner(const ScannerType : Byte;var Types : Array of Word; Range : Byte) : TFarmingSpots;
var
 TileInfo : TStaticCell;
begin 
 case ScannerType of
  0 : begin
  end;
  1 : begin
   for item in Types do 
    for dx := (-1*Range) to Range do
     for dy := (-1*Range) to Range do begin
       TileInfo := ReadStaticsXY(GetX(StealthSelf)+dx, GetY(StealthSelf)+dy, 0);
             
     end;
  end;
 end;
end;



end.