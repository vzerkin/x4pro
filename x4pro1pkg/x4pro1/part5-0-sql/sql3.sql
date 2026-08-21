/*
    Project: X4Pro - universal, fully relational EXFOR database (SQLite)
    Author:  Viktor Zerkin, IAEA(1999-2023), NRDC(1996-2024)
             v.zerkin@gmail.com; https://github.com/vzerkin
    Program: sql3.txt, ver.2024-12-17
    Purpose: two SQL commands to produce histogram DATA(EN) as plain text
    Run:     $ sqlite3 -header -box x4sqlite1.db <sql3.sql >sql3.txt
*/


/*  SQL1: Summary information about EXFOR Dataset 22703002
 */
select distinct x4.DatasetID as Dataset
  ,ds4.year1 as year
  ,ds4.author1ini || ' ' || ds4.author1 as Author1
  ,ds4.reacode as REACTION
  ,(select units from x4pro_hdr where DatasetID=x4.DatasetID and hdr='EN') as EN
  ,(select units from x4pro_hdr where DatasetID=x4.DatasetID and hdr='DATA') as DATA
  ,(select units from x4pro_hdr where DatasetID=x4.DatasetID and hdr='ERR-T') as `ERR-T`
  ,ds4.MF,ds4.MT,ds4.ndat as `Pt.`
  from x4pro_x4data as x4
  inner join x4pro_ds as ds4 on ds4.DatasetID=x4.DatasetID
  where x4.DatasetID='22703002'
;


/*  SQL2: Generating histogram DATA(EN) for EXFOR Dataset 22703002
 */
with slots as (
  select distinct json_extract(x4.xdat,'$.EN') as EN
    ,json_extract(x4.xdat,'$.DATA') as CS
    ,json_extract(x4.xdat,'$.ERR-T') as ErrT
    ,(select distinct units from x4pro_hdr where DatasetID=x4.DatasetID and hdr='EN') as EnUnit
    ,(select distinct units from x4pro_hdr where DatasetID=x4.DatasetID and hdr='DATA') as DataUnit
    ,row_number() over () as n
  from x4pro_x4data as x4
  where x4.DatasetID='22703002'
  order by EN
  limit 25 offset 2
),
maxData as (
  select max(cast(json_extract(x4.xdat,'$.DATA') as float)) as value
  from x4pro_x4data as x4
  where x4.DatasetID='22703002'
)
select n
--  ,printf('EN(%s)=%-5g ',EnUnit,EN) as E
--  ,printf('SIG(%s)=%-11g',DataUnit,CS) as SIG
  ,EN as E
  ,CS as SIG
  ,ErrT as dSIG
  ,printf('%.'||cast(round(CS*40/maxData.value) as int)||'c','#') as `SIG(E)`
from slots,maxData
order by EN
