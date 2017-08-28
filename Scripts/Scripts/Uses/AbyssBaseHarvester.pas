Unit AbyssBaseHarvester;

interface

implementation

uses
  BaseHarvester;

var
 FBaseHarvester : TBaseHarvester;
 Point : TPoint;

initialization
	Point.X := GetX(SelfId);
	Point.Y := GetY(SelfId);
	FBaseHarvester := TBaseHarvester.Create(0, [Point], [$0000]);	
end.