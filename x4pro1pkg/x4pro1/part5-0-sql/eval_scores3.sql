select 'Evaluator-Flags' as `X4Pro-Tables`,datetime() as now;

select * from x4evalscore_file order by fileID;

select row_number() over (order by fileID,DatasetID) as n,
  fileID,itype,author
 ,DatasetID,x4upd,accepted,evalflag,comment2
from x4evalscore
where itype='stat'
order by fileID,itype,DatasetID
;
