Program: sig1x.py, ver. 2024-10-18
Author:  V.Zerkin, IAEA-NRDC, Vienna, 2021-2024
Purpose: Retrieve and plot EXFOR cross sections
	 from SQL database and ENDF data from Web
Running: 2024-10-18 13:06:59

Number of arguments: 4 arguments.
Argument List: ['sig1x.py', '', '', 'log']
Script-name: sig1x.py
---Retrieve EXFOR data from SQL database---
___getConnSQLite: file:../../x4sqlite1.db?mode=ro
Connected to: [sqlite3]

___getX4SqlSearchCS: [Al-27] [n,a]] []
SQL:
select *                          
from sig1                         
where (Target like 'Al-27')  
  and (Reaction like 'n,a') 
  and (sProd like '') 

 select x4pro_c5dat.DatasetID
 ,x4pro_c5dat.idat as iPoint
 ,REACODE.fullCode   
 ,REACODE.Pointer,ENTRY.Entry,REACODE.SubAcc as Subent   
 ,ENTRY.YearRef1,ENTRY.nAuthors,ENTRY.Author1Ini,ENTRY.Author1 
 ,REACSTR.Target, REACSTR.Reaction
 ,lower(REACSTR.Projectile) as Projectile
 ,REACSTR.sProd,REACSTR.sTarg
 ,REACODE.zaTarget1,REACODE.zaIncident1
 ,REACODE.outParticles,REACODE.MF,REACODE.MT
 ,x4pro_c5dat.x1  as En
 ,x4pro_c5dat.dx1 as dEn
 ,x4pro_c5dat.y   as Sig
 ,x4pro_c5dat.dy  as dSig
from x4pro_c5dat
 inner join REACODE on REACODE.ReacodeID=x4pro_c5dat.DatasetID
 inner join REACSTR ON REACSTR.ReacodeID=REACODE.ReacodeID
 inner join SUBENT on REACODE.SubentID=SUBENT.SubentID
 inner join ENTRY on ENTRY.EntryID=SUBENT.EntryID
 inner join x4pro_ds on REACODE.ReacodeID=x4pro_ds.DatasetID
where
--      (REACSTR.SF58 like ',SIG')
((x4pro_ds.reatyp like 'CS') or (x4pro_ds.reatyp like 'Ratio' and x4pro_c5dat.m1 is not Null))
and (x4pro_ds.MF=3 or x4pro_ds.MF=203)
  and (REACSTR.SF8='')
  and ((REACSTR.SF9='') or (REACSTR.SF9='EXP'))
  and ((REACODE.nReacstr=1)or(REACODE.nReacstr=2))
and (Target like 'Al-27') and (Reaction like 'n,a') and (sProd like '')
order by
  REACODE.fullCode,ENTRY.YearRef1 desc,x4pro_c5dat.DatasetID
  ,En,x4pro_c5dat.idat
REACSTR.iReacstr=1
REACSTR.Target


select distinct x4pro_c5dat.DatasetID
 ,ENTRY.YearRef1,ENTRY.Author1Ini,ENTRY.Author1,REACODE.fullCode
from x4pro_c5dat
 inner join REACODE on REACODE.ReacodeID=x4pro_c5dat.DatasetID
 inner join REACSTR ON REACSTR.ReacodeID=REACODE.ReacodeID
 inner join SUBENT on REACODE.SubentID=SUBENT.SubentID
 inner join ENTRY on ENTRY.EntryID=SUBENT.EntryID
 inner join x4pro_ds on REACODE.ReacodeID=x4pro_ds.DatasetID
where
--      (REACSTR.SF58 like ',SIG')
 (x4pro_ds.MF=3 or (x4pro_ds.MF=203 and x4pro_c5dat.m1 is not Null))
  and (REACSTR.SF8='')
  and ((REACSTR.SF9='') or (REACSTR.SF9='EXP'))
 and (REACSTR.iReacstr=1)
 and (REACSTR.Target like 'Al-27') and (REACSTR.Reaction like 'n,a') and (sProd like '')
order by
  -- REACODE.fullCode,
  ENTRY.YearRef1 desc,x4pro_c5dat.DatasetID


 select distinct x4pro_c5dat.DatasetID
from x4pro_c5dat
 inner join REACODE on REACODE.ReacodeID=x4pro_c5dat.DatasetID
 inner join REACSTR ON REACSTR.ReacodeID=REACODE.ReacodeID
 inner join SUBENT on REACODE.SubentID=SUBENT.SubentID
 inner join ENTRY on ENTRY.EntryID=SUBENT.EntryID
 inner join x4pro_ds on REACODE.ReacodeID=x4pro_ds.DatasetID
where
--      (REACSTR.SF58 like ',SIG')
((x4pro_ds.reatyp like 'CS') or (x4pro_ds.reatyp like 'Ratio' and x4pro_c5dat.m1 is not Null))
and 
(x4pro_ds.MF=3 or ((x4pro_ds.MF=203)and(x4pro_c5dat.m1 is not Null))
  and (REACSTR.SF8='')
  and ((REACSTR.SF9='') or (REACSTR.SF9='EXP'))
  and ((REACODE.nReacstr=1)or(REACODE.nReacstr=2))
and (Target like 'Al-27') and (Reaction like 'n,a') and (sProd like '')
order by
  REACODE.fullCode,ENTRY.YearRef1 desc,x4pro_c5dat.DatasetID
  ,x4pro_c5dat.idat


EXFOR SQL executed: 1.43sec

___getDatasets from datapoints: 692
DS:1) 13-AL-27(N,A)11-NA-24,,SIG #31842017 2022,J.Jarosik
 pt:1/692) 13-AL-27(N,A)11-NA-24,,SIG 31842017 2022 J.Jarosik x:17.5 y:63.0 dy:6.0 dx:2.0
 pt:2/692) 13-AL-27(N,A)11-NA-24,,SIG 31842017 2022 J.Jarosik x:19.8 y:35.0 dy:4.0 dx:1.8
 pt:3/692) 13-AL-27(N,A)11-NA-24,,SIG 31842017 2022 J.Jarosik x:27.5 y:12.6 dy:1.7 dx:1.4
DS:2) 13-AL-27(N,A)11-NA-24,,SIG #31834002 2020,D.Kral
 pt:4/692) 13-AL-27(N,A)11-NA-24,,SIG 31834002 2020 D.Kral x:29.1 y:2.7 dy:0.4 dx:None
DS:3) 13-AL-27(N,A)11-NA-24,,SIG #33025010 2009,B.Lalremruata
 pt:5/692) 13-AL-27(N,A)11-NA-24,,SIG 33025010 2009 B.Lalremruata x:14.77 y:115.0 dy:17.9397 dx:None
DS:4) 13-AL-27(N,A)11-NA-24,,SIG #22976004 2007,W.Mannhart
 pt:6/692) 13-AL-27(N,A)11-NA-24,,SIG 22976004 2007 W.Mannhart x:8.334 y:45.8 dy:1.45644 dx:0.02
 pt:7/692) 13-AL-27(N,A)11-NA-24,,SIG 22976004 2007 W.Mannhart x:8.556 y:57.5 dy:1.84575 dx:0.02
 pt:8/692) 13-AL-27(N,A)11-NA-24,,SIG 22976004 2007 W.Mannhart x:8.907 y:65.1 dy:2.06367 dx:0.02
 pt:9/692) 13-AL-27(N,A)11-NA-24,,SIG 22976004 2007 W.Mannhart x:9.111 y:71.0 dy:2.3004 dx:0.02
 pt:10/692) 13-AL-27(N,A)11-NA-24,,SIG 22976004 2007 W.Mannhart x:9.265 y:72.8 dy:2.27864 dx:0.02
 pt:11/692) 13-AL-27(N,A)11-NA-24,,SIG 22976004 2007 W.Mannhart x:9.547 y:79.6 dy:2.53128 dx:0.02
 pt:12/692) 13-AL-27(N,A)11-NA-24,,SIG 22976004 2007 W.Mannhart x:9.837 y:84.4 dy:2.7008 dx:0.02
 pt:13/692) 13-AL-27(N,A)11-NA-24,,SIG 22976004 2007 W.Mannhart x:10.069 y:88.2 dy:2.85768 dx:0.02
 pt:14/692) 13-AL-27(N,A)11-NA-24,,SIG 22976004 2007 W.Mannhart x:10.264 y:89.1 dy:2.79774 dx:0.02
 pt:15/692) 13-AL-27(N,A)11-NA-24,,SIG 22976004 2007 W.Mannhart x:10.551 y:99.4 dy:3.1808 dx:0.02
 pt:16/692) 13-AL-27(N,A)11-NA-24,,SIG 22976004 2007 W.Mannhart x:10.751 y:101.8 dy:3.2576 dx:0.02
 pt:17/692) 13-AL-27(N,A)11-NA-24,,SIG 22976004 2007 W.Mannhart x:10.998 y:110.5 dy:3.59125 dx:0.02
 pt:18/692) 13-AL-27(N,A)11-NA-24,,SIG 22976004 2007 W.Mannhart x:11.223 y:107.0 dy:3.531 dx:0.02
 pt:19/692) 13-AL-27(N,A)11-NA-24,,SIG 22976004 2007 W.Mannhart x:11.399 y:112.0 dy:3.7744 dx:0.02
 pt:20/692) 13-AL-27(N,A)11-NA-24,,SIG 22976004 2007 W.Mannhart x:11.654 y:109.2 dy:3.7128 dx:0.02
 pt:21/692) 13-AL-27(N,A)11-NA-24,,SIG 22976004 2007 W.Mannhart x:11.654 y:108.5 dy:3.67815 dx:0.02
 pt:22/692) 13-AL-27(N,A)11-NA-24,,SIG 22976004 2007 W.Mannhart x:11.654 y:108.8 dy:3.76448 dx:0.02
 pt:23/692) 13-AL-27(N,A)11-NA-24,,SIG 22976004 2007 W.Mannhart x:11.839 y:116.7 dy:3.9678 dx:0.02
 pt:24/692) 13-AL-27(N,A)11-NA-24,,SIG 22976004 2007 W.Mannhart x:12.116 y:115.2 dy:4.07808 dx:0.02
 pt:25/692) 13-AL-27(N,A)11-NA-24,,SIG 22976004 2007 W.Mannhart x:12.273 y:114.9 dy:4.03299 dx:0.02
 pt:26/692) 13-AL-27(N,A)11-NA-24,,SIG 22976004 2007 W.Mannhart x:12.446 y:119.3 dy:4.30673 dx:0.02
 pt:27/692) 13-AL-27(N,A)11-NA-24,,SIG 22976004 2007 W.Mannhart x:12.703 y:119.5 dy:4.3259 dx:0.02
 pt:28/692) 13-AL-27(N,A)11-NA-24,,SIG 22976004 2007 W.Mannhart x:12.976 y:120.8 dy:4.54208 dx:0.02
 pt:29/692) 13-AL-27(N,A)11-NA-24,,SIG 22976004 2007 W.Mannhart x:13.187 y:120.2 dy:4.54356 dx:0.02
 pt:30/692) 13-AL-27(N,A)11-NA-24,,SIG 22976004 2007 W.Mannhart x:13.425 y:125.5 dy:4.93215 dx:0.02
 pt:31/692) 13-AL-27(N,A)11-NA-24,,SIG 22976004 2007 W.Mannhart x:13.609 y:126.2 dy:5.08586 dx:0.02
 pt:32/692) 13-AL-27(N,A)11-NA-24,,SIG 22976004 2007 W.Mannhart x:14.147 y:121.6 dy:5.13152 dx:0.02
 pt:33/692) 13-AL-27(N,A)11-NA-24,,SIG 22976004 2007 W.Mannhart x:14.74 y:111.8 dy:4.90802 dx:0.02
DS:5) 13-AL-27(N,A)11-NA-24,,SIG #22497003 2000,R.Coszach
 pt:34/692) 13-AL-27(N,A)11-NA-24,,SIG 22497003 2000 R.Coszach x:22.2 y:24.7 dy:3.8 dx:4.0
 pt:35/692) 13-AL-27(N,A)11-NA-24,,SIG 22497003 2000 R.Coszach x:31.1 y:21.9 dy:3.8 dx:4.0
 pt:36/692) 13-AL-27(N,A)11-NA-24,,SIG 22497003 2000 R.Coszach x:40.0 y:26.5 dy:3.8 dx:4.0
 pt:37/692) 13-AL-27(N,A)11-NA-24,,SIG 22497003 2000 R.Coszach x:49.0 y:22.3 dy:3.8 dx:4.0
DS:6) 13-AL-27(N,A)11-NA-24,,SIG #31528009 1997,Hongyu Zhou
 pt:38/692) 13-AL-27(N,A)11-NA-24,,SIG 31528009 1997 Hongyu Zhou x:14.9 y:113.7 dy:8.9 dx:0.5
DS:7) 13-AL-27(N,A)11-NA-24,,SIG #23279006 1996,Y.Uno
 pt:39/692) 13-AL-27(N,A)11-NA-24,,SIG 23279006 1996 Y.Uno x:17.55 y:68.72 dy:2.72 dx:None
 pt:40/692) 13-AL-27(N,A)11-NA-24,,SIG 23279006 1996 Y.Uno x:19.84 y:36.09 dy:1.42 dx:None
 pt:41/692) 13-AL-27(N,A)11-NA-24,,SIG 23279006 1996 Y.Uno x:22.66 y:18.41 dy:0.74 dx:None
 pt:42/692) 13-AL-27(N,A)11-NA-24,,SIG 23279006 1996 Y.Uno x:24.99 y:10.04 dy:0.4 dx:None
 pt:43/692) 13-AL-27(N,A)11-NA-24,,SIG 23279006 1996 Y.Uno x:27.79 y:5.38 dy:0.22 dx:None
 pt:44/692) 13-AL-27(N,A)11-NA-24,,SIG 23279006 1996 Y.Uno x:30.09 y:2.67 dy:0.11 dx:None
DS:8) 13-AL-27(N,A)11-NA-24,,SIG #22312002 1993,Y.Ikeda
 pt:45/692) 13-AL-27(N,A)11-NA-24,,SIG 22312002 1993 Y.Ikeda x:13.33 y:126.2 dy:4.4 dx:None
 pt:46/692) 13-AL-27(N,A)11-NA-24,,SIG 22312002 1993 Y.Ikeda x:13.57 y:128.0 dy:4.7 dx:None
 pt:47/692) 13-AL-27(N,A)11-NA-24,,SIG 22312002 1993 Y.Ikeda x:13.75 y:122.0 dy:4.5 dx:None
 pt:48/692) 13-AL-27(N,A)11-NA-24,,SIG 22312002 1993 Y.Ikeda x:13.98 y:122.7 dy:4.4 dx:None
 pt:49/692) 13-AL-27(N,A)11-NA-24,,SIG 22312002 1993 Y.Ikeda x:14.22 y:119.0 dy:5.7 dx:None
 pt:50/692) 13-AL-27(N,A)11-NA-24,,SIG 22312002 1993 Y.Ikeda x:14.42 y:114.5 dy:4.0 dx:None
 pt:51/692) 13-AL-27(N,A)11-NA-24,,SIG 22312002 1993 Y.Ikeda x:14.65 y:112.5 dy:4.0 dx:None
 pt:52/692) 13-AL-27(N,A)11-NA-24,,SIG 22312002 1993 Y.Ikeda x:14.91 y:112.0 dy:3.9 dx:None
DS:9) 13-AL-27(N,A)11-NA-24,,SIG #30993002 1993,Bao Zongyu
 pt:53/692) 13-AL-27(N,A)11-NA-24,,SIG 30993002 1993 Bao Zongyu x:14.57 y:113.2 dy:1.5 dx:0.02
DS:10) 13-AL-27(N,A)11-NA-24,,SIG #22703002 1992,Y.Uwamino
 pt:54/692) 13-AL-27(N,A)11-NA-24,,SIG 22703002 1992 Y.Uwamino x:3.5 y:0.0 dy:0.0 dx:None
 pt:55/692) 13-AL-27(N,A)11-NA-24,,SIG 22703002 1992 Y.Uwamino x:4.5 y:0.001383 dy:0.00018 dx:None
 pt:56/692) 13-AL-27(N,A)11-NA-24,,SIG 22703002 1992 Y.Uwamino x:5.5 y:0.6735 dy:0.086 dx:None
 pt:57/692) 13-AL-27(N,A)11-NA-24,,SIG 22703002 1992 Y.Uwamino x:6.5 y:12.93 dy:1.7 dx:None
 pt:58/692) 13-AL-27(N,A)11-NA-24,,SIG 22703002 1992 Y.Uwamino x:7.5 y:32.69 dy:4.2 dx:None
 pt:59/692) 13-AL-27(N,A)11-NA-24,,SIG 22703002 1992 Y.Uwamino x:8.5 y:60.6 dy:7.2 dx:None
 pt:60/692) 13-AL-27(N,A)11-NA-24,,SIG 22703002 1992 Y.Uwamino x:9.5 y:83.68 dy:8.9 dx:None
 pt:61/692) 13-AL-27(N,A)11-NA-24,,SIG 22703002 1992 Y.Uwamino x:10.5 y:97.89 dy:9.6 dx:None
 pt:62/692) 13-AL-27(N,A)11-NA-24,,SIG 22703002 1992 Y.Uwamino x:11.5 y:108.9 dy:9.5 dx:None
 pt:63/692) 13-AL-27(N,A)11-NA-24,,SIG 22703002 1992 Y.Uwamino x:12.5 y:119.2 dy:9.3 dx:None
 pt:64/692) 13-AL-27(N,A)11-NA-24,,SIG 22703002 1992 Y.Uwamino x:13.5 y:116.6 dy:8.7 dx:None
 pt:65/692) 13-AL-27(N,A)11-NA-24,,SIG 22703002 1992 Y.Uwamino x:14.5 y:106.6 dy:7.6 dx:None
 pt:66/692) 13-AL-27(N,A)11-NA-24,,SIG 22703002 1992 Y.Uwamino x:15.5 y:94.02 dy:7.4 dx:None
 pt:67/692) 13-AL-27(N,A)11-NA-24,,SIG 22703002 1992 Y.Uwamino x:16.5 y:76.27 dy:6.8 dx:None
 pt:68/692) 13-AL-27(N,A)11-NA-24,,SIG 22703002 1992 Y.Uwamino x:17.5 y:62.19 dy:6.0 dx:None
 pt:69/692) 13-AL-27(N,A)11-NA-24,,SIG 22703002 1992 Y.Uwamino x:18.5 y:49.26 dy:5.1 dx:None
 pt:70/692) 13-AL-27(N,A)11-NA-24,,SIG 22703002 1992 Y.Uwamino x:19.5 y:36.26 dy:4.2 dx:None
 pt:71/692) 13-AL-27(N,A)11-NA-24,,SIG 22703002 1992 Y.Uwamino x:20.5 y:28.08 dy:3.6 dx:None
 pt:72/692) 13-AL-27(N,A)11-NA-24,,SIG 22703002 1992 Y.Uwamino x:21.5 y:24.62 dy:3.0 dx:None
 pt:73/692) 13-AL-27(N,A)11-NA-24,,SIG 22703002 1992 Y.Uwamino x:22.5 y:24.88 dy:2.6 dx:None
 pt:74/692) 13-AL-27(N,A)11-NA-24,,SIG 22703002 1992 Y.Uwamino x:23.5 y:24.61 dy:2.2 dx:None
 pt:75/692) 13-AL-27(N,A)11-NA-24,,SIG 22703002 1992 Y.Uwamino x:24.5 y:21.45 dy:1.8 dx:None
 pt:76/692) 13-AL-27(N,A)11-NA-24,,SIG 22703002 1992 Y.Uwamino x:25.5 y:17.73 dy:1.5 dx:None
 pt:77/692) 13-AL-27(N,A)11-NA-24,,SIG 22703002 1992 Y.Uwamino x:26.5 y:14.55 dy:1.2 dx:None
 pt:78/692) 13-AL-27(N,A)11-NA-24,,SIG 22703002 1992 Y.Uwamino x:27.5 y:9.771 dy:1.0 dx:None
 pt:79/692) 13-AL-27(N,A)11-NA-24,,SIG 22703002 1992 Y.Uwamino x:28.5 y:5.502 dy:0.81 dx:None
 pt:80/692) 13-AL-27(N,A)11-NA-24,,SIG 22703002 1992 Y.Uwamino x:29.5 y:3.916 dy:0.63 dx:None
 pt:81/692) 13-AL-27(N,A)11-NA-24,,SIG 22703002 1992 Y.Uwamino x:30.5 y:2.724 dy:0.53 dx:None
 pt:82/692) 13-AL-27(N,A)11-NA-24,,SIG 22703002 1992 Y.Uwamino x:31.5 y:2.149 dy:0.48 dx:None
 pt:83/692) 13-AL-27(N,A)11-NA-24,,SIG 22703002 1992 Y.Uwamino x:32.5 y:2.164 dy:0.43 dx:None
 pt:84/692) 13-AL-27(N,A)11-NA-24,,SIG 22703002 1992 Y.Uwamino x:33.5 y:2.307 dy:0.4 dx:None
 pt:85/692) 13-AL-27(N,A)11-NA-24,,SIG 22703002 1992 Y.Uwamino x:34.5 y:2.133 dy:0.36 dx:None
 pt:86/692) 13-AL-27(N,A)11-NA-24,,SIG 22703002 1992 Y.Uwamino x:35.5 y:1.744 dy:0.33 dx:None
 pt:87/692) 13-AL-27(N,A)11-NA-24,,SIG 22703002 1992 Y.Uwamino x:36.5 y:1.357 dy:0.32 dx:None
 pt:88/692) 13-AL-27(N,A)11-NA-24,,SIG 22703002 1992 Y.Uwamino x:37.5 y:1.236 dy:0.29 dx:None
 pt:89/692) 13-AL-27(N,A)11-NA-24,,SIG 22703002 1992 Y.Uwamino x:38.5 y:1.206 dy:0.29 dx:None
DS:11) 13-AL-27(N,A)11-NA-24,,SIG #31459008 1992,I.Garlea
 pt:90/692) 13-AL-27(N,A)11-NA-24,,SIG 31459008 1992 I.Garlea x:14.758 y:115.4 dy:3.7 dx:0.3
DS:12) 13-AL-27(N,A)11-NA-24,,SIG #22209002 1991,Y.Ikeda
 pt:91/692) 13-AL-27(N,A)11-NA-24,,SIG 22209002 1991 Y.Ikeda x:11.0 y:102.4 dy:4.7 dx:0.5
 pt:92/692) 13-AL-27(N,A)11-NA-24,,SIG 22209002 1991 Y.Ikeda x:12.0 y:118.5 dy:4.3 dx:0.5
 pt:93/692) 13-AL-27(N,A)11-NA-24,,SIG 22209002 1991 Y.Ikeda x:13.2 y:125.1 dy:6.9 dx:0.5
DS:13) 13-AL-27(N,A)11-NA-24,,SIG #22209009 1991,Y.Ikeda
 pt:94/692) 13-AL-27(N,A)11-NA-24,,SIG 22209009 1991 Y.Ikeda x:9.5 y:77.6 dy:3.9 dx:0.5
 pt:95/692) 13-AL-27(N,A)11-NA-24,,SIG 22209009 1991 Y.Ikeda x:11.0 y:102.4 dy:4.5 dx:0.5
 pt:96/692) 13-AL-27(N,A)11-NA-24,,SIG 22209009 1991 Y.Ikeda x:12.0 y:116.5 dy:4.3 dx:0.5
 pt:97/692) 13-AL-27(N,A)11-NA-24,,SIG 22209009 1991 Y.Ikeda x:13.2 y:125.1 dy:6.9 dx:0.5
DS:14) 13-AL-27(N,A)11-NA-24,,SIG #131710032 1989,L.P.Geraldo
 pt:98/692) 13-AL-27(N,A)11-NA-24,,SIG 131710032 1989 L.P.Geraldo x:5.869 y:1.145 dy:None dx:0.163
 pt:99/692) 13-AL-27(N,A)11-NA-24,,SIG 131710032 1989 L.P.Geraldo x:6.399 y:4.837 dy:None dx:0.15
 pt:100/692) 13-AL-27(N,A)11-NA-24,,SIG 131710032 1989 L.P.Geraldo x:6.914 y:15.63 dy:None dx:0.138
 pt:101/692) 13-AL-27(N,A)11-NA-24,,SIG 131710032 1989 L.P.Geraldo x:7.419 y:26.33 dy:None dx:0.145
 pt:102/692) 13-AL-27(N,A)11-NA-24,,SIG 131710032 1989 L.P.Geraldo x:7.917 y:43.19 dy:None dx:0.16
 pt:103/692) 13-AL-27(N,A)11-NA-24,,SIG 131710032 1989 L.P.Geraldo x:8.408 y:53.6 dy:None dx:0.178
 pt:104/692) 13-AL-27(N,A)11-NA-24,,SIG 131710032 1989 L.P.Geraldo x:8.895 y:67.95 dy:None dx:0.188
 pt:105/692) 13-AL-27(N,A)11-NA-24,,SIG 131710032 1989 L.P.Geraldo x:9.379 y:82.13 dy:None dx:0.198
 pt:106/692) 13-AL-27(N,A)11-NA-24,,SIG 131710032 1989 L.P.Geraldo x:9.379 y:81.88 dy:None dx:0.198
 pt:107/692) 13-AL-27(N,A)11-NA-24,,SIG 131710032 1989 L.P.Geraldo x:9.859 y:85.74 dy:None dx:0.231
DS:15) 13-AL-27(N,A)11-NA-24,,SIG #30523002 1989,Lu Han-Lin
 pt:108/692) 13-AL-27(N,A)11-NA-24,,SIG 30523002 1989 Lu Han-Lin x:14.58 y:115.8 dy:3.0 dx:0.21
DS:16) 13-AL-27(N,A)11-NA-24,,SIG #30523003 1989,Lu Han-Lin
 pt:109/692) 13-AL-27(N,A)11-NA-24,,SIG 30523003 1989 Lu Han-Lin x:12.23 y:118.2 dy:5.1 dx:0.14
 pt:110/692) 13-AL-27(N,A)11-NA-24,,SIG 30523003 1989 Lu Han-Lin x:12.79 y:120.8 dy:5.3 dx:0.29
 pt:111/692) 13-AL-27(N,A)11-NA-24,,SIG 30523003 1989 Lu Han-Lin x:13.41 y:124.9 dy:3.3 dx:0.16
 pt:112/692) 13-AL-27(N,A)11-NA-24,,SIG 30523003 1989 Lu Han-Lin x:13.56 y:126.1 dy:3.3 dx:0.13
 pt:113/692) 13-AL-27(N,A)11-NA-24,,SIG 30523003 1989 Lu Han-Lin x:13.68 y:124.2 dy:3.3 dx:0.35
 pt:114/692) 13-AL-27(N,A)11-NA-24,,SIG 30523003 1989 Lu Han-Lin x:14.36 y:119.1 dy:3.2 dx:0.15
 pt:115/692) 13-AL-27(N,A)11-NA-24,,SIG 30523003 1989 Lu Han-Lin x:14.77 y:114.2 dy:3.0 dx:0.25
 pt:116/692) 13-AL-27(N,A)11-NA-24,,SIG 30523003 1989 Lu Han-Lin x:16.05 y:91.8 dy:4.0 dx:0.43
 pt:117/692) 13-AL-27(N,A)11-NA-24,,SIG 30523003 1989 Lu Han-Lin x:17.18 y:71.2 dy:3.1 dx:0.38
 pt:118/692) 13-AL-27(N,A)11-NA-24,,SIG 30523003 1989 Lu Han-Lin x:17.97 y:61.0 dy:2.6 dx:0.27
DS:17) 13-AL-27(N,A)11-NA-24,,SIG #410480022 1989,N.V.Kornilov
 pt:119/692) 13-AL-27(N,A)11-NA-24,,SIG 410480022 1989 N.V.Kornilov x:7.13 y:20.7 dy:1.1 dx:None
 pt:120/692) 13-AL-27(N,A)11-NA-24,,SIG 410480022 1989 N.V.Kornilov x:7.22 y:23.3 dy:1.3 dx:None
 pt:121/692) 13-AL-27(N,A)11-NA-24,,SIG 410480022 1989 N.V.Kornilov x:7.3 y:20.8 dy:1.1 dx:None
 pt:122/692) 13-AL-27(N,A)11-NA-24,,SIG 410480022 1989 N.V.Kornilov x:7.37 y:21.6 dy:1.2 dx:None
 pt:123/692) 13-AL-27(N,A)11-NA-24,,SIG 410480022 1989 N.V.Kornilov x:7.45 y:26.2 dy:1.4 dx:None
 pt:124/692) 13-AL-27(N,A)11-NA-24,,SIG 410480022 1989 N.V.Kornilov x:7.54 y:30.2 dy:0.7 dx:None
 pt:125/692) 13-AL-27(N,A)11-NA-24,,SIG 410480022 1989 N.V.Kornilov x:7.66 y:34.9 dy:0.8 dx:None
 pt:126/692) 13-AL-27(N,A)11-NA-24,,SIG 410480022 1989 N.V.Kornilov x:7.69 y:33.1 dy:1.8 dx:None
 pt:127/692) 13-AL-27(N,A)11-NA-24,,SIG 410480022 1989 N.V.Kornilov x:7.6901 y:32.1 dy:0.8 dx:None
 pt:128/692) 13-AL-27(N,A)11-NA-24,,SIG 410480022 1989 N.V.Kornilov x:7.78 y:33.3 dy:0.9 dx:None
 pt:129/692) 13-AL-27(N,A)11-NA-24,,SIG 410480022 1989 N.V.Kornilov x:7.91 y:39.6 dy:1.0 dx:None
 pt:130/692) 13-AL-27(N,A)11-NA-24,,SIG 410480022 1989 N.V.Kornilov x:7.96 y:43.6 dy:1.0 dx:None
 pt:131/692) 13-AL-27(N,A)11-NA-24,,SIG 410480022 1989 N.V.Kornilov x:8.04 y:44.3 dy:1.1 dx:None
 pt:132/692) 13-AL-27(N,A)11-NA-24,,SIG 410480022 1989 N.V.Kornilov x:8.12 y:44.2 dy:1.1 dx:None
 pt:133/692) 13-AL-27(N,A)11-NA-24,,SIG 410480022 1989 N.V.Kornilov x:8.2 y:45.3 dy:1.0 dx:None
 pt:134/692) 13-AL-27(N,A)11-NA-24,,SIG 410480022 1989 N.V.Kornilov x:8.28 y:47.9 dy:1.1 dx:None
 pt:135/692) 13-AL-27(N,A)11-NA-24,,SIG 410480022 1989 N.V.Kornilov x:8.37 y:49.1 dy:1.2 dx:None
 pt:136/692) 13-AL-27(N,A)11-NA-24,,SIG 410480022 1989 N.V.Kornilov x:8.45 y:54.0 dy:1.2 dx:None
 pt:137/692) 13-AL-27(N,A)11-NA-24,,SIG 410480022 1989 N.V.Kornilov x:8.57 y:58.0 dy:1.5 dx:None
 pt:138/692) 13-AL-27(N,A)11-NA-24,,SIG 410480022 1989 N.V.Kornilov x:8.71 y:63.1 dy:1.5 dx:None
 pt:139/692) 13-AL-27(N,A)11-NA-24,,SIG 410480022 1989 N.V.Kornilov x:8.83 y:66.2 dy:1.7 dx:None
 pt:140/692) 13-AL-27(N,A)11-NA-24,,SIG 410480022 1989 N.V.Kornilov x:8.97 y:64.9 dy:1.7 dx:None
 pt:141/692) 13-AL-27(N,A)11-NA-24,,SIG 410480022 1989 N.V.Kornilov x:9.1 y:72.9 dy:2.0 dx:None
DS:18) 13-AL-27(N,A)11-NA-24,,SIG #410480032 1989,N.V.Kornilov
 pt:142/692) 13-AL-27(N,A)11-NA-24,,SIG 410480032 1989 N.V.Kornilov x:7.62 y:35.1 dy:0.9 dx:None
 pt:143/692) 13-AL-27(N,A)11-NA-24,,SIG 410480032 1989 N.V.Kornilov x:7.7 y:32.1 dy:0.8 dx:None
 pt:144/692) 13-AL-27(N,A)11-NA-24,,SIG 410480032 1989 N.V.Kornilov x:7.78 y:34.1 dy:0.9 dx:None
 pt:145/692) 13-AL-27(N,A)11-NA-24,,SIG 410480032 1989 N.V.Kornilov x:7.87 y:34.5 dy:0.9 dx:None
 pt:146/692) 13-AL-27(N,A)11-NA-24,,SIG 410480032 1989 N.V.Kornilov x:7.95 y:45.0 dy:1.1 dx:None
 pt:147/692) 13-AL-27(N,A)11-NA-24,,SIG 410480032 1989 N.V.Kornilov x:8.04 y:44.7 dy:1.1 dx:None
 pt:148/692) 13-AL-27(N,A)11-NA-24,,SIG 410480032 1989 N.V.Kornilov x:8.12 y:43.8 dy:1.2 dx:None
 pt:149/692) 13-AL-27(N,A)11-NA-24,,SIG 410480032 1989 N.V.Kornilov x:8.21 y:45.6 dy:1.2 dx:None
 pt:150/692) 13-AL-27(N,A)11-NA-24,,SIG 410480032 1989 N.V.Kornilov x:8.3 y:49.1 dy:1.4 dx:None
 pt:151/692) 13-AL-27(N,A)11-NA-24,,SIG 410480032 1989 N.V.Kornilov x:8.38 y:50.4 dy:1.4 dx:None
 pt:152/692) 13-AL-27(N,A)11-NA-24,,SIG 410480032 1989 N.V.Kornilov x:8.47 y:55.2 dy:1.6 dx:None
 pt:153/692) 13-AL-27(N,A)11-NA-24,,SIG 410480032 1989 N.V.Kornilov x:8.55 y:59.8 dy:1.7 dx:None
 pt:154/692) 13-AL-27(N,A)11-NA-24,,SIG 410480032 1989 N.V.Kornilov x:8.64 y:58.8 dy:1.6 dx:None
 pt:155/692) 13-AL-27(N,A)11-NA-24,,SIG 410480032 1989 N.V.Kornilov x:8.73 y:65.9 dy:1.8 dx:None
 pt:156/692) 13-AL-27(N,A)11-NA-24,,SIG 410480032 1989 N.V.Kornilov x:8.82 y:68.7 dy:2.0 dx:None
 pt:157/692) 13-AL-27(N,A)11-NA-24,,SIG 410480032 1989 N.V.Kornilov x:8.91 y:66.8 dy:2.0 dx:None
 pt:158/692) 13-AL-27(N,A)11-NA-24,,SIG 410480032 1989 N.V.Kornilov x:9.0 y:68.9 dy:2.1 dx:None
 pt:159/692) 13-AL-27(N,A)11-NA-24,,SIG 410480032 1989 N.V.Kornilov x:9.09 y:74.5 dy:2.2 dx:None
 pt:160/692) 13-AL-27(N,A)11-NA-24,,SIG 410480032 1989 N.V.Kornilov x:9.0901 y:74.5 dy:2.2 dx:None
DS:19) 13-AL-27(N,A)11-NA-24,,SIG #410480042 1989,N.V.Kornilov
 pt:161/692) 13-AL-27(N,A)11-NA-24,,SIG 410480042 1989 N.V.Kornilov x:7.63 y:37.9 dy:1.3 dx:None
 pt:162/692) 13-AL-27(N,A)11-NA-24,,SIG 410480042 1989 N.V.Kornilov x:7.71 y:31.9 dy:1.0 dx:None
 pt:163/692) 13-AL-27(N,A)11-NA-24,,SIG 410480042 1989 N.V.Kornilov x:7.79 y:35.9 dy:1.1 dx:None
 pt:164/692) 13-AL-27(N,A)11-NA-24,,SIG 410480042 1989 N.V.Kornilov x:7.88 y:35.9 dy:1.1 dx:None
 pt:165/692) 13-AL-27(N,A)11-NA-24,,SIG 410480042 1989 N.V.Kornilov x:7.96 y:46.7 dy:1.4 dx:None
 pt:166/692) 13-AL-27(N,A)11-NA-24,,SIG 410480042 1989 N.V.Kornilov x:8.05 y:44.4 dy:1.1 dx:None
 pt:167/692) 13-AL-27(N,A)11-NA-24,,SIG 410480042 1989 N.V.Kornilov x:8.13 y:44.2 dy:1.3 dx:None
 pt:168/692) 13-AL-27(N,A)11-NA-24,,SIG 410480042 1989 N.V.Kornilov x:8.22 y:44.8 dy:1.5 dx:None
 pt:169/692) 13-AL-27(N,A)11-NA-24,,SIG 410480042 1989 N.V.Kornilov x:8.31 y:49.7 dy:1.5 dx:None
 pt:170/692) 13-AL-27(N,A)11-NA-24,,SIG 410480042 1989 N.V.Kornilov x:8.39 y:51.1 dy:1.4 dx:None
 pt:171/692) 13-AL-27(N,A)11-NA-24,,SIG 410480042 1989 N.V.Kornilov x:8.48 y:58.8 dy:1.9 dx:None
 pt:172/692) 13-AL-27(N,A)11-NA-24,,SIG 410480042 1989 N.V.Kornilov x:8.56 y:60.6 dy:1.9 dx:None
 pt:173/692) 13-AL-27(N,A)11-NA-24,,SIG 410480042 1989 N.V.Kornilov x:8.65 y:58.6 dy:1.7 dx:None
 pt:174/692) 13-AL-27(N,A)11-NA-24,,SIG 410480042 1989 N.V.Kornilov x:8.74 y:68.9 dy:1.9 dx:None
 pt:175/692) 13-AL-27(N,A)11-NA-24,,SIG 410480042 1989 N.V.Kornilov x:8.83 y:70.8 dy:2.3 dx:None
 pt:176/692) 13-AL-27(N,A)11-NA-24,,SIG 410480042 1989 N.V.Kornilov x:8.92 y:71.2 dy:2.2 dx:None
 pt:177/692) 13-AL-27(N,A)11-NA-24,,SIG 410480042 1989 N.V.Kornilov x:9.01 y:70.8 dy:2.1 dx:None
 pt:178/692) 13-AL-27(N,A)11-NA-24,,SIG 410480042 1989 N.V.Kornilov x:9.1 y:77.0 dy:2.4 dx:None
 pt:179/692) 13-AL-27(N,A)11-NA-24,,SIG 410480042 1989 N.V.Kornilov x:9.1001 y:75.6 dy:2.3 dx:None
DS:20) 13-AL-27(N,A)11-NA-24,,SIG #41051002 1989,N.N.Moiseev
 pt:180/692) 13-AL-27(N,A)11-NA-24,,SIG 41051002 1989 N.N.Moiseev x:14.8 y:110.2 dy:2.6448 dx:0.22
DS:21) 13-AL-27(N,A)11-NA-24,,SIG #41051003 1989,N.N.Moiseev
 pt:181/692) 13-AL-27(N,A)11-NA-24,,SIG 41051003 1989 N.N.Moiseev x:14.8 y:109.8 dy:2.3058 dx:0.22
DS:22) 13-AL-27(N,A)11-NA-24,,SIG #41051004 1989,N.N.Moiseev
 pt:182/692) 13-AL-27(N,A)11-NA-24,,SIG 41051004 1989 N.N.Moiseev x:14.8 y:110.0 dy:2.0 dx:0.22
DS:23) 13-AL-27(N,A)11-NA-24,,SIG #12969003 1987,J.W.Meadows
 pt:183/692) 13-AL-27(N,A)11-NA-24,,SIG 12969003 1987 J.W.Meadows x:14.74 y:109.4 dy:6.017 dx:0.02
DS:24) 13-AL-27(N,A)11-NA-24,,SIG #12977002 1987,L.R.Greenwood
 pt:184/692) 13-AL-27(N,A)11-NA-24,,SIG 12977002 1987 L.R.Greenwood x:14.5 y:117.0 dy:4.68 dx:0.4
 pt:185/692) 13-AL-27(N,A)11-NA-24,,SIG 12977002 1987 L.R.Greenwood x:14.65 y:113.0 dy:4.52 dx:0.4
 pt:186/692) 13-AL-27(N,A)11-NA-24,,SIG 12977002 1987 L.R.Greenwood x:14.8 y:111.0 dy:4.44 dx:0.4
 pt:187/692) 13-AL-27(N,A)11-NA-24,,SIG 12977002 1987 L.R.Greenwood x:14.85 y:107.0 dy:4.28 dx:0.4
 pt:188/692) 13-AL-27(N,A)11-NA-24,,SIG 12977002 1987 L.R.Greenwood x:14.9 y:108.0 dy:4.32 dx:0.4
DS:25) 13-AL-27(N,A)11-NA-24,,SIG #30755002 1987,Zhou Muyao
 pt:189/692) 13-AL-27(N,A)11-NA-24,,SIG 30755002 1987 Zhou Muyao x:14.6 y:115.0 dy:3.0 dx:0.2
DS:26) 13-AL-27(N,A)11-NA-24,,SIG #30821002 1986,T.Chimoye
 pt:190/692) 13-AL-27(N,A)11-NA-24,,SIG 30821002 1986 T.Chimoye x:13.84 y:122.9 dy:1.4748 dx:None
 pt:191/692) 13-AL-27(N,A)11-NA-24,,SIG 30821002 1986 T.Chimoye x:14.07 y:122.0 dy:1.464 dx:None
 pt:192/692) 13-AL-27(N,A)11-NA-24,,SIG 30821002 1986 T.Chimoye x:14.38 y:118.1 dy:1.4172 dx:None
 pt:193/692) 13-AL-27(N,A)11-NA-24,,SIG 30821002 1986 T.Chimoye x:14.62 y:114.7 dy:1.3764 dx:None
 pt:194/692) 13-AL-27(N,A)11-NA-24,,SIG 30821002 1986 T.Chimoye x:14.71 y:113.9 dy:1.3668 dx:None
DS:27) 13-AL-27(N,A)11-NA-24,,SIG #30933002 1986,J.Csikai
 pt:195/692) 13-AL-27(N,A)11-NA-24,,SIG 30933002 1986 J.Csikai x:13.4 y:126.4 dy:1.5168 dx:None
 pt:196/692) 13-AL-27(N,A)11-NA-24,,SIG 30933002 1986 J.Csikai x:13.48 y:127.1 dy:1.5252 dx:None
 pt:197/692) 13-AL-27(N,A)11-NA-24,,SIG 30933002 1986 J.Csikai x:13.74 y:124.4 dy:1.4928 dx:None
 pt:198/692) 13-AL-27(N,A)11-NA-24,,SIG 30933002 1986 J.Csikai x:13.84 y:122.9 dy:1.4748 dx:None
 pt:199/692) 13-AL-27(N,A)11-NA-24,,SIG 30933002 1986 J.Csikai x:14.01 y:122.0 dy:1.464 dx:None
 pt:200/692) 13-AL-27(N,A)11-NA-24,,SIG 30933002 1986 J.Csikai x:14.07 y:122.0 dy:1.464 dx:None
 pt:201/692) 13-AL-27(N,A)11-NA-24,,SIG 30933002 1986 J.Csikai x:14.38 y:118.1 dy:1.4172 dx:None
 pt:202/692) 13-AL-27(N,A)11-NA-24,,SIG 30933002 1986 J.Csikai x:14.46 y:115.6 dy:1.3872 dx:None
 pt:203/692) 13-AL-27(N,A)11-NA-24,,SIG 30933002 1986 J.Csikai x:14.62 y:114.7 dy:1.3764 dx:None
 pt:204/692) 13-AL-27(N,A)11-NA-24,,SIG 30933002 1986 J.Csikai x:14.71 y:113.9 dy:1.3668 dx:None
 pt:205/692) 13-AL-27(N,A)11-NA-24,,SIG 30933002 1986 J.Csikai x:14.74 y:112.2 dy:1.3464 dx:None
 pt:206/692) 13-AL-27(N,A)11-NA-24,,SIG 30933002 1986 J.Csikai x:14.83 y:111.9 dy:1.3428 dx:None
DS:28) 13-AL-27(N,A)11-NA-24,,SIG #22012003 1985,W.Enz
 pt:207/692) 13-AL-27(N,A)11-NA-24,,SIG 22012003 1985 W.Enz x:6.36 y:4.2 dy:0.4 dx:0.16
 pt:208/692) 13-AL-27(N,A)11-NA-24,,SIG 22012003 1985 W.Enz x:6.56 y:7.4 dy:0.8 dx:0.16
 pt:209/692) 13-AL-27(N,A)11-NA-24,,SIG 22012003 1985 W.Enz x:6.74 y:10.7 dy:1.1 dx:0.16
 pt:210/692) 13-AL-27(N,A)11-NA-24,,SIG 22012003 1985 W.Enz x:6.93 y:16.1 dy:1.7 dx:0.16
 pt:211/692) 13-AL-27(N,A)11-NA-24,,SIG 22012003 1985 W.Enz x:7.9 y:36.9 dy:4.2 dx:0.14
 pt:212/692) 13-AL-27(N,A)11-NA-24,,SIG 22012003 1985 W.Enz x:7.9 y:38.1 dy:4.7 dx:0.13
 pt:213/692) 13-AL-27(N,A)11-NA-24,,SIG 22012003 1985 W.Enz x:8.1 y:40.5 dy:4.6 dx:0.13
 pt:214/692) 13-AL-27(N,A)11-NA-24,,SIG 22012003 1985 W.Enz x:8.1 y:43.8 dy:5.4 dx:0.12
 pt:215/692) 13-AL-27(N,A)11-NA-24,,SIG 22012003 1985 W.Enz x:8.29 y:48.9 dy:5.5 dx:0.13
DS:29) 13-AL-27(N,A)11-NA-24,,SIG #21923002 1984,K.Kudo
 pt:216/692) 13-AL-27(N,A)11-NA-24,,SIG 21923002 1984 K.Kudo x:14.0 y:122.9 dy:2.1 dx:0.05
 pt:217/692) 13-AL-27(N,A)11-NA-24,,SIG 21923002 1984 K.Kudo x:14.6 y:113.4 dy:1.5 dx:0.1
 pt:218/692) 13-AL-27(N,A)11-NA-24,,SIG 21923002 1984 K.Kudo x:14.8 y:111.6 dy:1.7 dx:0.1
 pt:219/692) 13-AL-27(N,A)11-NA-24,,SIG 21923002 1984 K.Kudo x:15.21 y:105.2 dy:2.4 dx:0.28
 pt:220/692) 13-AL-27(N,A)11-NA-24,,SIG 21923002 1984 K.Kudo x:15.88 y:99.0 dy:2.3 dx:0.14
 pt:221/692) 13-AL-27(N,A)11-NA-24,,SIG 21923002 1984 K.Kudo x:16.98 y:80.4 dy:2.0 dx:0.1
 pt:222/692) 13-AL-27(N,A)11-NA-24,,SIG 21923002 1984 K.Kudo x:18.04 y:66.0 dy:1.8 dx:0.11
 pt:223/692) 13-AL-27(N,A)11-NA-24,,SIG 21923002 1984 K.Kudo x:19.87 y:44.9 dy:1.8 dx:0.15
DS:30) 13-AL-27(N,A)11-NA-24,,SIG #30813002 1984,I.Garlea
 pt:224/692) 13-AL-27(N,A)11-NA-24,,SIG 30813002 1984 I.Garlea x:14.75 y:126.1 dy:4.8 dx:None
DS:31) 13-AL-27(N,A)11-NA-24,,SIG #21941006 1983,S.Firkin
 pt:225/692) 13-AL-27(N,A)11-NA-24,,SIG 21941006 1983 S.Firkin x:7.35 y:25.4 dy:0.6 dx:None
 pt:226/692) 13-AL-27(N,A)11-NA-24,,SIG 21941006 1983 S.Firkin x:9.8 y:88.4 dy:2.2 dx:None
 pt:227/692) 13-AL-27(N,A)11-NA-24,,SIG 21941006 1983 S.Firkin x:11.8 y:117.0 dy:3.7 dx:None
 pt:228/692) 13-AL-27(N,A)11-NA-24,,SIG 21941006 1983 S.Firkin x:14.0 y:124.1 dy:0.7 dx:None
 pt:229/692) 13-AL-27(N,A)11-NA-24,,SIG 21941006 1983 S.Firkin x:14.1 y:122.0 dy:2.0 dx:None
DS:32) 13-AL-27(N,A)11-NA-24,,SIG #30640002 1982,J.Csikai
 pt:230/692) 13-AL-27(N,A)11-NA-24,,SIG 30640002 1982 J.Csikai x:13.5 y:128.3 dy:2.6 dx:None
 pt:231/692) 13-AL-27(N,A)11-NA-24,,SIG 30640002 1982 J.Csikai x:13.77 y:125.3 dy:2.5 dx:None
 pt:232/692) 13-AL-27(N,A)11-NA-24,,SIG 30640002 1982 J.Csikai x:14.39 y:117.6 dy:2.4 dx:None
 pt:233/692) 13-AL-27(N,A)11-NA-24,,SIG 30640002 1982 J.Csikai x:14.66 y:113.2 dy:2.3 dx:None
 pt:234/692) 13-AL-27(N,A)11-NA-24,,SIG 30640002 1982 J.Csikai x:14.78 y:113.3 dy:2.3 dx:None
DS:33) 13-AL-27(N,A)11-NA-24,,SIG #12912003 1981,P.Welch
 pt:235/692) 13-AL-27(N,A)11-NA-24,,SIG 12912003 1981 P.Welch x:20.0 y:164.5 dy:22.0 dx:0.1
 pt:236/692) 13-AL-27(N,A)11-NA-24,,SIG 12912003 1981 P.Welch x:23.0 y:90.0 dy:12.0 dx:0.1
DS:34) 13-AL-27(N,A)11-NA-24,,SIG #21756003 1981,H.Friedmann
 pt:237/692) 13-AL-27(N,A)11-NA-24,,SIG 21756003 1981 H.Friedmann x:13.7 y:127.6 dy:0.320273 dx:0.03
 pt:238/692) 13-AL-27(N,A)11-NA-24,,SIG 21756003 1981 H.Friedmann x:13.71 y:125.5 dy:0.315003 dx:0.03
 pt:239/692) 13-AL-27(N,A)11-NA-24,,SIG 21756003 1981 H.Friedmann x:13.76 y:126.1 dy:0.316508 dx:0.03
 pt:240/692) 13-AL-27(N,A)11-NA-24,,SIG 21756003 1981 H.Friedmann x:13.79 y:125.0 dy:0.313748 dx:0.03
 pt:241/692) 13-AL-27(N,A)11-NA-24,,SIG 21756003 1981 H.Friedmann x:13.83 y:124.2 dy:0.31174 dx:0.03
 pt:242/692) 13-AL-27(N,A)11-NA-24,,SIG 21756003 1981 H.Friedmann x:13.86 y:124.2 dy:0.31174 dx:0.03
 pt:243/692) 13-AL-27(N,A)11-NA-24,,SIG 21756003 1981 H.Friedmann x:13.9 y:125.2 dy:0.314249 dx:0.03
 pt:244/692) 13-AL-27(N,A)11-NA-24,,SIG 21756003 1981 H.Friedmann x:13.94 y:124.4 dy:0.312242 dx:0.03
 pt:245/692) 13-AL-27(N,A)11-NA-24,,SIG 21756003 1981 H.Friedmann x:13.99 y:124.4 dy:0.312242 dx:0.03
 pt:246/692) 13-AL-27(N,A)11-NA-24,,SIG 21756003 1981 H.Friedmann x:14.03 y:124.5 dy:0.312493 dx:0.03
 pt:247/692) 13-AL-27(N,A)11-NA-24,,SIG 21756003 1981 H.Friedmann x:14.07 y:124.6 dy:0.312744 dx:0.03
 pt:248/692) 13-AL-27(N,A)11-NA-24,,SIG 21756003 1981 H.Friedmann x:14.12 y:124.6 dy:0.312744 dx:0.03
 pt:249/692) 13-AL-27(N,A)11-NA-24,,SIG 21756003 1981 H.Friedmann x:14.16 y:124.8 dy:0.313246 dx:0.03
 pt:250/692) 13-AL-27(N,A)11-NA-24,,SIG 21756003 1981 H.Friedmann x:14.2 y:123.6 dy:0.310234 dx:0.03
 pt:251/692) 13-AL-27(N,A)11-NA-24,,SIG 21756003 1981 H.Friedmann x:14.24 y:121.3 dy:0.304461 dx:0.03
 pt:252/692) 13-AL-27(N,A)11-NA-24,,SIG 21756003 1981 H.Friedmann x:14.28 y:121.1 dy:0.303959 dx:0.03
 pt:253/692) 13-AL-27(N,A)11-NA-24,,SIG 21756003 1981 H.Friedmann x:14.32 y:120.5 dy:0.302453 dx:0.03
 pt:254/692) 13-AL-27(N,A)11-NA-24,,SIG 21756003 1981 H.Friedmann x:14.35 y:119.3 dy:0.299441 dx:0.03
 pt:255/692) 13-AL-27(N,A)11-NA-24,,SIG 21756003 1981 H.Friedmann x:14.39 y:119.2 dy:0.29919 dx:0.03
 pt:256/692) 13-AL-27(N,A)11-NA-24,,SIG 21756003 1981 H.Friedmann x:14.42 y:117.0 dy:0.293668 dx:0.03
DS:35) 13-AL-27(N,A)11-NA-24,,SIG #21756004 1981,H.Friedmann
 pt:257/692) 13-AL-27(N,A)11-NA-24,,SIG 21756004 1981 H.Friedmann x:13.7 y:126.7 dy:0.8869 dx:0.03
 pt:258/692) 13-AL-27(N,A)11-NA-24,,SIG 21756004 1981 H.Friedmann x:13.71 y:124.6 dy:0.8722 dx:0.03
 pt:259/692) 13-AL-27(N,A)11-NA-24,,SIG 21756004 1981 H.Friedmann x:13.76 y:125.2 dy:0.8764 dx:0.03
 pt:260/692) 13-AL-27(N,A)11-NA-24,,SIG 21756004 1981 H.Friedmann x:13.79 y:124.1 dy:0.8687 dx:0.03
 pt:261/692) 13-AL-27(N,A)11-NA-24,,SIG 21756004 1981 H.Friedmann x:13.83 y:123.3 dy:0.8631 dx:0.03
 pt:262/692) 13-AL-27(N,A)11-NA-24,,SIG 21756004 1981 H.Friedmann x:13.86 y:123.3 dy:0.8631 dx:0.03
 pt:263/692) 13-AL-27(N,A)11-NA-24,,SIG 21756004 1981 H.Friedmann x:13.9 y:124.3 dy:0.8701 dx:0.03
 pt:264/692) 13-AL-27(N,A)11-NA-24,,SIG 21756004 1981 H.Friedmann x:13.94 y:123.5 dy:0.8645 dx:0.03
 pt:265/692) 13-AL-27(N,A)11-NA-24,,SIG 21756004 1981 H.Friedmann x:13.99 y:123.5 dy:0.8645 dx:0.03
 pt:266/692) 13-AL-27(N,A)11-NA-24,,SIG 21756004 1981 H.Friedmann x:14.03 y:123.6 dy:0.8652 dx:0.03
 pt:267/692) 13-AL-27(N,A)11-NA-24,,SIG 21756004 1981 H.Friedmann x:14.07 y:123.7 dy:0.8659 dx:0.03
 pt:268/692) 13-AL-27(N,A)11-NA-24,,SIG 21756004 1981 H.Friedmann x:14.12 y:123.7 dy:0.8659 dx:0.03
 pt:269/692) 13-AL-27(N,A)11-NA-24,,SIG 21756004 1981 H.Friedmann x:14.16 y:122.9 dy:0.8603 dx:0.03
 pt:270/692) 13-AL-27(N,A)11-NA-24,,SIG 21756004 1981 H.Friedmann x:14.2 y:122.7 dy:0.8589 dx:0.03
 pt:271/692) 13-AL-27(N,A)11-NA-24,,SIG 21756004 1981 H.Friedmann x:14.24 y:120.5 dy:0.8435 dx:0.03
 pt:272/692) 13-AL-27(N,A)11-NA-24,,SIG 21756004 1981 H.Friedmann x:14.28 y:120.3 dy:0.8421 dx:0.03
 pt:273/692) 13-AL-27(N,A)11-NA-24,,SIG 21756004 1981 H.Friedmann x:14.32 y:119.6 dy:0.8372 dx:0.03
 pt:274/692) 13-AL-27(N,A)11-NA-24,,SIG 21756004 1981 H.Friedmann x:14.35 y:118.5 dy:0.8295 dx:0.03
 pt:275/692) 13-AL-27(N,A)11-NA-24,,SIG 21756004 1981 H.Friedmann x:14.39 y:118.3 dy:0.8281 dx:0.03
 pt:276/692) 13-AL-27(N,A)11-NA-24,,SIG 21756004 1981 H.Friedmann x:14.42 y:116.2 dy:0.8134 dx:0.03
DS:36) 13-AL-27(N,A)11-NA-24,,SIG #20986003 1979,M.T.Swinhoe
 pt:277/692) 13-AL-27(N,A)11-NA-24,,SIG 20986003 1979 M.T.Swinhoe x:7.5 y:25.4 dy:0.6 dx:None
 pt:278/692) 13-AL-27(N,A)11-NA-24,,SIG 20986003 1979 M.T.Swinhoe x:9.8 y:88.4 dy:2.2 dx:None
 pt:279/692) 13-AL-27(N,A)11-NA-24,,SIG 20986003 1979 M.T.Swinhoe x:11.8 y:117.0 dy:3.7 dx:None
DS:37) 13-AL-27(N,A)11-NA-24,,SIG #20986009 1979,M.T.Swinhoe
 pt:280/692) 13-AL-27(N,A)11-NA-24,,SIG 20986009 1979 M.T.Swinhoe x:14.0 y:124.0 dy:3.0 dx:None
DS:38) 13-AL-27(N,A)11-NA-24,,SIG #20842003 1978,P.Andersson
 pt:281/692) 13-AL-27(N,A)11-NA-24,,SIG 20842003 1978 P.Andersson x:14.9 y:113.0 dy:6.0 dx:0.2
DS:39) 13-AL-27(N,A)11-NA-24,,SIG #20843009 1978,C.Nordborg
 pt:282/692) 13-AL-27(N,A)11-NA-24,,SIG 20843009 1978 C.Nordborg x:8.5 y:55.0 dy:6.0 dx:None
DS:40) 13-AL-27(N,A)11-NA-24,,SIG #20867006 1978,T.B.Ryves
 pt:283/692) 13-AL-27(N,A)11-NA-24,,SIG 20867006 1978 T.B.Ryves x:14.65 y:112.4 dy:3.1 dx:0.1
 pt:284/692) 13-AL-27(N,A)11-NA-24,,SIG 20867006 1978 T.B.Ryves x:17.35 y:70.7 dy:2.4 dx:0.2
 pt:285/692) 13-AL-27(N,A)11-NA-24,,SIG 20867006 1978 T.B.Ryves x:18.06 y:62.1 dy:2.5 dx:0.19
 pt:286/692) 13-AL-27(N,A)11-NA-24,,SIG 20867006 1978 T.B.Ryves x:19.0 y:47.5 dy:2.4 dx:0.19
DS:41) 13-AL-27(N,A)11-NA-24,,SIG #30479002 1978,U.Garuska
 pt:287/692) 13-AL-27(N,A)11-NA-24,,SIG 30479002 1978 U.Garuska x:14.6 y:141.0 dy:8.0 dx:None
DS:42) 13-AL-27(N,A)11-NA-24,,SIG #21049003 1976,A.B.M.G.Mostafa
 pt:288/692) 13-AL-27(N,A)11-NA-24,,SIG 21049003 1976 A.B.M.G.Mostafa x:5.8 y:1.57 dy:0.18 dx:0.62
 pt:289/692) 13-AL-27(N,A)11-NA-24,,SIG 21049003 1976 A.B.M.G.Mostafa x:6.3 y:4.3 dy:0.36 dx:0.6
 pt:290/692) 13-AL-27(N,A)11-NA-24,,SIG 21049003 1976 A.B.M.G.Mostafa x:6.7 y:12.0 dy:1.0 dx:0.52
 pt:291/692) 13-AL-27(N,A)11-NA-24,,SIG 21049003 1976 A.B.M.G.Mostafa x:7.1 y:22.0 dy:1.6 dx:0.35
 pt:292/692) 13-AL-27(N,A)11-NA-24,,SIG 21049003 1976 A.B.M.G.Mostafa x:7.55 y:28.0 dy:2.0 dx:0.3
 pt:293/692) 13-AL-27(N,A)11-NA-24,,SIG 21049003 1976 A.B.M.G.Mostafa x:8.0 y:37.0 dy:2.7 dx:0.25
 pt:294/692) 13-AL-27(N,A)11-NA-24,,SIG 21049003 1976 A.B.M.G.Mostafa x:8.25 y:45.0 dy:3.0 dx:0.18
 pt:295/692) 13-AL-27(N,A)11-NA-24,,SIG 21049003 1976 A.B.M.G.Mostafa x:8.35 y:60.0 dy:4.0 dx:0.12
DS:43) 13-AL-27(N,A)11-NA-24,,SIG #40135002 1974,Yu.A.Nemilov
 pt:296/692) 13-AL-27(N,A)11-NA-24,,SIG 40135002 1974 Yu.A.Nemilov x:7.7 y:43.0 dy:5.0 dx:0.3
 pt:297/692) 13-AL-27(N,A)11-NA-24,,SIG 40135002 1974 Yu.A.Nemilov x:8.6 y:77.0 dy:8.0 dx:0.3
 pt:298/692) 13-AL-27(N,A)11-NA-24,,SIG 40135002 1974 Yu.A.Nemilov x:9.05 y:78.0 dy:7.0 dx:0.3
 pt:299/692) 13-AL-27(N,A)11-NA-24,,SIG 40135002 1974 Yu.A.Nemilov x:9.3 y:82.0 dy:6.0 dx:0.3
DS:44) 13-AL-27(N,A)11-NA-24,,SIG #20798002 1973,J.C.Robertson
 pt:300/692) 13-AL-27(N,A)11-NA-24,,SIG 20798002 1973 J.C.Robertson x:14.78 y:115.5 dy:3.0 dx:None
DS:45) 13-AL-27(N,A)11-NA-24,,SIG #10186005 1971,G.N.Salaita
 pt:301/692) 13-AL-27(N,A)11-NA-24,,SIG 10186005 1971 G.N.Salaita x:14.8 y:111.0 dy:9.0 dx:None
DS:46) 13-AL-27(N,A)11-NA-24,,SIG #10116002 1970,J.Lebowitz
 pt:302/692) 13-AL-27(N,A)11-NA-24,,SIG 10116002 1970 J.Lebowitz x:14.7 y:110.0 dy:15.0 dx:None
DS:47) 13-AL-27(N,A)11-NA-24,,SIG #20111002 1970,H.Vonach
 pt:303/692) 13-AL-27(N,A)11-NA-24,,SIG 20111002 1970 H.Vonach x:14.43 y:117.0 dy:0.8 dx:0.015
DS:48) 13-AL-27(N,A)11-NA-24,,SIG #10031002 1969,R.C.Barrall
 pt:304/692) 13-AL-27(N,A)11-NA-24,,SIG 10031002 1969 R.C.Barrall x:14.8 y:116.0 dy:8.0 dx:0.2
DS:49) 13-AL-27(N,A)11-NA-24,,SIG #20930005 1969,D.Crumpton
 pt:305/692) 13-AL-27(N,A)11-NA-24,,SIG 20930005 1969 D.Crumpton x:14.7 y:121.0 dy:6.0 dx:0.2
DS:50) 13-AL-27(N,A)11-NA-24,,SIG #21250002 1969,P.Boschung
 pt:306/692) 13-AL-27(N,A)11-NA-24,,SIG 21250002 1969 P.Boschung x:14.2 y:120.0 dy:5.0 dx:None
DS:51) 13-AL-27(N,A)11-NA-24,,SIG #20890003 1968,P.Cuzzocrea
 pt:307/692) 13-AL-27(N,A)11-NA-24,,SIG 20890003 1968 P.Cuzzocrea x:13.7 y:129.5 dy:11.6 dx:0.04
 pt:308/692) 13-AL-27(N,A)11-NA-24,,SIG 20890003 1968 P.Cuzzocrea x:13.745 y:137.0 dy:12.3 dx:0.04
 pt:309/692) 13-AL-27(N,A)11-NA-24,,SIG 20890003 1968 P.Cuzzocrea x:13.77 y:140.5 dy:12.6 dx:0.04
 pt:310/692) 13-AL-27(N,A)11-NA-24,,SIG 20890003 1968 P.Cuzzocrea x:13.795 y:137.0 dy:12.3 dx:0.04
 pt:311/692) 13-AL-27(N,A)11-NA-24,,SIG 20890003 1968 P.Cuzzocrea x:13.82 y:139.5 dy:12.5 dx:0.04
 pt:312/692) 13-AL-27(N,A)11-NA-24,,SIG 20890003 1968 P.Cuzzocrea x:13.845 y:135.5 dy:12.2 dx:0.04
 pt:313/692) 13-AL-27(N,A)11-NA-24,,SIG 20890003 1968 P.Cuzzocrea x:13.87 y:138.0 dy:12.4 dx:0.04
 pt:314/692) 13-AL-27(N,A)11-NA-24,,SIG 20890003 1968 P.Cuzzocrea x:13.895 y:135.5 dy:12.2 dx:0.04
 pt:315/692) 13-AL-27(N,A)11-NA-24,,SIG 20890003 1968 P.Cuzzocrea x:13.92 y:137.0 dy:12.3 dx:0.04
 pt:316/692) 13-AL-27(N,A)11-NA-24,,SIG 20890003 1968 P.Cuzzocrea x:13.95 y:141.0 dy:12.7 dx:0.04
 pt:317/692) 13-AL-27(N,A)11-NA-24,,SIG 20890003 1968 P.Cuzzocrea x:13.97 y:137.0 dy:12.3 dx:0.04
 pt:318/692) 13-AL-27(N,A)11-NA-24,,SIG 20890003 1968 P.Cuzzocrea x:14.0 y:141.0 dy:12.7 dx:0.04
 pt:319/692) 13-AL-27(N,A)11-NA-24,,SIG 20890003 1968 P.Cuzzocrea x:14.025 y:135.5 dy:12.2 dx:0.04
 pt:320/692) 13-AL-27(N,A)11-NA-24,,SIG 20890003 1968 P.Cuzzocrea x:14.055 y:136.5 dy:12.3 dx:0.04
 pt:321/692) 13-AL-27(N,A)11-NA-24,,SIG 20890003 1968 P.Cuzzocrea x:14.08 y:136.0 dy:12.2 dx:0.04
 pt:322/692) 13-AL-27(N,A)11-NA-24,,SIG 20890003 1968 P.Cuzzocrea x:14.11 y:142.5 dy:12.8 dx:0.04
 pt:323/692) 13-AL-27(N,A)11-NA-24,,SIG 20890003 1968 P.Cuzzocrea x:14.135 y:138.5 dy:12.5 dx:0.04
 pt:324/692) 13-AL-27(N,A)11-NA-24,,SIG 20890003 1968 P.Cuzzocrea x:14.16 y:134.5 dy:12.1 dx:0.04
 pt:325/692) 13-AL-27(N,A)11-NA-24,,SIG 20890003 1968 P.Cuzzocrea x:14.21 y:141.5 dy:12.7 dx:0.04
 pt:326/692) 13-AL-27(N,A)11-NA-24,,SIG 20890003 1968 P.Cuzzocrea x:14.26 y:136.5 dy:12.3 dx:0.04
 pt:327/692) 13-AL-27(N,A)11-NA-24,,SIG 20890003 1968 P.Cuzzocrea x:14.3 y:142.5 dy:12.8 dx:0.04
 pt:328/692) 13-AL-27(N,A)11-NA-24,,SIG 20890003 1968 P.Cuzzocrea x:14.36 y:139.5 dy:12.5 dx:0.045
 pt:329/692) 13-AL-27(N,A)11-NA-24,,SIG 20890003 1968 P.Cuzzocrea x:14.405 y:131.0 dy:11.8 dx:0.05
 pt:330/692) 13-AL-27(N,A)11-NA-24,,SIG 20890003 1968 P.Cuzzocrea x:14.445 y:133.0 dy:12.0 dx:0.055
 pt:331/692) 13-AL-27(N,A)11-NA-24,,SIG 20890003 1968 P.Cuzzocrea x:14.525 y:131.5 dy:11.8 dx:0.06
 pt:332/692) 13-AL-27(N,A)11-NA-24,,SIG 20890003 1968 P.Cuzzocrea x:14.585 y:125.5 dy:11.3 dx:0.065
 pt:333/692) 13-AL-27(N,A)11-NA-24,,SIG 20890003 1968 P.Cuzzocrea x:14.67 y:131.5 dy:11.8 dx:0.09
DS:52) 13-AL-27(N,A)11-NA-24,,SIG #10417008 1967,J.A.Grundl
 pt:334/692) 13-AL-27(N,A)11-NA-24,,SIG 10417008 1967 J.A.Grundl x:5.95 y:1.5 dy:0.09 dx:0.43
 pt:335/692) 13-AL-27(N,A)11-NA-24,,SIG 10417008 1967 J.A.Grundl x:6.97 y:15.9 dy:0.477 dx:0.33
 pt:336/692) 13-AL-27(N,A)11-NA-24,,SIG 10417008 1967 J.A.Grundl x:7.5 y:31.2 dy:1.248 dx:0.15
 pt:337/692) 13-AL-27(N,A)11-NA-24,,SIG 10417008 1967 J.A.Grundl x:8.07 y:41.8 dy:2.508 dx:0.16
 pt:338/692) 13-AL-27(N,A)11-NA-24,,SIG 10417008 1967 J.A.Grundl x:10.0 y:77.0 dy:5.39 dx:0.28
 pt:339/692) 13-AL-27(N,A)11-NA-24,,SIG 10417008 1967 J.A.Grundl x:14.1 y:135.0 dy:6.75 dx:0.1
DS:53) 13-AL-27(N,A)11-NA-24,,SIG #11421004 1967,H.O.Menlove
 pt:340/692) 13-AL-27(N,A)11-NA-24,,SIG 11421004 1967 H.O.Menlove x:6.13 y:2.24 dy:0.22 dx:0.28
 pt:341/692) 13-AL-27(N,A)11-NA-24,,SIG 11421004 1967 H.O.Menlove x:8.06 y:38.2 dy:3.8 dx:0.14
 pt:342/692) 13-AL-27(N,A)11-NA-24,,SIG 11421004 1967 H.O.Menlove x:13.28 y:116.0 dy:11.0 dx:0.61
 pt:343/692) 13-AL-27(N,A)11-NA-24,,SIG 11421004 1967 H.O.Menlove x:13.5 y:116.0 dy:14.0 dx:0.47
 pt:344/692) 13-AL-27(N,A)11-NA-24,,SIG 11421004 1967 H.O.Menlove x:14.96 y:111.0 dy:11.0 dx:0.87
 pt:345/692) 13-AL-27(N,A)11-NA-24,,SIG 11421004 1967 H.O.Menlove x:15.82 y:104.0 dy:10.0 dx:0.45
 pt:346/692) 13-AL-27(N,A)11-NA-24,,SIG 11421004 1967 H.O.Menlove x:16.52 y:89.3 dy:8.7 dx:0.35
 pt:347/692) 13-AL-27(N,A)11-NA-24,,SIG 11421004 1967 H.O.Menlove x:17.35 y:71.0 dy:7.0 dx:0.32
 pt:348/692) 13-AL-27(N,A)11-NA-24,,SIG 11421004 1967 H.O.Menlove x:18.44 y:51.2 dy:5.0 dx:0.33
 pt:349/692) 13-AL-27(N,A)11-NA-24,,SIG 11421004 1967 H.O.Menlove x:19.39 y:39.1 dy:3.9 dx:0.35
DS:54) 13-AL-27(N,A)11-NA-24,,SIG #11512003 1967,J.M.Ferguson
 pt:350/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:12.34 y:121.6 dy:1.2 dx:0.05
 pt:351/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:12.37 y:121.6 dy:0.7 dx:0.05
 pt:352/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:12.4 y:122.8 dy:0.8 dx:0.05
 pt:353/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:12.42 y:122.2 dy:0.8 dx:0.05
 pt:354/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:12.45 y:120.9 dy:0.9 dx:0.05
 pt:355/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:12.47 y:121.3 dy:0.7 dx:0.05
 pt:356/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:12.5 y:122.0 dy:0.9 dx:0.05
 pt:357/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:12.53 y:122.3 dy:1.0 dx:0.04
 pt:358/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:12.55 y:123.7 dy:1.0 dx:0.04
 pt:359/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:12.59 y:124.0 dy:1.0 dx:0.03
 pt:360/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:12.63 y:122.7 dy:1.0 dx:0.03
 pt:361/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:12.66 y:120.6 dy:0.9 dx:0.03
 pt:362/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:12.7 y:120.6 dy:2.0 dx:0.03
 pt:363/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:12.75 y:118.6 dy:2.0 dx:0.03
 pt:364/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:12.8 y:117.7 dy:3.1 dx:0.03
 pt:365/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:12.85 y:119.0 dy:1.8 dx:0.03
 pt:366/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:12.9 y:118.0 dy:2.8 dx:0.03
 pt:367/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:12.95 y:118.0 dy:2.8 dx:0.03
 pt:368/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:13.0 y:117.2 dy:3.6 dx:0.03
 pt:369/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:13.05 y:116.9 dy:3.9 dx:0.03
 pt:370/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:13.1 y:118.1 dy:2.7 dx:0.03
 pt:371/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:13.15 y:114.4 dy:6.4 dx:0.03
 pt:372/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:13.2 y:118.0 dy:2.8 dx:0.03
 pt:373/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:13.25 y:118.6 dy:2.2 dx:0.03
 pt:374/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:13.3 y:119.8 dy:1.0 dx:0.03
 pt:375/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:13.35 y:122.1 dy:0.7 dx:0.03
 pt:376/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:13.4 y:123.8 dy:3.0 dx:0.03
 pt:377/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:13.45 y:125.8 dy:5.0 dx:0.03
 pt:378/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:13.5 y:125.4 dy:4.6 dx:0.02
 pt:379/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:13.55 y:126.6 dy:5.8 dx:0.02
 pt:380/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:13.6 y:124.9 dy:4.0 dx:0.02
 pt:381/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:13.65 y:124.0 dy:3.2 dx:0.02
 pt:382/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:13.7 y:122.0 dy:1.2 dx:0.02
 pt:383/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:13.75 y:121.1 dy:3.0 dx:0.02
 pt:384/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:13.8 y:121.2 dy:4.0 dx:0.02
 pt:385/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:13.85 y:120.6 dy:2.0 dx:0.02
 pt:386/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:13.9 y:120.2 dy:0.6 dx:0.02
 pt:387/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:13.95 y:120.3 dy:0.5 dx:0.02
 pt:388/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:14.0 y:119.8 dy:0.0 dx:0.02
 pt:389/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:14.05 y:120.3 dy:0.0 dx:0.02
 pt:390/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:14.15 y:118.9 dy:0.0 dx:0.02
 pt:391/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:14.2 y:117.5 dy:0.0 dx:0.02
 pt:392/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:14.25 y:114.5 dy:0.0 dx:0.02
 pt:393/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:14.3 y:114.3 dy:0.0 dx:0.02
 pt:394/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:14.35 y:111.8 dy:0.0 dx:0.02
 pt:395/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:14.4 y:109.7 dy:0.0 dx:0.02
 pt:396/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:14.45 y:109.5 dy:0.0 dx:0.02
 pt:397/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:14.5 y:108.8 dy:0.0 dx:0.03
 pt:398/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:14.6 y:108.2 dy:0.0 dx:0.03
 pt:399/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:14.65 y:107.3 dy:0.0 dx:0.03
 pt:400/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:14.7 y:107.0 dy:0.0 dx:0.04
 pt:401/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:14.75 y:104.8 dy:0.0 dx:0.04
 pt:402/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:14.8 y:104.4 dy:0.0 dx:0.05
 pt:403/692) 13-AL-27(N,A)11-NA-24,,SIG 11512003 1967 J.M.Ferguson x:14.85 y:106.1 dy:0.0 dx:0.05
DS:55) 13-AL-27(N,A)11-NA-24,,SIG #21345002 1967,B.Minetti
 pt:404/692) 13-AL-27(N,A)11-NA-24,,SIG 21345002 1967 B.Minetti x:14.7 y:120.0 dy:10.0 dx:None
DS:56) 13-AL-27(N,A)11-NA-24,,SIG #20387003 1966,H.Liskien
 pt:405/692) 13-AL-27(N,A)11-NA-24,,SIG 20387003 1966 H.Liskien x:6.06 y:2.1 dy:0.2 dx:0.1
 pt:406/692) 13-AL-27(N,A)11-NA-24,,SIG 20387003 1966 H.Liskien x:6.19 y:2.5 dy:0.2 dx:0.12
 pt:407/692) 13-AL-27(N,A)11-NA-24,,SIG 20387003 1966 H.Liskien x:6.33 y:3.4 dy:0.2 dx:0.14
 pt:408/692) 13-AL-27(N,A)11-NA-24,,SIG 20387003 1966 H.Liskien x:6.47 y:5.5 dy:0.3 dx:0.14
 pt:409/692) 13-AL-27(N,A)11-NA-24,,SIG 20387003 1966 H.Liskien x:6.63 y:8.0 dy:0.4 dx:0.15
 pt:410/692) 13-AL-27(N,A)11-NA-24,,SIG 20387003 1966 H.Liskien x:6.8 y:11.5 dy:0.6 dx:0.15
 pt:411/692) 13-AL-27(N,A)11-NA-24,,SIG 20387003 1966 H.Liskien x:6.97 y:16.0 dy:0.9 dx:0.15
 pt:412/692) 13-AL-27(N,A)11-NA-24,,SIG 20387003 1966 H.Liskien x:7.13 y:21.1 dy:1.1 dx:0.15
 pt:413/692) 13-AL-27(N,A)11-NA-24,,SIG 20387003 1966 H.Liskien x:7.3 y:22.9 dy:1.2 dx:0.16
 pt:414/692) 13-AL-27(N,A)11-NA-24,,SIG 20387003 1966 H.Liskien x:7.47 y:26.6 dy:1.4 dx:0.17
 pt:415/692) 13-AL-27(N,A)11-NA-24,,SIG 20387003 1966 H.Liskien x:7.62 y:29.7 dy:1.5 dx:0.18
 pt:416/692) 13-AL-27(N,A)11-NA-24,,SIG 20387003 1966 H.Liskien x:7.76 y:37.6 dy:1.9 dx:0.19
 pt:417/692) 13-AL-27(N,A)11-NA-24,,SIG 20387003 1966 H.Liskien x:7.89 y:35.7 dy:1.8 dx:0.2
 pt:418/692) 13-AL-27(N,A)11-NA-24,,SIG 20387003 1966 H.Liskien x:8.0 y:40.7 dy:2.1 dx:0.2
 pt:419/692) 13-AL-27(N,A)11-NA-24,,SIG 20387003 1966 H.Liskien x:8.07 y:38.7 dy:2.0 dx:0.21
 pt:420/692) 13-AL-27(N,A)11-NA-24,,SIG 20387003 1966 H.Liskien x:8.15 y:43.3 dy:2.2 dx:0.21
 pt:421/692) 13-AL-27(N,A)11-NA-24,,SIG 20387003 1966 H.Liskien x:8.2 y:43.6 dy:2.3 dx:0.22
DS:57) 13-AL-27(N,A)11-NA-24,,SIG #21372002 1966,J.D.Hemingway
 pt:422/692) 13-AL-27(N,A)11-NA-24,,SIG 21372002 1966 J.D.Hemingway x:13.5 y:118.1 dy:6.0 dx:0.1
 pt:423/692) 13-AL-27(N,A)11-NA-24,,SIG 21372002 1966 J.D.Hemingway x:14.8 y:103.6 dy:5.5 dx:0.1
DS:58) 13-AL-27(N,A)11-NA-24,,SIG #20378003 1965,A.Paulsen
 pt:424/692) 13-AL-27(N,A)11-NA-24,,SIG 20378003 1965 A.Paulsen x:12.63 y:135.0 dy:8.0 dx:0.11
 pt:425/692) 13-AL-27(N,A)11-NA-24,,SIG 20378003 1965 A.Paulsen x:12.81 y:133.0 dy:8.0 dx:0.15
 pt:426/692) 13-AL-27(N,A)11-NA-24,,SIG 20378003 1965 A.Paulsen x:12.98 y:130.0 dy:8.0 dx:0.17
 pt:427/692) 13-AL-27(N,A)11-NA-24,,SIG 20378003 1965 A.Paulsen x:13.24 y:130.0 dy:8.0 dx:0.2
 pt:428/692) 13-AL-27(N,A)11-NA-24,,SIG 20378003 1965 A.Paulsen x:13.46 y:130.0 dy:8.0 dx:0.22
 pt:429/692) 13-AL-27(N,A)11-NA-24,,SIG 20378003 1965 A.Paulsen x:13.79 y:129.0 dy:8.0 dx:0.23
 pt:430/692) 13-AL-27(N,A)11-NA-24,,SIG 20378003 1965 A.Paulsen x:14.05 y:126.0 dy:8.0 dx:0.25
 pt:431/692) 13-AL-27(N,A)11-NA-24,,SIG 20378003 1965 A.Paulsen x:14.42 y:122.0 dy:7.0 dx:0.26
 pt:432/692) 13-AL-27(N,A)11-NA-24,,SIG 20378003 1965 A.Paulsen x:14.71 y:119.0 dy:7.0 dx:0.27
 pt:433/692) 13-AL-27(N,A)11-NA-24,,SIG 20378003 1965 A.Paulsen x:15.09 y:114.0 dy:7.0 dx:0.26
 pt:434/692) 13-AL-27(N,A)11-NA-24,,SIG 20378003 1965 A.Paulsen x:15.37 y:109.0 dy:7.0 dx:0.25
 pt:435/692) 13-AL-27(N,A)11-NA-24,,SIG 20378003 1965 A.Paulsen x:15.72 y:102.0 dy:6.0 dx:0.23
 pt:436/692) 13-AL-27(N,A)11-NA-24,,SIG 20378003 1965 A.Paulsen x:15.99 y:94.9 dy:5.7 dx:0.21
 pt:437/692) 13-AL-27(N,A)11-NA-24,,SIG 20378003 1965 A.Paulsen x:16.25 y:91.6 dy:5.5 dx:0.2
 pt:438/692) 13-AL-27(N,A)11-NA-24,,SIG 20378003 1965 A.Paulsen x:16.42 y:90.8 dy:5.4 dx:0.19
 pt:439/692) 13-AL-27(N,A)11-NA-24,,SIG 20378003 1965 A.Paulsen x:16.61 y:86.6 dy:5.2 dx:0.2
 pt:440/692) 13-AL-27(N,A)11-NA-24,,SIG 20378003 1965 A.Paulsen x:17.27 y:75.5 dy:4.6 dx:0.46
 pt:441/692) 13-AL-27(N,A)11-NA-24,,SIG 20378003 1965 A.Paulsen x:17.75 y:62.1 dy:3.7 dx:0.43
 pt:442/692) 13-AL-27(N,A)11-NA-24,,SIG 20378003 1965 A.Paulsen x:18.33 y:56.2 dy:3.4 dx:0.38
 pt:443/692) 13-AL-27(N,A)11-NA-24,,SIG 20378003 1965 A.Paulsen x:18.71 y:52.9 dy:3.2 dx:0.33
 pt:444/692) 13-AL-27(N,A)11-NA-24,,SIG 20378003 1965 A.Paulsen x:19.13 y:46.7 dy:2.8 dx:0.2
 pt:445/692) 13-AL-27(N,A)11-NA-24,,SIG 20378003 1965 A.Paulsen x:19.36 y:44.4 dy:2.7 dx:0.18
 pt:446/692) 13-AL-27(N,A)11-NA-24,,SIG 20378003 1965 A.Paulsen x:19.59 y:41.8 dy:2.5 dx:0.19
DS:59) 13-AL-27(N,A)11-NA-24,,SIG #20837006 1965,U.Seebeck
 pt:447/692) 13-AL-27(N,A)11-NA-24,,SIG 20837006 1965 U.Seebeck x:14.1 y:119.0 dy:10.0 dx:0.1
DS:60) 13-AL-27(N,A)11-NA-24,,SIG #20887014 1965,M.Bormann
 pt:448/692) 13-AL-27(N,A)11-NA-24,,SIG 20887014 1965 M.Bormann x:14.8 y:120.0 dy:8.76 dx:0.6
DS:61) 13-AL-27(N,A)11-NA-24,,SIG #11526003 1964,W.L.Imhof
 pt:449/692) 13-AL-27(N,A)11-NA-24,,SIG 11526003 1964 W.L.Imhof x:12.66 y:121.6 dy:18.24 dx:None
 pt:450/692) 13-AL-27(N,A)11-NA-24,,SIG 11526003 1964 W.L.Imhof x:15.26 y:106.5 dy:15.975 dx:None
 pt:451/692) 13-AL-27(N,A)11-NA-24,,SIG 11526003 1964 W.L.Imhof x:16.96 y:78.4 dy:11.76 dx:None
 pt:452/692) 13-AL-27(N,A)11-NA-24,,SIG 11526003 1964 W.L.Imhof x:17.98 y:61.4 dy:9.21 dx:None
DS:62) 13-AL-27(N,A)11-NA-24,,SIG #14818005 1964,W.W.Wadman
 pt:453/692) 13-AL-27(N,A)11-NA-24,,SIG 14818005 1964 W.W.Wadman x:6.192 y:1.867 dy:None dx:None
 pt:454/692) 13-AL-27(N,A)11-NA-24,,SIG 14818005 1964 W.W.Wadman x:6.398 y:3.482 dy:None dx:None
 pt:455/692) 13-AL-27(N,A)11-NA-24,,SIG 14818005 1964 W.W.Wadman x:6.427 y:2.465 dy:None dx:None
 pt:456/692) 13-AL-27(N,A)11-NA-24,,SIG 14818005 1964 W.W.Wadman x:6.524 y:5.787 dy:None dx:None
 pt:457/692) 13-AL-27(N,A)11-NA-24,,SIG 14818005 1964 W.W.Wadman x:6.556 y:4.216 dy:None dx:None
 pt:458/692) 13-AL-27(N,A)11-NA-24,,SIG 14818005 1964 W.W.Wadman x:6.628 y:8.016 dy:None dx:None
 pt:459/692) 13-AL-27(N,A)11-NA-24,,SIG 14818005 1964 W.W.Wadman x:6.803 y:11.32 dy:None dx:None
 pt:460/692) 13-AL-27(N,A)11-NA-24,,SIG 14818005 1964 W.W.Wadman x:6.83 y:14.38 dy:None dx:None
 pt:461/692) 13-AL-27(N,A)11-NA-24,,SIG 14818005 1964 W.W.Wadman x:6.857 y:9.988 dy:None dx:None
 pt:462/692) 13-AL-27(N,A)11-NA-24,,SIG 14818005 1964 W.W.Wadman x:6.981 y:16.44 dy:None dx:None
 pt:463/692) 13-AL-27(N,A)11-NA-24,,SIG 14818005 1964 W.W.Wadman x:7.059 y:17.92 dy:None dx:None
 pt:464/692) 13-AL-27(N,A)11-NA-24,,SIG 14818005 1964 W.W.Wadman x:7.109 y:15.22 dy:None dx:None
 pt:465/692) 13-AL-27(N,A)11-NA-24,,SIG 14818005 1964 W.W.Wadman x:7.148 y:21.5 dy:None dx:None
 pt:466/692) 13-AL-27(N,A)11-NA-24,,SIG 14818005 1964 W.W.Wadman x:7.276 y:20.09 dy:None dx:None
 pt:467/692) 13-AL-27(N,A)11-NA-24,,SIG 14818005 1964 W.W.Wadman x:7.492 y:22.32 dy:None dx:None
 pt:468/692) 13-AL-27(N,A)11-NA-24,,SIG 14818005 1964 W.W.Wadman x:7.502 y:24.33 dy:None dx:None
 pt:469/692) 13-AL-27(N,A)11-NA-24,,SIG 14818005 1964 W.W.Wadman x:7.522 y:29.19 dy:None dx:None
 pt:470/692) 13-AL-27(N,A)11-NA-24,,SIG 14818005 1964 W.W.Wadman x:7.877 y:33.35 dy:None dx:None
 pt:471/692) 13-AL-27(N,A)11-NA-24,,SIG 14818005 1964 W.W.Wadman x:7.897 y:39.64 dy:None dx:None
 pt:472/692) 13-AL-27(N,A)11-NA-24,,SIG 14818005 1964 W.W.Wadman x:7.935 y:30.3 dy:None dx:None
 pt:473/692) 13-AL-27(N,A)11-NA-24,,SIG 14818005 1964 W.W.Wadman x:8.106 y:41.56 dy:None dx:None
 pt:474/692) 13-AL-27(N,A)11-NA-24,,SIG 14818005 1964 W.W.Wadman x:8.122 y:47.99 dy:None dx:None
 pt:475/692) 13-AL-27(N,A)11-NA-24,,SIG 14818005 1964 W.W.Wadman x:8.159 y:36.33 dy:None dx:None
 pt:476/692) 13-AL-27(N,A)11-NA-24,,SIG 14818005 1964 W.W.Wadman x:8.386 y:44.41 dy:None dx:None
 pt:477/692) 13-AL-27(N,A)11-NA-24,,SIG 14818005 1964 W.W.Wadman x:8.71 y:38.42 dy:None dx:None
 pt:478/692) 13-AL-27(N,A)11-NA-24,,SIG 14818005 1964 W.W.Wadman x:8.72 y:42.29 dy:None dx:None
 pt:479/692) 13-AL-27(N,A)11-NA-24,,SIG 14818005 1964 W.W.Wadman x:8.805 y:48.82 dy:None dx:None
 pt:480/692) 13-AL-27(N,A)11-NA-24,,SIG 14818005 1964 W.W.Wadman x:12.023 y:107.2 dy:None dx:None
 pt:481/692) 13-AL-27(N,A)11-NA-24,,SIG 14818005 1964 W.W.Wadman x:12.73 y:136.0 dy:None dx:None
 pt:482/692) 13-AL-27(N,A)11-NA-24,,SIG 14818005 1964 W.W.Wadman x:13.068 y:133.3 dy:None dx:None
 pt:483/692) 13-AL-27(N,A)11-NA-24,,SIG 14818005 1964 W.W.Wadman x:13.191 y:118.7 dy:None dx:None
 pt:484/692) 13-AL-27(N,A)11-NA-24,,SIG 14818005 1964 W.W.Wadman x:13.537 y:125.7 dy:None dx:None
 pt:485/692) 13-AL-27(N,A)11-NA-24,,SIG 14818005 1964 W.W.Wadman x:13.885 y:134.2 dy:None dx:None
 pt:486/692) 13-AL-27(N,A)11-NA-24,,SIG 14818005 1964 W.W.Wadman x:13.931 y:110.8 dy:None dx:None
 pt:487/692) 13-AL-27(N,A)11-NA-24,,SIG 14818005 1964 W.W.Wadman x:13.939 y:118.5 dy:None dx:None
 pt:488/692) 13-AL-27(N,A)11-NA-24,,SIG 14818005 1964 W.W.Wadman x:14.407 y:110.6 dy:None dx:None
 pt:489/692) 13-AL-27(N,A)11-NA-24,,SIG 14818005 1964 W.W.Wadman x:14.482 y:117.2 dy:None dx:None
 pt:490/692) 13-AL-27(N,A)11-NA-24,,SIG 14818005 1964 W.W.Wadman x:14.954 y:112.6 dy:None dx:None
DS:63) 13-AL-27(N,A)11-NA-24,,SIG #20888002 1964,C.G.Bonazzola
 pt:491/692) 13-AL-27(N,A)11-NA-24,,SIG 20888002 1964 C.G.Bonazzola x:14.7 y:112.0 dy:4.0 dx:0.3
DS:64) 13-AL-27(N,A)11-NA-24,,SIG #40686002 1964,P.M.Aron
 pt:492/692) 13-AL-27(N,A)11-NA-24,,SIG 40686002 1964 P.M.Aron x:14.6 y:106.0 dy:2.3 dx:0.15
DS:65) 13-AL-27(N,A)11-NA-24,,SIG #11457005 1963,J.P.Butler
 pt:493/692) 13-AL-27(N,A)11-NA-24,,SIG 11457005 1963 J.P.Butler x:4.88 y:0.05 dy:0.03 dx:0.16
DS:66) 13-AL-27(N,A)11-NA-24,,SIG #11457006 1963,J.P.Butler
 pt:494/692) 13-AL-27(N,A)11-NA-24,,SIG 11457006 1963 J.P.Butler x:5.45 y:0.15 dy:0.01 dx:0.2
 pt:495/692) 13-AL-27(N,A)11-NA-24,,SIG 11457006 1963 J.P.Butler x:5.7 y:0.54 dy:0.03 dx:0.16
 pt:496/692) 13-AL-27(N,A)11-NA-24,,SIG 11457006 1963 J.P.Butler x:5.94 y:1.23 dy:0.05 dx:0.16
 pt:497/692) 13-AL-27(N,A)11-NA-24,,SIG 11457006 1963 J.P.Butler x:6.22 y:3.04 dy:0.09 dx:0.14
 pt:498/692) 13-AL-27(N,A)11-NA-24,,SIG 11457006 1963 J.P.Butler x:6.53 y:6.53 dy:0.21 dx:0.14
 pt:499/692) 13-AL-27(N,A)11-NA-24,,SIG 11457006 1963 J.P.Butler x:6.7 y:9.87 dy:0.3 dx:0.14
 pt:500/692) 13-AL-27(N,A)11-NA-24,,SIG 11457006 1963 J.P.Butler x:7.01 y:16.2 dy:0.5 dx:0.13
 pt:501/692) 13-AL-27(N,A)11-NA-24,,SIG 11457006 1963 J.P.Butler x:7.2 y:19.8 dy:0.6 dx:0.13
 pt:502/692) 13-AL-27(N,A)11-NA-24,,SIG 11457006 1963 J.P.Butler x:7.5 y:25.6 dy:0.8 dx:0.12
 pt:503/692) 13-AL-27(N,A)11-NA-24,,SIG 11457006 1963 J.P.Butler x:7.8 y:39.2 dy:1.2 dx:0.12
 pt:504/692) 13-AL-27(N,A)11-NA-24,,SIG 11457006 1963 J.P.Butler x:8.01 y:45.2 dy:1.4 dx:0.11
 pt:505/692) 13-AL-27(N,A)11-NA-24,,SIG 11457006 1963 J.P.Butler x:8.1 y:45.7 dy:1.4 dx:0.11
 pt:506/692) 13-AL-27(N,A)11-NA-24,,SIG 11457006 1963 J.P.Butler x:8.27 y:46.0 dy:1.4 dx:0.11
 pt:507/692) 13-AL-27(N,A)11-NA-24,,SIG 11457006 1963 J.P.Butler x:8.4 y:52.9 dy:1.6 dx:0.11
 pt:508/692) 13-AL-27(N,A)11-NA-24,,SIG 11457006 1963 J.P.Butler x:8.61 y:64.3 dy:1.9 dx:0.11
 pt:509/692) 13-AL-27(N,A)11-NA-24,,SIG 11457006 1963 J.P.Butler x:8.81 y:66.8 dy:2.0 dx:0.11
 pt:510/692) 13-AL-27(N,A)11-NA-24,,SIG 11457006 1963 J.P.Butler x:9.02 y:74.4 dy:2.2 dx:0.11
 pt:511/692) 13-AL-27(N,A)11-NA-24,,SIG 11457006 1963 J.P.Butler x:9.3 y:79.1 dy:2.5 dx:0.11
 pt:512/692) 13-AL-27(N,A)11-NA-24,,SIG 11457006 1963 J.P.Butler x:9.63 y:86.3 dy:2.7 dx:0.11
 pt:513/692) 13-AL-27(N,A)11-NA-24,,SIG 11457006 1963 J.P.Butler x:9.88 y:88.3 dy:2.8 dx:0.11
 pt:514/692) 13-AL-27(N,A)11-NA-24,,SIG 11457006 1963 J.P.Butler x:10.03 y:91.0 dy:2.9 dx:0.11
 pt:515/692) 13-AL-27(N,A)11-NA-24,,SIG 11457006 1963 J.P.Butler x:10.13 y:90.5 dy:3.0 dx:0.11
 pt:516/692) 13-AL-27(N,A)11-NA-24,,SIG 11457006 1963 J.P.Butler x:10.4 y:97.4 dy:3.2 dx:0.11
 pt:517/692) 13-AL-27(N,A)11-NA-24,,SIG 11457006 1963 J.P.Butler x:10.62 y:104.0 dy:3.0 dx:0.11
 pt:518/692) 13-AL-27(N,A)11-NA-24,,SIG 11457006 1963 J.P.Butler x:10.81 y:102.0 dy:3.0 dx:0.11
 pt:519/692) 13-AL-27(N,A)11-NA-24,,SIG 11457006 1963 J.P.Butler x:11.0 y:111.0 dy:4.0 dx:0.11
 pt:520/692) 13-AL-27(N,A)11-NA-24,,SIG 11457006 1963 J.P.Butler x:11.22 y:108.0 dy:4.0 dx:0.11
 pt:521/692) 13-AL-27(N,A)11-NA-24,,SIG 11457006 1963 J.P.Butler x:11.61 y:118.0 dy:4.0 dx:0.11
 pt:522/692) 13-AL-27(N,A)11-NA-24,,SIG 11457006 1963 J.P.Butler x:12.1 y:112.0 dy:5.0 dx:0.11
 pt:523/692) 13-AL-27(N,A)11-NA-24,,SIG 11457006 1963 J.P.Butler x:12.59 y:119.0 dy:6.0 dx:0.12
 pt:524/692) 13-AL-27(N,A)11-NA-24,,SIG 11457006 1963 J.P.Butler x:13.08 y:116.0 dy:7.0 dx:0.12
 pt:525/692) 13-AL-27(N,A)11-NA-24,,SIG 11457006 1963 J.P.Butler x:13.58 y:123.0 dy:9.0 dx:0.12
DS:67) 13-AL-27(N,A)11-NA-24,,SIG #11457007 1963,J.P.Butler
 pt:526/692) 13-AL-27(N,A)11-NA-24,,SIG 11457007 1963 J.P.Butler x:12.53 y:121.0 dy:6.0 dx:0.26
 pt:527/692) 13-AL-27(N,A)11-NA-24,,SIG 11457007 1963 J.P.Butler x:13.58 y:127.0 dy:5.0 dx:0.06
 pt:528/692) 13-AL-27(N,A)11-NA-24,,SIG 11457007 1963 J.P.Butler x:13.89 y:123.0 dy:5.0 dx:0.08
 pt:529/692) 13-AL-27(N,A)11-NA-24,,SIG 11457007 1963 J.P.Butler x:14.24 y:118.0 dy:5.0 dx:0.08
 pt:530/692) 13-AL-27(N,A)11-NA-24,,SIG 11457007 1963 J.P.Butler x:14.5 y:116.0 dy:4.0 dx:0.06
 pt:531/692) 13-AL-27(N,A)11-NA-24,,SIG 11457007 1963 J.P.Butler x:14.68 y:115.0 dy:5.0 dx:0.06
 pt:532/692) 13-AL-27(N,A)11-NA-24,,SIG 11457007 1963 J.P.Butler x:14.76 y:112.0 dy:5.0 dx:0.06
 pt:533/692) 13-AL-27(N,A)11-NA-24,,SIG 11457007 1963 J.P.Butler x:16.6 y:80.7 dy:4.0 dx:0.6
 pt:534/692) 13-AL-27(N,A)11-NA-24,,SIG 11457007 1963 J.P.Butler x:17.3 y:71.7 dy:4.0 dx:1.0
 pt:535/692) 13-AL-27(N,A)11-NA-24,,SIG 11457007 1963 J.P.Butler x:18.5 y:55.2 dy:3.0 dx:0.5
 pt:536/692) 13-AL-27(N,A)11-NA-24,,SIG 11457007 1963 J.P.Butler x:19.2 y:48.7 dy:2.4 dx:0.8
 pt:537/692) 13-AL-27(N,A)11-NA-24,,SIG 11457007 1963 J.P.Butler x:19.8 y:40.0 dy:2.4 dx:0.3
 pt:538/692) 13-AL-27(N,A)11-NA-24,,SIG 11457007 1963 J.P.Butler x:20.3 y:33.9 dy:2.0 dx:0.3
DS:68) 13-AL-27(N,A)11-NA-24,,SIG #20922002 1963,J.M.F.Jeronymo
 pt:539/692) 13-AL-27(N,A)11-NA-24,,SIG 20922002 1963 J.M.F.Jeronymo x:12.55 y:115.0 dy:12.0 dx:0.2
 pt:540/692) 13-AL-27(N,A)11-NA-24,,SIG 20922002 1963 J.M.F.Jeronymo x:13.55 y:115.0 dy:12.0 dx:0.2
 pt:541/692) 13-AL-27(N,A)11-NA-24,,SIG 20922002 1963 J.M.F.Jeronymo x:14.9 y:107.0 dy:11.0 dx:0.2
 pt:542/692) 13-AL-27(N,A)11-NA-24,,SIG 20922002 1963 J.M.F.Jeronymo x:16.5 y:84.0 dy:9.0 dx:0.2
 pt:543/692) 13-AL-27(N,A)11-NA-24,,SIG 20922002 1963 J.M.F.Jeronymo x:18.15 y:64.0 dy:7.0 dx:0.2
 pt:544/692) 13-AL-27(N,A)11-NA-24,,SIG 20922002 1963 J.M.F.Jeronymo x:19.6 y:52.0 dy:7.0 dx:0.2
 pt:545/692) 13-AL-27(N,A)11-NA-24,,SIG 20922002 1963 J.M.F.Jeronymo x:20.6 y:37.0 dy:6.0 dx:0.2
 pt:546/692) 13-AL-27(N,A)11-NA-24,,SIG 20922002 1963 J.M.F.Jeronymo x:21.0 y:31.0 dy:6.0 dx:0.2
DS:69) 13-AL-27(N,A)11-NA-24,,SIG #30118007 1963,J.Csikai
 pt:547/692) 13-AL-27(N,A)11-NA-24,,SIG 30118007 1963 J.Csikai x:14.6 y:118.0 dy:None dx:None
DS:70) 13-AL-27(N,A)11-NA-24,,SIG #11494003 1962,F.Gabbard
 pt:548/692) 13-AL-27(N,A)11-NA-24,,SIG 11494003 1962 F.Gabbard x:12.45 y:145.0 dy:5.0 dx:None
 pt:549/692) 13-AL-27(N,A)11-NA-24,,SIG 11494003 1962 F.Gabbard x:12.6 y:140.0 dy:10.0 dx:None
 pt:550/692) 13-AL-27(N,A)11-NA-24,,SIG 11494003 1962 F.Gabbard x:12.75 y:137.0 dy:5.0 dx:None
 pt:551/692) 13-AL-27(N,A)11-NA-24,,SIG 11494003 1962 F.Gabbard x:13.05 y:128.0 dy:5.0 dx:None
 pt:552/692) 13-AL-27(N,A)11-NA-24,,SIG 11494003 1962 F.Gabbard x:13.15 y:120.0 dy:5.0 dx:None
 pt:553/692) 13-AL-27(N,A)11-NA-24,,SIG 11494003 1962 F.Gabbard x:13.5 y:135.0 dy:8.0 dx:None
 pt:554/692) 13-AL-27(N,A)11-NA-24,,SIG 11494003 1962 F.Gabbard x:13.7 y:120.0 dy:10.0 dx:None
 pt:555/692) 13-AL-27(N,A)11-NA-24,,SIG 11494003 1962 F.Gabbard x:14.0 y:123.0 dy:7.0 dx:None
 pt:556/692) 13-AL-27(N,A)11-NA-24,,SIG 11494003 1962 F.Gabbard x:14.3 y:115.0 dy:5.0 dx:None
 pt:557/692) 13-AL-27(N,A)11-NA-24,,SIG 11494003 1962 F.Gabbard x:14.45 y:120.0 dy:5.0 dx:None
 pt:558/692) 13-AL-27(N,A)11-NA-24,,SIG 11494003 1962 F.Gabbard x:14.6 y:115.0 dy:5.0 dx:None
 pt:559/692) 13-AL-27(N,A)11-NA-24,,SIG 11494003 1962 F.Gabbard x:15.4 y:105.0 dy:5.0 dx:None
 pt:560/692) 13-AL-27(N,A)11-NA-24,,SIG 11494003 1962 F.Gabbard x:15.9 y:97.0 dy:5.0 dx:None
 pt:561/692) 13-AL-27(N,A)11-NA-24,,SIG 11494003 1962 F.Gabbard x:16.3 y:90.0 dy:5.0 dx:None
 pt:562/692) 13-AL-27(N,A)11-NA-24,,SIG 11494003 1962 F.Gabbard x:16.45 y:85.0 dy:5.0 dx:None
 pt:563/692) 13-AL-27(N,A)11-NA-24,,SIG 11494003 1962 F.Gabbard x:16.55 y:90.0 dy:5.0 dx:None
 pt:564/692) 13-AL-27(N,A)11-NA-24,,SIG 11494003 1962 F.Gabbard x:16.8 y:82.0 dy:6.0 dx:None
 pt:565/692) 13-AL-27(N,A)11-NA-24,,SIG 11494003 1962 F.Gabbard x:17.3 y:70.0 dy:5.0 dx:None
 pt:566/692) 13-AL-27(N,A)11-NA-24,,SIG 11494003 1962 F.Gabbard x:17.7 y:70.0 dy:5.0 dx:None
DS:71) 13-AL-27(N,A)11-NA-24,,SIG #20903002 1962,Langmann
 pt:567/692) 13-AL-27(N,A)11-NA-24,,SIG 20903002 1962 Langmann x:14.1 y:109.0 dy:15.26 dx:0.1
DS:72) 13-AL-27(N,A)11-NA-24,,SIG #30008029 1962,P.Strohal
 pt:568/692) 13-AL-27(N,A)11-NA-24,,SIG 30008029 1962 P.Strohal x:14.6 y:115.0 dy:2.0 dx:0.3
DS:73) 13-AL-27(N,A)11-NA-24,,SIG #11462002 1961,B.P.Bayhurst
 pt:569/692) 13-AL-27(N,A)11-NA-24,,SIG 11462002 1961 B.P.Bayhurst x:7.0 y:15.2 dy:1.1 dx:0.25
 pt:570/692) 13-AL-27(N,A)11-NA-24,,SIG 11462002 1961 B.P.Bayhurst x:12.13 y:113.5 dy:7.9 dx:0.15
 pt:571/692) 13-AL-27(N,A)11-NA-24,,SIG 11462002 1961 B.P.Bayhurst x:13.4 y:127.4 dy:6.4 dx:0.2
 pt:572/692) 13-AL-27(N,A)11-NA-24,,SIG 11462002 1961 B.P.Bayhurst x:13.52 y:130.6 dy:6.5 dx:0.15
 pt:573/692) 13-AL-27(N,A)11-NA-24,,SIG 11462002 1961 B.P.Bayhurst x:13.69 y:131.1 dy:6.6 dx:0.1
 pt:574/692) 13-AL-27(N,A)11-NA-24,,SIG 11462002 1961 B.P.Bayhurst x:13.88 y:128.5 dy:6.4 dx:0.1
 pt:575/692) 13-AL-27(N,A)11-NA-24,,SIG 11462002 1961 B.P.Bayhurst x:14.09 y:128.3 dy:6.4 dx:0.1
 pt:576/692) 13-AL-27(N,A)11-NA-24,,SIG 11462002 1961 B.P.Bayhurst x:14.31 y:123.6 dy:6.2 dx:0.13
 pt:577/692) 13-AL-27(N,A)11-NA-24,,SIG 11462002 1961 B.P.Bayhurst x:14.5 y:119.8 dy:6.0 dx:0.2
 pt:578/692) 13-AL-27(N,A)11-NA-24,,SIG 11462002 1961 B.P.Bayhurst x:14.68 y:119.5 dy:6.0 dx:0.26
 pt:579/692) 13-AL-27(N,A)11-NA-24,,SIG 11462002 1961 B.P.Bayhurst x:14.81 y:114.7 dy:5.7 dx:0.31
 pt:580/692) 13-AL-27(N,A)11-NA-24,,SIG 11462002 1961 B.P.Bayhurst x:14.93 y:112.9 dy:5.6 dx:0.36
 pt:581/692) 13-AL-27(N,A)11-NA-24,,SIG 11462002 1961 B.P.Bayhurst x:16.5 y:76.8 dy:5.4 dx:0.3
 pt:582/692) 13-AL-27(N,A)11-NA-24,,SIG 11462002 1961 B.P.Bayhurst x:17.95 y:46.7 dy:3.3 dx:0.32
 pt:583/692) 13-AL-27(N,A)11-NA-24,,SIG 11462002 1961 B.P.Bayhurst x:19.76 y:38.0 dy:2.7 dx:0.43
DS:74) 13-AL-27(N,A)11-NA-24,,SIG #11530002 1961,H.W.Schmitt
 pt:584/692) 13-AL-27(N,A)11-NA-24,,SIG 11530002 1961 H.W.Schmitt x:6.12 y:1.65 dy:0.1155 dx:None
 pt:585/692) 13-AL-27(N,A)11-NA-24,,SIG 11530002 1961 H.W.Schmitt x:6.26 y:3.4 dy:0.238 dx:0.09
 pt:586/692) 13-AL-27(N,A)11-NA-24,,SIG 11530002 1961 H.W.Schmitt x:6.46 y:5.0 dy:0.531507 dx:None
 pt:587/692) 13-AL-27(N,A)11-NA-24,,SIG 11530002 1961 H.W.Schmitt x:6.56 y:7.0 dy:0.774661 dx:None
 pt:588/692) 13-AL-27(N,A)11-NA-24,,SIG 11530002 1961 H.W.Schmitt x:6.61 y:8.4 dy:0.840086 dx:None
 pt:589/692) 13-AL-27(N,A)11-NA-24,,SIG 11530002 1961 H.W.Schmitt x:6.659 y:9.4 dy:0.890485 dx:None
 pt:590/692) 13-AL-27(N,A)11-NA-24,,SIG 11530002 1961 H.W.Schmitt x:6.705 y:8.3 dy:0.871815 dx:None
 pt:591/692) 13-AL-27(N,A)11-NA-24,,SIG 11530002 1961 H.W.Schmitt x:6.76 y:8.6 dy:0.849944 dx:None
 pt:592/692) 13-AL-27(N,A)11-NA-24,,SIG 11530002 1961 H.W.Schmitt x:6.81 y:13.5 dy:1.14696 dx:None
 pt:593/692) 13-AL-27(N,A)11-NA-24,,SIG 11530002 1961 H.W.Schmitt x:6.842 y:11.0 dy:0.976166 dx:None
 pt:594/692) 13-AL-27(N,A)11-NA-24,,SIG 11530002 1961 H.W.Schmitt x:6.86 y:12.4 dy:1.05519 dx:None
 pt:595/692) 13-AL-27(N,A)11-NA-24,,SIG 11530002 1961 H.W.Schmitt x:6.97 y:16.9 dy:1.48643 dx:None
 pt:596/692) 13-AL-27(N,A)11-NA-24,,SIG 11530002 1961 H.W.Schmitt x:7.03 y:17.4 dy:1.51444 dx:0.07
 pt:597/692) 13-AL-27(N,A)11-NA-24,,SIG 11530002 1961 H.W.Schmitt x:7.07 y:18.9 dy:1.6001 dx:None
 pt:598/692) 13-AL-27(N,A)11-NA-24,,SIG 11530002 1961 H.W.Schmitt x:7.1 y:19.1 dy:1.6117 dx:None
 pt:599/692) 13-AL-27(N,A)11-NA-24,,SIG 11530002 1961 H.W.Schmitt x:7.125 y:20.0 dy:1.72047 dx:None
 pt:600/692) 13-AL-27(N,A)11-NA-24,,SIG 11530002 1961 H.W.Schmitt x:7.175 y:20.8 dy:1.76633 dx:None
 pt:601/692) 13-AL-27(N,A)11-NA-24,,SIG 11530002 1961 H.W.Schmitt x:7.22 y:21.5 dy:1.80694 dx:None
 pt:602/692) 13-AL-27(N,A)11-NA-24,,SIG 11530002 1961 H.W.Schmitt x:7.235 y:23.5 dy:2.03618 dx:None
 pt:603/692) 13-AL-27(N,A)11-NA-24,,SIG 11530002 1961 H.W.Schmitt x:7.242 y:24.5 dy:2.09314 dx:None
 pt:604/692) 13-AL-27(N,A)11-NA-24,,SIG 11530002 1961 H.W.Schmitt x:7.285 y:23.6 dy:2.04184 dx:None
 pt:605/692) 13-AL-27(N,A)11-NA-24,,SIG 11530002 1961 H.W.Schmitt x:7.335 y:21.7 dy:1.87546 dx:None
 pt:606/692) 13-AL-27(N,A)11-NA-24,,SIG 11530002 1961 H.W.Schmitt x:7.395 y:21.1 dy:1.84161 dx:None
 pt:607/692) 13-AL-27(N,A)11-NA-24,,SIG 11530002 1961 H.W.Schmitt x:7.405 y:21.4 dy:1.8585 dx:None
 pt:608/692) 13-AL-27(N,A)11-NA-24,,SIG 11530002 1961 H.W.Schmitt x:7.445 y:23.6 dy:2.04184 dx:None
 pt:609/692) 13-AL-27(N,A)11-NA-24,,SIG 11530002 1961 H.W.Schmitt x:7.495 y:24.9 dy:2.11614 dx:None
 pt:610/692) 13-AL-27(N,A)11-NA-24,,SIG 11530002 1961 H.W.Schmitt x:7.555 y:29.1 dy:2.5297 dx:None
 pt:611/692) 13-AL-27(N,A)11-NA-24,,SIG 11530002 1961 H.W.Schmitt x:7.565 y:29.3 dy:2.54098 dx:None
 pt:612/692) 13-AL-27(N,A)11-NA-24,,SIG 11530002 1961 H.W.Schmitt x:7.66 y:34.0 dy:2.92479 dx:None
 pt:613/692) 13-AL-27(N,A)11-NA-24,,SIG 11530002 1961 H.W.Schmitt x:7.73 y:33.8 dy:2.91341 dx:0.06
 pt:614/692) 13-AL-27(N,A)11-NA-24,,SIG 11530002 1961 H.W.Schmitt x:7.775 y:31.3 dy:2.71302 dx:None
 pt:615/692) 13-AL-27(N,A)11-NA-24,,SIG 11530002 1961 H.W.Schmitt x:7.88 y:34.5 dy:2.95334 dx:None
 pt:616/692) 13-AL-27(N,A)11-NA-24,,SIG 11530002 1961 H.W.Schmitt x:7.895 y:35.2 dy:3.05144 dx:None
 pt:617/692) 13-AL-27(N,A)11-NA-24,,SIG 11530002 1961 H.W.Schmitt x:7.925 y:33.0 dy:3.47794 dx:None
 pt:618/692) 13-AL-27(N,A)11-NA-24,,SIG 11530002 1961 H.W.Schmitt x:8.055 y:47.5 dy:4.28318 dx:None
 pt:619/692) 13-AL-27(N,A)11-NA-24,,SIG 11530002 1961 H.W.Schmitt x:8.15 y:41.9 dy:3.78979 dx:None
 pt:620/692) 13-AL-27(N,A)11-NA-24,,SIG 11530002 1961 H.W.Schmitt x:8.225 y:42.7 dy:3.89668 dx:None
 pt:621/692) 13-AL-27(N,A)11-NA-24,,SIG 11530002 1961 H.W.Schmitt x:8.3 y:45.5 dy:3.92864 dx:0.06
DS:75) 13-AL-27(N,A)11-NA-24,,SIG #115300032 1961,H.W.Schmitt
 pt:622/692) 13-AL-27(N,A)11-NA-24,,SIG 115300032 1961 H.W.Schmitt x:14.76 y:117.0 dy:8.0 dx:None
DS:76) 13-AL-27(N,A)11-NA-24,,SIG #20904002 1961,M.Bormann
 pt:623/692) 13-AL-27(N,A)11-NA-24,,SIG 20904002 1961 M.Bormann x:12.6 y:100.0 dy:8.0 dx:0.3
 pt:624/692) 13-AL-27(N,A)11-NA-24,,SIG 20904002 1961 M.Bormann x:14.1 y:118.0 dy:9.44 dx:0.4
 pt:625/692) 13-AL-27(N,A)11-NA-24,,SIG 20904002 1961 M.Bormann x:16.0 y:90.4 dy:7.232 dx:0.4
 pt:626/692) 13-AL-27(N,A)11-NA-24,,SIG 20904002 1961 M.Bormann x:18.0 y:64.0 dy:5.76 dx:0.4
 pt:627/692) 13-AL-27(N,A)11-NA-24,,SIG 20904002 1961 M.Bormann x:19.6 y:43.5 dy:4.35 dx:0.3
DS:77) 13-AL-27(N,A)11-NA-24,,SIG #11504003 1960,H.A.Tewes
 pt:628/692) 13-AL-27(N,A)11-NA-24,,SIG 11504003 1960 H.A.Tewes x:8.4 y:36.0 dy:7.2 dx:0.2
 pt:629/692) 13-AL-27(N,A)11-NA-24,,SIG 11504003 1960 H.A.Tewes x:9.1 y:51.0 dy:10.2 dx:0.2
 pt:630/692) 13-AL-27(N,A)11-NA-24,,SIG 11504003 1960 H.A.Tewes x:9.35 y:61.0 dy:12.2 dx:0.2
 pt:631/692) 13-AL-27(N,A)11-NA-24,,SIG 11504003 1960 H.A.Tewes x:9.8 y:61.0 dy:12.2 dx:0.2
 pt:632/692) 13-AL-27(N,A)11-NA-24,,SIG 11504003 1960 H.A.Tewes x:10.35 y:71.0 dy:14.2 dx:0.2
 pt:633/692) 13-AL-27(N,A)11-NA-24,,SIG 11504003 1960 H.A.Tewes x:11.0 y:74.0 dy:14.8 dx:0.2
 pt:634/692) 13-AL-27(N,A)11-NA-24,,SIG 11504003 1960 H.A.Tewes x:11.5 y:80.0 dy:16.0 dx:0.2
 pt:635/692) 13-AL-27(N,A)11-NA-24,,SIG 11504003 1960 H.A.Tewes x:11.8 y:89.0 dy:17.8 dx:0.2
 pt:636/692) 13-AL-27(N,A)11-NA-24,,SIG 11504003 1960 H.A.Tewes x:12.3 y:83.0 dy:16.6 dx:0.2
 pt:637/692) 13-AL-27(N,A)11-NA-24,,SIG 11504003 1960 H.A.Tewes x:12.8 y:93.0 dy:18.6 dx:0.2
 pt:638/692) 13-AL-27(N,A)11-NA-24,,SIG 11504003 1960 H.A.Tewes x:13.0 y:91.0 dy:18.2 dx:0.2
 pt:639/692) 13-AL-27(N,A)11-NA-24,,SIG 11504003 1960 H.A.Tewes x:13.8 y:95.0 dy:19.0 dx:0.2
 pt:640/692) 13-AL-27(N,A)11-NA-24,,SIG 11504003 1960 H.A.Tewes x:14.0 y:88.0 dy:17.6 dx:0.2
 pt:641/692) 13-AL-27(N,A)11-NA-24,,SIG 11504003 1960 H.A.Tewes x:14.5 y:107.0 dy:21.4 dx:0.2
 pt:642/692) 13-AL-27(N,A)11-NA-24,,SIG 11504003 1960 H.A.Tewes x:15.1 y:93.0 dy:18.6 dx:0.2
DS:78) 13-AL-27(N,A)11-NA-24,,SIG #20921003 1960,G.S.Mani
 pt:643/692) 13-AL-27(N,A)11-NA-24,,SIG 20921003 1960 G.S.Mani x:11.92 y:108.0 dy:7.5 dx:None
 pt:644/692) 13-AL-27(N,A)11-NA-24,,SIG 20921003 1960 G.S.Mani x:12.13 y:118.5 dy:4.0 dx:None
 pt:645/692) 13-AL-27(N,A)11-NA-24,,SIG 20921003 1960 G.S.Mani x:12.33 y:121.0 dy:3.5 dx:None
 pt:646/692) 13-AL-27(N,A)11-NA-24,,SIG 20921003 1960 G.S.Mani x:12.55 y:113.0 dy:6.0 dx:None
 pt:647/692) 13-AL-27(N,A)11-NA-24,,SIG 20921003 1960 G.S.Mani x:12.63 y:134.5 dy:3.0 dx:None
 pt:648/692) 13-AL-27(N,A)11-NA-24,,SIG 20921003 1960 G.S.Mani x:13.05 y:127.0 dy:4.0 dx:None
 pt:649/692) 13-AL-27(N,A)11-NA-24,,SIG 20921003 1960 G.S.Mani x:13.56 y:128.0 dy:4.0 dx:None
 pt:650/692) 13-AL-27(N,A)11-NA-24,,SIG 20921003 1960 G.S.Mani x:13.82 y:123.0 dy:5.0 dx:None
 pt:651/692) 13-AL-27(N,A)11-NA-24,,SIG 20921003 1960 G.S.Mani x:14.16 y:117.5 dy:5.0 dx:None
 pt:652/692) 13-AL-27(N,A)11-NA-24,,SIG 20921003 1960 G.S.Mani x:14.66 y:111.0 dy:2.0 dx:None
 pt:653/692) 13-AL-27(N,A)11-NA-24,,SIG 20921003 1960 G.S.Mani x:14.75 y:111.0 dy:3.0 dx:None
 pt:654/692) 13-AL-27(N,A)11-NA-24,,SIG 20921003 1960 G.S.Mani x:15.61 y:96.5 dy:4.0 dx:None
 pt:655/692) 13-AL-27(N,A)11-NA-24,,SIG 20921003 1960 G.S.Mani x:16.2 y:97.5 dy:3.0 dx:None
 pt:656/692) 13-AL-27(N,A)11-NA-24,,SIG 20921003 1960 G.S.Mani x:16.63 y:115.5 dy:7.5 dx:None
 pt:657/692) 13-AL-27(N,A)11-NA-24,,SIG 20921003 1960 G.S.Mani x:16.84 y:89.0 dy:4.0 dx:None
 pt:658/692) 13-AL-27(N,A)11-NA-24,,SIG 20921003 1960 G.S.Mani x:17.45 y:72.0 dy:2.5 dx:None
 pt:659/692) 13-AL-27(N,A)11-NA-24,,SIG 20921003 1960 G.S.Mani x:17.66 y:76.0 dy:9.0 dx:None
 pt:660/692) 13-AL-27(N,A)11-NA-24,,SIG 20921003 1960 G.S.Mani x:17.83 y:72.0 dy:3.0 dx:None
 pt:661/692) 13-AL-27(N,A)11-NA-24,,SIG 20921003 1960 G.S.Mani x:18.13 y:65.7 dy:3.0 dx:None
 pt:662/692) 13-AL-27(N,A)11-NA-24,,SIG 20921003 1960 G.S.Mani x:18.3 y:61.5 dy:5.0 dx:None
 pt:663/692) 13-AL-27(N,A)11-NA-24,,SIG 20921003 1960 G.S.Mani x:19.48 y:50.0 dy:6.5 dx:None
 pt:664/692) 13-AL-27(N,A)11-NA-24,,SIG 20921003 1960 G.S.Mani x:20.15 y:45.5 dy:5.0 dx:None
 pt:665/692) 13-AL-27(N,A)11-NA-24,,SIG 20921003 1960 G.S.Mani x:20.57 y:38.0 dy:4.0 dx:None
 pt:666/692) 13-AL-27(N,A)11-NA-24,,SIG 20921003 1960 G.S.Mani x:20.72 y:39.0 dy:1.0 dx:None
DS:79) 13-AL-27(N,A)11-NA-24,,SIG #21419004 1960,M.J.Depraz
 pt:667/692) 13-AL-27(N,A)11-NA-24,,SIG 21419004 1960 M.J.Depraz x:15.0 y:116.0 dy:9.0 dx:0.4
DS:80) 13-AL-27(N,A)11-NA-24,,SIG #11464003 1959,B.D.Kern
 pt:668/692) 13-AL-27(N,A)11-NA-24,,SIG 11464003 1959 B.D.Kern x:13.03 y:141.4 dy:17.0 dx:0.2
 pt:669/692) 13-AL-27(N,A)11-NA-24,,SIG 11464003 1959 B.D.Kern x:13.38 y:135.5 dy:16.0 dx:None
 pt:670/692) 13-AL-27(N,A)11-NA-24,,SIG 11464003 1959 B.D.Kern x:13.84 y:129.9 dy:15.0 dx:0.03
 pt:671/692) 13-AL-27(N,A)11-NA-24,,SIG 11464003 1959 B.D.Kern x:14.28 y:113.9 dy:15.0 dx:None
 pt:672/692) 13-AL-27(N,A)11-NA-24,,SIG 11464003 1959 B.D.Kern x:14.74 y:113.1 dy:14.0 dx:None
 pt:673/692) 13-AL-27(N,A)11-NA-24,,SIG 11464003 1959 B.D.Kern x:14.74 y:120.6 dy:15.0 dx:None
 pt:674/692) 13-AL-27(N,A)11-NA-24,,SIG 11464003 1959 B.D.Kern x:15.06 y:114.6 dy:15.0 dx:None
 pt:675/692) 13-AL-27(N,A)11-NA-24,,SIG 11464003 1959 B.D.Kern x:15.44 y:111.2 dy:15.0 dx:None
 pt:676/692) 13-AL-27(N,A)11-NA-24,,SIG 11464003 1959 B.D.Kern x:15.44 y:113.8 dy:14.0 dx:None
 pt:677/692) 13-AL-27(N,A)11-NA-24,,SIG 11464003 1959 B.D.Kern x:15.51 y:101.5 dy:13.0 dx:None
 pt:678/692) 13-AL-27(N,A)11-NA-24,,SIG 11464003 1959 B.D.Kern x:15.51 y:98.29 dy:13.0 dx:None
 pt:679/692) 13-AL-27(N,A)11-NA-24,,SIG 11464003 1959 B.D.Kern x:15.66 y:106.8 dy:13.0 dx:0.4
DS:81) 13-AL-27(N,A)11-NA-24,,SIG #11484002 1959,A.Poularikas
 pt:680/692) 13-AL-27(N,A)11-NA-24,,SIG 11484002 1959 A.Poularikas x:14.8 y:114.0 dy:7.0 dx:0.9
DS:82) 13-AL-27(N,A)11-NA-24,,SIG #30403002 1959,C.S.Khurana
 pt:681/692) 13-AL-27(N,A)11-NA-24,,SIG 30403002 1959 C.S.Khurana x:14.0 y:111.0 dy:17.5506 dx:None
DS:83) 13-AL-27(N,A)11-NA-24,,SIG #11481002 1958,J.A.Grundl
 pt:682/692) 13-AL-27(N,A)11-NA-24,,SIG 11481002 1958 J.A.Grundl x:6.73 y:11.3 dy:1.5 dx:0.6
 pt:683/692) 13-AL-27(N,A)11-NA-24,,SIG 11481002 1958 J.A.Grundl x:7.45 y:25.5 dy:4.02244 dx:0.4
 pt:684/692) 13-AL-27(N,A)11-NA-24,,SIG 11481002 1958 J.A.Grundl x:8.09 y:37.6 dy:5.64358 dx:0.25
 pt:685/692) 13-AL-27(N,A)11-NA-24,,SIG 11481002 1958 J.A.Grundl x:8.58 y:39.7 dy:6.94622 dx:0.14
 pt:686/692) 13-AL-27(N,A)11-NA-24,,SIG 11481002 1958 J.A.Grundl x:8.9 y:48.1 dy:5.81808 dx:0.08
 pt:687/692) 13-AL-27(N,A)11-NA-24,,SIG 11481002 1958 J.A.Grundl x:9.01 y:51.3 dy:4.83839 dx:0.04
 pt:688/692) 13-AL-27(N,A)11-NA-24,,SIG 11481002 1958 J.A.Grundl x:14.1 y:116.0 dy:9.31504 dx:0.04
DS:84) 13-AL-27(N,A)11-NA-24,,SIG #20283002 1958,I.Kumabe
 pt:689/692) 13-AL-27(N,A)11-NA-24,,SIG 20283002 1958 I.Kumabe x:14.8 y:82.0 dy:17.0 dx:0.07
DS:85) 13-AL-27(N,A)11-NA-24,,SIG #20280003 1957,S.Yasumi
 pt:690/692) 13-AL-27(N,A)11-NA-24,,SIG 20280003 1957 S.Yasumi x:14.1 y:120.0 dy:14.4 dx:0.2
DS:86) 13-AL-27(N,A)11-NA-24,,SIG #11274009 1953,E.B.Paul
 pt:691/692) 13-AL-27(N,A)11-NA-24,,SIG 11274009 1953 E.B.Paul x:14.5 y:78.9 dy:15.78 dx:None
DS:87) 13-AL-27(N,A)11-NA-24,,SIG #11474002 1952,S.G.Forbes
 pt:692/692) 13-AL-27(N,A)11-NA-24,,SIG 11474002 1952 S.G.Forbes x:14.1 y:135.0 dy:9.45 dx:None
datasets: 87

Datasets: 87
1) 13-AL-27(N,A)11-NA-24,,SIG
Reaction codes: 1 

Plot:1/87) #31842017 2022, J.Jarosik pt:3
Plot:2/87) #31834002 2020, D.Kral pt:1
Plot:3/87) #33025010 2009, B.Lalremruata pt:1
Plot:4/87) #22976004 2007, W.Mannhart pt:28
Plot:5/87) #22497003 2000, R.Coszach pt:4
Plot:6/87) #31528009 1997, Hongyu Zhou pt:1
Plot:7/87) #23279006 1996, Y.Uno pt:6
Plot:8/87) #22312002 1993, Y.Ikeda pt:8
Plot:9/87) #30993002 1993, Bao Zongyu pt:1
Plot:10/87) #22703002 1992, Y.Uwamino pt:36
Plot:11/87) #31459008 1992, I.Garlea pt:1
Plot:12/87) #22209002 1991, Y.Ikeda pt:3
Plot:13/87) #22209009 1991, Y.Ikeda pt:4
Plot:14/87) #131710032 1989, L.P.Geraldo pt:10
Plot:15/87) #30523002 1989, Lu Han-Lin pt:1
Plot:16/87) #30523003 1989, Lu Han-Lin pt:10
Plot:17/87) #410480022 1989, N.V.Kornilov pt:23
Plot:18/87) #410480032 1989, N.V.Kornilov pt:19
Plot:19/87) #410480042 1989, N.V.Kornilov pt:19
Plot:20/87) #41051002 1989, N.N.Moiseev pt:1
Plot:21/87) #41051003 1989, N.N.Moiseev pt:1
Plot:22/87) #41051004 1989, N.N.Moiseev pt:1
Plot:23/87) #12969003 1987, J.W.Meadows pt:1
Plot:24/87) #12977002 1987, L.R.Greenwood pt:5
Plot:25/87) #30755002 1987, Zhou Muyao pt:1
Plot:26/87) #30821002 1986, T.Chimoye pt:5
Plot:27/87) #30933002 1986, J.Csikai pt:12
Plot:28/87) #22012003 1985, W.Enz pt:9
Plot:29/87) #21923002 1984, K.Kudo pt:8
Plot:30/87) #30813002 1984, I.Garlea pt:1
Plot:31/87) #21941006 1983, S.Firkin pt:5
Plot:32/87) #30640002 1982, J.Csikai pt:5
Plot:33/87) #12912003 1981, P.Welch pt:2
Plot:34/87) #21756003 1981, H.Friedmann pt:20
Plot:35/87) #21756004 1981, H.Friedmann pt:20
Plot:36/87) #20986003 1979, M.T.Swinhoe pt:3
Plot:37/87) #20986009 1979, M.T.Swinhoe pt:1
Plot:38/87) #20842003 1978, P.Andersson pt:1
Plot:39/87) #20843009 1978, C.Nordborg pt:1
Plot:40/87) #20867006 1978, T.B.Ryves pt:4
Plot:41/87) #30479002 1978, U.Garuska pt:1
Plot:42/87) #21049003 1976, A.B.M.G.Mostafa pt:8
Plot:43/87) #40135002 1974, Yu.A.Nemilov pt:4
Plot:44/87) #20798002 1973, J.C.Robertson pt:1
Plot:45/87) #10186005 1971, G.N.Salaita pt:1
Plot:46/87) #10116002 1970, J.Lebowitz pt:1
Plot:47/87) #20111002 1970, H.Vonach pt:1
Plot:48/87) #10031002 1969, R.C.Barrall pt:1
Plot:49/87) #20930005 1969, D.Crumpton pt:1
Plot:50/87) #21250002 1969, P.Boschung pt:1
Plot:51/87) #20890003 1968, P.Cuzzocrea pt:27
Plot:52/87) #10417008 1967, J.A.Grundl pt:6
Plot:53/87) #11421004 1967, H.O.Menlove pt:10
Plot:54/87) #11512003 1967, J.M.Ferguson pt:54
Plot:55/87) #21345002 1967, B.Minetti pt:1
Plot:56/87) #20387003 1966, H.Liskien pt:17
Plot:57/87) #21372002 1966, J.D.Hemingway pt:2
Plot:58/87) #20378003 1965, A.Paulsen pt:23
Plot:59/87) #20837006 1965, U.Seebeck pt:1
Plot:60/87) #20887014 1965, M.Bormann pt:1
Plot:61/87) #11526003 1964, W.L.Imhof pt:4
Plot:62/87) #14818005 1964, W.W.Wadman pt:38
Plot:63/87) #20888002 1964, C.G.Bonazzola pt:1
Plot:64/87) #40686002 1964, P.M.Aron pt:1
Plot:65/87) #11457005 1963, J.P.Butler pt:1
Plot:66/87) #11457006 1963, J.P.Butler pt:32
Plot:67/87) #11457007 1963, J.P.Butler pt:13
Plot:68/87) #20922002 1963, J.M.F.Jeronymo pt:8
Plot:69/87) #30118007 1963, J.Csikai pt:1
Plot:70/87) #11494003 1962, F.Gabbard pt:19
Plot:71/87) #20903002 1962, Langmann pt:1
Plot:72/87) #30008029 1962, P.Strohal pt:1
Plot:73/87) #11462002 1961, B.P.Bayhurst pt:15
Plot:74/87) #11530002 1961, H.W.Schmitt pt:38
Plot:75/87) #115300032 1961, H.W.Schmitt pt:1
Plot:76/87) #20904002 1961, M.Bormann pt:5
Plot:77/87) #11504003 1960, H.A.Tewes pt:15
Plot:78/87) #20921003 1960, G.S.Mani pt:24
Plot:79/87) #21419004 1960, M.J.Depraz pt:1
Plot:80/87) #11464003 1959, B.D.Kern pt:12
Plot:81/87) #11484002 1959, A.Poularikas pt:1
Plot:82/87) #30403002 1959, C.S.Khurana pt:1
Plot:83/87) #11481002 1958, J.A.Grundl pt:7
Plot:84/87) #20283002 1958, I.Kumabe pt:1
Plot:85/87) #20280003 1957, S.Yasumi pt:1
Plot:86/87) #11274009 1953, E.B.Paul pt:1
Plot:87/87) #11474002 1952, S.G.Forbes pt:1

___getEndfDataForPlot: [Al-27] [n,a]
web1addr=https://www-nds.iaea.org/exfor/servlet/E4sSearch2?Target=Al-27&Reaction=n,a&Quantity=SIG&json
format=WebEndfSectionsList-0.1
___Retrieved sections:44
SelectedLib-Sect:2) {'Targ': 'AL-27', 'ZT': 13, 'AT': 27, 'NSUB': 10, 'MT': 107, 'MF': 3, 'R': 'N,A', 'RC': 'AL-27(N,A)NA-24,SIG', 'EvalID': 301095, 'SectID': 21383122, 'PenSectID': 26220297, 'LibID': 830, 'LibName': 'ENDF/B-VIII.1', 'DATE': '20240830', 'AUTH': 'M.B.Chadwick+,Derrien+'}
SelectedLib-Sect:3) {'Targ': 'AL-27', 'ZT': 13, 'AT': 27, 'NSUB': 10, 'MT': 107, 'MF': 3, 'R': 'N,A', 'RC': 'AL-27(N,A)NA-24,SIG', 'EvalID': 149470, 'SectID': 8945716, 'PenSectID': 13670440, 'LibID': 800, 'LibName': 'ENDF/B-VIII.0', 'DATE': '20111222', 'AUTH': 'M.B.Chadwick+,Derrien+'}
SelectedLib-Sect:6) {'Targ': 'AL-27', 'ZT': 13, 'AT': 27, 'NSUB': 10, 'MT': 107, 'MF': 3, 'R': 'N,A', 'RC': 'AL-27(N,A)NA-24,SIG', 'EvalID': 150453, 'SectID': 9041090, 'PenSectID': 13681520, 'LibID': 3300, 'LibName': 'JEFF-3.3', 'DATE': '20171231', 'AUTH': 'M.B.Chadwick & P.G.Young'}
SelectedLib-Sect:10) {'Targ': 'AL-27', 'ZT': 13, 'AT': 27, 'NSUB': 10, 'MT': 107, 'MF': 3, 'R': 'N,A', 'RC': 'AL-27(N,A)NA-24,SIG', 'EvalID': 276797, 'SectID': 19186300, 'PenSectID': 24021365, 'LibID': 51, 'LibName': 'JENDL-5', 'DATE': '20090828', 'AUTH': 'Y.Harima,H.Kitazawa,T.Fukahori'}
SelectedLib-Sect:16) {'Targ': 'AL-27', 'ZT': 13, 'AT': 27, 'NSUB': 10, 'MT': 107, 'MF': 3, 'R': 'N,A', 'RC': 'AL-27(N,A)NA-24,SIG', 'EvalID': 118524, 'SectID': 6050917, 'PenSectID': 10712405, 'LibID': 41031, 'LibName': 'BROND-3.1', 'DATE': 'DEC06', 'AUTH': 'M.B.Chadwick+,Derrien+'}
SelectedLib-Sect:19) {'Targ': 'AL-27', 'ZT': 13, 'AT': 27, 'NSUB': 10, 'MT': 107, 'MF': 3, 'R': 'N,A', 'RC': 'AL-27(N,A)NA-24,SIG', 'EvalID': 199067, 'SectID': 14174292, 'PenSectID': 18847510, 'LibID': 5040, 'LibName': 'CENDL-3.2', 'DATE': '20150815', 'AUTH': 'Y.L.Han'}
SelectedLib-Sect:34) {'Targ': 'AL-27', 'ZT': 13, 'AT': 27, 'NSUB': 10, 'MT': 107, 'MF': 3, 'R': 'N,A', 'RC': 'AL-27(N,A)NA-24,SIG', 'EvalID': 196329, 'SectID': 13291298, 'PenSectID': 17932694, 'LibID': 61020, 'LibName': 'TENDL-2019.s60', 'DATE': 'NOV19', 'AUTH': 'A.J. Koning and D. Rochman'}
Required sections:7
Downloaded:1)	AL-27(N,A)NA-24,SIG	ENDF/B-VIII.1	PenSectID:26220297	pts:185	idy=0
Downloaded:2)	AL-27(N,A)NA-24,SIG	ENDF/B-VIII.0	PenSectID:13670440	pts:55	idy=0
Downloaded:3)	AL-27(N,A)NA-24,SIG	JEFF-3.3	PenSectID:13681520	pts:55	idy=52
Downloaded:4)	AL-27(N,A)NA-24,SIG	JENDL-5	PenSectID:24021365	pts:73	idy=0
Downloaded:5)	AL-27(N,A)NA-24,SIG	BROND-3.1	PenSectID:10712405	pts:55	idy=0
Downloaded:6)	AL-27(N,A)NA-24,SIG	CENDL-3.2	PenSectID:18847510	pts:109	idy=0
Downloaded:7)	AL-27(N,A)NA-24,SIG	TENDL-2019.s60	PenSectID:17932694	pts:269	idy=267
Plot:1/7) 26220297	ENDF/B-VIII.1	pt:183	color:0,0,255
Plot:2/7) 13670440	ENDF/B-VIII.0	pt:53	color:0,127,127
Plot:3/7) 13681520	JEFF-3.3	pt:53	color:0,255,255
Plot:4/7) 24021365	JENDL-5	pt:71	color:0,255,0
Plot:5/7) 10712405	BROND-3.1	pt:53	color:255,0,255
Plot:6/7) 18847510	CENDL-3.2	pt:109	color:255,0,0
Plot:7/7) 17932694	TENDL-2019.s60	pt:267	color:127,127,127

EXFOR SQL executed:  1.43sec
ENDF Web downloaded: 2.083sec

Program successfully completed




select distinct x4pro_c5dat.DatasetID
 ,x4pro_ds.x4status,x4pro_ds.MF,x4pro_ds.reacode
 ,ENTRY.YearRef1,ENTRY.Author1Ini,ENTRY.Author1,REACODE.fullCode
from x4pro_c5dat
 inner join REACODE on REACODE.ReacodeID=x4pro_c5dat.DatasetID
 inner join REACSTR ON REACSTR.ReacodeID=REACODE.ReacodeID
 inner join SUBENT on REACODE.SubentID=SUBENT.SubentID
 inner join ENTRY on ENTRY.EntryID=SUBENT.EntryID
 inner join x4pro_ds on REACODE.ReacodeID=x4pro_ds.DatasetID
where
--      (REACSTR.SF58 like ',SIG')
 (x4pro_ds.MF=3 or (x4pro_ds.MF=203 and x4pro_c5dat.m1 is not Null))
  and (REACSTR.SF8='')
  and ((REACSTR.SF9='') or (REACSTR.SF9='EXP'))
and (REACSTR.iReacstr=1)
and (REACSTR.Target like 'Al-27') and (REACSTR.Reaction like 'n,a') and (sProd like '')
order by
  -- REACODE.fullCode,
  ENTRY.YearRef1 desc,x4pro_c5dat.DatasetID





CREATE VIEW sig1ratio AS
 select x4pro_c5dat.DatasetID
 ,x4pro_ds.x4status,x4pro_ds.MF,x4pro_ds.MT
 ,REACSTR.code as fullCode
-- ,x4pro_ds.reacode
-- ,REACODE.fullCode   
 ,x4pro_c5dat.idat as iPoint
 ,REACODE.Pointer,ENTRY.Entry,REACODE.SubAcc as Subent   
 ,ENTRY.YearRef1,ENTRY.nAuthors,ENTRY.Author1Ini,ENTRY.Author1 
 ,REACSTR.Target, REACSTR.Reaction
 ,lower(REACSTR.Projectile) as Projectile
 ,REACSTR.sProd,REACSTR.sTarg
 ,REACODE.zaTarget1,REACODE.zaIncident1
 ,REACODE.outParticles,REACODE.MF,REACODE.MT
 ,REACSTR.code as reacode1
 ,x4pro_c5dat.x1  as En
 ,x4pro_c5dat.dx1 as dEn
 ,x4pro_c5dat.y   as Sig
 ,x4pro_c5dat.dy  as dSig
 ,x4pro_c5dat.m1  as m1
 ,x4pro_c5dat.dm1 as dm1
from x4pro_c5dat
 inner join REACODE on REACODE.ReacodeID=x4pro_c5dat.DatasetID
 inner join REACSTR ON REACSTR.ReacodeID=REACODE.ReacodeID
 inner join SUBENT on REACODE.SubentID=SUBENT.SubentID
 inner join ENTRY on ENTRY.EntryID=SUBENT.EntryID
 inner join x4pro_ds on REACODE.ReacodeID=x4pro_ds.DatasetID
where
 (x4pro_ds.MF=3 or (x4pro_ds.MF=203 and x4pro_c5dat.m1 is not Null))
 and (REACSTR.iReacstr=1)
 and (x4pro_ds.x4status<>'S' and x4pro_ds.x4status<>'P')
  and (REACSTR.SF8='')
  and ((REACSTR.SF9='') or (REACSTR.SF9='EXP'))
 and (REACSTR.Target like 'U-235')
 and (
       (REACSTR.Reaction like 'n,g' and REACSTR.SF58 like ',SIG')
    or (REACSTR.Reaction like 'n,abs' and REACSTR.SF58 like ',ALF')
    )
 and (sProd like '')
order by
--  REACODE.fullCode,
  ENTRY.YearRef1 desc,x4pro_c5dat.DatasetID
  ,En,x4pro_c5dat.idat
;




select distinct x4pro_c5dat.DatasetID
 ,x4pro_ds.x4status,x4pro_ds.MF,x4pro_ds.reacode
 ,REACSTR.code as reacode1
 ,ENTRY.YearRef1,ENTRY.Author1Ini,ENTRY.Author1,REACODE.fullCode
from x4pro_c5dat
 inner join REACODE on REACODE.ReacodeID=x4pro_c5dat.DatasetID
 inner join REACSTR ON REACSTR.ReacodeID=REACODE.ReacodeID
 inner join SUBENT on REACODE.SubentID=SUBENT.SubentID
 inner join ENTRY on ENTRY.EntryID=SUBENT.EntryID
 inner join x4pro_ds on REACODE.ReacodeID=x4pro_ds.DatasetID
where
 (x4pro_ds.MF=3 or (x4pro_ds.MF=203 and x4pro_c5dat.m1 is not Null))
 and (REACSTR.iReacstr=1)
 and (x4pro_ds.x4status<>'S' and x4pro_ds.x4status<>'P')
  and (REACSTR.SF8='')
  and ((REACSTR.SF9='') or (REACSTR.SF9='EXP'))
and (REACSTR.Target like 'Al-27') and (REACSTR.Reaction like 'n,a') and (sProd like '')
order by
  REACSTR.code,ENTRY.YearRef1 desc,x4pro_c5dat.DatasetID
  ,x4pro_c5dat.idat
