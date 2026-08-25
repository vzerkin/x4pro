"""
 *******************************************************************************
 * Copyright: (C) 2023-2025 Viktor Zerkin, Vienna, Austria                     *
 * Author: Viktor Zerkin, v.zerkin@gmail.com, IAEA(1999-2023), NRDC(1996-2025) *
 *******************************************************************************
"""
import sys
sys.path.append('./')
sys.path.append('../')
from x4subr import *

def getX4SqlSearchCS(target,react,sProd='',eMinEv=None,eMaxEv=None,iYearMin=None):
    print('\n___getX4SqlSearchCS: target:['+target+'] react:['+react+'] sProd:['+sProd+']')
    sql="""	select x4pro_c5dat.DatasetID
	 ,x4pro_ds.x4status,x4pro_ds.MF,x4pro_ds.MT
	 ,REACSTR.code as Reacode
	 ,REACODE.fullCode
	 ,x4pro_c5dat.idat as iPoint
	 ,REACODE.Pointer,ENTRY.Entry,REACODE.SubAcc as Subent   
	 ,ENTRY.YearRef1,ENTRY.nAuthors,ENTRY.Author1Ini,ENTRY.Author1 
	 ,REACSTR.Target, REACSTR.Reaction
	 ,lower(REACSTR.Projectile) as Projectile
	 ,REACSTR.sProd,REACSTR.sTarg
	 ,REACODE.zaTarget1,REACODE.zaIncident1
	 ,REACODE.outParticles,REACODE.MF,REACODE.MT
	 ,REACSTR.code as reacode1
	 ,x4pro_c5dat.x1   as En
	 ,x4pro_c5dat.dx1  as dEn
	 ,x4pro_c5dat.y    as Sig
	 ,x4pro_c5dat.dy   as dSig
	 ,x4pro_c5dat.m0   as m0
	 ,x4pro_c5dat.dm0  as dm0
	 ,x4pro_c5dat.m1   as m1
	 ,x4pro_c5dat.dm1  as dm1
	 ,x4pro_c5dat.Fcm0 as Fc
	 ,x4pro_autocorr.FcDecayData
	 ,x4pro_autocorr.FcDecayMon
	 ,x4pro_autocorr.autoCorr
	from x4pro_c5dat
	 inner join REACODE        on REACODE.ReacodeID=x4pro_c5dat.DatasetID
	 inner join REACSTR        on REACSTR.ReacodeID=REACODE.ReacodeID
	 inner join SUBENT         on REACODE.SubentID=SUBENT.SubentID
	 inner join ENTRY          on ENTRY.EntryID=SUBENT.EntryID
	 inner join x4pro_ds       on REACODE.ReacodeID=x4pro_ds.DatasetID
	 left  join x4pro_autocorr on x4pro_autocorr.DatasetID=x4pro_ds.DatasetID
	where
	 (x4pro_ds.MF=3 or (x4pro_ds.MF=203 and x4pro_c5dat.m1 is not Null))
	 and (REACSTR.iReacstr=1)
	 and (x4pro_ds.x4status<>'S' and x4pro_ds.x4status<>'P')
	 and (REACSTR.SF8='')
	 and ((REACSTR.SF9='') or (REACSTR.SF9='EXP'))
"""

    sql+="	 and (Target like '"+target+"') \n"
    sql+="	 and ((Reaction like '"+react+"' and REACSTR.SF58 like ',SIG') \n"
    if react=='n,g':
        sql+="	   or (REACSTR.Reaction like 'n,abs' and REACSTR.SF58 like ',ALF') \n"
    sql+="	 )\n"
    sql+="	 and (sProd like '"+sProd+"') \n"
    #sql+="	 and (x4pro_c5dat.DatasetID like '11457007') \n"
    #sql+="	 and (x4pro_c5dat.DatasetID like '30403002') \n"
#    sql+="	 and (x4pro_c5dat.DatasetID like '23032009') \n"
    #sql+="	 and (ENTRY.Author1 like 'Laptev') \n"
    if eMinEv is not None: sql+="	 and (x4pro_c5dat.x1>="+str(eMinEv)+") \n"
    if eMaxEv is not None: sql+="	 and (x4pro_c5dat.x1<="+str(eMaxEv)+") \n"
    if iYearMin is not None: sql+="	 and (ENTRY.YearRef1>="+str(iYearMin)+") \n"

    #sql+="	order by ENTRY.YearRef1 desc,x4pro_c5dat.DatasetID,En,x4pro_c5dat.idat"
    sql+="""	order by
	--  Reacode desc,
	  ENTRY.YearRef1 desc,x4pro_c5dat.DatasetID
	  ,En,x4pro_c5dat.idat"""

    #print("SQL:\n"+sql)

    return sql

def getDatasets4plot(rows,fx=1e-6,fy=1e3
	,flagRenormCS=True,flagRatio2CS=True,groupByMT=True
	,flagRenormDD=True,flagRenormDM=True
	,datasetBlackList=None
	,x4evalflags=None
	,markRejected=False
	):
    lx=len(rows)
    datasets=[]
    ii=0; lastDatasetID=''; lastDataset={}
    print('\n___getDatasets from datapoints:',len(rows))
    printedDeleted={}
    for row in rows:
        DatasetID=row['DatasetID']
        if datasetBlackList is not None:
            if DatasetID in datasetBlackList:
                if DatasetID not in printedDeleted:
                    print('-rejected- datasetBlackList["'+DatasetID+'"]: "'+datasetBlackList[DatasetID]+'"')
                    printedDeleted[DatasetID]=datasetBlackList[DatasetID]
                continue
        fullCode=row['fullCode']
        Reacode=row['Reacode']
        iPoint=row['iPoint']
        Target=row['Target']
        YearRef1=row['YearRef1']; Author1Ini=row['Author1Ini']; Author1=row['Author1'];
        xx=row['En'];  yy=row['Sig'];  dyy=row['dSig'];  dxx=row['dEn']
        MF=row['MF'];  MT=row['MT']
        m0=row['m0'];  dm0=row['dm0']
        m1=row['m1'];  dm1=row['dm1']
        Fc=row['Fc']
        FcDecayData=row['FcDecayData']
        FcDecayMon=row['FcDecayMon']
        autoCorr=row['autoCorr']
        if not flagRatio2CS and MF!=3: continue
        if xx is None: continue;
        if yy is None: continue;
        if Author1Ini is not None: Author1=Author1Ini+Author1
        if DatasetID!=lastDatasetID:
            lastDataset={}
            lastDataset['LIBRARY']='EXFOR'
            lastDataset['mode']='points'
            lastDataset['DatasetID']=DatasetID
            lastDataset['Reacode']=Reacode
            lastDataset['year']=YearRef1
            if groupByMT: lastDataset['Reacode']=Target+" MT"+str(MT)
            lastDataset['x4lbl']=str(YearRef1)+', '+str(Author1)
            set_x4evalflags(lastDataset,DatasetID,x4evalflags,markRejected=markRejected)
            lastDataset['x4corr']=''
            if autoCorr is not None: autoCorr=autoCorr.split("\r\n")
            if flagRenormCS or flagRenormDD or flagRenormDM:
                lastDataset['autoCorr']=autoCorr
            if MF==203:
                lastDataset['x4lbl']+='#'
                lastDataset['x4corr']='ratio*m1'
            lastDataset['fx']=fx
            lastDataset['fy']=fy
            x=[];     lastDataset['x']=x
            y=[];     lastDataset['y']=y
            dy=[];    lastDataset['dy']=dy
            dx=[];    lastDataset['dx']=dx
            FcApplied=[];    lastDataset['FcApplied']=FcApplied
            datasets.append(lastDataset);
            lastDatasetID=DatasetID
            print('-DS:'+str(len(datasets)).rjust(3)+') #'+str(DatasetID).ljust(9)+' '+str(YearRef1)+','+Author1.ljust(24)+' MF:'+str(MF).ljust(3)+' MT:'+str(MT)+' '+str(fullCode)+' ds.reac:'+lastDataset['Reacode'])
        FcNow=1
        if MF==203:
            #if DatasetID=='41380002': print('\t--0--DatasetID:'+DatasetID+' x:'+str(xx)+' y:'+str(yy)+' dy:'+str(dyy)+' m1:'+str(m1)+' dm1:'+str(dm1))
            FcNow=FcNow*m1
            yy1=yy*m1
            if dyy is not None:
                if dm1 is not None: dyy=(dyy/yy+dm1/m1)*yy1
                else: dyy*=m1
            yy=yy1
            #if DatasetID=='41380002': print('\t--1--DatasetID:'+DatasetID+' x:'+str(xx)+' y:'+str(yy)+' dy:'+str(dyy))
        if MF==3:
            if flagRenormCS and (m0 is not None) and (m1 is not None):
                FcNow=FcNow/m0*m1
                yy1=yy/m0*m1
                if (dyy is not None) and (dm0 is not None) and (dm1 is not None):
                    dyy=(dyy/yy+dm0/m0+dm1/m1)*yy1
                yy=yy1
                markCorr(lastDataset,'*m1/m0')
            if flagRenormDD and (FcDecayData is not None):
                FcNow=FcNow*FcDecayData
                yy1=yy*FcDecayData
                if dyy is not None: dyy=dyy*FcDecayData
                yy=yy1
                markCorr(lastDataset,'*dd')
            if flagRenormDM and (FcDecayMon is not None):
                FcNow=FcNow*FcDecayMon
                yy1=yy*FcDecayMon
                if dyy is not None: dyy=dyy*FcDecayMon
                yy=yy1
                markCorr(lastDataset,'*dm')
        xx=c5data2factor(xx,fx)
        yy=c5data2factor(yy,fy)
        dyy=c5error2factor(dyy,fy)
        dxx=c5error2factor(dxx,fx)
        x.append(xx);
        y.append(yy);
        dy.append(dyy)
        dx.append(dxx)
        FcApplied.append(FcNow)
        ii+=1
#        print('MF'+str(MF)+' pt:'+str(ii)+'/'+str(lx)+') '+str(DatasetID)+' '+str(YearRef1)+' '+Author1+" x:"+str(xx)+" y:"+str(yy)+" dy:"+str(dyy)+" dx:"+str(dxx)
#	+' m0:'+str(m0)+' m1:'+str(m1)+' Fc:'+str(Fc))
    for dataset in datasets:
        idx=delColumnIfEmpty(dataset,'dx')
        idy=delColumnIfEmpty(dataset,'dy')
        #print('DS:'+dataset['DatasetID']+' idx:'+str(idx)+' idy:'+str(idy)+' '+dataset['x4lbl'])
    return datasets

def markCorr(ds,typ):
    if ds['x4corr'].find(typ)<0:
        ds['x4corr']+=typ
        if '*' not in ds['x4lbl']: ds['x4lbl']+='*'
    return

def delColumnIfEmpty(dataset,fld):
    ival=0
    col=dataset.get(fld)
    if col is not None:
        for val in col:
            if val is not None: ival+=1
        if ival<=0: del dataset[fld]
    return ival

def getReacodes(datasets):
    lx=len(datasets)
    groups={}
    ii=0
    print('\n---getReacodes---Datasets:',len(datasets))
    for dataset in datasets:
        Reacode=dataset['Reacode']
        arr=groups.get(Reacode)
        if arr is None:
            arr=[]
            groups[Reacode]=arr
        arr.append(dataset);
        ii+=1
        print('   Dataset:'+str(ii)+'/'+str(lx)+') '+Reacode+' '+dataset['DatasetID']+' L.group:'+str(len(arr)))
    return list(groups)

def set_x4evalflags(dataset,DatasetID,dict1,markRejected=False):
    if dict1 is None: return
    arrFlags=dict1.get(DatasetID)
    if arrFlags is None: return
    str1=""
    for obj1 in arrFlags:
        if str1!="": str1+=","
        #str1+=str(obj1['accepted'])
#        if obj1.get('evalflag') is not None: str1+="("
#        if obj1['accepted']==0: str1+="-"
#        else: str1+="+"
        if obj1['accepted']==0: str1+="n"
        else: str1+="y"
#        if obj1.get('evalflag') is not None: str1+=obj1['evalflag']+")"
        if obj1.get('evalflag') is not None: str1+=obj1['evalflag']
#    dataset['x4lbl']+='['+str1+']'
    dataset['x4evalflags']=str1
    dataset['x4evalscores']=arrFlags
    if markRejected:
#        if "n" in str1: dataset['Reacode']+=" --rejected"
        if str1!="": dataset['Reacode']+=" --"+str1
