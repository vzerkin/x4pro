"""
 **********************************************************************
 * Copyright (c) 2021-2026 Viktor Zerkin, v.zerkin@gmail.com          *
 * Author:   Viktor Zerkin, PhD, IAEA-NDS(1999-2023), NRDC(1999-2026) *
 * License:  MIT License (MIT)                                        *
 **********************************************************************
"""

import sys
import math
import json
sys.path.append('./')
sys.path.append('../')
from fort2pfns import *

MxwCur=None #Maxwellian distribution

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
#??	"14854002"	: 1.041	, #92-U-235(N,F),PR,NU/DE  Pt:47   2025, B.Mauss En=7.4MeV  "1.041" makes it compatible with LSTTAB-code
	"40740002"	: 5.07	, #92-U-238(N,F),PR,NU/DE  Pt:62   1979, V.Ya.Baryba En=14.3MeV, see: 40740003:DATA=5.07(PRT/FIS)
	"30426002"	: 0.1	, #???
	"41611010z"	: 2.49	, #test, see in EXFOR: MONIT(PRT/FIS)=2.49
}

def datasets2mxwRatio(datasets,oper,renorm2shapeOnly=False,Tm=1.32e6):
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
        dataset2mxwRatio(dataset,renorm2shapeOnly=renorm2shapeOnly,Tm=Tm)
        dssout.append(dataset)
    return dssout

def dataset2mxwRatio(dataset,renorm2shapeOnly=False,Tm=1.32e6):
    SF8=dataset['SF8']
    if dataset['Reacode'].find('MXD')>0: #Mxw ratio already given in EXFOR: keep it
        dataset['x4lbl']+=" /ratio/"
        return False
    typ=" /shape:"+dataset['SF8'].lower()+"/"
    fx=dataset['fx']
    fy=dataset['fy']
    xx=dataset['x']
    dxx=dataset['dx']
    yy=dataset['y']
    dyy=dataset['dy']
    nuTxt=None
    FSP=None #apply only shape re-normalisation
    if not renorm2shapeOnly:
        FSP=getAbs2MxwFactor(dataset)  #try to get Abs2Mxw Factor
        if FSP is not None:
            typ=" /abs/"
            if SF8!='': typ=" /abs:"+dataset['SF8'].lower()+"/"
            if FSP!=1: nuTxt=format(1/FSP,"<.3g").strip()
            else: nuTxt='/1/'
    if FSP is None:
#       FSP=getShape2MxwFactor_00(xx,yy,fx,fy,Tm)
#       FSP=getShape2MxwFactor_01(xx,dxx,yy,fx,fy,Tm)
        FSP=getShape2MxwFactor(xx,dxx,yy,fx,fy,Tm)
#       FSP=getShape2MxwFactor_00log(xx,yy,fx,fy,Tm)
    print ('  PFNS re-normalisation to Maxwellian',FSP,dataset['yBasicUnits'])
    print('---dataset2mxwRatio---Target:['+dataset['Target']+'] 1/FSP='+str(1/FSP))
    if dataset['DatasetID']=="32587002": FSP/=1.1
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
    dataset['x4lbl']+=typ
    dataset['x4lbl']+=" T="+format(Tm/1e6,"<.5g").strip()+"MeV"
    if nuTxt is not None:
        dataset['x4lbl']+=" &#957;="+nuTxt
    return True

def getMaxw(E,T):
    fc=(2/T)*math.sqrt(E/(math.pi*T))*math.exp(-E/T)
#   fc=2/math.sqrt(math.pi*T*T*T)*math.sqrt(E)*math.exp(-E/T)
#   print('---getMaxw\t'+' E:'+format(E,"<11.5g")+' fc:'+format(fc,"<11.5g"))
    return fc

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

def getShape2MxwFactor(xx,dxx,yy,fx,fy,Tm):
    global MxwCur
    FSP=1
    if len(xx)<=0: return FSP
#-- Energy: MeV --> eV
#-- Calculate the ratio to Maxwellian
    ii=0; EP=[]; FP=[]
    while ii<len(xx):
        ee=xx[ii]*fx
        ff=getMaxw(ee,Tm)
        EP.append(ee)
        FP.append(yy[ii]/ff)
        ii+=1
#-- test output
#   for ii,ee in enumerate(EP): print('-0-',ii,EP[ii],FP[ii])
#-- Prepare Maxwellian spectrum
    if MxwCur is None:
        MxwCur=generateMxwCur(TMXW=Tm)
        #-- test output
        with open("mxwCurve.json","w") as FF: json.dump(MxwCur,FF,indent=1)
#-- Adopt parameters preparing interpolation and integration
    KP=len(EP)
    EA=EP[0]
    EB=EP[KP-1]
    ES=MxwCur['ENR']
    SG=MxwCur['XSP']
    NP=len(ES)
#-- Integrate Maxwellian in the range of experim. data
    SC=YTGPNT(NP,ES,SG,EA,EB)
    print('-1-',NP,EA,EB,'SC:',SC)
#-- Interpolate the ratio to the function grid
    RWO=FITGRD(KP,EP,FP,NP,ES)
#-- Restore the function values
    for ii,ee in enumerate(ES):
        ff=getMaxw(ee,Tm)
        RWO[ii]*=ff
#-- Integrate the function in the range of experim. data
    SP=YTGPNT(NP,ES,RWO,EA,EB)
    print('-1-','NP:',NP,'EA:',EA,'EB:',EB,'SP:',SP,'SC/SP:',SC/SP)
    if SP>0: FSP=SC/SP
    return FSP
