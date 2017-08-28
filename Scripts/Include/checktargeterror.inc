procedure CheckTargetError(lines, checktime : integer);
var D : TDateTime;
begin
{5 minutes in DateTime = (1.0 * checktime) / 1440 = 0.00347}
D := Now - ((1.0 * checktime) / 1440.0);
InJournalBetweenTimes('I am already performing another action|doing something',D,Now);

if LineCount > lines then
  begin
  AddToSystemJournal('Error with target. Disconnected');
ClearJournal;
  Disconnect;
  end;

end;
