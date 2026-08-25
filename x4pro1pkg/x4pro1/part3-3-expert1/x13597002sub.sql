select x4.DatasetID
 ,x4.idat as iPoint,x4.xdat,c5.y,c5.dy
 ,REACODE.fullCode   
 ,REACODE.Pointer,ENTRY.EntryID,REACODE.SubentID   
 ,ENTRY.YearRef1,ENTRY.Author1Ini,ENTRY.Author1 
 ,REACSTR.Target, REACSTR.Reaction
 ,REACODE.outParticles
 ,c5.x1 as En,c5.dx1 as dEn
 ,round(c5.y*c5.Fcm0,10) as ynew0
 ,c5.dyerr,c5.dysys,c5.dystat
 ,c5.Fcm0,corr.FcDecayData,corr.FcDecayMon
 ,c5.m0,c5.dm0,c5.m1,c5.dm1
 ,case                                                                
  when c5.Fcm0>0 and corr.FcDecayData>0 and corr.FcDecayMon>0         
   then c5.Fcm0*corr.FcDecayData*corr.FcDecayMon                      
  when c5.Fcm0>0 and corr.FcDecayData>0 then c5.Fcm0*corr.FcDecayData 
  when c5.Fcm0>0 and corr.FcDecayMon>0  then c5.Fcm0*corr.FcDecayMon  
  when corr.FcDecayData>0 and corr.FcDecayMon>0                       
   then corr.FcDecayData*corr.FcDecayMon                              
  when c5.Fcm0>0 then c5.Fcm0                                         
  when corr.FcDecayData>0 then corr.FcDecayData                       
  when corr.FcDecayMon>0  then corr.FcDecayMon                        
  else null                                                           
 end as FcNew                                                         
from x4pro_x4data x4
 inner join x4pro_c5dat c5 on
 x4.DatasetID=c5.DatasetID and x4.idat=c5.idat
 inner join x4pro_ds ds on x4.DatasetID=ds.DatasetID
 left  join x4pro_autocorr corr on corr.DatasetID=ds.DatasetID
 inner join REACODE on REACODE.ReacodeID=c5.DatasetID
 inner join REACSTR ON REACSTR.ReacodeID=REACODE.ReacodeID
 inner join SUBENT on REACODE.SubentID=SUBENT.SubentID
 inner join ENTRY on ENTRY.EntryID=SUBENT.EntryID
where
      (REACSTR.SF58 like ',SIG')
  and (REACSTR.SF8='')
  and ((REACSTR.SF9='') or (REACSTR.SF9='EXP'))
  and (REACODE.nReacstr=1)
  and (REACSTR.Target like 'Zn-64')
  and (REACSTR.Reaction like 'n,p')
order by
  REACODE.fullCode,ENTRY.YearRef1 desc,c5.DatasetID
  ,En,c5.idat
