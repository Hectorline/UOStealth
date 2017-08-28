Unit Util;

Interface

Type TIntegerList = class
private
  flist : Array of Integer;
  fsize : Integer;
public
  procedure add(a : Integer);
end;     

Implementation
{$Region TIntegerList}
procedure TIntegerList.add(a : Integer);
begin
  SetLength(flist,(Length(flist) + 1));
  fsize := Length(flist);  
  flist[(fsize - 1)] := a;
end;
{$Endregion}
end.