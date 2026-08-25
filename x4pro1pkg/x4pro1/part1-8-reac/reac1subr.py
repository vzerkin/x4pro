"""
 **********************************************************************
 * Copyright (c) 2021-2026 Viktor Zerkin, v.zerkin@gmail.com          *
 * Author:   Viktor Zerkin, PhD, IAEA-NDS(1999-2023), NRDC(1999-2026) *
 * License:  MIT License (MIT)                                        *
 **********************************************************************
"""

import sys
sys.path.append('./')
sys.path.append('../')
from sqlsubr import *

def print_reacodes(dbConn,conn,reacodes,add2Where=''):
    if len(reacodes)<1: return
    where=" where 1=1 and (\n"
    for ii,reacode in enumerate(reacodes):
        if (ii!=0): where+="   or"
        else:       where+="     "
        where+=" reacode like '"+reacode+"'\n"
    where+=" )"
    sql=str("select distinct reacode\n"
	+", reatyp as ReactionType, DICT013.ShortHelp as ReactionTypeHelp \n"
	+", quant1 as WebQuantity1, QUANTITY.ShortHelp as WebQuantity1Help\n"
	+", yformula as Formula, nx as nx, MF, MT \n"
	+" ,hy.BasicUnits  as yBasicUnits , hy.expansion as yexpansion \n"
	+" ,hx1.BasicUnits as x1BasicUnits, hx1.famCode as x1family, hx1.expansion as x1expansion \n"
	+" ,hx2.BasicUnits as x2BasicUnits, hx2.famCode as x2family, hx2.expansion as x2expansion \n"
	+" ,hx3.BasicUnits as x3BasicUnits, hx3.famCode as x3family, hx3.expansion as x3expansion \n"
	+" ,hx4.BasicUnits as x4BasicUnits, hx4.famCode as x4family, hx4.expansion as x4expansion \n"
	+" ,hx5.BasicUnits as x5BasicUnits, hx5.famCode as x5family, hx5.expansion as x5expansion \n"
	+" from x4pro_ds \n"
	+" left join QUANTITY on QUANTITY.Code=x4pro_ds.quant1 \n"
	+" left join DICT013  on DICT013.Code=x4pro_ds.reatyp  \n"
	+" join x4pro_hdr as hy on hy.DatasetID=x4pro_ds.DatasetID and hy.typ='c' and hy.hdr='y'           \n"
	+" left join x4pro_hdr as hx1 on hx1.DatasetID=x4pro_ds.DatasetID and hx1.typ='c' and hx1.hdr='x1' \n"
	+" left join x4pro_hdr as hx2 on hx2.DatasetID=x4pro_ds.DatasetID and hx2.typ='c' and hx2.hdr='x2' \n"
	+" left join x4pro_hdr as hx3 on hx3.DatasetID=x4pro_ds.DatasetID and hx3.typ='c' and hx3.hdr='x3' \n"
	+" left join x4pro_hdr as hx4 on hx4.DatasetID=x4pro_ds.DatasetID and hx4.typ='c' and hx4.hdr='x4' \n"
	+" left join x4pro_hdr as hx5 on hx5.DatasetID=x4pro_ds.DatasetID and hx5.typ='c' and hx5.hdr='x5' \n"
	+where+" \n"
	+" order by reacode"
	)
    rows,cols=execute1sql(dbConn,conn,sql,ttout=False)
#   print('\n---print_reacodes---rows:',len(rows),' cols:',len(cols))
    irow=0; ww=14; lcode=10; lexpansion=36
    allBasicUnits={}
    print('Summary of Reaction-Codes',len(rows))
    for row in rows:
        irow+=1
#       print('row-'+str(irow)+':\t',tuple(row))
#       print('\n----'+str(irow)+': '+str(row['reacode']))
        print('----'+str(irow)+'.')
        if row['reacode'] is not None: 
            print('    '+'fullCode'.ljust(ww)+' '+str(row['reacode']).ljust(lcode))
        if row['ReactionType'] is not None: 
            print('    '+'ReactionType'.ljust(ww)+' '+str(row['ReactionType']).ljust(lcode),end='')
            print(' '+str(row['ReactionTypeHelp']),end='')
            print('')
        if row['WebQuantity1'] is not None: 
            print('    '+'WebQuantity1'.ljust(ww)+' '+str(row['WebQuantity1']).ljust(lcode),end='')
            print(' '+str(row['WebQuantity1Help']),end='')
            print('')
        print('    '+'nx'.ljust(ww)+' '+str(row['nx']).ljust(lcode)+' Number of x (independent variables)')
        for i in range(6):
            xi='x'+str(i)
            if i==0: xi='y'; family='c5data'
            else: family=row[xi+'family']
            BasicUnits=row[xi+'BasicUnits']
            expansion=row[xi+'expansion']
            if family is not None: 
                allBasicUnits[BasicUnits]=BasicUnits
                h1units=getStrFromSQL(dbConn,conn,"select ShortHelp from DICT025 where Code like '"+str(BasicUnits)+"'")
                print('    '+xi.ljust(2)+'    '+family.ljust(ww-6)+' '+str(BasicUnits).ljust(lcode)+' '+str(expansion).ljust(lexpansion)+' ///'+str(h1units))
    print('/Summary of Reaction-Codes')
    print('Summary of Units',len(allBasicUnits))
    for basicUnits in allBasicUnits:
#       print('---basicUnits:',basicUnits)
        Category=getStrFromSQL(dbConn,conn
	,"select Category from DICT025 where Code like '"+str(basicUnits)+"'"
	,verbose=False)
        if Category=='': continue
        sql="select * from DICT025 where Category like '"+str(Category)+"' and Factor is not null order by Factor"
        rows=executeSql(dbConn,conn,sql,verbose=False)
        irow=0
        print('---basicUnits:'+str(basicUnits).ljust(11)+' category:'+str(Category))
        for row in rows:
            irow+=1
            print('   '+Category.ljust(4)+' '+(str(irow)+'/'+str(len(rows))).ljust(5)
		+' '+str(row['Code']).ljust(12)+str(row['Factor']).ljust(15)+' '+row['ShortHelp'])
    print('/Summary of Units')
    return

def getUnits(dbConn,conn,basicUnits,factor=1,verbose=True):
    if verbose: print('--0--getUnits---',basicUnits,factor)
    if factor==1: return basicUnits
    if verbose: print('--A--getUnits---',basicUnits,factor)
    units=''
    Category=getStrFromSQL(dbConn,conn,"select Category from DICT025 where Code like '"+str(basicUnits)+"'")
    if verbose: print('--1--getUnits---',basicUnits,factor,' Category:',Category)
    if Category!='':
        units=getStrFromSQL(dbConn,conn,"select Code from DICT025 where Category like '"+str(Category)+"' and Factor="+str(factor))
    if units!='': return units
    units=basicUnits+'&times;'+"{:.0e}".format(factor).replace('e+0','e').replace('e-0','e-')
    return units

def getRows_sqlSearch_reacodes(dbConn,conn,reacodes,xn,add2Where=''):
    sql=getX4SqlSearch_Reacodes(reacodes,xn,add2Where)
    rows=executeSql(dbConn,conn,sql)
#    rows=execute1sql(dbConn,conn,sql,verbose=True,ttout=True)
    return rows


def getX4SqlSearch_Reacodes(reacodes,xn,add2Where=''):
    print("---getX4SqlSearch_Reacodes: xn=",xn,' reacodes:',reacodes)
    if len(reacodes)<1: return ''
    where=" where 1=1 \n"
    if len(reacodes)>0:
        where+=" and (\n"
        for ii,reacode in enumerate(reacodes):
            if (ii!=0): where+="   or"
            else:       where+="     "
            where+=" fullCode like '"+reacode+"'\n"
        where+=" )"
#   where=" where uni2.DatasetID='22754004'"
    sql=str(""
	+"select *                                                   \n"
	+" ,y  as YY, dy  as dYY                                     \n"
	+" ,"+xn+" as XX, d"+xn+" as dXX                             \n"
	+" ,hy.BasicUnits as yBasicUnits, hy.expansion as yexpansion \n"
	+" ,hx.BasicUnits as xBasicUnits, hx.expansion as xexpansion \n"
	+" ,hx1.BasicUnits as x1BasicUnits, hx1.famCode as x1family  \n"
	+" ,hx2.BasicUnits as x2BasicUnits, hx2.famCode as x2family  \n"
	+" ,hx3.BasicUnits as x3BasicUnits, hx3.famCode as x3family  \n"
	+" ,hx4.BasicUnits as x4BasicUnits, hx4.famCode as x4family  \n"
	+" ,hx5.BasicUnits as x5BasicUnits, hx5.famCode as x5family  \n"
	+" from uni2                                                 \n"
	+" left join DICT036 on DICT036.Code=uni2.SF58               \n"
	+" join x4pro_ds  as ds on ds.DatasetID=uni2.DatasetID       \n"
	+" join x4pro_hdr as hy on hy.DatasetID=uni2.DatasetID and hy.hdr='y'          \n"
	+" join x4pro_hdr as hx on hx.DatasetID=uni2.DatasetID and hx.hdr='"+xn+"'     \n"
	+" left join x4pro_hdr as hx1 on hx1.DatasetID=uni2.DatasetID and hx1.hdr='x1' \n"
	+" left join x4pro_hdr as hx2 on hx2.DatasetID=uni2.DatasetID and hx2.hdr='x2' \n"
	+" left join x4pro_hdr as hx3 on hx3.DatasetID=uni2.DatasetID and hx3.hdr='x3' \n"
	+" left join x4pro_hdr as hx4 on hx4.DatasetID=uni2.DatasetID and hx4.hdr='x4' \n"
	+" left join x4pro_hdr as hx5 on hx5.DatasetID=uni2.DatasetID and hx5.hdr='x5' \n"
	+where+" \n"
	+add2Where+" "
#+" and uni2.DatasetID='40230006'"
#+" and uni2.DatasetID='40017010'"
#+" and uni2.DatasetID like '4%'"
#+" and uni2.DatasetID like '1%'"
#+" and uni2.DatasetID like 'o%'"
#+" and uni2.Author1 like 'hauser'"
#+" and uni2.DatasetID='22754004'"
#+" and uni2.DatasetID='21984097'"
	+" order by fullCode,YearRef1 desc,DatasetID \n"
	+" ,x1,x2,x2,x4,x5,iPoint                    \n"
#	+" ,iPoint                    \n"
	)
    print("SQL:\n"+sql)
    return sql

def getDatasets4plot(rows,xn,fx=1,fy=1):
    lx=len(rows)
    datasets=[]
    ii=0; lastDatasetSplit=''; lastDataset={}
    print('\n---getDatasets4plot---datapoints:'+str(len(rows))+' xn='+str(xn),' fx='+format(fx,".1e")+' fy='+format(fy,".1e"))
    outDatasets={}
    for row in rows:
        fullCode=row['fullCode']; DatasetID=row['DatasetID']; iPoint=row['iPoint']
        YearRef1=row['YearRef1']; Author1Ini=row['Author1Ini']; Author1=row['Author1'];
        Quant=row['Quant']
        yformula=row['yformula']
        yval=row['yval']  #2:DATA-MIN 3:DATA-MAX
        if DatasetID=='41109007': continue #Mistake in EXFOR: "DATA" --> "DATA-MAX"
        Author1=Author1.replace("`","'")
        yy=row['YY'];   dyy=row['dYY']
        xx=row['XX'];   dxx=row['dXX']
        ShortHelp=row['ShortHelp']
        if ShortHelp is None: ShortHelp=''
        xBasicUnits=row['xBasicUnits']
        yBasicUnits=row['yBasicUnits']
        xexpansion=row['xexpansion']
        yexpansion=row['yexpansion']
        if xx is None: continue;
        if yy is None: continue;
        if xexpansion.endswith(': mass'): xBasicUnits='AMU'
        if Author1Ini is None: Author1Ini=''
        fullCode=fullCode.replace(",,,EXP",""); fullCode=fullCode.replace(",,EXP","")
        nowDatasetSplit=DatasetID
        grp=''
        if yval=='2': grp=' /data-min/'
        if yval=='3': grp=' /data-max/'
        ig=0; g0=0; g1=0
        for i in range(1,5+1):
            xi='x'+str(i)
            if xi==xn: continue
            xival=row[xi]
            if xival is None: continue;
            xifam=row[xi+'family'].title()
            xiunt=row[xi+'BasicUnits']
            if ig==0: g0=xival
            if ig==1: g1=xival
            ig+=1
            if xiunt=='EV':
#                smev="{:.6e}".format(xival/1e6)
#                smev="{:.4e}".format(xival/1e6)
#                smev="{:.3e}".format(xival/1e6)
                smev="{:.2e}".format(xival/1e6)
                emev=float(smev)
                grp+=' '+xifam+'='+str(emev)
                if grp.endswith('.0'): grp=grp[:-2]
                grp+='MeV'
            else:
#               xivaltx="{:.3e}".format(xival)
                xivaltx="{:.2e}".format(xival)
                xival=float(xivaltx)
#               grp+=' '+xifam+':'+str(xival)+xiunt
                grp+=' '+xifam+'='+str(xival)
                if grp.endswith('.0'): grp=grp[:-2]
                if xiunt=='ADEG': grp+='&deg;'
                else: grp+=xiunt.title()
                if grp.endswith('.0'): grp=grp[:-2]
        grp=grp.replace('e+0','e').replace('e-0','e-')
        nowDatasetSplit+=grp
#        print('nowDatasetSplit:'+nowDatasetSplit)

        nowDataset=outDatasets.get(nowDatasetSplit)
        if nowDataset is None:
            nowDataset={}
            outDatasets[nowDatasetSplit]=nowDataset
            nowDataset['DatasetID']=DatasetID
            nowDataset['Reacode']=fullCode
            nowDataset['Quantity']=ShortHelp
            nowDataset['xBasicUnits']=xBasicUnits
            nowDataset['yBasicUnits']=yBasicUnits
            nowDataset['xexpansion']=xexpansion
            nowDataset['yexpansion']=yexpansion
            nowDataset['Quant']=Quant
            nowDataset['yformula']=yformula
            nowDataset['DatasetSplit']=''
            nowDataset['g0']=g0
            nowDataset['g1']=g1
            nowDataset['YearRef1']=YearRef1
            nowDataset['Author1Ini']=Author1Ini
            nowDataset['Author1']=Author1
            nowDataset['x4lbl']=str(YearRef1)+', '+str(Author1Ini)+str(Author1)+grp
            nowDataset['fx']=1/fx
            nowDataset['fy']=1/fy
            x=[];     nowDataset['x']=x
            y=[];     nowDataset['y']=y
            dy=[];    nowDataset['dy']=dy
            dx=[];    nowDataset['dx']=dx
            print('\n-new-'+str(len(outDatasets))+') '+str(fullCode)+' '+str(DatasetID)+grp+' '+str(YearRef1)+' '+Author1+' '+yformula)
        else:
#            print('-old-'+str(len(outDatasets))+') '+nowDatasetSplit)
            y=nowDataset['y']; dy=nowDataset['dy']
            x=nowDataset['x']; dx=nowDataset['dx']
#        print(str(ii)+'/'+str(lx)+':'+str(len(outDatasets))+') '+str(fullCode)+' '+str(DatasetID)+grp+' '+str(YearRef1)+' '+Author1+" x:"+str(xx)+" y:"+str(yy)+" g0:"+str(g0)+" g1:"+str(g1))
        if DatasetID=='40017010' and g0==0.12e6 and xx==154: yy=1.5687E+02*1e6
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
        print(str(ii)+'/'+str(lx)+':'+str(len(outDatasets))+') '+str(fullCode)+' '+str(DatasetID)+grp+' '+str(YearRef1)+' '+Author1+" x:"+str(xx)+" y:"+str(yy)+" dy:"+str(dyy)+" dx:"+str(dxx))
    datasets=[]
    for nowDatasetSplit in outDatasets:
        dataset=outDatasets[nowDatasetSplit]
#       if len(dataset['y'])<8: continue
        datasets.append(outDatasets[nowDatasetSplit])
    datasets=sorted(datasets,key=lambda x:(x['Reacode'],-x['YearRef1'],x['Author1'],x['g0'],x['g1']))
#   datasets=sorted(datasets,key=lambda x:(-x['YearRef1'],x['Author1'],x['g0'],x['g1']))
    print('---outDatasets:'+str(len(outDatasets))+' datasets:'+str(len(datasets)))
    typeEntries(datasets)
    return datasets


def getReacodes(datasets,nptmin):
#    print('--0--getReacodes: datasets:'+str(len(datasets))+' nptmin:'+str(nptmin))
    lx=len(datasets)
    Reacodes=[]
    ii=0; lastReacodeStr='---'; lastReacode={}
    print('---getReacodes---Datasets:',len(datasets))
    for dataset in datasets:
#        print('\t'+str(ii)+'---getReacodes---dataset:',dataset['DatasetID'],len(dataset['x']),nptmin)
        if len(dataset['x'])<nptmin: continue
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
        print('\tDataset:'+str(ii)+'/'+str(lx)+') '+str(Reacode)+' '+str(dataset['DatasetID'])+' '+str(dataset['x4lbl']))
#    print('--1--getReacodes: Reacodes:'+str(len(Reacodes))+' nptmin:'+str(nptmin)+' ii:'+str(ii))
    return Reacodes

def getReacodes2Datasets(reacodes):
    datasets=[]
    for reacode in reacodes:
        for dataset in reacode['datasets']:
            datasets.append(dataset)
    return datasets

def typeEntries(datasets):
    entries=[];ientry=0
    print('---ENTRY: ',end='')
    for dataset in datasets:
        entry=dataset['DatasetID'][:5]
        if entry not in entries:
            entries.append(entry)
            if ientry>0: print(';',end='')
            print(entry,end='')
            ientry+=1
    print('')
    return entries

def typeEntries(datasets):
    entries=[]
    for dataset in datasets:
        entry=dataset['DatasetID'][:5]
        if entry not in entries: entries.append(entry)
    entries=sorted(entries)
    print('---ENTRY: ',end='')
    for ii,entry in enumerate(entries):
        print(entry+'*;',end='')
    print('')
    return entries

def getNDataPoints(datasets):
    nn=0
    for dataset in datasets: nn+=len(dataset['x'])
    return nn
