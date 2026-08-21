"""
 **********************************************************************
 * Copyright: (C) 2021-2022 International Atomic Energy Agency (IAEA) *
 * Author: Viktor Zerkin, V.Zerkin@iaea.org, (IAEA-NDS)               *
 **********************************************************************
"""
def getX4SqlSearchCSP(target,react,sProd='',sf58=",sig",add2where=""):
    print('\n___getX4SqlSearchCS: ['+target+'] ['+react+']'+'] ['+sProd+']')
    sql=str(""
	+"select x4pro_c5dat.DatasetID                                    \n"
	+" ,x4pro_c5dat.idat as iPoint                                    \n"
	+" ,REACODE.fullCode                                              \n"
	+" ,REACODE.Pointer,ENTRY.Entry,REACODE.SubAcc as Subent          \n"
	+" ,ENTRY.YearRef1,ENTRY.nAuthors,ENTRY.Author1Ini,ENTRY.Author1  \n"
	+" ,REACSTR.Target, REACSTR.Reaction                              \n"
	+" ,lower(REACSTR.Projectile) as Projectile                       \n"
	+" ,REACSTR.sProd,REACSTR.sTarg                                   \n"
	+" ,REACODE.zaTarget1,REACODE.zaIncident1                         \n"
	+" ,REACODE.outParticles,REACODE.MF,REACODE.MT                    \n"
	+" ,x4pro_c5dat.y   as Sig                                        \n"
	+" ,x4pro_c5dat.dy  as dSig                                       \n"
	+" ,x4pro_c5dat.x1  as En                                         \n"
	+" ,x4pro_c5dat.dx1 as dEn                                        \n"
	+" ,x4pro_c5dat.x2  as Elv                                        \n"
	+" ,x4pro_c5dat.dx2 as dElv                                       \n"
	+"from x4pro_c5dat                                                \n"
	+" inner join REACODE on REACODE.ReacodeID=x4pro_c5dat.DatasetID  \n"
	+" inner join REACSTR ON REACSTR.ReacodeID=REACODE.ReacodeID      \n"
	+" inner join SUBENT on REACODE.SubentID=SUBENT.SubentID          \n"
	+" inner join ENTRY on ENTRY.EntryID=SUBENT.EntryID               \n"
	+"where                                                           \n"
	+"      (REACSTR.SF58 like '"+sf58+"')                            \n"
	+"  and (REACSTR.SF8='')                                          \n"
	+"  and ((REACSTR.SF9='') or (REACSTR.SF9='EXP'))                 \n"
	+"  and (REACODE.nReacstr=1)                                      \n"
	+"  and (Target like '"+target+"')                                \n"
	+"  and (Reaction like '"+react+"')                               \n"
	+" "+add2where+" "
	+"order by                                                        \n"
	+"  REACODE.fullCode,ENTRY.YearRef1 desc,x4pro_c5dat.DatasetID    \n"
	+"  ,Elv,En,x4pro_c5dat.idat                                      \n"
	)

    print("SQL:\n"+sql)
    return sql

def getDatasets4plot(rows,fx=1e-6,fy=1e3):
    lx=len(rows)
    datasets=[]
    ii=0; lastDatasetSplit=''; lastDataset={}
    print('\n___getDatasets from datapoints:',len(rows))
    for row in rows:
        fullCode=row['fullCode']; DatasetID=row['DatasetID']; iPoint=row['iPoint']
        YearRef1=row['YearRef1']; Author1Ini=row['Author1Ini']; Author1=row['Author1'];
        xx=row['En'];  yy=row['Sig'];  dyy=row['dSig'];  dxx=row['dEn']
        Elv=row['Elv'];   dElv=row['dElv']
        if xx is None: continue;
        if yy is None: continue;
        fullCode=fullCode.replace(",,,EXP","")
        fullCode=fullCode.replace(",,EXP","")
        if Author1Ini is not None: Author1=Author1Ini+Author1
        nowDatasetSplit=DatasetID+' '+str(Elv)
        if nowDatasetSplit!=lastDatasetSplit:
            lastDataset={}
            lastDataset['DatasetID']=DatasetID
            lastDataset['Reacode']=fullCode
#            lastDataset['DatasetSplit']='ELv='+str(Elv/1e6)+'MeV'
            lastDataset['x4lbl']=str(YearRef1)+', '+str(Author1)+' ELv='+str(Elv/1e6)+'MeV'
            x=[];     lastDataset['x']=x
            y=[];     lastDataset['y']=y
            dy=[];    lastDataset['dy']=dy
            dx=[];    lastDataset['dx']=dx
            datasets.append(lastDataset);
            lastDatasetSplit=nowDatasetSplit
            print('DS:'+str(len(datasets))+') '+str(fullCode)+' #'+str(DatasetID)+' '+str(YearRef1)+','+Author1)
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
