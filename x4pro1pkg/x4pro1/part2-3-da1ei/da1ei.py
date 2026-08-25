"""
 ***********************************************************************************
 * Copyright (C) 2021-2023 International Atomic Energy Agency (IAEA)               *
 * Copyright (C) 2023-2025 Viktor Zerkin (NRDC), v.zerkin@gmail.com                *
 *-----------------------------------------------------------------------------    *
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
 *-----------------------------------------------------------------------------    *
 *   AUTHOR:                                                                       *
 *   Viktor Zerkin, PhD, IAEA-NDS(1999-2023), NRDC(1999-2024)                      *
 *   e-mail: v.zerkin@gmail.com                                                    *
 ***********************************************************************************
"""
import os
import sys
import datetime
import math
sys.path.append('./')
sys.path.append('../')
import dbConn
from rx4da_ei   import *
from rweb12     import *
from x4out      import *
from exfor2plot import * #plot by plotly/matplotlib
from endf2plot  import *

print("Program: da1ei.py, ver. 2025-07-10")
print("Author:  V.Zerkin, IAEA-NRDC, Vienna, 2021-2025")
print("Purpose: Retrieve and plot EXFOR/ENDF angular distributions\n")
ct=str(datetime.datetime.now())[:19]
print("Running: "+ct+"\n")

quant=",da"
nexample='default'

if (len(sys.argv)>1) and (sys.argv[1]!=''): nexample=str(sys.argv[1])
print('___sys___nexample:['+nexample+']'+str(sys.argv))

xtype=None; xrange=None; ytype=None; yrange=None
outhtml='da1ei'

target="C-12";react="a,el";e4react="a,*"
x4sqlparam=" and (An>=127 and An<=134) and (En<=9e6)"
e4webparam="&an=130&mf=4&mt=40002&zap=2004"
xtype='log'; xrange=[math.log10(1.25),math.log10(11.04)]
xtype='linear'; xrange=[1,9.015]
ytype='log'; yrange=[0.3,1020]
#ytype='log'; yrange=[math.log10(0.5),math.log10(507)]
at=' \u03B8=130\u00B0'

if nexample=='ex1':
    target="O-16";react="p,el";e4react="p,*"
    x4sqlparam=" and (An>=140 and An<=140.5) and (En>=14.1e6 and En<=14.2e6)"
    x4sqlparam=" and (An>=138 and An<=141)"
    #x4sqlparam=" and (An>=138 and An<=141) and (En<=20e6)"
    e4webparam="&an=140&mf=4&mt=40002&zap=1001"
    xtype='log'; xrange=[0.5,7]
    ytype='log'; yrange=[20,507]
    outhtml='da1ei-ex1'
    at=' \u03B8=140\u00B0'

if nexample=='ex2':  #by Oscar Cabellos, 2022-11-07
    target="Fe-56";react="n,el";e4react="n,*"
    x4sqlparam=" and (An>=39 and An<=39) and (En<=9e6)"
    e4webparam="&an= 39&mf=4&mt=40002&zap=0001"
    xtype='log'; xrange=[0.01,1]
    ytype='log'; yrange=[0.1,100000]
    outhtml='da1ei-ex2'
    at=' \u03B8=39\u00B0'

print("---Retrieve EXFOR data from SQL database---")
conn=dbConn.getConnSQLx4db()
if conn is None:
    print("___0___No connection...")
    sys.exit(1)
print("Connected to: ["+dbConn.dbType+"]")

cursor=dbConn.getCursor(conn)

sql=getX4SqlSearchDA_Ei(target,react,x4sqlparam)
print("SQL:\n"+sql)

plotTitle=target+'('+react+')'+quant+at;

try:
    cursor.execute(sql)
    rows=cursor.fetchall()
except Exception as ex:
    print("___1___execute-SQL error: ", ex)
    rows=[]

conn.close()

datasets=getDatasets4plot(rows)
print('datasets:',len(datasets))
ldata=len(datasets)
if (ldata<=0):
    print("---No data found---")
    sys.exit(2)

reacodes=getReacodes(datasets,9) #reacodes with #points >9
print('reacodes:',len(reacodes),'\n')
datasets=getReacodes2Datasets(reacodes) #filter only large datasets

#_________________Output EXFOR datasets_________________
outX4Datasets(datasets,outhtml)

#_________________Preparing EXFOR data for plot_________________
data1=prepareExforDataForPlot(datasets,msize=8,groupReac=len(reacodes)>1,lines=True,lwidth=0.9)

#_________________Retrieve ENDF_________________
data2=[]
reqLibs={
#	'ENDF/B-VIII.1':"0,0,255"
	'ENDF/B-VIII.0':"0,127,127"
	,'JENDL-5':"255,127,0"
#	,'JEFF-3.3':"0,255,255"
#	,'CENDL-3.2':"255,0,0"
#	,'BROND-3.1':"255,0,255"
#	,'ENDF/B-V':"0,127,127"
#	,'TENDL-2019':"127,127,127"
	,'IBA-EVAL':"0,0,192"
	}
#data2=getSigmacalcDataForPlot('sc1c12aa130.json')
e4datasets=webEndfDataForPlot_DADE(target,e4react,e4webparam,reqLibs,1e-6,1e3)

#data2=prepareEndfDataForPlot(e4datasets,'',True)
data2=prepareEndfDataForPlot(e4datasets,'',True,lwidth=3,showAuth=True)

#_________________Store EXFOR and ENDF_________________
outX4Datasets(datasets,outhtml+"--exfor",frmArray=2)
outX4Datasets(e4datasets,outhtml+"--endf",frmArray=2)

#_________________Plot data from EXFOR and ENDF_________________
myOfflinePlot(data1+data2,'EXFOR/ENDF angular distributions d\u03c3/d\u03a9(E,\u03B8): '+plotTitle
	+'<br><i>X4Pro, by V.Zerkin, Vienna, 2021-2025, ver.2025-07-10 //run:'+ct+'</i>'
	,'Incident energy (MeV)'
	,'Cross section (mb/sr)'
	,xtype=xtype,ytype=ytype
	,xrange=xrange,yrange=yrange
#	,legendInside=False
	,filename=outhtml
	)
print('\nProgram successfully completed')
