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
from rx4db      import *
from x4out      import *
from exfor2plot import * #plot by plotly/matplotlib

print("Program: sig0x.py, ver. 2022-11-09")
print("Author:  V.Zerkin, IAEA-NDS, Vienna, 2021-2022")
print("Purpose: Retrieve and plot EXFOR cross sections\n")

ct=str(datetime.datetime.now())[:19]
print("Running: "+ct+"\n")

target="Al-27"; react="n,a"; quant=",sig"
xtype='log'; ytype='linear'
plotTitle=target+'('+react+')'+quant;
outhtml=target.replace('-','')+react.replace(',','')+'-1'

print("---Retrieve EXFOR data from SQL database---")
conn=dbConn.getConnSQLx4db()
if conn is None:
    print("___0___No connection...")
    sys.exit(1)
print("Connected to: ["+dbConn.dbType+"]")

cursor=dbConn.getCursor(conn)

sql=getX4SqlSearchCS(target,react)
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

outX4Datasets(datasets,outhtml)

data1=prepareExforDataForPlot(datasets)

myOfflinePlot(data1,'EXFOR cross sections \u03c3(E): '+plotTitle
	+'<br><i>X4Pro, by V.Zerkin, IAEA-NDS, 2021-2022, ver.2022-11-09 //running:'+ct+'</i>'
	,'Incident energy (MeV)'
	,'Cross section (mb)'
	,xtype=xtype,ytype=ytype
	,filename=outhtml
	,legendInside=False
	)
print('\nProgram successfully completed')
