"""
 ***********************************************************************************
 * Copyright (C) 2023-2025 Viktor Zerkin, v.zerkin@gmail.com                       *
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
from endf2plot_js  import *
from exfor2plot_js import *

#python -B myplot.py python -B myplot.py Pu240nf-n

def str2float(str0,ndefault):
    try:
        rr=float(str0)
    except ValueError:
        rr=ndefault
    return rr

def read_data_file(file1):
    datasets=[]
    try:
        with open(file1, encoding='utf-8') as F:
            obj1=json.loads(F.read())
            datasets=obj1['datasets']
            for dataset in datasets:
                extract_x_y_dy_dx_fc(dataset)
    except Exception as e:
        print("===Exception==="+str(e))
        datasets=[]
    return datasets

def read_plotparams(file1,default):
    plotParams=default
    try:
        with open(file1, encoding='utf-8') as F:
            plotParams=json.loads(F.read())
    except Exception as e:
        print("===Exception==="+str(e))
        plotParams=default
    return plotParams

def extract_x_y_dy_dx_fc(dataset):
    x=[]; y=[]; dy=[]; dx=[]; fc=[]
    dataset['x']=x
    dataset['y']=y
    dataset['dy']=dy
    dataset['dx']=dx
    dataset['FcApplied']=fc
    arr2=dataset.get('x_y_dy_dx_fc')
    if arr2 is None: return
    ll=len(arr2)
    for ii in range(ll):
        arr1=arr2[ii]
        l=len(arr1)
        x1=0; y1=0; dy1=0; dx1=0; fc1=1
        for ii in range(l):
            rr1=arr1[ii]
            if   ii==0: x1=rr1
            elif ii==1: y1=rr1
            elif ii==2: dy1=rr1
            elif ii==3: dx1=rr1
            elif ii==4: fc1=rr1
        x.append(x1);
        y.append(y1);
        dy.append(dy1)
        dx.append(dx1)
        fc.append(fc1)
    del dataset['x_y_dy_dx_fc']

def getReacodes(datasets):
    lx=len(datasets)
    Reacodes=[]
    ii=0; lastReacodeStr='---'; lastReacode={}
    print('\nDatasets:',len(datasets))
    for dataset in datasets:
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
        #print('\tDataset:'+str(ii)+'/'+str(lx)+') '+str(Reacode)+' '+str(dataset['DatasetID']))
    return Reacodes

def getNDataPoints(datasets):
    nn=0
    for dataset in datasets: nn+=len(dataset['x'])
    return nn

print("Program: myplot.py, ver.2025-01-22")
print("Author:  V.Zerkin, Vienna, 2025")
print("Purpose: Plot EXFOR/ENDF/MyData")

if len(sys.argv)<2:
    print('\n---Help---')
    print('Run:')
    print('	$ python  -B myplot.py ')
    print('Options:')
    print('	-x:log    X-Axes - logarithmic scale')
    print('	-y:log    Y-Axes - logarithmic scale')
    print('Examples:')
    print('	$ python -B myplot.py Pu240nf-n -o:Pu240nf-n-myplot.html')
    print('	$ python -B myplot.py Mn55ng-n -x:log -y:log')
    sys.exit(0)

ct=str(datetime.datetime.now())[:19]
print("Running: "+ct+"\n")
#input("Press the <ENTER> key to continue...")

outhtml="tmp0x"#;react="n,a";sProd=''
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

#print('Number of arguments:', len(sys.argv), 'arguments.')
#print('Argument List:', str(sys.argv))

x4datasets=[]
e4datasets=[]
plotParams0={
	 "now":		ct
	,"plotQuantity":"Cross sections \u03c3(E)"
	,"plotTitle":	"---"
	,"plotSummary":	"---"
	,"plotLegend":	"---"
	,"plotAuthor":	"X4Pro, by V.Zerkin, IAEA-NRDC, 2021-2025, ver.2025-01-22 //run:"+ct
	,"xTitle":	"Incident energy"
	,"xunit":	xunit
	,"yTitle":	"Cross section"
	,"yunit":	yunit
	,"xtype":	xtype
	,"ytype":	ytype
}
plotParams=plotParams0

for ii,arg in enumerate(sys.argv):
    print('---arg['+str(ii)+']:'+arg)
    if ii==0:	continue
    if arg=='-x:log':	      xtype='log';	  continue
    if arg=='-y:log':	      ytype='log';	  continue
    if arg.startswith('-p:'): sProd=arg[3:];	  continue
    if arg.lower()=='-g:mt':  groupByMT=True;	  continue
    if arg.lower()=='-g:n':   markRejected=True;  continue
    if arg.lower()=='-g:f':   markRejected=True;  continue
    if arg=='-nosort':	      sortDatasets=False; continue
    if arg.startswith('-emin:'): eMinEv=str2float(arg[6:],None); continue
    if arg.startswith('-emax:'): eMaxEv=str2float(arg[6:],None); continue

    if arg.startswith('-o:'): outhtml=arg[3:];	  continue
    if not arg.startswith('-'):
        file1=arg
        x4datasets+=read_data_file(file1+'--exfor.json')
        e4datasets+=read_data_file(file1+'--endf.json')
#       plotParams=read_plotparams(file1+'--plot.json',plotParams)
        plotParams=read_plotparams(file1+'--plot.json',None)
        continue

if plotParams is not None:
    plotParams['xtype']=xtype
    plotParams['ytype']=ytype

print('---Parameters:'
	+'\n   xaxis:['+xtype+']'  +'\n   ytype:['+ytype+']'
	+'\n   groupByMT:'+str(groupByMT)
	+'\n   sortDatasets:'+str(sortDatasets)
	+'\n   markRejected:'+str(markRejected)
	+'\n   outhtml:'+outhtml
	+'\n'
	)

#sys.exit(2)

data1all=[]

reacodes=getReacodes(x4datasets)
print('Reaction codes:',len(reacodes),'\n')
data1=prepareExforDataForPlot(x4datasets,msize=10,groupReac=len(reacodes)>1,symBorder=True,useRecalcFlag=True)
data1all+=data1

grp1=''
if len(reacodes)>1: grp1='grp1'
data2=prepareEndfDataForPlot(e4datasets,grp1,True,lwidth=2,showAuth=True)
data1all+=data2

plotTopLine="Cross sections \u03c3(E)<br>X4Pro, by V.Zerkin, 2021-2026, ver.2026-08-30 //run:"+ct

if plotParams is None:
    plotParams=plotParams0
    plotParams['xtype']=xtype
    plotParams['ytype']=ytype
    if len(x4datasets)>0:
        ds=x4datasets[0]
        plotParams['plotQuantity']=ds['Quantity']
        plotParams['plotTitle']=ds['Reacode']
        plotParams['yTitle']=ds['Quantity']
        plotParams['xTitle']=ds['xexpansion']
        plotParams['xunit']=ds['xBasicUnits']
        plotParams['yunit']=ds['yBasicUnits']
        plotParams['plotSummary']='Datasets:'+str(len(x4datasets))+' Datapoints:'+str(getNDataPoints(x4datasets))

#_________________Plot data from EXFOR and ENDF_________________
if plotParams is not None:
    plotTopLine=plotParams['plotQuantity']+': '+plotParams['plotTitle']+plotParams['plotSummary']
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
	,plotParams=plotParams
	)

print('\nProgram successfully completed')
