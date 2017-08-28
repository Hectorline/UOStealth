Unit NewWaypointBuilder;

interface

type
    TWaypointBuilder = class
        MapWidth, MapHeight : Integer;
        Waypoints : Array of TPoint;
        function AddWaypointToList(x, y : Integer) : Integer;
        function WaypointValidate(x, y, z : Integer) : Boolean;
        function WaypointBuild() : Integer; 
        constructor Create(MapWidth, MapHeight : Integer);
    end;

implementation

Procedure DrawMap(xstart, ystart, X, Y: Integer);
Var
Figure: TMapFigure;
Begin
  Figure.kind := fkLine;
  Figure.coord := fcWorld;
  Figure.x1 := X;
  Figure.y1 := Y;
  Figure.x2 := xstart;
  Figure.y2 := ystart;
  Figure.brushStyle := bsClear;
  Figure.brushColor := $FFFF00;
  Figure.color := $FF00FF;        
  Figure.text := '';  
  if((X > 0) and (Y > 0)) then
   AddFigure(Figure);
End; 


function TWaypointBuilder.WaypointValidate(x, y, z: Integer): Boolean;
label ex_label;
begin
    if((x > MapWidth) OR (y > MapHeight))then
      begin
        Result := False;
        goto ex_label;
      end;

    if((x = 0) AND (y = 0))then
      begin
        Result := False;
        goto ex_label;
      end;
    Result := True;
ex_label:
  Result := Result;
end;

function TWaypointBuilder.WaypointBuild : Integer;
const 
  Step = 5;
var 
  x, y : Integer;
  z : ShortInt;
  validationResult : Boolean;
begin
  for x := 0 to MapWidth do
    for y := 0 to MapHeight do
      if(((x mod Step) = 0) and ((y mod Step)=0))then
      begin
        z := GetSurfaceZ(x, y, WorldNum);
        validationResult := WaypointValidate(x, y, z);
        if(validationResult)then
          begin
            AddWaypointToList(x, y);
            DrawMap(x-1, y-1, x, y);
          end;
      end;
  Result := Length(Waypoints);
end;

constructor TWaypointBuilder.Create(MapWidth, MapHeight: Integer);
begin
  ClearFigures;
  Self.MapWidth := MapWidth;
  Self.MapHeight := MapHeight;
end;

function TWaypointBuilder.AddWaypointToList(x, y: Integer): Integer;
begin
  SetLength(Waypoints, Length(Waypoints));
  Waypoints[High(Waypoints)].X := x;
  Waypoints[High(Waypoints)].Y := y;
  Result := Length(Waypoints);
end;

var
 b : TWaypointBuilder;

begin
  b := TWaypointBuilder.Create(2560, 2048);
  b.WaypointBuild();
  b.Free;
end.