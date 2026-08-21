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
from reac1subr  import *
from x4out      import *
from exfor2plot import * #plot by plotly/matplotlib

#-------------------------------------------------------------------------------
def main():

    print('  +-----------------------------------------+')
    print('  | Program: reac1.py, ver.2026-08-14       |')
    print('  | Author:  V.Zerkin, Vienna, 2021-2026    |')
    print('  | Purpose: Retrieve and plot any type of  |')
    print('  |          data from local EXFOR database |')
    print('  +-----------------------------------------+')

    if len(sys.argv)<=1: print(getHelp()); sys.exit(0)

    ct=str(datetime.datetime.now())[:19]
    print("Running: "+ct)
    x4ei=''
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
    symBorder=False
    annot=None

    x1min=None; x1max=None
    x2min=None; x2max=None
    x3min=None; x3max=None
    xmin=None; xmax=None
    x1fam=None; x2fam=None
    x3fam=None; x4fam=None
    x5fam=None

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
        print('   '+str(ii).ljust(2)+" arg: "+arg)
        if arg=='-xlog': xtype='log';  continue
        if arg=='-ylog': ytype='log';  continue
        if arg.startswith('-x1min:'):  x1min=str2float(arg[7:]);   continue
        if arg.startswith('-x1max:'):  x1max=str2float(arg[7:]);   continue
        if arg.startswith('-x2min:'):  x2min=str2float(arg[7:]);   continue
        if arg.startswith('-x2max:'):  x2max=str2float(arg[7:]);   continue
        if arg.startswith('-x3min:'):  x3min=str2float(arg[7:]);   continue
        if arg.startswith('-x3max:'):  x3max=str2float(arg[7:]);   continue
        if arg.startswith('-xmin:'):   xmin=str2float(arg[6:]);    continue
        if arg.startswith('-xmax:'):   xmax=str2float(arg[6:]);    continue
        if arg.startswith('-fx:'):     fx=str2float(arg[4:]);      continue
        if arg.startswith('-fy:'):     fy=str2float(arg[4:]);      continue
        if arg.startswith('-x:'):      xn=arg[3:];                 continue
        if arg.startswith('-x1fam:'):  x1fam=arg[7:];              continue
        if arg.startswith('-x2fam:'):  x2fam=arg[7:];              continue
        if arg.startswith('-x3fam:'):  x3fam=arg[7:];              continue
        if arg.startswith('-x4fam:'):  x4fam=arg[7:];              continue
        if arg.startswith('-x5fam:'):  x5fam=arg[7:];              continue
        if arg=='-sym':                symBorder=True;             continue
        if arg=='-lines':              lines=True;                 continue
        if arg=='-nogrp':              groupReactions=False;       continue
        if arg.startswith('-o:') and len(arg)>4: outhtml=arg[3:];  continue
        if arg.startswith('-annot:'):  annot=str2annot(arg[7:]);   continue
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

    print('\n---Input:')
    print('   Reaction: ',reacodes)
    print('   xn:       ',xn)
    print('   xrange:   ',str(xmin),'-',str(xmax))
    print('   x1range:  ',str(x1min),'-',str(x1max))
    print('   x2range:  ',str(x2min),'-',str(x2max))
    print('   x3range:  ',str(x3min),'-',str(x3max))
    print('   fx:       ',str(fx))
    print('   fy:       ',str(fy))
    print('   Output:   ',outhtml)
    print('   x4ei:     ',x4ei)
    print('')

    print("---Connect to SQL database---")
    conn=dbConn.getConnSQLx4db()
    if conn is None:
        print("___0___No connection...")
        sys.exit(1)
    print("   Connected to: ["+dbConn.dbType+"]")

    print("\n---Print summary---")
    print_reacodes(dbConn,conn,reacodes)

    print("\n---Retrieve EXFOR data from SQL database---")
    rows=getRows_sqlSearch_reacodes(dbConn,conn,reacodes,xn,x4ei)
    print("   Retrieved rows: "+str(len(rows)))

    print("\n---Extract EXFOR data from recordsets (rows)---")
    datasets=getDatasets4plot(rows,xn,fx=1/fx,fy=1/fy)
    print('datasets:',len(datasets))
    ldata=len(datasets)
    if (ldata<=0):
        print("---No data found---")
        sys.exit(2)
    #sys.exit(2)

    groupReac=False
    if groupReactions:
        print("\n---Groupping datasets by Reaction-codes---")
        reacodes=getReacodes(datasets,nPntMin) #filter only large datasets
        print('---reacodes:',len(reacodes),'\n')
        if (len(reacodes)<=0):
            print("---No data after filtering by #DataPoints:",nPntMin)
            sys.exit(2)
        groupReac=len(reacodes)>1
        datasets=getReacodes2Datasets(reacodes)
    nPnt=getNDataPoints(datasets)

    print("\n---Output EXFOR datasets to JSON file---")
    outX4Datasets(datasets,outhtml)

    data1=prepareExforDataForPlot(datasets,msize=8,groupReac=groupReac,lines=lines,lwidth=0.9,symBorder=symBorder)

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

    myOfflinePlot(data1,'Reaction:'+plotTitle
	+'<br><i>X4Pro, by V.Zerkin, NRDC, 2026, ver.2026-08-14 //running:'+ct+'</i>'
	,xtitle
	,ytitle
	,xtype=xtype,ytype=ytype
	,filename=outhtml
	,annot1=annot
	)
    return


#-------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
    print('\nProgram successfully completed')
