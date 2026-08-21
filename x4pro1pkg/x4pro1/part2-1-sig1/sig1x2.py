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

print("Program: sig1x2.py, ver. 2022-11-09")
print("Author:  V.Zerkin, IAEA-NDS, Vienna, 2021-2022")
print("Purpose: Retrieve and plot EXFOR cross sections\n"
	+"	 from SQL database and ENDF data from Web")

ct=str(datetime.datetime.now())[:19]
print("Running: "+ct+"\n")
#input("Press the <ENTER> key to continue...")

target="Al-27";react="n,a"
xtype='linear';ytype='linear'
quant=",sig"

print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))
print('Script-name:', str(sys.argv[0]))
if (len(sys.argv)>1) and (sys.argv[1]!=''): target=str(sys.argv[1])
if (len(sys.argv)>2) and (sys.argv[2]!=''): react=str(sys.argv[2])
if (len(sys.argv)>3) and (sys.argv[3]=='log'): xtype='log'
if (len(sys.argv)>4) and (sys.argv[4]=='log'): ytype='log'

plotTitle=target+'('+react+')'+quant;
outhtml=target.replace('-','')+react.replace(',','')+'2'

print("---Retrieve EXFOR data from SQL database---")
conn=dbConn.getConnSQLx4db()
if conn is None:
    print("___0___No connection...")
    sys.exit(1)
print("Connected to: ["+dbConn.dbType+"]")

cursor=dbConn.getCursor(conn)

sql=getX4SqlSearchCS(target,react)
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

datasets=getDatasets(rows)
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
data1=prepareExforDataForPlot(datasets,msize=8,groupReac=len(reacodes)>1)

#_________________Retrieve and prepare ENDF data________________
data2=[]
reqLibs={'ENDF/B-VIII.0':"0,0,255"
	,'JENDL-5':"0,255,0"
	,'JEFF-3.3':"0,255,255"
	,'CENDL-3.2':"255,0,0"
	,'BROND-3.1':"255,0,255"
	,'TENDL-2019.s60':"127,127,127"
	}
t0=time.perf_counter()
e4datasets=webEndfDataForPlot_SIG(target,react,'',reqLibs,1e-6,1e3)
#data2=prepareEndfDataForPlot(e4datasets,'',True)
data2=prepareEndfDataForPlot(e4datasets,'grp1',True,showAuth=True)
t1=time.perf_counter()
print("\nEXFOR SQL executed:  "+str(round(x4time,3))+"sec")
print("ENDF Web downloaded: "+str(round(t1-t0,3))+"sec")

#_________________Plot data from EXFOR and ENDF_________________
myOfflinePlot(data1+data2
	,'EXFOR/ENDF cross sections \u03c3(E): '+plotTitle+' //'+ct
	+"<br><i>X4Pro, by V.Zerkin, IAEA-NDS, 2021-12-07--2022-11-09</i>"
	,'Incident energy (MeV)'
	,'Cross section (mb)'
	,xtype=xtype,ytype=ytype
	,filename=outhtml
	,legendInside=False
	)
print('\nProgram successfully completed')
