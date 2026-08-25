select 'Summary' as `Title`,'Evaluator-Flags' as `X4Pro-Tables`,datetime() as now
,substr(max(UpdateDate),1,10) as `X4Pro-database` from X4UPDATE where UpdateFlag='O';

select * from x4evalscore_file order by fileID;

select tblfile.fileID
 ,substr(tblfile.srcFileDate,1,10) as srcFileDate
 ,tblflag.author as `evaluator/compiler`
 ,tblflag.itype
 ,count(tblflag.DatasetID) as nDatasets
 ,sum(case when tblflag.accepted=0 then 1 else 0 end) as nRejected
 ,sum(tblflag.accepted) as nAccepted
 ,tblfile.srcFileName
from x4evalscore as tblflag
 left join x4evalscore_file as tblfile on tblfile.fileID=tblflag.fileID
group by tblflag.itype,tblflag.author,tblfile.fileID
order by tblfile.fileID
;
