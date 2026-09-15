"""
 **********************************************************************
 * Copyright (c) 2021-2026 Viktor Zerkin, v.zerkin@gmail.com          *
 * Author:   Viktor Zerkin, PhD, IAEA-NDS(1999-2023), NRDC(1999-2026) *
 * License:  MIT License (MIT)                                        *
 **********************************************************************
"""

import math
import sys
sys.path.append('./')
sys.path.append('../')
import json

delBlackList={
   "14682002"	:"94-PU-239(N,F),PR,NU/DE,,NPD En=14.5MeV 2020 Kelly",
#  "14379002"	:"94-PU-239(N,F),PR,NU/DE Pt:28   2014, A.Chatillon En=14.2MeV",
}

stdNubar=None
stdNubarFile='nubar-endf.json'
absNubarList={
    "41332002"	: 1	, #93-NP-237(N,F),PR,NU/DE Pt:44   2000, N.V.Kornilov En=0.52MeV
    "14379002"	: 1	, #94-PU-239(N,F),PR,NU/DE Pt:28   2014, A.Chatillon En=14.2MeV
    "14430002"	: 1	, #94-PU-239(N,F),PR,NU/DE Pt:11   2014, J.P.Lestone En=1.5MeV
    "14854002"	: 1	, #92-U-235(N,F),PR,NU/DE  Pt:47   2025, B.Mauss En=7.4MeV
    "40740002"	: 5.07	, #92-U-238(N,F),PR,NU/DE  Pt:62   1979, V.Ya.Baryba En=14.3MeV, see: 40740003:DATA=5.07(PRT/FIS)
}

def datasets2mxwRatio(datasets,oper,Tm=1.32e6):
    print('--0--datasets2mxwRatio: datasets:'+str(len(datasets))+' oper:'+str(oper)+' Tm:'+str(Tm))
    lx=len(datasets)
    dssout=[]
    for ii,dataset in enumerate(datasets):
        print('\tDataset:'+str(ii)+'/'+str(lx)+') '+str(dataset['Reacode'])+' '+str(dataset['DatasetID'])
	+' Pt:'+str(len(dataset['x'])).ljust(4)+' '+str(dataset['x4lbl'])
	)
        if dataset['DatasetID'] in delBlackList:
            print('---Dataset in delBlackList:',dataset['DatasetID'],' [',dataset['x4lbl']+']')
            continue
#       dataset2mxwRatio(dataset)
        dataset2mxwRatio(dataset,renorm2maxw=False,Tm=Tm)
        dssout.append(dataset)
    return dssout

def dataset2mxwRatio(dataset,renorm2maxw=True,Tm=1.32e6):
    if dataset['Reacode'].find('MXD')>0: return False
    fx=dataset['fx']
    fy=dataset['fy']
    xx=dataset['x']
    dxx=dataset['dx']
    yy=dataset['y']
    dyy=dataset['dy']
    nuTxt=None
    FSP=None
    FSP=getAbs2MxwFactor(dataset)
    if FSP is not None:
        if FSP!=1: nuTxt=format(1/FSP,"<.3g").strip()
        else: nuTxt='/1/'
    if FSP is None:
        FSP=getShape2MxwFactor(xx,yy,fx,fy,Tm)
    print ('  PFNS re-normalisation to Maxwellian',FSP,dataset['yBasicUnits'])
    print('---dataset2mxwRatio---Target:['+dataset['Target']+'] 1/FSP='+str(1/FSP))
    for ii,x in enumerate(xx):
        ee=xx[ii]*fx
        yy[ii]*=FSP
        y00=yy[ii]
        if dyy[ii] is not None: dyy[ii]*=FSP
        FC=getMaxw(ee,Tm)
        yy[ii]=yy[ii]/FC
        yy[ii]=float(format(yy[ii],".5e"))
        if dyy[ii] is not None: dyy[ii]=dyy[ii]/FC; dyy[ii]=float(format(dyy[ii],".5e"))
        print('\t'+format(ii,"5d")+') E:'+format(ee,"<11.5g")+' FC:'+format(FC,"<11.5g")+' y0:'+format(y00,"<11.5g")+' yy:'+format(yy[ii],"<11.5g"))
    dataset['Quantity']="PFNS Ratio to Maxwellian (T="+str(Tm/1e6)+'MeV)'
    dataset['yBasicUnits']='no-dim'
    dataset['fy']=1
    dataset['x4lbl']+=" T:"+format(Tm/1e6,"<.5g").strip()+"MeV"
    if nuTxt is not None:
        dataset['x4lbl']+=" &#957;="+nuTxt
    return True

def getMaxw(E,T):
    fc=(2/T)*math.sqrt(E/(math.pi*T))*math.exp(-E/T)
#   fc=2/math.sqrt(math.pi*T*T*T)*math.sqrt(E)*math.exp(-E/T)
    return fc

def getShape2MxwFactor(xx,yy,fx,fy,Tm,getVal=getMaxw):
    #---2026-09-15, ZV: doubtful, needs to be worked out
    FSP=1
    #---copy from LSTTAB.F (by A.Trkov:EndVer/Empire-codes)
    SSP=0 #---integral over points as given in the dataset
    SSG=0 #---integral of Maxwellian on the same E-grid
    for ii,x in enumerate(xx):
        e2=xx[ii]*fx
        f2=yy[ii]*fy
        g2=getVal(e2,Tm)
        if ii==0:
            e1=e2; f1=f2; g1=g2
        else:
            SSP+=(e2-e1)*(f2+f1)/2
            SSG+=(e2-e1)*(g2+g1)/2
    if SSP>0: FSP=SSG/SSP
    return FSP

def getAbs2MxwFactor(dataset):
    FC=None
    if dataset['yBasicUnits']!='PC/FIS/MEV': return None
    if dataset['DatasetID'] in absNubarList:
        nubar=absNubarList[dataset['DatasetID']]
        print('---getAbs2MxwFactor---Dataset in absNubarList:',dataset['DatasetID'],' [',dataset['x4lbl']+'] nubar='+str(nubar))
        if nubar<=0: return None
        FC=1/nubar
        return FC
    Target=dataset['Target']
    En=dataset.get('En')
    if En is None: En=dataset.get('Spe')
    nubar=getNubar(Target,En)
    print('---getAbs2MxwFactor.Target:',Target,' En:',En,' Nubar:',nubar)
    if nubar is None: return None
    FC=1/nubar
    return FC

def getNubar(Target,En):
    global stdNubar
    if stdNubar is None:
        try:
            with open(stdNubarFile, encoding='utf-8') as F:
                stdNubar=json.loads(F.read())
        except Exception as e:
            print("===Exception==="+str(e))
            return None
    obj0=stdNubar.get(Target)
    if obj0 is None: return None
    arr=obj0.get('x_y_dy_dx_fc')
    if arr is None: return None
    for ii,xy in enumerate(arr):
        e2=xy[0]; y2=xy[1]
        if ii==0:
            e1=e2; y1=y2
            if En<e1: return None
            continue
        else:
            if En<e2:
                y=y1+(y2-y1)*(En-e1)/(e2-e1)
                return y
    return None
