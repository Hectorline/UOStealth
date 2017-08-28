unit mover3d;

interface



type TMoveCallback = function(x, y : Integer) : Boolean;

function Mover(x, y, z, acc, accz : Integer; run : Boolean; callback : TMoveCallback): boolean;

implementation

function _Step(dir : Byte; run : Boolean) : boolean;
var res : Integer;
begin
  while true do
  begin
    res := StepQ(dir, run);
    result := res >= 0;
    // ��� ������ ������� ��� ������� � ���� ����������� ������ - �������
    // ����� (������� ����� ���������) ���� � ������� ������� �����
    if (res >= 0) or (res = -2) then break;
    wait(10);
  end;
end;


function Mover(x, y, z, acc, accz : Integer; run : Boolean; callback : TMoveCallback): boolean;
var path : TPathArray;
    cnt, idx, i, cx, cy, cz, steps, dx, dy : Integer;
    destX, destY : Word;
    destZ : ShortInt;
    recompute : Boolean;
    dir : Byte;
begin
  result := False;
  recompute := True;

  while true do
  begin
    // ������������ ����
    if recompute then
    begin
      addToSystemJournal('������ ����');
      recompute := False;
      cnt := GetPathArray3D(PredictedX, PredictedY, PredictedZ, x, y, z, WorldNum, acc, accz, run, path);
      if cnt <= 0 then 
      begin
        addToSystemJournal('���������� ����� ����');
        exit;
      end;
      idx := 0; 
    end;
    
    cx := PredictedX;
    cy := PredictedY;
    cz := PredictedZ;

    // �������� ������������ �� 4 ���� ������ 
    steps := idx + 4;
    if steps >= cnt then steps := cnt-1;
    
    for i := idx to steps do
    begin
      destX := path[i].X;
      destY := path[i].Y;
      if IsWorldCellPassable(cx, cy, cz, destX, destY, destZ, WorldNum) then
      begin
        cx := destX;
        cy := destY;
        cz := destZ;
      end
      else
      begin
        // ����� �� ����� �� ���������, ���� ������� ���� �� �����
        addToSystemJournal('������������ ����� ' + intToStr(destX) + ' ' + intToStr(destY));
        recompute := True;
        break;
      end;
    end;
    
    if recompute then continue;
    
    // ���� ���� ����� ���������� �������
    while (not Dead) and (Stam < moveCheckStamina) do
      Wait(100);
      
    // ���������� �� �����
    dx := Integer(PredictedX) - Integer(path[idx].x);
    dy := Integer(PredictedY) - Integer(path[idx].y);

    // ��� ����� �� ����� ���� ���� �������, ��� ����� ������ ��� � ����� �����
    // ������ ����� �� ����� - ���� ��������� ���� �� ����� 
    if ((dx = 0) and (dy = 0)) or ((abs(dx) > 1) or (abs(dy) > 1)) then
    begin
      addToSystemJournal('������ ��� ������ �� ��������� �����: ' + intToStr(dx) + ' ' + intToStr(dy));

      recompute := True;
      continue;
    end;
    
    // ����������� ����
    dir := CalcDir(PredictedX, PredictedY, path[idx].x, path[idx].y);
    
    if dir = 100 then
    begin
      addToSystemJournal('dir=100');
      recompute := True;
      continue;
    end;
    
    // ������� ���� ����
    if PredictedDirection <> dir then
      if not _Step(dir, run) then
      begin
        recompute := True;
        continue;
      end;
      
    // � ���
    if not _Step(dir, run) then
    begin
      recompute := True;
      continue;
    end;
    
    // ���� ���� Callback �������� ���, ���� �� ������ False �� ������������
    //if assigned(callback) and not callback(path[idx].x, path[idx].y) then exit;
    
    Inc(idx);
    // ����� �� ����� ����
    if idx >= cnt then
    begin
      dx := Integer(PredictedX) - Integer(path[idx-1].x);
      dy := Integer(PredictedY) - Integer(path[idx-1].y);
     
      // ���� ������� �� ���������� ����������, �� ��� - �����
      if (abs(dx) <= acc) and (abs(dy) <= acc) then 
      begin
        addToSystemJournal('�� �����');
        result := True;
        break;
      end;
      
      // ���� �� �� ������ - ������� ���� �� �����
      addToSystemJournal('����� ��������, �� �� ������ ' + intToStr(dx) + ' ' + intToStr(dy));

      recompute := True;
    end;
  end;
end;

 
end.