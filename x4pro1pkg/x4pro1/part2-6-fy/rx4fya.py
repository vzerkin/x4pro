"""
 **********************************************************************
 * Copyright: (C) 2021-2022 International Atomic Energy Agency (IAEA) *
 * Author: Viktor Zerkin, V.Zerkin@iaea.org, (IAEA-NDS)               *
 **********************************************************************
"""

def getX4SqlSearchFY_MASS(reacode,x4sqlparam):
    print("___getX4SqlSearchFY_MASS:",reacode,x4sqlparam)
    sql=str(""
	+"select *                                  \n"
	+" ,y  as FY, dy  as dFY                    \n"
	+" ,x1 as En, dx1 as dEn                    \n"
	+" ,x2 as MASS                              \n"
	+"from uni1                                 \n"
	+"where                                     \n"
	+" fullCode='"+reacode+"'                   \n"
	+x4sqlparam+"\n"
	+"order by fullCode,YearRef1 desc,DatasetID \n"
	+" ,En,iPoint                               \n"
	)
    #print("SQL:\n"+sql)
    return sql

def getDatasets4plot(rows,fx=1,fy=1,fe=1e-6):
    lx=len(rows)
    datasets=[]
    ii=0; lastDatasetSplit=''; lastDataset={}
    print('\ndatapoints:',len(rows))
    for row in rows:
        fullCode=row['fullCode']; DatasetID=row['DatasetID']; iPoint=row['iPoint']
        YearRef1=row['YearRef1']; Author1Ini=row['Author1Ini']; Author1=row['Author1'];
        yy=row['FY'];    dyy=row['dFY']
        xx=row['MASS'];  dxx=None
        ee=row['En'];    dee=row['dEn']
        e1=ee*fe; e2=ee*fe
        if dee is not None: e1=(ee-dee)*fe; e2=(ee+dee)*fe
        if e1 is not None: e1=round(e1,7)
        if e2 is not None: e2=round(e2,7)
        splt="Ei:"+str(e1)
        if e1!=e2: splt=splt+"-"+str(e2)
        splt=splt+"MeV"
        if xx is None: continue;
        if yy is None: continue;
        if Author1Ini is not None: Author1=Author1Ini+Author1
        nowDatasetSplit=DatasetID+' '+str(splt)
        fullCode=fullCode.replace(",,,EXP",""); fullCode=fullCode.replace(",,EXP","")
        if nowDatasetSplit!=lastDatasetSplit:
            lastDataset={}
            lastDataset['DatasetID']=DatasetID
            lastDataset['Reacode']=fullCode
            lastDataset['DatasetSplit']=splt
            lastDataset['x4lbl']=str(YearRef1)+', '+str(Author1)
            x=[];     lastDataset['x']=x
            y=[];     lastDataset['y']=y
            dy=[];    lastDataset['dy']=dy
            dx=[];    lastDataset['dx']=dx
            datasets.append(lastDataset);
            lastDatasetSplit=nowDatasetSplit
            print(str(len(datasets))+')'+' '+str(DatasetID)+' '+str(YearRef1)+' '+Author1+' '+str(fullCode)+' '+lastDataset['DatasetSplit'])
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
#        print(str(ii)+'/'+str(lx)+') '+str(fullCode)+' '+str(DatasetID)+' '+str(YearRef1)+' '+Author1+" x:"+str(xx)+" y:"+str(yy)+" dy:"+str(dyy)+" dx:"+str(dxx)+" ee:"+str(ee)+" dee:"+str(dee))
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
