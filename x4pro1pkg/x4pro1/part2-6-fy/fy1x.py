"""
 ***********************************************************************************
 * Copyright (C) 2021-2022 International Atomic Energy Agency (IAEA)               *
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
 *   Viktor Zerkin, PhD                                                            *
 *   e-mail: V.Zerkin@iaea.org                                                     *
 *   International Atomic Energy Agency                                            *
 *   Nuclear Data Section, P.O.Box 100                                             *
 *   Wagramerstrasse 5, Vienna A-1400, AUSTRIA                                     *
 *   Phone: +43 1 2600 21714; Fax: +43 1 26007                                     *
 *                                                                                 *
 ***********************************************************************************
"""
import os
import sys
import datetime
sys.path.append('./')
sys.path.append('../')
import dbConn
from rx4fya     import *
from rweb1fy    import *
from x4out      import *
from exfor2plot import * #plot by plotly/matplotlib
from endf2plot  import * #plot by plotly/matplotlib

print("Program: fy0x.py, ver. 2022-11-09")
print("Author:  V.Zerkin, IAEA-NDS, Vienna, 2021-2022")
print("Purpose: Retrieve and plot EXFOR fission yield (mass distribution)\n")

flagEndf=True

ct=str(datetime.datetime.now())[:19]
print("Running: "+ct+"\n")

target="U-238";react="n,f"
xtype='linear';ytype='linear'
ytype='log'
quant="mass,fy"
xrange=None; yrange=None
annot=None

EiMin=13e6;EiMax=15e6

xrange=[71,161];yrange=[0.00025,0.088];annot=('<b><sup>238</sup>U(n,f)</b>',120,0.001)

plotTitle=target+'('+react+')'+quant;
plotTitle="92-U-238(N,F)MASS,CHN,FY";
outhtml=target.replace('-','')+react.replace(',','')+'-fy'

print("---Retrieve EXFOR data from SQL database---")
conn=dbConn.getConnSQLx4db()
if conn is None:
    print("___0___No connection...")
    sys.exit(1)
print("Connected to: ["+dbConn.dbType+"]")

cursor=dbConn.getCursor(conn)

sql=getX4SqlSearchFY_MASS('92-U-238(N,F)MASS,CHN,FY','and (En>=13e6)and (En<15e6)')
print("SQL:\n"+sql)

try:
    cursor.execute(sql)
    rows=cursor.fetchall()
except Exception as ex:
    print("___1___execute-SQL error: ", ex)
    rows=[]
conn.close()
print("\nEXFOR SQL executed: OK")

datasets=getDatasets4plot(rows)
print('datasets:',len(datasets))
ldata=len(datasets)
if (ldata<=0):
    print("---No data found---")
    sys.exit(2)

reacodes=getReacodes(datasets)
print('Reaction codes:',len(reacodes),'\n')

outX4Datasets(datasets,outhtml)

data1=prepareExforDataForPlot(datasets,msize=10,groupReac=len(reacodes)>1,lines=False)

#_________________Retrieve ENDF_________________
data2=[]
reqLibs={
	'ENDF/B-VIII.0':"0,0,255"
#	,'JENDL-5':"255,0,0"
#	,'JEFF-3.3':"0,255,255"
#	,'BROND-3.1':"255,0,255"
#	,'ENDF/B-V':"127,127,127"
	}
if flagEndf:
    e4datasets=webEndfDataForPlot_FYA(target,"n*,ind_FY",reqLibs,EiMin,EiMax)
    data2=prepareEndfDataForPlot(e4datasets,'',True,autocolor=False,lwidth=3)

myOfflinePlot(data1+data2,'EXFOR fission yield FY(A,Ei): '+plotTitle
	+'<br><i>X4Pro, by V.Zerkin, IAEA-NDS, 2021-2022, ver.2022-11-09 //running:'+ct+'</i>'
	,'Atomic Mass'
	,'Yield (PART/FIS)'
	,xtype=xtype,ytype=ytype
	,filename=outhtml
	,xrange=xrange
	,yrange=yrange
	,annot1=annot
	)
print('\nProgram successfully completed')
