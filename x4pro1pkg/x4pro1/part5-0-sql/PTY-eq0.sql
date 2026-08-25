SELECT distinct x4pro_c5dat.DatasetID,REACODE.FullCode
FROM x4pro_c5dat 
inner join REACODE on REACODE.ReacodeID=x4pro_c5dat.DatasetID
where fullCode like '%,PTY' and y=0
