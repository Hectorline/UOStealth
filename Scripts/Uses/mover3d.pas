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
    // шаг сделан успешно или шагнуть в этом направлении нельзя - выходим
    // иначе (очередь шагов заполнена) ждем и пробуем шагнуть опять
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
    // рассчитываем путь
    if recompute then
    begin
      addToSystemJournal('Расчет пути');
      recompute := False;
      cnt := GetPathArray3D(PredictedX, PredictedY, PredictedZ, x, y, z, WorldNum, acc, accz, run, path);
      if cnt <= 0 then 
      begin
        addToSystemJournal('Невозможно найти путь');
        exit;
      end;
      idx := 0; 
    end;
    
    cx := PredictedX;
    cy := PredictedY;
    cz := PredictedZ;

    // проверка проходимости на 4 шага вперед 
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
        // точка по курсу не проходима, надо считать путь но новой
        addToSystemJournal('Непроходимая точка ' + intToStr(destX) + ' ' + intToStr(destY));
        recompute := True;
        break;
      end;
    end;
    
    if recompute then continue;
    
    // ждем пока будет достаточно стамины
    while (not Dead) and (Stam < moveCheckStamina) do
      Wait(100);
      
    // Расстояние до точки
    dx := Integer(PredictedX) - Integer(path[idx].x);
    dy := Integer(PredictedY) - Integer(path[idx].y);

    // уже стоим на точке куда надо шагнуть, или точка дальше чем в одном тайле
    // значит какая то фигня - надо посчитать путь но новой 
    if ((dx = 0) and (dy = 0)) or ((abs(dx) > 1) or (abs(dy) > 1)) then
    begin
      addToSystemJournal('близко или далеко от следующий точки: ' + intToStr(dx) + ' ' + intToStr(dy));

      recompute := True;
      continue;
    end;
    
    // направление шага
    dir := CalcDir(PredictedX, PredictedY, path[idx].x, path[idx].y);
    
    if dir = 100 then
    begin
      addToSystemJournal('dir=100');
      recompute := True;
      continue;
    end;
    
    // поворот если надо
    if PredictedDirection <> dir then
      if not _Step(dir, run) then
      begin
        recompute := True;
        continue;
      end;
      
    // и шаг
    if not _Step(dir, run) then
    begin
      recompute := True;
      continue;
    end;
    
    // если есть Callback вызываем его, если он вернул False то закругляемся
    //if assigned(callback) and not callback(path[idx].x, path[idx].y) then exit;
    
    Inc(idx);
    // дошли до конца пути
    if idx >= cnt then
    begin
      dx := Integer(PredictedX) - Integer(path[idx-1].x);
      dy := Integer(PredictedY) - Integer(path[idx-1].y);
     
      // если подошли на правильное расстояние, то все - конец
      if (abs(dx) <= acc) and (abs(dy) <= acc) then 
      begin
        addToSystemJournal('на месте');
        result := True;
        break;
      end;
      
      // если же не пришли - считаем путь по новой
      addToSystemJournal('Конец маршрута, но мы далеко ' + intToStr(dx) + ' ' + intToStr(dy));

      recompute := True;
    end;
  end;
end;

 
end.