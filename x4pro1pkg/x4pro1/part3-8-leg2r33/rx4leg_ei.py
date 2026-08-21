"""
 **********************************************************************
 * Copyright: (C) 2021-2022 International Atomic Energy Agency (IAEA) *
 * Author: Viktor Zerkin, V.Zerkin@iaea.org, (IAEA-NDS)               *
 **********************************************************************
"""

import math

def getX4SqlSearch_DA_LEG(target,react,Enstr):
    print("___getX4SqlSearch_DA_LEG:",target,react)

    addWhere=""
    if (target.upper()=='LI-6') and (react.upper()=='P,HE3'): #test case: fast
        addWhere=(""
	+" and (t1.DatasetID='F0012004') \n"
	)

    sql=(""
	+"select t1.Entry                        \n"
	+" ,t1.DatasetID                         \n"
	+" ,t1.Target,t1.Reaction                \n"
	+" ,t1.YearRef1,t1.nAuthors              \n"
	+" ,t1.Author1Ini,t1.Author1             \n"
	+" ,t1.fullCode,t1.iPoint                \n"
	+" ,t1.zaTarget1,t1.zaIncident1          \n"
	+" ,t1.Projectile,t1.sProd,t1.sTarg      \n"
	+" ,t1.MF as MF ,t1.MT as MT             \n"
	+" ,t1.y as LEG,t1.dy as dLEG            \n"
	+" ,h0.cm as LEG_CM                      \n"
	+" ,t1.x1 as En,t1.dx1 as dEn            \n"
	+" ,t1.x2 as number                      \n"
	+" from uni1 as t1                       \n"
	+" inner join x4pro_hdr as h0            \n"
	+" on h0.DatasetID=t1.DatasetID and h0.typ='c' and h0.ihdr=0\n"
	+" where 1=1                             \n"
	+" and (t1.Target like '"+target+"')     \n"
	+" and (t1.Reaction like '"+react+"')    \n"
	+" and (t1.SF58 like ',DA,,LEG') and (t1.SF8 like 'LEG')\n"
	+addWhere+"\n"
	+Enstr+"\n"
	+" order by t1.fullCode,t1.YearRef1 desc \n"
	+" ,t1.DatasetID,En,number               \n"
	)

    #print("SQL:\n"+sql)
    return sql

def rows2leg(rows):
    lx=len(rows)
    datasets=[]
    ii=0; lastDatasetSplit=''; lastEnSplit=''; lastDataset={}
    print('\n__rows2leg::datapoints:',len(rows))
    for row in rows:
        fullCode=row['fullCode']; DatasetID=row['DatasetID']; iPoint=row['iPoint']
        YearRef1=row['YearRef1']; Author1Ini=row['Author1Ini']; Author1=row['Author1'];
        En=row['En'];		dEn=row['dEn']
        LEG=row['LEG'];         dLEG=row['dLEG']
        LEG_CM=row['LEG_CM']
        #dLEG=None #debug
        number=row['number']
        zaTarget1=row['zaTarget1']
        zaIncident1=row['zaIncident1']
        if En is None: continue;
        if LEG is None: continue;
        if number is None: continue;
        number=int(number)
        if Author1Ini is not None: Author1=Author1Ini+Author1
        nowDatasetSplit=DatasetID
        nowEnSplit=DatasetID+' Ei:'+str(En)
        if nowDatasetSplit!=lastDatasetSplit:
            lastDataset={}
            lastDataset['DatasetID']=DatasetID
            lastDataset['YearRef1']=YearRef1
            lastDataset['Author1']=Author1
            lastDataset['zaIncident1']=zaIncident1
            lastDataset['zaTarget1']=zaTarget1
            lastDataset['Reacode']=fullCode.replace(",EXP","")
            lastDataset['x4lbl']=str(Author1)+'('+str(YearRef1)+')'
            lastDataset['LEG_CM']=LEG_CM
            lastDataset['arrEn']=[]
            datasets.append(lastDataset);
            lastDatasetSplit=nowDatasetSplit
            print('DS:'+str(len(datasets))+') '+str(fullCode)+' '+str(YearRef1)+' '+Author1+' #'+nowDatasetSplit)
        if nowEnSplit!=lastEnSplit:
            lastEn={}
            lastEn['En']=En
            lastEn['dEn']=dEn
            lastEn['number']=[]
            lastEn['LEG']=[]
            lastEn['dLEG']=[]
            lastDataset['arrEn'].append(lastEn);
            lastEnSplit=nowEnSplit
            print('DS:'+str(len(datasets))+') '+str(fullCode)+' '+str(YearRef1)+' '+Author1+' #'+nowDatasetSplit+' Ei:'+str(En/1e6)+'MeV')
        lastEn['number'].append(number)
        lastEn['LEG'].append(LEG)
        lastEn['dLEG'].append(dLEG)
        ii+=1
        print(' pt:'+str(ii)+'/'+str(lx)+')'
	#+' '+str(fullCode)
	#+' '+str(DatasetID)+' '+str(YearRef1)+' '+Author1
	#+" En:"+str(En/1e6)+"MeV"
	+" L:"+str(number)+"   LEG:"+str(LEG)+"\tdLEG:"+str(dLEG)
	+"\tarrEn:"+str(len(lastDataset['arrEn']))
	)
    return datasets


def calcLegDatasets2da4plot(ang,datasets,fx=1e-6,fy=1e3,noCM=False):
    lx=len(datasets)
    print('\n___calcLegrsDatasets2da4plot::Datasets:',len(datasets))
    outdatasets=[]
    ii=0
    for dataset in datasets:
        if (noCM and dataset['LEG_CM']!=0): continue
        calcLegrsDatasets2da(ang,dataset,fx,fy)
        outdatasets.append(dataset);
        ii+=1
        print('\tDataset:'+str(ii)+'/'+str(lx)+')'
	#+' '+str(Reacode)
	+' '+str(dataset['DatasetID'])+' Ei:'+str(len(dataset['arrEn']))
	+' CM:'+str(dataset['LEG_CM'])
	)
    return outdatasets

def calcLegrsDatasets2da(ang,dataset,fx=1e-6,fy=1e3):
    x=[];     dataset['x']=x
    y=[];     dataset['y']=y
    dy=[];    dataset['dy']=dy
    dx=[];    dataset['dx']=dx
    mu=math.cos(ang*math.pi/180)
    arrEn=dataset['arrEn']
    dataset['ang']=ang
    dataset['DatasetSplit']='An='+str(ang)+'deg'
    for objEn in arrEn:
        En=objEn['En']
        #print('---En:',En)
        dEn=objEn['dEn']
        if dEn is None: dEn=0
        nums=objEn['number']
        Ai=objEn['LEG']
        dAi=objEn['dLEG']
        maxnum=max(nums)
        P=calcLegPol(mu,maxnum)
        sum=0; dsum=0 #https://en.wikipedia.org/wiki/Propagation_of_uncertainty
        lnum=len(nums)
        for i in range(0,lnum,1):
            n=nums[i]
            sum=sum+Ai[i]*P[n]
            if (dAi[i] is not None): dsum=dsum+math.pow(dAi[i]*P[n],2)
        f=sum
        df=math.sqrt(dsum)
        xx=round(En*fx,7)
        yy=round(f*fy,7)
        dyy=round(df*fy,7)
        dxx=round(dEn*fx,7)
        x.append(xx)
        y.append(yy)
        dy.append(dyy)
        dx.append(dxx)
#        print('outDA_AN::'+' an:'+str(ang)+' En:'+str(xx)+' L:'+str(maxnum)+' y:'+str(yy)+' dy:'+str(dyy))

    return True

def calcLegPol(x,n):
    P=[]
    P.append(1)
    if (n<1): return P
    P.append(x)
    if (n<2): return P
    for i in range(2,n+1,1):
        pp=((2*i-1)*x*P[i-1] - (i-1)*P[i-2])/i
        #print('\tPL:x:'+str(x)+' n:'+str(n)+' i:'+str(i)+' pp:'+str(pp)+' p[i-1]:'+str(P[i-1])+' p[i-2]:'+str(P[i-2]))
        P.append(pp)
    return P
