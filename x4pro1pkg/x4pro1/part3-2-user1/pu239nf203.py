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
from pu239nf203sql  import *
from pu239nf203corr import *
from exfor2plot     import * #plot by plotly/matplotlib

print("Program: pu239nf203.py, ver. 2022-11-09")
print("Author:  V.Zerkin, IAEA-NDS, Vienna, 2021-2022")
print("Purpose: Local user's corrections of EXFOR cross sections ratios\n")
ct=str(datetime.datetime.now())[:19]
print("Running: "+ct+"\n")

target="Pu-239";react="n,f";reatyp="ratio"
quant="cs"
reacode=target+'('+react+')'+quant;
outhtml='user1.html'

print("---Retrieve EXFOR data from SQL database---")
#conn=dbConn.getConnSQLite('file:../x4sqlite1.db?mode=ro')
conn=dbConn.getConnSQLx4db()
if conn is None:
    print("___0___No connection...")
    sys.exit(1)
print("Connected to: ["+dbConn.dbType+"]")

cursor=dbConn.getCursor(conn)

sql=getX4SqlSearchRatioCS(target,react,reatyp,quant)
print("SQL:\n"+sql)

try:
    cursor.execute(sql)
    rows=cursor.fetchall()
except Exception as ex:
    print("___1___execute-SQL error: ", ex)
    rows=[]
conn.close()

#prepare rows to corrections
newrows=[]
for row in rows:
    newrow=dict(row)	#newrow=dict(zip(row.keys(), row))
    newrows.append(newrow)
    #print(newrow)
rows=newrows

datasets=getDatasets4plot(rows)
print('datasets:',len(datasets))
ldata=len(datasets)
if (ldata<=0):
    print("---No data found---")
    sys.exit(2)

reacodes=getReacodes(datasets)
print('reacodes:',len(reacodes),'\n')
data1=prepareExforDataForPlot(datasets,msize=7,groupReac=False,lines=False)


datasets00=rows2datasets(rows)
print('_____________datasets correction:',len(datasets00))
ii=0;correctedrows=[]
for dataset in datasets00:
    rows11=corr_dataset(dataset,cursor)
    if (len(rows11)>0): correctedrows=correctedrows+rows11
    ii+=1
    print(str(ii)+') '+str(len(correctedrows))+' '+' pt:'+str(len(rows11)))

datasets=getDatasets4plot(correctedrows)
print('corrected datasets:',len(datasets))
ldata=len(datasets)

reacodes=getReacodes(datasets)
print('corrected reacodes:',len(reacodes),'\n')
data1+=prepareExforDataForPlot(datasets,msize=8,groupReac=False,lines=False,lblPrefix='mycorr-',symBorder=True)

#_________________Retrieve ENDF_________________
data2=[]

#_________________Plot data from EXFOR and ENDF_________________
myOfflinePlot(data1+data2,'<b>Local user\'s corrections</b> of EXFOR cross sections ratios: Pu-239/U-235(n,f)CS'
	+'<br><i>X4Pro, by V.Zerkin, IAEA-NDS, 2021-2022, ver.2022-11-09 //running:'+ct+'</i>'
	,'Incident energy (MeV)'
	,'Cross section ratio'
	,xtype='log'
	,legendInside=False
	,filename=outhtml
	)
print('\nProgram successfully completed')
