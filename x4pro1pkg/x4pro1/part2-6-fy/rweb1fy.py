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
web1prog='/servlet/E4sGetSect2?'

def webEndfDataForPlot_FYA(target,react,reqLibs,EiMin,EiMax,fx=1,fy=1):
    aaMin=12 #exclude Ternary fission
    datasets=[]
    print('\n___webEndfDataForPlot_FYA: ['+target+'] ['+react+']')
    web0par='Target='+target+'&Reaction='+react+'&json'
    print('web0get:'+web0prog+web0par)
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
        print('SelectedLib-Sect:'+str(ii)+') '+str(sect1))
        sections.append(sect1)
    print('___Required sections:'+str(len(sections)))

    ii=0
    for sect1 in sections:
        ii+=1
        LibName=sect1['LibName']
        SectID=sect1['SectID']
        myColor=reqLibs.get(LibName)
        web1param='SectID='+str(SectID)
        print('WebReq:'+str(ii)+')'+' SectID:'+str(SectID)+' Lib:'+LibName+' Color:'+myColor+'\n'+web1prog+web1param)
        txt=wget_nds(web1prog,web1param)
        if txt is None: continue
        #print('___webEndfDataForPlot_FYA::txt='+txt)
        try:
            obj2=json.loads(txt)
        except Exception as ex:
            print("___2___web-read-error: ",ex)
            continue

        dss=obj2['datasets']
        if (len(dss)<=0): continue
        for ds in dss:
            Ei=ds['Ei']
            if (Ei<EiMin): continue
            if (Ei>EiMax): continue
            pts=ds['FYs']
            Library=obj2['HSUB1']
            print('Download...DS:'+str(ii)+'/'+str(len(dss))+')\t'+ds['Title']+'\t'+Library+'\tpts:'+str(len(pts)))
            lastDataset={}
            lastDataset['DatasetID']=obj2['id']
            lastDataset['myColor']=myColor
            lastDataset['x4lbl']=ds['Title']
            datasets.append(lastDataset);
            ipt=0;idy=0
            masses=[]
            for pt in pts:
                aa=pt['ZAFP']%1000
                if (aa not in masses): masses.append(aa)
            XXs=[]
            for i in range(len(masses)):
                if (masses[i]>=aaMin): XXs.append(masses[i])
            #XXs.sort(reverse=True)
            XXs.sort()
            YYs=[0]*len(XXs)
            DYYs=[0]*len(XXs)
            print('________masses:'+str(len(masses))+' XXs:'+str(len(XXs))+' YYs:'+str(len(YYs))+' DYYs:'+str(len(DYYs)))
            #print('As:',masses)
            #print('Xs:',XXs)
            for pt in pts:
                ipt+=1
                #print(str(ipt)+') '+str(pt))
                aa=pt['ZAFP']%1000
                yy=pt['FY']
                if "DFY" in pt: dyy=pt['DFY']; idy+=1
                else: dyy=None
                if (aa not in XXs): continue
                ix=XXs.index(aa)
                #print('\t'+str(ipt)+') A:'+str(aa)+' FY:'+str(yy)+' dFY:'+str(dyy)+' ix:'+str(ix))
                YYs[ix]+=yy
                if dyy is not None: DYYs[ix]+=dyy
            lastDataset['idy']=idy
            lastDataset['x']=XXs
            lastDataset['y']=YYs
            lastDataset['dy']=DYYs
            print('Downloaded:DS:'+str(ii)+'/'+str(len(dss))+')\t'+'\t'+Library+'\tpts:'+str(len(pts))+'\tidy='+str(idy))
    return datasets
