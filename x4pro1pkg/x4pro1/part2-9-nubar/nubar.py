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
from rx4nubar   import *
from rweb12     import *
from x4out      import *
from exfor2plot import * #plot by plotly/matplotlib
from endf2plot  import *

print("Program: nubar.py, ver. 2026-08-24")
print("Author:  V.Zerkin, Vienna, 2026")
print("Purpose: Retrieve and plot EXFOR and ENDF nu-bar data\n")

ct=str(datetime.datetime.now())[:19]
print("Running: "+ct+"\n")

xmin=None; xmax=None
ymin=None; ymax=None
xrange=None; yrange=None;
xtype='linear';ytype='linear'
#ytype='log'
x4sqlparam=" and sf8='' "
flagEndf=True
e4webparam=""
outhtml=None

#---default
target="U-235"
react="n,f"
quant="pr,nu"
#quant="dl,nu"
#quant=",nu"

def input2x4quant(str0,default):
    if str0 is None: return default
    str0=str0.lower()
    print("   ---input2x4quant:["+str0+"]")
    if str0=='pr':  return "pr,nu"
    if str0=='dl':  return "dl,nu"
    if str0=='tot': return ",nu"
    return default

def str2float(str1):
    if str1 is None: return None
    try: rr=float(str1)
    except ValueError: rr=None
#   print("   ---str2float:["+str1+"] --> "+str(rr))
    return rr

print('\n---Arguments from command-line---')
for ii,arg in enumerate(sys.argv):
    if (ii==0): continue
    print('   '+str(ii).ljust(2)+" arg: "+arg)
    if arg=='-xlog': xtype='log';  continue
    if arg=='-ylog': ytype='log';  continue
    if arg.startswith('-xmin:'):  xmin=str2float(arg[6:]);        continue
    if arg.startswith('-xmax:'):  xmax=str2float(arg[6:]);        continue
    if arg.startswith('-ymin:'):  ymin=str2float(arg[6:]);        continue
    if arg.startswith('-ymax:'):  ymax=str2float(arg[6:]);        continue
    if arg.startswith('-q:'): quant=input2x4quant(arg[3:],quant); continue
    if arg.startswith('-o:') and len(arg)>4: outhtml=arg[3:];     continue
    if arg.startswith('-'): continue
    target=arg

if xmin is not None or xmax is not None: xrange=[xmin,xmax]
if ymin is not None or ymax is not None: yrange=[ymin,ymax]

if quant.lower()=="pr,nu": e4reac="n,nu_p"
if quant.lower()=="dl,nu": e4reac="n,nu_d"
if quant.lower()==",nu":   e4reac="n,nu_tot"

plotTitle=target+'('+react+')'+quant;

ytitle='Nu-bar'
if quant.upper().startswith('PR'): ytitle='Prompt '+ytitle
elif quant.upper().startswith('DL'): ytitle='Delayed '+ytitle
elif quant.startswith(','): ytitle='Total '+ytitle
ytitle+=' (part/fis)'

if outhtml is None:
    outhtml=str(target.replace('-','').title()+react.replace(',','')+
	'_'+quant.replace(',','-').replace('%',''))

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

#sql=getX4SqlSearch_NUBAR('92-U-238(N,F),PR,NU','')
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

datasets=getDatasets4plot(rows,fx=1e-6)
print('datasets:',len(datasets))
ldata=len(datasets)
if (ldata<=0):
    print("---No EXFOR data found---")
#    sys.exit(2)

if len(datasets)>0:
    plotTitle=datasets[0]['Reacode']

reacodes=getReacodes(datasets)
print('Reaction codes:',len(reacodes),'\n')
plotTitle+='  Exp.Datasets:'+str(len(datasets))
plotTitle+='  Points:'+str(len(rows))

outX4Datasets(datasets,outhtml)

#_________________Retrieve ENDF_________________
data2=[]
reqLibs={
	'ENDF/B-VIII.0':"0,0,255",
#	'JENDL-5':"0,255,0",
#	'JEFF-3.3':"0,255,255"
	'JEFF-3.1':"0,255,255"
#	'JEF-2.2':"0,255,255"
#	,'CENDL-3.2':"255,0,0"
#	,'CENDL-2':"255,0,0"
	,'BROND-3.1':"255,0,255"
	,'ENDF/B-V':"127,127,127"
	}
if flagEndf:
    e4datasets=webEndfDataForPlot_DADE(target,e4reac,e4webparam,reqLibs,1e-6,1,quantPrexix="")
    print('---e4datasets:',len(e4datasets))
#   data2=prepareEndfDataForPlot(e4datasets,'',True,autocolor=True,lwidth=3,showAuth=True)
    data2=prepareEndfDataForPlot(e4datasets,'',True,lwidth=3,showAuth=True)

#_________________Store EXFOR and ENDF_________________
outX4Datasets(datasets,outhtml+"--exfor",frmArray=2)
outX4Datasets(e4datasets,outhtml+"--endf",frmArray=2)

#data1=prepareExforDataForPlot(datasets,msize=10,groupReac=len(reacodes)>1,lines=False)
data1=prepareExforDataForPlot(datasets,msize=10,groupReac=len(reacodes)>1,lines=True,lwidth=0.9,symBorder=True)

myOfflinePlot(data1+data2,'EXFOR-ENDF NUBAR: '+plotTitle
	+'<br><i>X4Pro, by V.Zerkin, 2026, ver.2026-08-24 //running:'+ct+'</i>'
	,'Incident Energy (MeV)'
	,ytitle
	,xtype=xtype,ytype=ytype
	,xrange=xrange,yrange=yrange
	,filename=outhtml
	)
print('\nProgram successfully completed')
