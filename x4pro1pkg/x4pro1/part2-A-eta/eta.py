"""
 **********************************************************************
 * Copyright (c) 2026 Viktor Zerkin, v.zerkin@gmail.com               *
 * Author:   Viktor Zerkin, PhD, IAEA-NDS(1999-2023), NRDC(1999-2026) *
 * License:  MIT License (MIT)                                        *
 **********************************************************************
"""
import os
import sys
import time
import datetime
sys.path.append('./')
sys.path.append('../')
import dbConn
from rx4eta     import *
from rweb12     import *
from x4out      import *
from exfor2plot import * #plot by plotly/matplotlib
from endf2plot  import *

print("Program: eta.py, ver.2026-08-31")
print("Author:  V.Zerkin, Vienna, 2026")
print("Purpose: Retrieve and plot EXFOR and ENDF data\n"
     +"         Eta: neutron yield per nonelastic even\n")

ct=str(datetime.datetime.now())[:19]
print("Running: "+ct+"\n")

xmin=None; xmax=None
ymin=None; ymax=None
xrange=None; yrange=None;
xtype='linear';ytype='linear'
#ytype='log'
annot=None
x4sqlparam=" and sf8='' "
flagEndf=True
groupReactions=False
e4webparam=""
outhtml=None
plotLegend=''
fx=1; xunit="eV"
fy=1; yunit="prd/reac"

#---default
target="U-235"
react="n,abs"
quant=",eta"
e4reac="n,nu_tot"
e4mt=18
e4webparam='&eta='+str(e4mt)
#flagEndf=False

react="n,non"
react="n,abs;n,non"
#react="n,el"; e4webparam='&eta=2'
#groupReactions=True

#target="Pu-239"
#target="U-233"


def str2float(str1):
    if str1 is None: return None
    try: rr=float(str1)
    except ValueError: rr=None
#   print("   ---str2float:["+str1+"] --> "+str(rr))
    return rr

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

print('\n---Arguments from command-line---')
for ii,arg in enumerate(sys.argv):
    if (ii==0): continue
    print('   '+str(ii).ljust(2)+" arg: "+arg)
    if arg=='-xlog': xtype='log';  continue
    if arg=='-ylog': ytype='log';  continue
    if arg.startswith('-xmin:'):  xmin=str2float(arg[6:]);	continue
    if arg.startswith('-xmax:'):  xmax=str2float(arg[6:]);	continue
    if arg.startswith('-ymin:'):  ymin=str2float(arg[6:]);	continue
    if arg.startswith('-ymax:'):  ymax=str2float(arg[6:]);	continue
    if arg.startswith('-o:') and len(arg)>4: outhtml=arg[3:];	continue
    if arg.startswith('-r:'): react=arg[3:];			continue
    if arg.startswith('-t:'): target=arg[3:];			continue
    if arg.startswith('-mt:'): e4webparam='&eta='+arg[4:];	continue
    if arg.startswith('-annot:'):  annot=str2annot(arg[7:]);	continue
    if arg.startswith('-'): continue
    target=arg

if xmin is not None or xmax is not None: xrange=[xmin,xmax]
if ymin is not None or ymax is not None: yrange=[ymin,ymax]

if react.lower()=="n,el": e4mt=2
e4webparam='&eta='+str(e4mt)

plotTitle='EXFOR:'+target.title()+'('+react+')'+quant+' ENDF:MT='+str(e4mt)

ytitle='Neutron yield ETA'

if outhtml is None:
    outhtml=target.replace('-','').title()
    if react.lower().find("n,abs")<0 and react.lower().find("n,non")<0: outhtml+=react.replace(',','').replace(';','-')
    outhtml+=quant.replace(',','-').replace('%','')

print('\n---Parameters:')
print('   target:  '+target)
print('   x4react: '+react)
print('   e4react: '+e4reac)
print('   x4quant: '+quant)
print('   Output:  '+outhtml)
print('   x-axis:  '+str(xtype).ljust(7)+ ' range: '+str(xrange))
print('   y-axis:  '+str(ytype).ljust(7)+ ' range: '+str(yrange))
print('')


print("---Retrieve EXFOR data from SQL database---")
conn=dbConn.getConnSQLx4db()
if conn is None:
    print("___0___No connection...")
    sys.exit(1)
print("Connected to: ["+dbConn.dbType+"]")

cursor=dbConn.getCursor(conn)

sql=getX4SqlSearch_NUBAR(target,react,quant,x4sqlparam)
print("SQL:\n"+sql)

t0=time.perf_counter()
try:
    cursor.execute(sql)
    rows=cursor.fetchall()
except Exception as ex:
    print("___1___execute-SQL error: ", ex)
    rows=[]
t1=time.perf_counter()
conn.close()
x4time=t1-t0
print("\nEXFOR SQL executed: "+str(round(x4time,3))+"sec rows:"+str(len(rows)))

datasets=getDatasets4plot(rows,fx=1)
print('datasets:',len(datasets))
ldata=len(datasets)
if (ldata<=0):
    print("---No EXFOR data found---")
#    sys.exit(2)

if len(datasets)>0:
#   plotTitle='EXFOR:'+datasets[0]['Reacode']+'  ENDF:MT'+str(e4mt)
    plotTitle=' EXFOR:'+datasets[0]['Target']
    str1=''
    for dataset in datasets:
        if str1.find(dataset['Reaction'].lower())<0:
            str1+='('+dataset['Reaction'].lower()+')'
    plotTitle+=str1
    plotTitle+='  ENDF:MT'+str(e4mt)

groupReac=False
if groupReactions:
    reacodes=getReacodes(datasets)
    print('Reaction codes:',len(reacodes),'\n')
    groupReac=len(reacodes)>1
x4_summary=''
x4_summary+=' Exp.datasets:'+str(len(datasets))
x4_summary+=', points:'+str(len(rows))

outX4Datasets(datasets,outhtml)

#_________________Preparing EXFOR data for plot_________________
data1=[]
#data1=prepareExforDataForPlot(datasets,msize=10,groupReac=len(reacodes)>1,lines=False)
#data1=prepareExforDataForPlot(datasets,msize=10,groupReac=groupReac,lines=True,lwidth=0.9,symBorder=True,bwColor=True)
data1=prepareExforDataForPlot(datasets,msize=10,groupReac=groupReac,lines=True,lwidth=0.9,symBorder=True)

#_________________Retrieve ENDF_________________
data2=[]
e4datasets=[]
reqLibs={
	'ENDF/B-VIII.0':"0,0,255",
#	'JENDL-5':"0,255,0",
	'JEFF-4.0':"255,0,0"
#	'JEFF-3.3':"0,255,255",
#	'JEFF-3.1':"0,255,255",
#	'JEF-2.2':"0,255,255",
#	'CENDL-3.2':"255,0,0"
#	'CENDL-2':"255,0,0"
#	'BROND-3.1':"255,0,255"
#	'ENDF/B-V':"127,127,127"
	}
if flagEndf:
    #_________________Retrieve ENDF_________________
    e4datasets=webEndfDataForPlot_DADE(target,e4reac,e4webparam,reqLibs,1,1,quantPrexix="")
    print('---e4datasets:',len(e4datasets))
    #_________________Preparing ENDF data for plot_________________
#   data2=prepareEndfDataForPlot(e4datasets,'',True,autocolor=True,lwidth=3,showAuth=True)
#   data2=prepareEndfDataForPlot(e4datasets,'eee',True,lwidth=3,showAuth=True)
    data2=prepareEndfDataForPlot(e4datasets,'',True,lwidth=3,showAuth=True)

if len(datasets)+len(e4datasets)<=0:
    print("---No data found---")
    sys.exit(1)

#_________________Store EXFOR and ENDF_________________
outX4Datasets(datasets,outhtml+"--exfor",frmArray=2)
outX4Datasets(e4datasets,outhtml+"--endf",frmArray=2)


plotParams={
	 "now":		ct
#	,"plotQuantity":"Neutron yield per nonelastic event \u03B7"
	,"plotQuantity":"Eta neutron yield"
	,"plotTitle":	plotTitle
	,"plotSummary":	x4_summary
	,"plotLegend":	plotLegend
	,"plotAuthor":	"X4Pro, by V.Zerkin, 2021-2026, ver.2026-08-31 //run:"+ct
	,"xTitle":	"Incident energy"
	,"xunit":	xunit
	,"yTitle":	ytitle
	,"yunit":	yunit
	,"xtype":	xtype
	,"ytype":	ytype
}

#_________________Output plot parameters________________________
save1obj2file(plotParams,outhtml+"--plot")

plotTopLine=plotParams['plotQuantity']+' '+plotParams['plotTitle']+' '+plotParams['plotSummary']
#plotTopLine+='<br>'+plotParams['plotLegend']
plotTopLine+='<br><i>'+plotParams['plotAuthor']+'</i>'

myOfflinePlot(data1+data2
	,plotTopLine
	,plotParams['xTitle']+', '+plotParams['xunit']
	,plotParams['yTitle']+', '+plotParams['yunit']
	,xtype=plotParams['xtype']
	,ytype=plotParams['ytype']
	,xrange=xrange
	,yrange=yrange
	,filename=outhtml
	,legendInside=False
	,annot1=annot
	)

print('\nProgram successfully completed')
