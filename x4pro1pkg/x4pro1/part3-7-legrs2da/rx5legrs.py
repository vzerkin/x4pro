"""
 **********************************************************************
 * Copyright: (C) 2021-2022 International Atomic Energy Agency (IAEA) *
 * Author: Viktor Zerkin, V.Zerkin@iaea.org, (IAEA-NDS)               *
 **********************************************************************
"""

import math

def getX4SqlSearch_DA_LEGRS(target,react,Enstr):
    print("___getX4SqlSearch_DA_LEGRS:",target,react,Enstr)

    addWhere=""
    if (target.upper()=='CU-0') and (react.upper()=='N,EL'): #test case: fast
        addWhere=(""
	+" and (t1.DatasetID='11749005' or t1.DatasetID='40940008') \n"
	+" and (t2.DatasetID='11749006' or t2.DatasetID='40940002') \n"
	)
    #addWhere="" #slow: ~45sec on complete EXFOR database
    sql=(""
	+"select t1.Entry                                           \n"
	+" ,t1.DatasetID,t2.DatasetID as DS2                        \n"
	+" ,t1.Target,t1.Reaction                                   \n"
	+" ,t1.YearRef1,t1.nAuthors                                 \n"
	+" ,t1.Author1Ini,t1.Author1                                \n"
	+" ,t1.fullCode,t1.iPoint                                   \n"
	+" ,t1.zaTarget1,t1.zaIncident1                             \n"
	+" ,t1.Projectile,t1.sProd,t1.sTarg                         \n"
	+" ,t2.fullCode as R2                                       \n"
	+" ,t1.MF as MF ,t1.MT as MT                                \n"
	+" ,t2.MF as MF2,t2.MT as MT2                               \n"
	+" ,t1.y as LEGRS,t1.dy as dLEGRS                           \n"
	+" ,t2.y as Sig,t2.dy as dSig                               \n"
	+" ,t1.x1 as En,t1.dx1 as dEn,t1.dx1 as dEn2                \n"
	+" ,t1.x2 as number                                         \n"
	+" from uni1 as t1                                          \n"
	+" inner join uni1 as t2 on t1.Entry=t2.Entry               \n"
	+"       and t1.x1=t2.x1                                    \n"
	+" where 1=1                                                \n"
	+" and (t1.Target like '"+target+"')                        \n" #
	+" and (t1.Reaction like '"+react+"')                       \n" #
	+" and (t1.SF58 like ',DA,,LEG/RS')                         \n" #
	+" and (t2.SF58 like ',SIG')                                \n" #
	+" and (t2.Target=t1.Target)                                \n" #
	+" and (t2.Reaction=t1.Reaction)                            \n" #
#	+" and (t1.DatasetID='11749005' or t1.DatasetID='40940008') \n"
#	+" and (t2.DatasetID='11749006' or t2.DatasetID='40940002') \n"
	+addWhere+"\n"
	+Enstr+"\n"
	+" order by t1.fullCode,t1.YearRef1 desc                    \n"
	+" ,t1.DatasetID,En,number                                  \n"
	)

    #print("SQL:\n"+sql)
    return sql

def rows2legrs(rows):
    lx=len(rows)
    datasets=[]
    ii=0; lastDatasetSplit=''; lastDataset={}
    print('\n___rows2legrs::datapoints:',len(rows))
    for row in rows:
        fullCode=row['fullCode']; DatasetID=row['DatasetID']; iPoint=row['iPoint'];DS2=row['DS2']
        YearRef1=row['YearRef1']; Author1Ini=row['Author1Ini']; Author1=row['Author1'];
        En=row['En'];		dEn=row['dEn']
        Sig=row['Sig'];		dSig=row['dSig']
        LEGRS=row['LEGRS'];     dLEGRS=row['dLEGRS']
        #dSig=None #debug
        #dLEGRS=None #debug
        number=row['number']
        if En is None: continue;
        if Sig is None: continue;
        if LEGRS is None: continue;
        if number is None: continue;
        number=int(number)
        if Author1Ini is not None: Author1=Author1Ini+Author1
        nowDatasetSplit=DatasetID+' Ei:'+str(En)
        if nowDatasetSplit!=lastDatasetSplit:
            lastDataset={}
            lastDataset['DatasetID']=DatasetID
            lastDataset['DatasetCorel']=DS2
            lastDataset['Reacode']=fullCode.replace("LEG/RS","LEG")
            lastDataset['En']=En
            lastDataset['dEn']=dEn
            lastDataset['Sig']=Sig
            lastDataset['dSig']=dSig
            lastDataset['x4lbl']=str(YearRef1)+', '+str(Author1)
            lastDataset['DatasetSplit']='Ei='+str(En/1e6)+'MeV'
            lastDataset['LEG']=[]
            lastDataset['dLEG']=[]
            lastDataset['number']=[]
            datasets.append(lastDataset);
            lastDatasetSplit=nowDatasetSplit
            print('#DS:'+str(len(datasets))+') '+str(fullCode)+' '+str(YearRef1)+' '+Author1+' #'+nowDatasetSplit+' Ei:'+str(En/1e6)+'MeV')
        if len(lastDataset['number'])<=0:
            lastDataset['number'].append(0)
            lastDataset['LEG'].append(Sig/(4*math.pi))
            rr=dSig
            if (dSig is not None): rr=rr/(4*math.pi)
            lastDataset['dLEG'].append(rr)
        lastDataset['number'].append(number)
        lastDataset['LEG'].append(LEGRS)
        lastDataset['dLEG'].append(dLEGRS)
        ii+=1
        print(' pt:'+str(ii)+'/'+str(lx)+')'
	#+' '+str(fullCode)
	#+' '+str(DatasetID)+' '+str(YearRef1)+' '+Author1
	#+" En:"+str(En/1e6)+"MeV"
	+" L:"+str(number)+"   y:"+str(LEGRS)+"\tdy:"+str(dLEGRS)+"\tSig:"+str(Sig)
	+"\tarray:"+str(len(lastDataset['LEG']))
	)
    return datasets


def calcLegrsDatasets2da4plot(datasets):
    lx=len(datasets)
    print('\n___calcLegrsDatasets2da4plot::Datasets:',len(datasets))
    outdatasets=[]
    ii=0
    for dataset in datasets:
        print('______Dataset:'+str(ii+1)+'/'+str(lx)+')'
	+' '+str(dataset['DatasetID'])+' Ei:'+str(dataset['En']/1e6)+'MeV '
	+'\tnum:'+str(dataset['number'])+' LEGRS:'+str(dataset['LEG']))
        calcLegrsDatasets2da(dataset)
        outdatasets.append(dataset);
        ii+=1
    return outdatasets

def calcLegrsDatasets2da(dataset):
    En=dataset['En']
    nums=dataset['number']
    W=dataset['LEG']
    dW=dataset['dLEG']
#    print('______calcLegrsDatasets2da::Dataset:'+str(dataset['DatasetID'])
#	+' Ei:'+str(dataset['En']/1e6)+'MeV '
#	+'\tnum:'+str(dataset['number'])+' LEGRS:'+str(dataset['LEG']))
    x=[];     dataset['x']=x
    y=[];     dataset['y']=y
    dy=[];    dataset['dy']=dy
    num=max(nums)
    lnum=len(nums)
    for adeg in range(0,181,6):
        mu=math.cos(adeg*math.pi/180)
        P=calcLegPol(mu,num)
        sum=1
        for i in range(1,lnum,1):
            n=nums[i]
            sum=sum+W[i]*P[n]
        f=sum*W[0]
        df=None
        if (dW[0] is not None): #https://en.wikipedia.org/wiki/Propagation_of_uncertainty
            sum=math.pow(dW[0]/W[0]*f,2)
            for i in range(1,lnum,1):
                n=nums[i]
                if (dW[i] is not None): sum=sum+math.pow(dW[i]*P[n],2)
            df=W[0]*math.sqrt(sum)
        f=round(f,7)
        if df is not None: df=round(df,7)
        x.append(adeg)
        y.append(f)
        dy.append(df)
        print('-0-outDA_AN:En:'+str(En)+' an:'+str(adeg)+' f:'+str(f)+' df:'+str(df)+' df%:'+strproc(df,f))
    return True

def calcLegPol(x,n):
    P=[]
    P.append(1)
    if (n<1): return P
    P.append(x)
    if (n<2): return P
    for i in range(2,n+1,1):
        pp=((2*i-1)*x*P[i-1] - (i-1)*P[i-2])/i
        #print('\tP:cos(an):'+str(x)+'\tan:'+str(math.acos(x)/math.pi*180)+' i:'+str(i)+'/'+str(n)+' pp:'+str(pp)+' p[i-1]:'+str(P[i-1])+' p[i-2]:'+str(P[i-2]))
        P.append(pp)
    #print('')
    return P

def strproc(dy,yy):
    if (dy is None): return 'None'
    if (yy is None): return 'None'
    if (yy==0): return 'Inf'
    dyr=dy/yy*100
    str1=str(dyr)
    str1=f'{dyr:.2f}'
    return str1
