"""
 **********************************************************************
 * Copyright: (C) 2021-2022 International Atomic Energy Agency (IAEA) *
 * Author: Viktor Zerkin, V.Zerkin@iaea.org, (IAEA-NDS)               *
 **********************************************************************
"""
def getX4SqlSearchDA_Ei(target,react,x4sqlparam):
    print("___getX4SqlSearchDA_a:",target,react)
    sql=str(""
	+"select *                           \n"
	+" ,round(An) as Anint               \n"
	+"from da1                           \n"
	+"where (Target like '"+target+"')   \n"
	+"  and (Reaction like '"+react+"')  \n"
	+x4sqlparam+"\n"
	+"order by fullCode,                 \n"
	+"  YearRef1 desc,DatasetID          \n"
	+"  ,Anint,En,iPoint                 \n"
	)
    #print("SQL:\n"+sql)
    return sql

def getDatasets4plot(rows,fx=1e-6,fy=1e3):
    lx=len(rows)
    datasets=[]
    ii=0; lastDatasetSplit=''; lastDataset={}
    print('\ndatapoints:',len(rows))
    for row in rows:
        fullCode=row['fullCode']; DatasetID=row['DatasetID']; iPoint=row['iPoint']
        YearRef1=row['YearRef1']; Author1Ini=row['Author1Ini']; Author1=row['Author1'];
        yy=row['Sig'];    dyy=row['dSig']
        xx=row['En'];     dxx=row['dEn']
        zz=row['Anint'];     dzz=row['dAn']
        if xx is None: continue;
        if yy is None: continue;
        if Author1Ini is not None: Author1=Author1Ini+Author1
        nowDatasetSplit=DatasetID+' '+str(zz)
        fullCode=fullCode.replace(",,,EXP","")
        fullCode=fullCode.replace(",,EXP","")
        if nowDatasetSplit!=lastDatasetSplit:
            lastDataset={}
            lastDataset['DatasetID']=DatasetID
            lastDataset['Reacode']=fullCode
            lastDataset['DatasetSplit']='An='+str(zz)+'deg'
            lastDataset['x4lbl']=str(YearRef1)+', '+str(Author1)
            x=[];     lastDataset['x']=x
            y=[];     lastDataset['y']=y
            dy=[];    lastDataset['dy']=dy
            dx=[];    lastDataset['dx']=dx
            datasets.append(lastDataset);
            lastDatasetSplit=nowDatasetSplit
            print(str(len(datasets))+') '+str(fullCode)+' '+str(DatasetID)+' '+str(YearRef1)+' '+Author1)
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
#        print(str(ii)+'/'+str(lx)+') '+str(fullCode)+' '+str(DatasetID)+' '+str(YearRef1)+' '+Author1+" x:"+str(xx)+" y:"+str(yy)+" dy:"+str(dyy)+" dx:"+str(dxx))
    return datasets


def getReacodes(datasets,nptmin):
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
        if (len(dataset['x'])>nptmin):
            lastReacode['datasets'].append(dataset);
            ii+=1
        print('\tDataset:'+str(ii)+'/'+str(lx)+') '+str(Reacode)+' '+str(dataset['DatasetID'])+' npt:'+str(len(dataset['x'])))
#        print('\tDataset:'+str(ii)+'/'+str(lx)+') '+str(Reacode)+' '+str(dataset['DatasetID'])+' npt:"+str(len(dataset["x"]))
    return Reacodes

def getReacodes2Datasets(reacodes):
    datasets=[]
    for reacode in reacodes:
        for dataset in reacode['datasets']:
            datasets.append(dataset)
    return datasets
