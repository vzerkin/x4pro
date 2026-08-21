-- General database statistics (simple)
-- select datetime() as Now, max(UpdateDate) as `X4Pro-database`, count(distinct ENTRY.EntryID) as "Total Entry"
-- from X4UPDATE,ENTRY;

-- General database statistics
select datetime() as Now, max(UpdateDate) as `X4Pro-database`
 , count(distinct ENTRY.EntryID) as "Total Entry"
 , count(distinct REACODE.FullCode) as "Reaction-codes"
 , count(distinct REACODE.ReacodeID) as "Datasets"
 , sum(REACODE.nDataLines) as "Data Points"
from REACODE
inner join ENTRY on ENTRY.Entry=substring(REACODE.ReacodeID,1,5)
inner join X4UPDATE on ENTRY.UpdateNo=X4UPDATE.UpdateNo
;

-- List of Reaction-codes without reaction combinations
select
 ROW_NUMBER() over (order by REACSTR.zIncident,proj,zTarg1,aTarg1,Targ1,reacode) as "row",
 -- Proj,DICT033.expansion as projectile
 -- ,Targ1 as target
 reacode
 ,count(distinct x4pro_ds.DatasetID) as dsets
 ,sum(x4pro_ds.ndat) as points
 ,Targ1 as target
 -- ,Proc1 as process
 ,REACSTR.Reaction
 ,CASE
   when DICT030.ShortHelp is not null then DICT030.ShortHelp
   when optbl.Expansion is not null then optbl.Expansion
   else ''
  END as "process/particle"
 ,quant1 as webQuantity
 -- ,QUANTITY.ShortHelp as webQuantityHelp
 -- ,reatyp,DICT013.ShortHelp as reatypHelp
 ,REACSTR.SF58,DICT036.ShortHelp as QuantityHelp
from x4pro_ds
 left join DICT033  on x4pro_ds.Proj like DICT033.Code
 left join QUANTITY on QUANTITY.Code like x4pro_ds.quant1
 left join DICT013  on DICT013.Code = x4pro_ds.reatyp
 left join DICT030  on DICT030.Code = x4pro_ds.Proc1
 left join REACSTR  on REACSTR.ReacodeID=x4pro_ds.DatasetID
 left join DICT036  on DICT036.Code = REACSTR.SF58
 left join DICT033 as optbl on x4pro_ds.Proc1 like optbl.Code
where reacode not like '(%' -- no reaction-combinations
 -- and proj='n'
 -- and target like 'f-19'
 -- and target like 'Al-27'
 -- and target like 'f%'
 -- and quant1 like 'cs'
 group by reacode
   order by REACSTR.zIncident,proj,zTarg1,aTarg1,Targ1,reacode
-- order by points desc,REACSTR.zIncident,proj,zTarg1,aTarg1,Targ1,reacode
-- order by REACSTR.zIncident,proj,REACSTR.SF58,zTarg1,aTarg1,Targ1,reacode
