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
web1prog='/servlet/E4sGetTabSect?'

def getEndfDate(str0):
    if str0 is None: return ''
    nd=0; out=''
    for i, ch in enumerate(str0):
        out+=ch
        if ch.isdigit():
            nd+=1
            if nd>=4: return out+' '
    return out+' '

def webEndfDataForPlot_SIG(target,react,strPar,reqLibs,fx=1,fy=1,eMinEv=None,eMaxEv=None):
    datasets=[]
    print('\n___getEndfDataForPlot: ['+target+'] ['+react+']'+strPar)
    web0par='Target='+target+'&Reaction='+react+'&Quantity=SIG&json'+strPar
    txt=wget_nds(web0prog,web0par)
    if txt is None: return datasets
    print('txt='+txt)

    obj1=json.loads(txt)
    print('format='+obj1['format'])
    list1=obj1.get('sections')
    if list1 is None: return datasets
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
    print('Required sections:'+str(len(sections)))

    ii=0;datasets=[]
    for sect1 in sections:
        ii+=1
        LibName=sect1['LibName']
        PenSectID=sect1['PenSectID']
        myColor=reqLibs.get(LibName)
        web1param='PenSectID='+str(PenSectID)+'&json'
        txt=wget_nds(web1prog,web1param)
        if txt is None: continue

        try:
            obj2=json.loads(txt)
        except Exception as ex:
            print("___2___web-read-error: ",ex)
            print("___2___web-read-error:\n"+web1prog+web1param)
            print("___2___web-read-error:\n",txt)
            continue
        dss=obj2['datasets'];    ds=dss[0];    pts=ds['pts']
        #print(str(ii)+')\t'+ds['REACTION']+'\t'+ds['LIBRARY']+'\tID:'+str(PenSectID)+'\tpts:'+str(len(pts)))
        lastDataset={}
        lastDataset['LIBRARY']=ds['LIBRARY']
        lastDataset['mode']='curve'
        lastDataset['DatasetID']=PenSectID
        lastDataset['Reacode']=ds['REACTION']
        lastDataset['myColor']=myColor
        lastDataset['x4lbl']=ds['LIBRARY']#+' '+ds['REACTION'].lower()
#        lastDataset['AUTH']=sect1['AUTH']
        lastDataset['DATE']=getEndfDate(sect1.get('DATE'))
        lastDataset['AUTH']=getEndfDate(sect1.get('DATE'))+sect1['AUTH']
        lastDataset['MF']=sect1['MF']
        lastDataset['MT']=sect1['MT']
        lastDataset['fx']=fx
        lastDataset['fy']=fy
        lastDataset['idy']=0
        x=[];     lastDataset['x']=x
        y=[];     lastDataset['y']=y
        dy=[];    lastDataset['dy']=dy
        datasets.append(lastDataset);
        ipt=0;idy=0
        for pt in pts:
            #print(str(ipt)+') '+str(pt))
            xx=pt['E'];yy=pt['Sig']
            if "dSig" in pt: dyy=pt['dSig']
            else: dyy=None
            #print('\t'+str(ipt)+') '+str(xx)+': '+str(yy)+' '+str(dyy))
            if eMinEv is not None:
                if xx<eMinEv: continue
            if eMaxEv is not None:
                if xx>eMaxEv: continue
            ipt+=1
            xx=float(xx)*fx; #xx=round(xx,10)
            yy=float(yy)*fy; #yy=round(yy,7)
            if dyy is not None: dyy=float(dyy)*fy; idy+=1; #dyy=round(dyy,7);
            else: dyy=0
            x.append(xx);
            y.append(yy);
            dy.append(dyy)
        lastDataset['idy']=idy
        lx=len(x)
        if lx<=0: datasets.pop(); continue
        if y[lx-1]==0 and y[lx-2]==0: del x[-1];del y[-1];del x[-1];del y[-1]
        print('Downloaded:'+str(ii)+')\t'+ds['REACTION']+'\t'+ds['LIBRARY']+'\tPenSectID:'+str(PenSectID)+'\tpts:'+str(len(pts))+'\tidy='+str(idy))
    return datasets
