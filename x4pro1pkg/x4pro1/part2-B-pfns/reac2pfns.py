"""
 **********************************************************************
 * Copyright (c) 2026 Viktor Zerkin, v.zerkin@gmail.com               *
 * Author:   Viktor Zerkin, PhD, IAEA-NDS(1999-2023), NRDC(1999-2026) *
 * License:  MIT License (MIT)                                        *
 **********************************************************************
"""
import os
import sys
import datetime
sys.path.append('./')
sys.path.append('../')
import dbConn
from reac1help  import *
from reac2subr  import *
from reac2proc  import *
from x4out      import *
from rweb12     import *
from exfor2plot import * #plot by plotly/matplotlib
from endf2plot  import *
from readMaslovSp1 import *
from readZvdat import *

#-------------------------------------------------------------------------------
def main():

    print('  +-----------------------------------------+')
    print('  | Program: reac2pfns.py, ver.2026-09-16   |')
    print('  | Author:  V.Zerkin, Vienna, 2021-2026    |')
    print('  | Purpose: Retrieve and plot any type of  |')
    print('  |          data from local EXFOR database |')
    print('  +-----------------------------------------+')

    if len(sys.argv)<=1: print(getHelp()); sys.exit(0)

    ct=str(datetime.datetime.now())[:19]
    print("Running: "+ct)

    x4ei=''
    x4where0=''
    usr2where=''
    fx=1; fy=1
    nPntMin=1
    plotTitle=''
    outhtml='reac1'
    xn='x1'
    reacode1=''
    reacodes=[]
    xtype='linear';ytype='linear'
    lines=False
    groupReactions=True
    msize=8
    lwidth=0.9
    symBorder=False
    annot=None
    showgrid=True
    zeroline=True
#   showgrid=False;    zeroline=False
    flagEndf=True
    e4webparam=""
    add2title=""
    showSpectra=False
#   fy=1e-6 #?default for spectra
    legendInside=False
    bwColor=False
    myCurveFiles=[]
    zvdatCurFiles=[]
#   showSpectra=True

    xrange=None; yrange=None;
    x1min=None; x1max=None
    x2min=None; x2max=None
    x3min=None; x3max=None
    xmin=None; xmax=None
    ymin=None; ymax=None
    x1fam=None; x2fam=None
    x3fam=None; x4fam=None
    x5fam=None
    a1=None
    dsids=None
    aprod=None #product in SF4 or DATA(ELEM/MASS)
    oper=None
    Tmxw=1.32e6
    Einc=None

    def str2float(str1):
        if str1 is None: return None
        try: rr=float(str1)
        except ValueError: rr=None
    #   print("   ---str2float:["+str1+"] --> "+str(rr))
        return rr

    def str2int(str0,default):
        try: nn=int(str0.strip())
        except ValueError: nn=default
        return nn

    def str2annot(str0):
        if str0 is None: return None
        strs=str0.split(",")
        if len(strs)<3: return None
        x=str2float(strs[0])
        y=str2float(strs[1])
        if x is None: return None
        if y is None: return None
        i1=str0.find(',')
        i2=str0.find(',',i1+1)
        str3=str0[i2+1:]
        annot1=(str3,x,y)
        print("   ---str2annot:["+str0+"] --> "+str(annot1))
        return annot1

    def str2legend(str0):
        nonlocal legendInside
        legendInside=True

    def xfamily2where(xnam,str0):
        if str0 is None: return ''
        strs=str0.split(";")
        where=""
        for ii,fam in enumerate(strs):
            if where!="": where+=" or "
            where+=" ("+xnam+"family like '"+fam+"')"
        if where!="": where=" and ("+where+")\n"
        return where


    print('\n---Arguments from command-line---')
    for ii,arg in enumerate(sys.argv):
        if (ii==0): continue
        if arg=='-h':		print(getHelp());	sys.exit(0)
        if arg=='-help':	print(getHelp());	sys.exit(0)
        if arg=='--h':		print(getHelp());	sys.exit(0)
        if arg=='--help':	print(getHelp());	sys.exit(0)
        print('   '+str(ii).ljust(2)+" arg: "+arg)
        if arg=='-xlog': xtype='log';  continue
        if arg=='-ylog': ytype='log';  continue
        if arg=='-bw':   bwColor=True; continue
        if arg.startswith('-T:'):  Tmxw=str2float(arg[3:]);        continue
        if arg.startswith('-Ei:'): Einc=str2float(arg[4:]);        continue
        if arg.startswith('-x1:'): x1max=x1min=str2float(arg[4:]); continue
        if arg.startswith('-x2:'): x2max=x2min=str2float(arg[4:]); continue
        if arg.startswith('-x3:'): x3max=x3min=str2float(arg[4:]); continue
        if arg.startswith('-x1min:'):  x1min=str2float(arg[7:]);   continue
        if arg.startswith('-x1max:'):  x1max=str2float(arg[7:]);   continue
        if arg.startswith('-x2min:'):  x2min=str2float(arg[7:]);   continue
        if arg.startswith('-x2max:'):  x2max=str2float(arg[7:]);   continue
        if arg.startswith('-x3min:'):  x3min=str2float(arg[7:]);   continue
        if arg.startswith('-x3max:'):  x3max=str2float(arg[7:]);   continue
        if arg.startswith('-symw:'):   msize=str2int(arg[6:],msize); continue
        if arg.startswith('-nmin:'):   nPntMin=str2int(arg[6:],1); continue
        if arg.startswith('-xmin:'):   xmin=str2float(arg[6:]);    continue
        if arg.startswith('-xmax:'):   xmax=str2float(arg[6:]);    continue
        if arg.startswith('-ymin:'):   ymin=str2float(arg[6:]);    continue
        if arg.startswith('-ymax:'):   ymax=str2float(arg[6:]);    continue
        if arg.startswith('-fx:'):     fx=str2float(arg[4:]);      continue
        if arg.startswith('-fy:'):     fy=str2float(arg[4:]);      continue
        if arg.startswith('-x:'):      xn=arg[3:];                 continue
        if arg.startswith('-x1fam:'):  x1fam=arg[7:];              continue
        if arg.startswith('-x2fam:'):  x2fam=arg[7:];              continue
        if arg.startswith('-x3fam:'):  x3fam=arg[7:];              continue
        if arg.startswith('-x4fam:'):  x4fam=arg[7:];              continue
        if arg.startswith('-x5fam:'):  x5fam=arg[7:];              continue
        if arg.startswith('-prod:'):   aprod=arg[6:];              continue
        if arg=='-sym':                symBorder=True;             continue
        if arg=='-lines':              lines=True;                 continue
        if arg=='-nogrp':              groupReactions=False;       continue
#       if arg=='-sp':                 showSpectra=True;           continue	#not implemented
        if arg.startswith('-o:') and len(arg)>4: outhtml=arg[3:];  continue
        if arg.startswith('-annot:'):  annot=str2annot(arg[7:]);   continue
        if arg.startswith('-leg'):     str2legend(arg[4:]);        continue
        if arg.lower().startswith('-a1:'):  a1=arg[4:];            continue
        if arg.lower().startswith('-ds:'):  dsids=arg[4:];         continue
        if arg.startswith('-w:'):           usr2where=arg[3:];     continue
        if arg.startswith('-rsp1:') and len(arg)>7: myCurveFiles.append(arg[6:]); continue
        if arg.startswith('-zdat:') and len(arg)>7: zvdatCurFiles.append(arg[6:]); continue
        if arg.startswith('-'): continue
        reacodes.append(arg)

    x4ei=''
    if x1min is not None: x4ei+=' and x1>='+str(x1min)
    if x1max is not None: x4ei+=' and x1<='+str(x1max)
    if x2min is not None: x4ei+=' and x2>='+str(x2min)
    if x2max is not None: x4ei+=' and x2<='+str(x2max)
    if x3min is not None: x4ei+=' and x3>='+str(x3min)
    if x3max is not None: x4ei+=' and x3<='+str(x3max)
    x4ei+=xfamily2where('x1',x1fam)
    x4ei+=xfamily2where('x2',x2fam)
    x4ei+=xfamily2where('x3',x3fam)
    x4ei+=xfamily2where('x4',x4fam)
    x4ei+=xfamily2where('x5',x5fam)
    x4ei+=addStrToWhere('a1',a1)
    x4ei+=addStrToWhere('dsid',dsids)
    x4where0+=addStrToWhere('a1',a1)
    x4where0+=addStrToWhere('dsid',dsids)
    if aprod is not None: x4ei+=" and (prod like '%"+aprod+"' or outParticles like '%["+aprod+"]%')\n"
    if xmin is not None or xmax is not None: xrange=[xmin,xmax]
    if ymin is not None or ymax is not None: yrange=[ymin,ymax]

    print('\n---Input:')
    print('   Reaction: ',reacodes)
    print('   xn:       ',xn)
    print('   x1range:  ',str(x1min),'-',str(x1max))
    print('   x2range:  ',str(x2min),'-',str(x2max))
    print('   x3range:  ',str(x3min),'-',str(x3max))
    print('   fx:       ',str(fx))
    print('   fy:       ',str(fy))
    print('   nPntMin:  ',str(nPntMin))
    print('   xrange:   ',str(xrange))
    print('   yrange:   ',str(yrange))
    print('   Output:   ',outhtml)
    print('   x4ei:     ',x4ei)
    print('   legendInside: ',str(legendInside))
    print('')

    print("---Connect to SQL database---")
    conn=dbConn.getConnSQLx4db()
    if conn is None:
        print("___0___No connection...")
        sys.exit(1)
    print("   Connected to: ["+dbConn.dbType+"]")

    print("\n---Print summary---")
    print_reacodes(dbConn,conn,reacodes,add2Where=x4where0)

    print("\n---Retrieve EXFOR data from SQL database---")
    sys.stderr.write("---Retrieve EXFOR data from SQL database---\n")
    rows=getRows_sqlSearch_reacodes(dbConn,conn,reacodes,xn,x4ei,usr2where=usr2where)
    print("   Retrieved rows: "+str(len(rows)))
    sys.stderr.write("   Retrieved rows: "+str(len(rows))+"\n")

    print("\n---Extract EXFOR data from recordsets (rows)---")
    datasets=getDatasets4plot(dbConn,conn,rows,xn,fx=1/fx,fy=1/fy)
    print('datasets:',len(datasets))
    ldata=len(datasets)
    if (ldata<=0):
        print("---No data found---")
        sys.exit(2)
#   print(json.dumps(datasets[0],indent=2))
#   print(json.dumps(datasets,indent=2))

    if nPntMin>1:
        print("\n---filter only large datasets:"+str(len(datasets))+' nPntMin='+str(nPntMin))
        datasets=getDatasets_nPointsMin(datasets,nPntMin) #filter only large datasets
        print('---datasets:',len(datasets),'\n')
        if (len(datasets)<=0):
            print("---No data after filtering by #DataPoints:",nPntMin)
            sys.exit(2)
    if not showSpectra:
        datasets=datasets2mxwRatio(datasets,oper,Tm=Tmxw)

    groupReac=False
    if groupReactions:
        print("\n---Groupping datasets by Reaction-codes---")
        reacodes=getReacodes(datasets)
        print('---reacodes:',len(reacodes),'\n')
        if (len(reacodes)<=0):
            print("---No data after filtering by #DataPoints:",nPntMin)
            sys.exit(2)
        groupReac=len(reacodes)>1
        datasets=getReacodes2Datasets(reacodes)

    nPnt=getNDataPoints(datasets)

    print("\n---Output EXFOR datasets to JSON file---")
    outX4Datasets(datasets,outhtml)

    data1=prepareExforDataForPlot(datasets,msize=msize,groupReac=groupReac,lines=lines
	,lwidth=lwidth,symBorder=symBorder,bwColor=bwColor)


#- One of the following dash styles: ['solid', 'dot', 'dash', 'longdash', 'dashdot', 'longdashdot']
#- A string containing a dash length list in pixels or percentages (e.g. '5px 10px 2px 2px', '5, 10, 2, 2', '10% 20% 40%', etc.)

    #_________________Retrieve ENDF_________________
    data2=[]
    e4datasets=[]
    reqLibs={
#	'ENDF/B-VIII.1':"0,80,255",
	'ENDF/B-VIII.0':"0,0,255|solid|2",	#dash | dot | dashdot
#	'ENDF/B-VIII.1':"0,0,255",
	'ENDF/B-VII.1':"200,0,255|dashdot|2",
	'INDEN-Aug2023':"0,80,255",
	'JENDL-5':"0,200,0",
#	'JEFF-4.0':"255,0,0",
#	'JEFF-3.3':"0,255,255",
#	'JEFF-3.1':"0,255,255",
#	'JEF-2.2':"0,255,255",
#	'CENDL-3.2':"255,0,0"
#	'CENDL-2':"255,0,0"
	'BROND-3.1':"255,0,255",
#	'ENDF/B-V':"127,127,127"
	'MINKS-ACT':"255,80,80|dashdot"
	}
    if flagEndf:
        target=datasets[0]['Target']
        e4reac=datasets[0]['Reaction']
        g0=datasets[0]['g0']
        if Einc is None: Einc=g0
#       e4webparam="&mf=5&mt=18&ei=0.0253"
#       e4webparam="&mf=5&mt=18&ei="+str(g0)
        e4webparam="&mf=5&mt=18&ei="+str(Einc)
#       add2title=" (T=1.32MeV)"

        if not showSpectra:
            add2title=" (T="+format(Tmxw/1e6,"<.5g").strip()+"MeV)"
        else:
            Tmxw=0
            add2title=" /spectrum/"
        add2json=dict(Tmxw=Tmxw)
        e4webparam+="&T="+str(Tmxw)

        #_________________Retrieve ENDF_________________
        sys.stderr.write("---Retrieve data from remote ENDF server---\n")
        sys.stderr.write("   e4webparam:"+e4webparam+"\n")
#       e4datasets=webEndfDataForPlot_DADE(target,e4reac,e4webparam,reqLibs,1/fx,1,quantPrexix="")
#       e4datasets=webEndfDataForPlot_DADE(target,e4reac,e4webparam,reqLibs,1/fx,1/10*2,quantPrexix="",add2title=add2title)
#       e4datasets=webEndfDataForPlot_DADE(target,e4reac,e4webparam,reqLibs,1/fx,1/2,quantPrexix="",add2title=add2title)
#?sp    e4datasets=webEndfDataForPlot_DADE(target,e4reac,e4webparam,reqLibs,1/fx,1/fy*1e-3,quantPrexix="",add2title=add2title,add2json=add2json)
        e4datasets=webEndfDataForPlot_DADE(target,e4reac,e4webparam,reqLibs,1/fx,1/fy,quantPrexix="",add2title=add2title,add2json=add2json)
        print('---e4datasets:',len(e4datasets))
        sys.stderr.write("   Retrieved ENDF datasets: "+str(len(e4datasets))+"\n")
#       print(json.dumps(e4datasets[0],indent=2))
#       ds1=getMaslovSp1()
        iCurve=0
        for ii,zvdatCurFile in enumerate(zvdatCurFiles):
            ds1=readZvdatSp1(zvdatCurFile,iCurve,Einc,T=Tmxw)
            if ds1 is not None: e4datasets.append(ds1); iCurve+=1
        for ii,myCurveFile in enumerate(myCurveFiles):
#           ds1=readMaslovSp1(myCurveFile,iCurve,T=Tmxw)
            ds1=readMaslovSp1(myCurveFile,ii+1,T=Tmxw)
            if ds1 is not None: e4datasets.append(ds1); iCurve+=1
        #_________________Preparing ENDF data for plot_________________
        grp1=''
#       if len(reacodes)>1: grp1='grp1'
        if groupReac: grp1='grp1'
        data2=prepareEndfDataForPlot(e4datasets,grp1,True,lwidth=3,showAuth=True)

    if len(datasets)+len(e4datasets)<=0:
        print("---No data found---")
        sys.exit(1)

    #_________________Store EXFOR and ENDF_________________
    outX4Datasets(datasets,outhtml+"--exfor",frmArray=2)
    outX4Datasets(e4datasets,outhtml+"--endf",frmArray=2)




    xtitle='XX'
    ytitle='YY'
    yformula=''
    if len(datasets)>0:
        xtitle=datasets[0]['xexpansion']+', '+getUnits(dbConn,conn,datasets[0]['xBasicUnits'],fx)
        ytitle=datasets[0]['Quantity']  +', '+getUnits(dbConn,conn,datasets[0]['yBasicUnits'],fy)
        Quant=datasets[0]['Quant']
        yformula=datasets[0]['yformula'].title().replace('Y=','y=')
        plotTitle=datasets[0]['Reacode']
        plotTitle+='  Quantity:'+Quant+':'+yformula
        plotTitle+='  Datasets:'+str(len(datasets))
        if len(datasets)!=ldata: plotTitle+='/'+str(ldata)
    #   plotTitle+='  datapoints:'+str(len(rows))
        plotTitle+='  Points:'+str(nPnt)
        if len(rows)!=nPnt: plotTitle+='/'+str(len(rows))

    conn.close()

    myOfflinePlot(data1+data2
	,'Reaction:'+plotTitle
	+'<br><i>X4Pro, by V.Zerkin, Vienna, 2026, ver.2026-09-16 //running:'+ct+'</i>'
	,xtitle
	,ytitle
	,xtype=xtype,ytype=ytype
	,xrange=xrange,yrange=yrange
	,filename=outhtml
	,annot1=annot
	,showgrid=showgrid
	,zeroline=zeroline
	,legendInside=legendInside
#	,wwPng=1200
	)
    return


#-------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
    print('\nProgram successfully completed')
