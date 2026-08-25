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
from rx5da      import *
from x4out      import *
from exfor2plot import *

print("Program: da0an.py, ver. 2022-12-20")
print("Author:  V.Zerkin, IAEA-NDS, Vienna, 2021-2022")
print("Purpose: Retrieve and plot EXFOR angular distributions\n")
ct=str(datetime.datetime.now())[:19]
print("Running: "+ct+"\n")

flagShow=True
if (len(sys.argv)>1) and (sys.argv[1]=='show=0'): flagShow=False

quant=",da"
target="Fe-54"; react="n,el"
x4ei=' and (En>=4.9e6 and En<=5.1e6)'

target="O-16";react="n,el"
#x4ei=' and (En>13.9e6 and En<14.2e6)'
ei=14.1e6
x4ei=' and (En>'+str(ei-0.2e6)+' and En<'+str(ei+0.2e6)+')'

plotTitle=target+'('+react+')'+quant;
outhtml='da0an'

print("---Retrieve EXFOR data from SQL database---")
conn=dbConn.getConnSQLx4db()
if conn is None:
    print("___0___No connection...")
    sys.exit(1)
print("Connected to: ["+dbConn.dbType+"]")

cursor=dbConn.getCursor(conn)

#sql=getX4SqlSearch_DA_e(target,react,' and (En=5e6)')
sql=getX4SqlSearch_DA_e(target,react,x4ei)
print("SQL:\n"+sql)

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

reacodes=getReacodes(datasets)
print('reacodes:',len(reacodes),'\n')

outX4Datasets(datasets,outhtml)

data1=prepareExforDataForPlot(datasets,msize=10,groupReac=len(reacodes)>1,lines=True,lwidth=0.5)

myOfflinePlot(data1,'Plot EXFOR angular distributions d\u03c3/d\u03a9(E,\u03B8): '+plotTitle
	+'<br><i>X4Pro, by V.Zerkin, IAEA-NDS, 2021-2022, ver.2022-12-20 //running:'+ct+'</i>'
	,'Angle (deg)'
	,'Cross section (b/sr)'
	,xtype='linear',ytype='log'
	,filename=outhtml
	,flagShow=flagShow
	,xstep30=True
	)
print('\nProgram successfully completed')
