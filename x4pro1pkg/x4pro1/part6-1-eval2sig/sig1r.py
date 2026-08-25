"""
 ***********************************************************************************
 * Copyright (C) 2023-2025 Viktor Zerkin (NRDC), v.zerkin@gmail.com                *
 *---------------------------------------------------------------------------------*
 * Permission is hereby granted, free of charge, to any person obtaining a copy    *
 * of this software and associated documentation files (the "Software"), to deal   *
 * in the Software without restriction, including without limitation the rights    *
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell       *
 * copies of the Software, and to permit persons to whom the Software is furnished *
 * to do so, subject to the following conditions:                                  *
 *                                                                                 *
 * The above copyright notice and this permission notice shall be included in all  *
 * copies or substantial portions of the Software.                                 *
 *                                                                                 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR      *
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,        *
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE     *
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER          *
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,   *
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN       *
 * THE SOFTWARE.                                                                   *
 *                                                                                 *
 *---------------------------------------------------------------------------------*
 *   AUTHOR: Viktor Zerkin, PhD, IAEA(1999-2023), NRDC(1996-2025)                  *
 *   e-mail: v.zerkin@gmail.com                                                    *
 ***********************************************************************************
"""
import os
import sys
import time
import datetime
sys.path.append('./')
sys.path.append('../')
from rx4dbr      import *
from rweb11      import *
from x4out       import *
from endf2plot   import *
from exfor2plot  import *
from x4evalscore import *
import dbConn

import functools 
def cmpDatasets(ds1,ds2):
    if ds1['Reacode']<ds2['Reacode']: return -1
    if ds1['Reacode']>ds2['Reacode']: return 1
    if ds1['year']<ds2['year']: return 1
    if ds1['year']>ds2['year']: return -1
    if ds1['DatasetID']<ds2['DatasetID']: return -1
    if ds1['DatasetID']>ds2['DatasetID']: return 1
    if ds1['x4lbl']<ds2['x4lbl']: return -1
    if ds1['x4lbl']>ds2['x4lbl']: return 1
    return 0

def str2float(str0,ndefault):
    try:
        rr=float(str0)
    except ValueError:
        rr=ndefault
    return rr

def read_myBlackListFile(file1):
    blackList={}
    print('---Reading blackList '+file1+' with datasets to be ignored')
    try:
        with open(file1, encoding='utf-8') as F:
            blackList=json.loads(F.read())
    except Exception as ex:
        print("___Reading JSON file error: ",ex)
        return blackList
    print('---blackList: '+str(len(blackList))+' records')
	#---filter comments starting with #
    blackList={key:val for key,val in blackList.items() if not key.startswith('#')}
    print('---blackList: '+str(len(blackList))+' datasets')
    return blackList

print("Program: sig1r.py, ver. 2025-03-26")
print("Author:  V.Zerkin, Vienna, 2024-2025")
print("Purpose: Retrieve EXFOR cross sections, ratios\n"
	+"         and monitor data from SQL database,\n"
	+"         convert ratios to cross sections,\n"
	+"         renormalize cross sections to new monitors,\n"
	+"         search and download ENDF data from Web,\n"
	+"         plot evaluated and experimental data."
	)

if len(sys.argv)<3:
    print('\n---Help---')
    print('Run:')
    print('	$ python  -B sig1r.py target reaction [options]')
    print('	$ python3 -B sig1r.py target reaction [options]')
    print('Options:')
    print('	-o:file   output file (without extension)')
    print('	-p:<meta> product state: m, m1, m2, g, "%" (% - all)')
    print('	-x:log    X-Axes - logarithmic scale')
    print('	-y:log    Y-Axes - logarithmic scale')
    print('	-emin:nn  min.energy to retrieve EXFOR and ENDF data')
    print('	-emax:nn  max.energy ...')
    print('	-g:MT     group datasets by MT')
#    print('	-g:n      mark and group rejected datasets')
    print('	-g:f      mark and group datasets by evaluators flags')
    print('	-nosort   no global datasets sorting')
    print('Examples:')
    print('	$ python -B sig1r.py Al-27 n,a -x:log')
    print('	$ python -B sig1r.py Al-27 n,a -x:log -p:"%"')
    print('	$ python -B sig1r.py mn-55 n,g -x:log -y:log')
    print('	$ python -B sig1r.py mn-55 n,a -x:log -nosort')
    print('	$ python -B sig1r.py zn-64 n,p -nosort')
    print('	$ python -B sig1r.py U-235 n,g -x:log -y:log -g:MT')
    print('	$ python -B sig1r.py Pu-240 n,f -emin:6.5e+6 -emax:23e+6')
    sys.exit(0)

ct=str(datetime.datetime.now())[:19]
print("Running: "+ct+"\n")
#input("Press the <ENTER> key to continue...")

target="Al-27";react="n,a";sProd=''
xtype='linear';ytype='linear'
quant=",sig"
xrange=None; yrange=None
annot=None
groupByMT=False #group EXFOR datasets by EXFOR reaction code
#groupByMT=True  #group by <EXFOR.Target,ENDF.MT>
#If there is more than one group, they will be shown in separated sections
sortDatasets=True
eMinEv=None
eMaxEv=None
#eMinEv=6.2e+6;eMaxEv=23e+6
markRejected=False
fx=1e-6; xunit="MeV"	#fx=1e-3; xunit="keV"
fy=1e3;  yunit="mb"	#fy=1;    yunit="barn"
myBlackListFile="myBlackList.json"
myBlackList={}
outhtml=None

#print('Number of arguments:', len(sys.argv), 'arguments.')
#print('Argument List:', str(sys.argv))

for ii,arg in enumerate(sys.argv):
    print('---arg['+str(ii)+']:'+arg)
    if ii==0:	continue
    if ii==1 and arg!='':     target=arg;	  continue
    if ii==2 and arg!='':     react=arg;	  continue
    if arg=='-x:log':	      xtype='log';	  continue
    if arg=='-y:log':	      ytype='log';	  continue
    if arg.startswith('-p:'): sProd=arg[3:];	  continue
    if arg.startswith('-o:'): outhtml=arg[3:];	  continue
    if arg.lower()=='-g:mt':  groupByMT=True;	  continue
    if arg.lower()=='-g:n':   markRejected=True;  continue
    if arg.lower()=='-g:f':   markRejected=True;  continue
    if arg=='-nosort':	      sortDatasets=False; continue
    if arg.startswith('-emin:'): eMinEv=str2float(arg[6:],None); continue
    if arg.startswith('-emax:'): eMaxEv=str2float(arg[6:],None); continue

#if sProd!='': groupByMT=False

#target="Al-27";react="n,a";xrange=[5,37];yrange=[0,183];annot=('<b><sup>27</sup>Al(n,a)</b>',7,131)

plotTitle=target+'('+react+')'+quant;
if outhtml is None:
    outhtml=target.replace('-','')+react.replace(',','')
    if sProd!='': outhtml+='2'
    if markRejected: outhtml+='-n'

myBlackList=read_myBlackListFile(myBlackListFile)

print('\n===Parameters:'
	+'\n  target: "'+target+'"'+'\n   react: "'+react+'"'
	+'\n   quant: "'+quant+'"'  +'\n   sProd: "'+sProd+'"'
	+'\n   xaxis: "'+xtype+'"'  +'\n   ytype: "'+ytype+'"'
	+'\n   groupByMT: '+str(groupByMT)
	+'\n   sortDatasets: '+str(sortDatasets)
	+'\n   markRejected: '+str(markRejected)
	+'\n   myBlackListFile: "'+str(myBlackListFile)+'"'
	+'\n   myBlackList: '+str(len(myBlackList))+' datasets'
	+'\n   outhtml: "'+outhtml+'"'
	+'\n'
	)


if plotTitle.lower()=='zn-64(n,p),sig': xrange=[0.01,22] #for plot: initial x-range


print("---Retrieve EXFOR data from SQL database---")
conn=dbConn.getConnSQLx4db()
if conn is None:
    print("___0___No connection...")
    sys.exit(1)
print("Connected to: ["+dbConn.dbType+"]")

print('\n---Read x4evalscores from X4Pro database...')
x4evalflags=get_x4evalscores(conn)
print('---x4evalflags:'+str(len(x4evalflags))+' datasets')
#sys.exit(2)

cursor=dbConn.getCursor(conn)

sql=getX4SqlSearchCS(target,react,sProd=sProd,eMinEv=eMinEv,eMaxEv=eMaxEv)
print("SQL:\n"+sql)

t0=time.perf_counter()
try:
    cursor.execute(sql)
    rows=cursor.fetchall()
except Exception as ex:
    print("___1___execute-SQL error: ", ex)
    rows=[]
x4time=time.perf_counter()-t0
print("\nEXFOR SQL executed: "+str(round(x4time,3))+"sec")

conn.close()

#extract all Entries
entries=[ds['DatasetID'][:5] for ds in rows]
entries=sorted(set(entries))
print("---All entries: "+str(len(entries)))
strEntries='*;'.join(entries)+'*;'
print(strEntries)
#sys.exit(2)


#filter rows having MF=3
rows_MF3=list(filter(lambda x:(x['MF']==3),rows))
x4original=getDatasets4plot(rows_MF3,fx=fx,fy=fy,groupByMT=groupByMT
	,flagRenormCS=False,flagRenormDD=False,flagRenormDM=False
	,datasetBlackList=myBlackList
	,x4evalflags=x4evalflags,markRejected=markRejected)
print("---Extracted original datasets: "+str(len(x4original)))

#filter rows having data for automatic renormalization
rows_MF3auto=list(filter(lambda x:
	   (x['m0'] is not None and x['m1'] is not None)
	or (x['FcDecayData'] is not None)
	or (x['FcDecayMon'] is not None)
	,rows_MF3))
x4auto=getDatasets4plot(rows_MF3auto,fx=fx,fy=fy,groupByMT=groupByMT
	,flagRenormCS=True,flagRenormDD=True,flagRenormDM=True
	,datasetBlackList=myBlackList
	,x4evalflags=x4evalflags,markRejected=markRejected)
print("---Extracted automatically renormalized datasets: "+str(len(x4auto)))

#filter rows having MF=203 (cross section ratio)
#Note. Denominator's CS is given - see SQL WHERE: "x4pro_c5dat.m1 is not Null"
rows_MF203=list(filter(lambda x:(x['MF']==203),rows))
x4ratio2cs=getDatasets4plot(rows_MF203,fx=fx,fy=fy,groupByMT=groupByMT
	,datasetBlackList=myBlackList
	,x4evalflags=x4evalflags,markRejected=markRejected)
print("---Extract datasets converted from ratios: "+str(len(x4ratio2cs)))

datasets=x4original+x4auto+x4ratio2cs
x4_summary='datasets:'+str(len(datasets)) \
	+' original:'+str(len(x4original))+'X' \
	+' auto-corrected:'+str(len(x4auto))+'A*' \
	+' ratio2cs:'+str(len(x4ratio2cs))+'R#'
print(x4_summary)

ldata=len(datasets)
if (ldata<=0):
    print("---No data found---")
    sys.exit(2)

#datasets=sorted(datasets,key=lambda x:(x['Reacode']+str(x['year'])+x['DatasetID']+x['x4lbl']),reverse=True)
#if groupByMT:
#if sProd!='': datasets=sorted(datasets,key=functools.cmp_to_key(cmpDatasets))
if sortDatasets: datasets=sorted(datasets,key=functools.cmp_to_key(cmpDatasets))

reacodes=getReacodes(datasets)
print('Reaction codes:',len(reacodes),'\n')

#_________________Output EXFOR datasets_________________
outX4Datasets(datasets,outhtml+"--exfor",frmArray=2)

#_________________Preparing EXFOR data for plot_________________
data1=[]
#data1=prepareExforDataForPlot(datasets,msize=8)
data1=prepareExforDataForPlot(datasets,msize=10,groupReac=len(reacodes)>1,symBorder=True,useRecalcFlag=True)

#_________________Retrieve ENDF data________________
data2=[]
reqLibs={
#	'ENDF/B-VIII.0':"0,127,127"
	'ENDF/B-VIII.1':"0,0,255"
#	,'JENDL-5':"0,255,0"
	,'JEFF-3.3':"0,127,63"
	,'CENDL-3.2':"255,0,0"
	,'BROND-3.1':"255,0,255"
#	,'TENDL-2019.s60':"127,127,127"
	}
t0=time.perf_counter()
e4datasets=[]
e4datasets=webEndfDataForPlot_SIG(target,react,'',reqLibs,fx,fy,eMinEv=eMinEv,eMaxEv=eMaxEv)
e4time=time.perf_counter()-t0
print("")
print("EXFOR SQL executed:  "+str(round(x4time,3))+"sec")
print("ENDF Web downloaded: "+str(round(e4time,3))+"sec")

#_________________Output ENDF datasets_________________
outX4Datasets(e4datasets,outhtml+"--endf",frmArray=2)

#_________________Preparing ENDF data for plot_________________
#data2=prepareEndfDataForPlot(e4datasets,'',True)
grp1=''
if len(reacodes)>1: grp1='grp1'
data2=prepareEndfDataForPlot(e4datasets,grp1,True,lwidth=2,showAuth=True)

#_________________Preparing plotting____________________________
#x4_summary+='<br>Evaluators flags: y:accepted, n:rejected\
plotLegend='Eva-flags: y:accepted, n:rejected\
, R:reviewed, T:theoretical comparison\
, N:no pdf, 1:good, 2:doubtful, 3:outlier'

plotParams={
	 "now":		ct
	,"plotQuantity":"Cross sections \u03c3(E)"
	,"plotTitle":	plotTitle
	,"plotSummary":	x4_summary
	,"plotLegend":	plotLegend
	,"plotAuthor":	"X4Pro, by V.Zerkin, IAEA-NRDC, 2021-2025, ver.2025-03-26 //run:"+ct
	,"xTitle":	"Incident energy"
	,"xunit":	xunit
	,"yTitle":	"Cross section"
	,"yunit":	yunit
	,"xtype":	xtype
	,"ytype":	ytype
}

#_________________Output plot parameters________________________
save1obj2file(plotParams,outhtml+"--plot")

#_________________Plot data from EXFOR and ENDF_________________
plotTopLine=plotParams['plotQuantity']+': '+plotParams['plotTitle']+' '+plotParams['plotSummary']
plotTopLine+='<br>'+plotParams['plotLegend']
plotTopLine+='<br><i>'+plotParams['plotAuthor']+'</i>'

myOfflinePlot(data1+data2
	,plotTopLine
	,plotParams['xTitle']+'('+plotParams['xunit']+')'
	,plotParams['yTitle']+'('+plotParams['yunit']+')'
	,xtype=plotParams['xtype']
	,ytype=plotParams['ytype']
	,xrange=xrange
	,yrange=yrange
	,filename=outhtml
	,legendInside=False
	,annot1=annot
	)

print('\nProgram successfully completed')
