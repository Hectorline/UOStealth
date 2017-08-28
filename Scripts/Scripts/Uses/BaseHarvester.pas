Unit BaseHarvester;

interface

type

	TBaseHarvestSpot = record
		Tile, X, Y, Z : Integer;
		LastCollected : TDateTime;  
	end;
	
	TBaseHarvestSpots = Array of TBaseHarvestSpot;
	
	TBaseHarvestArea = record
		Title : String;
		Initialized : Boolean;
		BaseHarvestSpots : TBaseHarvestSpots;
	end;
	
	TBaseHarvestAreas = Array of TBaseHarvestArea;
	
	TToolTypes = Array of Word;
	
	TTilesArray = Array of Word;
	
	TBaseHarvester = class
	private
		FTiles : TTilesArray;
		FGatheringTools : TToolTypes;				
	public		
		BaseHarvestAreas : TBaseHarvestAreas;		
		function InitializeSpots(Idx : Integer) : Integer;		
		constructor Create(ScriptType : Byte; Areas : Array of TPoint; GatheringTools : TToolTypes); override;			
	end;

implementation

constructor TBaseHarvester.Create(ScriptType : Byte; Areas : Array of TPoint; GatheringTools : TToolTypes);
var 
	i : Integer;
begin
	for i := Low(Areas) to High(Areas) do begin
		SetLength(BaseHarvestAreas, Length(BaseHarvestAreas) + 1);
		BaseHarvestAreas[High(BaseHarvestAreas)].Title := 'X=' + IntToStr(Areas[i].X) + ', Y=' + IntToStr(Areas[i].Y);
		BaseHarvestAreas[High(BaseHarvestAreas)].Initialized := False;
	end;	
	
	for i := Low(GatheringTools) to High(GatheringTools) do begin
		SetLength(FGatheringTools, Length(FGatheringTools) + 1);
		FGatheringTools[High(FGatheringTools)] := GatheringTools[i];
	end;		
	
	case ScriptType of
	//mining
		0 : FTiles := [1339, 1340, 1341, 1342, 1343, 1344, 1345, 1346, 1347, 1348, 1349, 13450, 1351, 1352, 1353, 1354, 1355, 1356, 1357, 1358, 1359];
	//lumber
		1 : FTiles := [3274, 3275, 3277, 3280, 3283, 3286, 3288, 3290, 3293, 3296, 3299, 3302, 3320, 3323, 3326, 3329, 3393, 3394, 3395, 3396, 3415, 
		3416, 3417, 3418, 3419, 3438, 3439, 3440, 3441, 3442, 3460, 3461, 3462, 3476, 3478, 3480, 3482, 3484, 3492, 3496]; 
	end;
end;

function TBaseHarvester.InitializeSpots(Idx : Integer) : Integer;
var
	TileInfo : TStaticCell;
	dx, dy, i, dTile : Integer;
begin
	for dx := -20 to 20 do
		for dy := -20 to 20 do begin
			TileInfo := ReadStaticsXY(GetX(SelfID)+dx, GetY(SelfID)+dy, GetZ(SelfID));     
			if TileInfo.StaticCount > 0 then
				for i := Low(TileInfo.Statics) to High(TileInfo.Statics) do
					for dTile := Low(FTiles) to High(FTiles) do
						if (TileInfo.Statics[i].Tile = FTiles[dTile]) and (TileInfo.Statics[i].z = GetZ(SelfID)) then begin
							SetLength(BaseHarvestAreas[Idx].BaseHarvestSpots, Length(BaseHarvestAreas[Idx].BaseHarvestSpots) + 1);
							BaseHarvestAreas[Idx].BaseHarvestSpots[High(BaseHarvestAreas[Idx].BaseHarvestSpots)].Tile := TileInfo.Statics[i].Tile;
							BaseHarvestAreas[Idx].BaseHarvestSpots[High(BaseHarvestAreas[Idx].BaseHarvestSpots)].X := TileInfo.Statics[i].X;
							BaseHarvestAreas[Idx].BaseHarvestSpots[High(BaseHarvestAreas[Idx].BaseHarvestSpots)].Y := TileInfo.Statics[i].Y;							
						end;
		end;
	BaseHarvestAreas[Idx].Initialized := True;
	Result := Length(BaseHarvestAreas[Idx].BaseHarvestSpots);
end;	

end.