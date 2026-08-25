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
 *   Viktor Zerkin, PhD, IAEA-NDS(1999-2023), NRDC(1999-2025)                      *
 *   e-mail: v.zerkin@gmail.com                                                    *
 ***********************************************************************************
"""
import os
import sys
import time
import datetime
sys.path.append('./')
sys.path.append('../')
from rx4db      import *
from rweb11     import *
from x4out      import *
from endf2plot  import *
from exfor2plot import *
import dbConn

print("Program: sig1x.py, ver. 2025-01-24")
print("Author:  V.Zerkin, IAEA-NRDC, Vienna, 2021-2025")
print("Purpose: Retrieve and plot EXFOR cross sections\n"
	+"	 from SQL database and ENDF data from Web")

ct=str(datetime.datetime.now())[:19]
print("Running: "+ct+"\n")
#input("Press the <ENTER> key to continue...")

target="Al-27";react="n,a";sProd=''
xtype='linear';ytype='linear'
quant=",sig"
xrange=None; yrange=None
annot=None

print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))
print('Script-name:', str(sys.argv[0]))
if (len(sys.argv)>1) and (sys.argv[1]!=''): target=str(sys.argv[1])
if (len(sys.argv)>2) and (sys.argv[2]!=''): react=str(sys.argv[2])
if (len(sys.argv)>3) and (sys.argv[3]=='log'): xtype='log'
if (len(sys.argv)>4) and (sys.argv[4]=='log'): ytype='log'
if len(sys.argv)>5 : sProd=str(sys.argv[5])

#target="Al-27";react="n,a";xrange=[5,37];yrange=[0,183];annot=('<b><sup>27</sup>Al(n,a)</b>',7,131)

plotTitle=target+'('+react+')'+quant;
outhtml=target.replace('-','')+react.replace(',','')
if sProd!='': outhtml+='2'

print("---Retrieve EXFOR data from SQL database---")
conn=dbConn.getConnSQLx4db()
if conn is None:
    print("___0___No connection...")
    sys.exit(1)
print("Connected to: ["+dbConn.dbType+"]")

cursor=dbConn.getCursor(conn)

sql=getX4SqlSearchCS(target,react,sProd=sProd)
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
print("\nEXFOR SQL executed: "+str(round(x4time,3))+"sec")

datasets=getDatasets4plot(rows)
print('datasets:',len(datasets))
ldata=len(datasets)
if (ldata<=0):
    print("---No data found---")
    sys.exit(2)

reacodes=getReacodes(datasets)
print('Reaction codes:',len(reacodes),'\n')

#_________________Output EXFOR datasets_________________
outX4Datasets(datasets,outhtml)

#_________________Preparing EXFOR data for plot_________________
data1=[]
#data1=prepareExforDataForPlot(datasets,msize=8)
data1=prepareExforDataForPlot(datasets,msize=8,groupReac=len(reacodes)>1,symBorder=True)

#_________________Retrieve and prepare ENDF data________________
data2=[]
reqLibs={'ENDF/B-VIII.0':"0,127,127"
	,'ENDF/B-VIII.1':"0,0,255"
	,'JENDL-5':"0,255,0"
	,'JEFF-3.3':"0,255,255"
	,'CENDL-3.2':"255,0,0"
	,'BROND-3.1':"255,0,255"
	,'TENDL-2019.s60':"127,127,127"
	}
t0=time.perf_counter()
e4datasets=webEndfDataForPlot_SIG(target,react,'',reqLibs,1e-6,1e3)
#data2=prepareEndfDataForPlot(e4datasets,'',True)
grp1=''
if len(reacodes)>1: grp1='grp1'
data2=prepareEndfDataForPlot(e4datasets,grp1,True,lwidth=3,showAuth=True)
t1=time.perf_counter()
print("\nEXFOR SQL executed:  "+str(round(x4time,3))+"sec")
print("ENDF Web downloaded: "+str(round(t1-t0,3))+"sec")

#_________________Plot data from EXFOR and ENDF_________________
myOfflinePlot(data1+data2
	,'EXFOR/ENDF cross sections \u03c3(E): '+plotTitle
	+'  EXFOR-datasets:'+str(len(datasets))
	+'<br><i>X4Pro, by V.Zerkin, IAEA-NRDC, 2021-2025, ver.2025-01-24 //run:'+ct+'</i>'
	,'Incident energy (MeV)'
	,'Cross section (mb)'
	,xtype=xtype,ytype=ytype
	,xrange=xrange
	,yrange=yrange
	,filename=outhtml
	,legendInside=False
	,annot1=annot
	)
print('\nProgram successfully completed')
