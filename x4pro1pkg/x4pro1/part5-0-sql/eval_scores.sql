select 'Evaluator-Flags in X4Pro',datetime();

select * from x4evalscore_file order by fileID;

select row_number() over (order by fileID,itype,DatasetID) as n,
fileID,itype,author
,DatasetID,x4upd,accepted,evalflag,comment2
from x4evalscore
where itype='expert_x4'
order by fileID,itype,DatasetID
;

