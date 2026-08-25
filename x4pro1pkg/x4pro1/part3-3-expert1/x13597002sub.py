"""
 **********************************************************************
 * Copyright: (C) 2021-2022 International Atomic Energy Agency (IAEA) *
 * Author: Viktor Zerkin, V.Zerkin@iaea.org, (IAEA-NDS)               *
 **********************************************************************
"""

def getX4SqlSearchCS(target,react):
    print('\n___getX4SqlSearchCS: ['+target+'] ['+react+']')
    sql="\
select x4.DatasetID                                                   \n\
 ,x4.idat as iPoint,x4.xdat,c5.y,c5.dy                                \n\
 ,REACODE.fullCode                                                    \n\
 ,REACODE.Pointer,ENTRY.EntryID,REACODE.SubentID                      \n\
 ,ENTRY.YearRef1,ENTRY.Author1Ini,ENTRY.Author1                       \n\
 ,REACSTR.Target, REACSTR.Reaction                                    \n\
 ,REACODE.outParticles                                                \n\
 ,c5.x1 as En,c5.dx1 as dEn                                           \n\
 ,round(c5.y*c5.Fcm0,10) as ynew0                                     \n\
 ,c5.dyerr,c5.dysys,c5.dystat                                         \n\
 ,c5.Fcm0,corr.FcDecayData,corr.FcDecayMon                            \n\
 ,c5.m0,c5.dm0,c5.m1,c5.dm1                                           \n\
 ,case                                                                \n\
  when c5.Fcm0>0 and corr.FcDecayData>0 and corr.FcDecayMon>0         \n\
   then c5.Fcm0*corr.FcDecayData*corr.FcDecayMon                      \n\
  when c5.Fcm0>0 and corr.FcDecayData>0 then c5.Fcm0*corr.FcDecayData \n\
  when c5.Fcm0>0 and corr.FcDecayMon>0  then c5.Fcm0*corr.FcDecayMon  \n\
  when corr.FcDecayData>0 and corr.FcDecayMon>0                       \n\
   then corr.FcDecayData*corr.FcDecayMon                              \n\
  when c5.Fcm0>0 then c5.Fcm0                                         \n\
  when corr.FcDecayData>0 then corr.FcDecayData                       \n\
  when corr.FcDecayMon>0  then corr.FcDecayMon                        \n\
  else null                                                           \n\
 end as FcNew                                                         \n\
from x4pro_x4data x4                                                  \n\
 inner join x4pro_c5dat c5 on                                         \n\
 x4.DatasetID=c5.DatasetID and x4.idat=c5.idat                        \n\
 inner join x4pro_ds ds on x4.DatasetID=ds.DatasetID                  \n\
 left  join x4pro_autocorr corr on corr.DatasetID=ds.DatasetID        \n\
 inner join REACODE on REACODE.ReacodeID=c5.DatasetID                 \n\
 inner join REACSTR ON REACSTR.ReacodeID=REACODE.ReacodeID            \n\
 inner join SUBENT on REACODE.SubentID=SUBENT.SubentID                \n\
 inner join ENTRY on ENTRY.EntryID=SUBENT.EntryID                     \n\
where                                                                 \n\
      (REACSTR.SF58 like ',SIG')                                      \n\
  and (REACSTR.SF8='')                                                \n\
  and ((REACSTR.SF9='') or (REACSTR.SF9='EXP'))                       \n\
  and (REACODE.nReacstr=1)                                            \n\
  and (REACSTR.Target like '"+target+"')                              \n\
  and (REACSTR.Reaction like '"+react+"')                             \n\
--  and ENTRY.YearRef1>=1991                                          \n\
--  and ds.ndat>=2                                                    \n\
-- and x4.DatasetID='13597002'                                        \n\
   and (x4.DatasetID='13597002'                      \n\
     or x4.DatasetID='22209012'                      \n\
     or x4.DatasetID='10224002'                      \n\
     or (x4.DatasetID='40485003' and En<9e6)         \n\
     )  \n\
order by                                                              \n\
  REACODE.fullCode,ENTRY.YearRef1 desc,c5.DatasetID                   \n\
  ,En,c5.idat                                                         \n\
"
    #print("SQL:\n"+sql)
    return sql

def getDatasets4plot(rows,fx=1e-6,fy=1e3):
    lx=len(rows)
    datasets=[]
    ii=0; lastDatasetID=''; lastDataset={}
    print('\n___getDatasets from datapoints:',len(rows))
    for row in rows:
        fullCode=row['fullCode']; DatasetID=row['DatasetID']; iPoint=row['iPoint']
        YearRef1=row['YearRef1']; Author1Ini=row['Author1Ini']; Author1=row['Author1'];
        xx=row['En'];  yy=row['y'];  dyy=row['dy'];  dxx=row['dEn']
        if xx is None: continue;
        if yy is None: continue;
        if Author1Ini is not None: Author1=Author1Ini+Author1
        if DatasetID!=lastDatasetID:
            lastDataset={}
            lastDataset['DatasetID']=DatasetID
            lastDataset['Reacode']=fullCode
            str1=''
            if row.get('corrected') is not None: str1='*'
            lastDataset['x4lbl']=str(YearRef1)+', '+str(Author1)+str1
            x=[];     lastDataset['x']=x
            y=[];     lastDataset['y']=y
            dy=[];    lastDataset['dy']=dy
            dx=[];    lastDataset['dx']=dx
            lastDataset['row0']=row
            datasets.append(lastDataset);
            lastDatasetID=DatasetID
            print('DS:'+str(len(datasets))+') '+str(fullCode)+' '+str(DatasetID)+' '+str(YearRef1)+' '+Author1)
        xx=float(xx)*fx; xx=float(format(xx,".5e")) #precision: 11 columns = 6 digits: 1.23456e-02
        yy=float(yy)*fy; yy=float(format(yy,".5e"))
        if dyy is not None:
            dyy=float(dyy)*fy
            dyy=float(format(dyy,".5e"))
            if dyy<0: dyy=-dyy
        if dxx is not None:
            dxx=float(dxx)*fx
            dxx=float(format(dxx,".5e"))
            if dxx<0: dxx=-dxx
        x.append(xx);
        y.append(yy);
        dy.append(dyy)
        dx.append(dxx)
        ii+=1
        print(' pt:'+str(ii)+'/'+str(lx)+') '+str(fullCode)+' '+str(DatasetID)+' '+str(YearRef1)+' '+Author1+" x:"+str(xx)+" y:"+str(yy)+" dy:"+str(dyy)+" dx:"+str(dxx))
    return datasets

def getDatasets00(rows):
    lx=len(rows)
    datasets=[]
    ii=0; lastDatasetID=''; lastRows=[]
    print('\ndatapoints:',len(rows))
    for row in rows:
        DatasetID=row['DatasetID']
        if DatasetID!=lastDatasetID:
            lastRows=[]
            datasets.append(lastRows);
            lastDatasetID=DatasetID
            print(str(len(datasets))+') '+'___________')
        lastRows.append(row);
        ii+=1
        #print(str(ii)+'/'+str(lx)+') '+str(fullCode)+' '+str(DatasetID)+' '+str(YearRef1)+' '+Author1+" x:"+str(xx)+" y:"+str(yy)+" dy:"+str(dyy)+" dx:"+str(dxx))
    return datasets


def getReacodes(datasets):
    lx=len(datasets)
    Reacodes=[]
    ii=0; lastReacodeStr='---'; lastReacode={}
    print('\nDatasets:',len(datasets))
    for dataset in datasets:
        Reacode=dataset['Reacode']
        if Reacode!=lastReacodeStr:
            lastReacode={}
            lastReacode['Reacode']=Reacode
            lastReacode['datasets']=[]
            Reacodes.append(lastReacode)
            lastReacodeStr=Reacode
            print(str(len(Reacodes))+') '+str(Reacode))
        lastReacode['datasets'].append(dataset);
        ii+=1
        #print('\tDataset:'+str(ii)+'/'+str(lx)+') '+str(Reacode)+' '+str(dataset['DatasetID']))
    return Reacodes
