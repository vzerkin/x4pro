"""
 **********************************************************************
 * Copyright: (C) 2021-2022 International Atomic Energy Agency (IAEA) *
 * Author: Viktor Zerkin, V.Zerkin@iaea.org, (IAEA-NDS)               *
 **********************************************************************
"""

def getX4SqlSearch_NUBAR(target,react,sf58,x4sqlparam):
    print("---getX4SqlSearch_NUBAR:",target,react,sf58,x4sqlparam)
    whereReact=addStrToWhere('Reaction',react)
    sql=str(""
	+"select *                                  \n"
	+" ,y  as YY, dy  as dYY                    \n"
	+" ,x1 as En, dx1 as dEn                    \n"
	+"from uni1                                 \n"
	+"where                                     \n"
	+" Target like '"+target+"'                 \n"
#	+" and Reaction like '"+react+"'            \n"
	+whereReact+" \n"
	+" and SF58 like '"+sf58+"'                 \n"
	+" and x2 is null                           \n"
	+x4sqlparam+" \n"
	+"order by fullCode,YearRef1 desc,DatasetID \n"
	+" ,En,iPoint                               \n"
	)
#   print("SQL:\n"+sql)
    return sql

def getDatasets4plot(rows,fx=1,fy=1):
    lx=len(rows)
    datasets=[]
    ii=0; lastDatasetSplit=''; lastDataset={}
    print('\ndatapoints:',len(rows))
    for row in rows:
        fullCode=row['fullCode']; DatasetID=row['DatasetID']; iPoint=row['iPoint']
        YearRef1=row['YearRef1']; Author1Ini=row['Author1Ini']; Author1=row['Author1'];
        Target=row['Target']; Reaction=row['Reaction'];
        yy=row['YY'];    dyy=row['dYY']
        xx=row['En'];    dxx=row['dEn']
        if xx is None: continue;
        if yy is None: continue;
        if Author1Ini is not None: Author1=Author1Ini+Author1
        nowDatasetSplit=DatasetID
        fullCode=fullCode.replace(",,,EXP",""); fullCode=fullCode.replace(",,EXP","")
        if nowDatasetSplit!=lastDatasetSplit:
            lastDataset={}
            lastDataset['DatasetID']=DatasetID
            lastDataset['Reacode']=fullCode
            lastDataset['Target']=Target
            lastDataset['Reaction']=Reaction
            lastDataset['x4lbl']=str(YearRef1)+', '+str(Author1)
            x=[];     lastDataset['x']=x
            y=[];     lastDataset['y']=y
            dy=[];    lastDataset['dy']=dy
            dx=[];    lastDataset['dx']=dx
            datasets.append(lastDataset);
            lastDatasetSplit=nowDatasetSplit
            print(str(len(datasets))+')'+' '+str(DatasetID)+' '+str(YearRef1)+' '+Author1+' '+str(fullCode))
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
    typeEntries(datasets)
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

def typeEntries(datasets):
    entries=[]
    for dataset in datasets:
        entry=dataset['DatasetID'][:5]
        if entry not in entries: entries.append(entry)
    entries=sorted(entries)
    print('---ENTRY: ',end='')
    for ii,entry in enumerate(entries):
#       if ii>0: print(';',end='')
#       print(entry,end='')
        print(entry+'*;',end='')
    print('')
    return entries

def addStrToWhere(field,str0,end=''):
    if str0 is None: return ''
    strs=str0.split(";")
    str1=addArrToWhere(field,strs,end)
    return str1

def addArrToWhere(field,arr,end='\n'):
    where=""
    if len(arr)>0:
        where+=" and ("+end
        for ii,value1 in enumerate(arr):
            if (ii!=0): where+=" or"
            else:       where+=" "
            value1=value1.replace('*','%')
            where+=" ("+field+" like '"+value1+"')"+end
        where+=" )"
    return where
