SELECT substr(DatasetID,1,5) as Entry
  ,DatasetID,idat
  ,CAST(json_extract(x4.xdat,'$.EN') AS FLOAT) as EN
  ,REACODE.FullCode
--  ,xdat
FROM x4pro_x4data as x4
  inner join REACODE on REACODE.ReacodeID=x4.DatasetID
where json_extract(x4.xdat,'$.EN') is not null
 and json_extract(x4.xdat,'$.EN') <=0
