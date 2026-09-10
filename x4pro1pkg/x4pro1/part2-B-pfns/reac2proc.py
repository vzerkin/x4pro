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

def datasets2mxwRatio(datasets,oper):
    print('--0--treatDatasets: datasets:'+str(len(datasets))+' oper:'+str(oper))
    lx=len(datasets)
    dssout=[]
    for ii,dataset in enumerate(datasets):
        print('\tDataset:'+str(ii)+'/'+str(lx)+') '+str(dataset['Reacode'])+' '+str(dataset['DatasetID'])
	+' Pt:'+str(len(dataset['x'])).ljust(4)+' '+str(dataset['x4lbl'])
	)
        dataset2mxwRatio(dataset)
        dssout.append(dataset)
    return dssout

def dataset2mxwRatio(dataset,renorm2maxw=True,TMxw=1.32e6):
    if dataset['Reacode'].find('MXD')>0: return False
    fx=dataset['fx']
    fy=dataset['fy']
    xx=dataset['x']
    dxx=dataset['dx']
    yy=dataset['y']
    dyy=dataset['dy']
    FSP=1
    if renorm2maxw:
        FSP=getIntegralsRatio(xx,yy,fx,fy,TMxw)
        print ('  PFNS re-normalisation to Maxwellian',FSP)
    print('---dataset2mxwRatio---Target:['+dataset['Target']+'] 1/FSP='+str(1/FSP))
    for ii,x in enumerate(xx):
        ee=xx[ii]*fx
        yy[ii]*=FSP
        y00=yy[ii]
        if dyy[ii] is not None: dyy[ii]*=FSP
        FC=getMaxw(ee,TMxw)
        yy[ii]=yy[ii]/FC
        if dyy[ii] is not None: dyy[ii]=dyy[ii]/FC
#        yy[ii]=FC
#        if dyy[ii] is not None: dyy[ii]=0
        print('\t'+format(ii,"5d")+') E:'+format(ee,"11.5e")+' FC:'+format(FC,"11.5e")+' y0:'+format(y00,"11.5e")+' yy:'+format(yy[ii],"11.5e"))
    dataset['Quantity']="PFNS Ratio to Maxwellian (T="+str(TMxw/1e6)+'MeV)'
    dataset['yBasicUnits']='no-dim'
    dataset['fy']=1
    return True

def getMaxw(E,T):
    fc=(2/T)*math.sqrt(E/(math.pi*T))*math.exp(-E/T)
#   fc=2/math.sqrt(math.pi*T*T*T)*math.sqrt(E)*math.exp(-E/T)
    return fc

def getIntegralsRatio(xx,yy,fx,fy,TMxw,getVal=getMaxw):
    FSP=1
    SSP=0; SSG=0
    for ii,x in enumerate(xx):
        e2=xx[ii]*fx
        f2=yy[ii]*fy
        g2=getVal(e2,TMxw)
        if ii==0:
            e1=e2; f1=f2; g1=g2
        else:
            SSP+=(e2-e1)*(f2+f1)/2
            SSG+=(e2-e1)*(g2+g1)/2
    if SSP>0: FSP=SSG/SSP
    return FSP
