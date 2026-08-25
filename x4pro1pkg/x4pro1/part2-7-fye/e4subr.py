"""
 **********************************************************************
 * Copyright: (C) 2021-2023 International Atomic Energy Agency (IAEA) *
 * Author: Viktor Zerkin, V.Zerkin@iaea.org, (IAEA-NDS)               *
 **********************************************************************
"""
import sys
sys.path.append('./')
sys.path.append('../')
from websubr import *
import json

eweb0prog='/e4list?'
eweb1prog='/e4fy?'

def get_elist_fy(Target,Reaction,debug=False):
    #print('---get_elist_fy---')
    params='Target='+Target
    params+='&Reaction='+Reaction
    params+='&json'
    datasets=[]
    txt=wget_nds(eweb0prog,params)
    if txt is None: return datasets
    if debug: print('txt='+txt)
    obj1=json.loads(txt)
    print('   format:'+obj1['format'])
    list1=obj1.get('sections')
    if list1 is not None: datasets=list1
    return datasets


def get_e4fy(SectID):
#    print('---get_e4fy---'+str(SectID))
    params='SectID='+str(SectID)
    params+='&json'
    txt=wget_nds(eweb1prog,params)
    #print('\n\n\n---txt::\n'+txt)
    return txt

def e4fy2json(txt):
    obj1=json.loads(txt)
    return obj1

def e4fy2prod2data(obj1,Prod,mev=1e-6,proc=100):
#    print('---e4fy2prod2data---')
    xx=[];dxx=[];yy=[];dyy=[]
    obj1['x']=xx;
    obj1['dx']=dxx;
    obj1['y']=yy;
    obj1['dy']=dyy;
    obj1['idy']=0;
    datasets=obj1.get('datasets')
#    print(datasets)
    if datasets is None: return obj1
#    print('edatasets:'+str(len(datasets)))
    Prod=Prod.lower()
    Prod=Prod.replace('-m2','n').replace('-m3','o')
    Prod=Prod.replace('-m1','m').replace('-m','m')
    Prod=Prod.replace('-g','')
    for dataset in datasets:
        ene=dataset.get('Ei')
        ene=round(ene*mev,7)
#        print('ene:'+str(ene))
        Products=dataset.get('FYs')
        if Products is None: continue
        for Product in Products:
            Nucl=Product.get('PROD')
            if Nucl is None: continue
            if Nucl.lower()!=Prod.lower(): continue
            y=Product.get('FY')
            if y is None: continue
            dy=Product.get('DFY')
            if dy is None: dy=0
            else: obj1['idy']+=1;
            y=round(y*proc,7)
            dy=round(dy*proc,7)
            xx.append(ene)
            dxx.append(0)
            yy.append(y)
            dyy.append(dy)
    return obj1
