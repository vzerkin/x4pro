"""
 *******************************************************************************
 * Copyright: (C) 2021-2023 International Atomic Energy Agency (IAEA)          *
 * Copyright: (C) 2023-2026 Viktor Zerkin, Vienna, Austria                     *
 * Author: Viktor Zerkin, v.zerkin@gmail.com, IAEA(1999-2023), NRDC(1996-2026) *
 *******************************************************************************
"""

import sys
sys.path.append('./')
sys.path.append('../')
from websubr import *
import json

web0prog='/servlet/E4sSearch2?'
web1prog='/servlet/E4sGetSectData?'

def webEndfDataForPlot_DADE(target,react,strPar,reqLibs,fx=1,fy=1,quantPrexix="DA"):
    datasets=[]
    print('\n___webEndfDataForPlot_DADE: ['+target+'] ['+react+'] ['+strPar+']')
    web0par='Target='+target+'&Reaction='+react+'&Quantity='+quantPrexix+'*&json&mats'
    txt=wget_nds(web0prog,web0par)
    if txt is None: return datasets
#    print('___1___txt='+txt)

    obj1=json.loads(txt)
    print('format='+obj1['format'])
    list1=obj1.get('sections')
    if list1 is None:
        print('___Retrieved list of sections: empty.')
        return datasets
    print('___Retrieved sections:'+str(len(list1)))

    ii=0;sections=[]
    for sect1 in list1:
        ii+=1
        LibName=sect1['LibName']
        if reqLibs.get(LibName) is None: continue
        if sect1['PenSectID'] is None: continue
        if sect1['NSUB']==19: continue #exclude STD sublib
        print('SelectedLib-Sect:'+str(ii)+') '+str(sect1))
        sections.append(sect1)
    print('___Required sections:'+str(len(sections)))

    ii=0
    for sect1 in sections:
        ii+=1
        LibName=sect1['LibName']
        PenSectID=sect1['PenSectID']
        EvalID=sect1['EvalID']
        myColor=reqLibs.get(LibName)
        web1param='EvalID='+str(EvalID)+'&PenSectID='+str(PenSectID)+'&json'
        web1param+=strPar
        print('WebReq:'+str(ii)+')'+' EvalID:'+str(EvalID)+' PenSectID:'+str(PenSectID)+' Lib:'+LibName+' Color:'+myColor+'\n'
	+web1prog+web1param)
        txt=wget_nds(web1prog,web1param)
        if txt is None: continue
        #print('___webEndfDataForPlot_DADE::txt='+txt)

        try:
            obj2=json.loads(txt)
        except Exception as ex:
            print("___2___web-read-error: ",ex)
            continue
        dss=obj2['datasets']
        if (len(dss)<=0): continue
        for ds in dss:
            pts=ds['pts']
            print('Download...DS:'+str(ii)+'/'+str(len(dss))+')\t'+ds['REACTION']+'\t'+ds['LIBRARY']+'\tEID:'+str(EvalID)+'\tSID:'+str(PenSectID)+'\tf(x):'+ds['f(x)']+'\tpts:'+str(len(pts)))
            lastDataset={}
            lastDataset['DatasetID']=PenSectID
            lastDataset['myColor']=myColor
            lastDataset['TARGET']=ds['TARGET']
            lastDataset['MF']=ds['MF']
            lastDataset['MT']=ds['MT']
            #lastDataset['x4lbl']=ds['LIBRARY']#+' '+ds['REACTION'].lower()
            lastDataset['x4lbl']=(ds['LIBRARY']+' '+ds['param']).strip()
#            lastDataset['AUTH']=sect1['AUTH']
            lastDataset['DATE']=getEndfDate(sect1.get('DATE')).strip()
            lastDataset['AUTH']=getEndfDate(sect1.get('DATE'))+sect1['AUTH']
            x=[];     lastDataset['x']=x
            y=[];     lastDataset['y']=y
            dy=[];    lastDataset['dy']=dy
            datasets.append(lastDataset);
            ipt=0;idy=0
            for pt in pts:
                ipt+=1
                #print(str(ipt)+') '+str(pt))
#                xx=pt['E'];yy=pt['Sig']
#                if "dSig" in pt: dyy=pt['dSig']
#                else: dyy=None
                xx=pt['x'];yy=pt['y']
                if "dy" in pt: dyy=pt['dy']
                else: dyy=None
                #print('\t'+str(ipt)+') '+str(xx)+': '+str(yy)+' '+str(dyy))
                xx=float(xx)*fx; #xx=round(xx,10)
                yy=float(yy)*fy; #yy=round(yy,7)
                if dyy is not None: dyy=float(dyy)*fy; idy+=1; #dyy=round(dyy,7);
                else: dyy=0
                x.append(xx);
                y.append(yy);
                dy.append(dyy)
            lastDataset['idy']=idy
            lx=len(x)
#            if y[lx-1]==0 and y[lx-2]==0: del x[-1];del y[-1];del x[-1];del y[-1]
            if y[lx-1]==0 and y[lx-2]==0: del x[-1];del y[-1]
            print('Downloaded:DS:'+str(ii)+'/'+str(len(dss))+')\t'+ds['REACTION']+'\t'+ds['LIBRARY']+'\tEID:'+str(EvalID)+'\tSID:'+str(PenSectID)+'\tf(x):'+ds['f(x)']+'\tpts:'+str(len(pts))+'\tidy='+str(idy))
    return datasets

def getEndfDate(str0):
    if str0 is None: return ''
    nd=0; out=''
    for i,ch in enumerate(str0):
        if ch.isdigit():
            out+=ch
    out=out[:4].strip()
    if out=='': return ''
    if out=='0': return ''
    if len(out)<2: return ''
    try: nn=int(out)
    except ValueError: return ''
    if nn>=100 and nn<1000: nn=nn//10 #901 -->90
    if nn<50: nn=2000+nn
    if nn<100: nn=1900+nn
    if nn>5000: nn=1900+(nn//100) #example: 9303 --> 1993
    out=str(nn)
    return out+' '
