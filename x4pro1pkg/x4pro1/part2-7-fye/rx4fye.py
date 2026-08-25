"""
 **********************************************************************
 * Copyright: (c) 2021-2023 International Atomic Energy Agency (IAEA) *
 * Copyright: (c) 2023-2024 Viktor Zerkin (NRDC)                      *
 * Author: Viktor Zerkin, v.zerkin@gmail.com                          *
 **********************************************************************
"""

def getX4SqlSearchFY_ene(Target,Product,x4sqlparam=''):
    print("___getX4SqlSearchFY_ene:",Target,Product,x4sqlparam)
    andProd=" and prod like '%"+Product+"'"
    if (Product.endswith("-m")):  andProd=" and ((prod like '%"+Product+"') or (prod like '%"+Product+"1'))"
    if (Product.endswith("-m1")): andProd=" and ((prod like '%"+Product+"') or (prod like '%"+Product[:-1]+"'))"
    sql=str(""
	+"select *                                  \n"
	+" ,y  as FY, dy  as dFY                    \n"
	+" ,x1 as En, dx1 as dEn                    \n"
	+" ,x2 as zap                               \n"
	+"from uni2                                 \n"
	+"where Target like '"+Target+"'            \n"
#	+" and prod like '%"+Product+"'             \n"
	+andProd+"\n"
	+" and Reaction='N,F' and Quant='FY'        \n"
	+" and SF58='CUM,FY' and SF8=''             \n"
	+x4sqlparam+" "
	+"order by fullCode,YearRef1 desc,DatasetID \n"
	+" ,En,iPoint                               \n"
	)
    #print("SQL:\n"+sql)
    return sql

def getDatasets4plot(rows,multy=1e2,multx=1e-6):
    lx=len(rows)
    datasets=[]
    ii=0; lastDatasetSplit=''; lastDataset={}
    print('\ndatapoints:',len(rows))
    for row in rows:
        fullCode=row['fullCode']; DatasetID=row['DatasetID']; iPoint=row['iPoint']
        YearRef1=row['YearRef1']; Author1Ini=row['Author1Ini']; Author1=row['Author1'];
        yy=row['FY'];    dyy=row['dFY']
        xx=row['En'];    dxx=row['dEn']
        zap=row['zap']
        if xx is None: continue;
        if yy is None: continue;
        splt="ZAP:"+str(zap)
        splt=""
        if Author1Ini is not None: Author1=Author1Ini+Author1
        nowDatasetSplit=DatasetID+' '+str(splt)
        fullCode=fullCode.replace(",,,EXP",""); fullCode=fullCode.replace(",,EXP","")
        if nowDatasetSplit!=lastDatasetSplit:
            lastDataset={}
            lastDataset['DatasetID']=DatasetID
            #lastDataset['Reacode']=fullCode
            lastDataset['Reacode']=fullCode.replace('ELEM/MASS',row['prod'].upper())
            lastDataset['DatasetSplit']=splt
            lastDataset['prod']=row['prod'] #store to be used in plotTitle
            lastDataset['x4lbl']=str(YearRef1)+', '+str(Author1)
            x=[];     lastDataset['x']=x
            y=[];     lastDataset['y']=y
            dy=[];    lastDataset['dy']=dy
            dx=[];    lastDataset['dx']=dx
            datasets.append(lastDataset);
            lastDatasetSplit=nowDatasetSplit
            print(str(len(datasets))+')'+' '+str(DatasetID)+' '+str(YearRef1)+' '+Author1+' '+str(fullCode)+' '+lastDataset['DatasetSplit'])
        xx=float(xx)*multx; xx=float(format(xx,".5e")) #precision: 11 columns = 6 digits: 1.23456e-02
        yy=float(yy)*multy; yy=float(format(yy,".5e"))
        if dyy is not None:
            dyy=float(dyy)*multy
            dyy=float(format(dyy,".5e"))
            if dyy<0: dyy=-dyy
        if dxx is not None:
            dxx=float(dxx)*multx
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
