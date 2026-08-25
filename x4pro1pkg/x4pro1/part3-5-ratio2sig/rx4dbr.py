"""
 **********************************************************************
 * Copyright: (C) 2021-2022 International Atomic Energy Agency (IAEA) *
 * Author: Viktor Zerkin, V.Zerkin@iaea.org, (IAEA-NDS)               *
 **********************************************************************
"""
def getX4SqlSearchCS(target,react,sProd=''):
    print('\n___getX4SqlSearchCS: ['+target+'] ['+react+']'+'] ['+sProd+']')
    sql="""
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
 ,x4pro_c5dat.x1   as En
 ,x4pro_c5dat.dx1  as dEn
 ,x4pro_c5dat.y    as Sig
 ,x4pro_c5dat.dy   as dSig
 ,x4pro_c5dat.m0   as m0
 ,x4pro_c5dat.dm0  as dm0
 ,x4pro_c5dat.m1   as m1
 ,x4pro_c5dat.dm1  as dm1
 ,x4pro_c5dat.Fcm0 as Fc
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
	"""

    sql+=" and (Target like '"+target+"') \n"
    sql=sql+" and (\n       (Reaction like '"+react+"' and REACSTR.SF58 like ',SIG') \n"
    if react=='n,g':
        sql+="    or (REACSTR.Reaction like 'n,abs' and REACSTR.SF58 like ',ALF') \n"
    sql+="     )\n"
    sql+="  and (sProd like '"+sProd+"') \n"

#    sql+="  and (x4pro_c5dat.DatasetID like '11457007') \n"

    sql+="""
	order by
	--  REACODE.fullCode,
	  ENTRY.YearRef1 desc,x4pro_c5dat.DatasetID
	  ,En,x4pro_c5dat.idat
	"""
    print("SQL:\n"+sql)

    return sql

def getDatasets4plot(rows,fx=1e-6,fy=1e3,flagRenormCS=True,flagRatio2CS=True):
    lx=len(rows)
    datasets=[]
    ii=0; lastDatasetID=''; lastDataset={}
    print('\n___getDatasets from datapoints:',len(rows))
    for row in rows:
        fullCode=row['fullCode']; DatasetID=row['DatasetID']; iPoint=row['iPoint']
        YearRef1=row['YearRef1']; Author1Ini=row['Author1Ini']; Author1=row['Author1'];
        xx=row['En'];  yy=row['Sig'];  dyy=row['dSig'];  dxx=row['dEn']
        MF=row['MF'];  MT=row['MT']
        m0=row['m0'];  dm0=row['dm0']
        m1=row['m1'];  dm1=row['dm1']
        Fc=row['Fc']
        if not flagRatio2CS and MF!=3: continue
        if xx is None: continue;
        if yy is None: continue;
        if Author1Ini is not None: Author1=Author1Ini+Author1
        if DatasetID!=lastDatasetID:
            lastDataset={}
            lastDataset['DatasetID']=DatasetID
            lastDataset['Reacode']=fullCode
            lastDataset['x4lbl']=str(YearRef1)+', '+str(Author1)
            if MF==203:
                lastDataset['x4lbl']+='#'
            x=[];     lastDataset['x']=x
            y=[];     lastDataset['y']=y
            dy=[];    lastDataset['dy']=dy
            dx=[];    lastDataset['dx']=dx
            datasets.append(lastDataset);
            lastDatasetID=DatasetID
            print('DS:'+str(len(datasets))+') '+str(fullCode)+' #'+str(DatasetID)+' '+str(YearRef1)+','+Author1)
        if MF==203:
            yy=yy*m1
            if (dyy is not None) and (dm1 is not None): dyy=(dyy+dm1)*m1
        if flagRenormCS and MF==3 and (dm0 is not None) and (dm1 is not None):
            yy1=yy/m0*m1
            if (dyy is not None) and (dm0 is not None) and (dm1 is not None):
                dyy=(dyy/yy+dm0/m0+dm1/m1)*yy1
            yy=yy1
            if lastDataset['x4lbl'].find('*')<0: lastDataset['x4lbl']+='*'
        xx=float(xx)*fx; xx=round(xx,7)
        yy=float(yy)*fy; yy=round(yy,7)
        if dyy is not None: dyy=float(dyy)*fy; dyy=round(dyy,7)
        if dxx is not None: dxx=float(dxx)*fx; dxx=round(dxx,7)
        x.append(xx);
        y.append(yy);
        dy.append(dyy)
        dx.append(dxx)
        ii+=1
        print(str(MF)+' pt:'+str(ii)+'/'+str(lx)+') '+str(fullCode)+' '+str(DatasetID)+' '+str(YearRef1)+' '+Author1+" x:"+str(xx)+" y:"+str(yy)+" dy:"+str(dyy)+" dx:"+str(dxx)
	+' m0:'+str(m0)+' m1:'+str(m1)+' Fc:'+str(Fc))
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
