select * from x4evalscore_file order by fileID;

select x4evalscore.fileID,x4evalscore.DatasetID
 ,x4evalscore.author
 ,x4evalscore_file.myComment
 ,x4evalscore.itype
 ,x4evalscore.accepted
 ,x4evalscore.evalflag
 ,x4evalscore.comment2
from x4evalscore
 left  join x4evalscore_file on x4evalscore_file.fileID=x4evalscore.fileID
-- where x4evalscore.fileID<>4
order by
 x4evalscore.itype,
 x4evalscore.fileID desc
,x4evalscore.DatasetID
-- limit 20

