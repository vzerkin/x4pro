-- select 'Statistical verification' as `Title`,'Evaluator-Flags' as `X4Pro-Tables`,datetime() as now;
select 'Statistical verification' as `Title`,'Evaluator-Flags' as `X4Pro-Tables`,datetime() as now
,max(UpdateDate) as `X4Pro-database` from X4UPDATE;

select tblfile.fileID
 ,substr(tblfile.srcFileDate,1,10) as srcFileDate
 ,tblflag.author as `author`
 ,tblflag.itype
 ,count(tblflag.DatasetID) as nDatasets
 ,sum(case when tblflag.accepted=0 then 1 else 0 end) as nRejected
 ,sum(tblflag.accepted) as nAccepted
 ,tblfile.srcFileName
from x4evalscore as tblflag
 left join x4evalscore_file as tblfile on tblfile.fileID=tblflag.fileID
where itype='stat'
group by tblflag.itype,tblflag.author,tblfile.fileID
order by tblfile.srcFileDate
;

select row_number() over (order by fileID,accepted,DatasetID) as n,
  DatasetID,x4upd
 ,(case when accepted=0 then 'REJECTED' else 'accepted' end) as accepted
 ,author as evaluator
 ,fileID,itype
 ,comment2
from x4evalscore
where itype='stat'
order by fileID,x4evalscore.accepted,DatasetID
;
