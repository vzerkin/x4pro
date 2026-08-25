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
import json
sys.path.append('./')
sys.path.append('../')
import dbConn
from x13597002sub import *
from expert_corr  import *
from rweb11       import *
from exfor2plot   import * #plot by plotly/matplotlib
from endf2plot    import *

print("Program: x13597002.py, ver. 2022-11-09")
print("Author:  V.Zerkin, IAEA-NDS, Vienna, 2021-2022")
print("Purpose: Apply experts corrections from database to EXFOR data\n")
ct=str(datetime.datetime.now())[:19]
print("Running: "+ct+"\n")

target="Zn-64";react="n,p";quant=",sig"
reacode=target+'('+react+')'+quant;
outhtml='expert1'

print("---Retrieve EXFOR data from SQL database---")
#conn=dbConn.getConnSQLite('file:../x4sqlite1.db?mode=ro')
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

newrows=[]
for row in rows:
    newrow=dict(row)	#newrow=dict(zip(row.keys(), row))
    xdat=newrow.get('xdat')
    if (xdat is not None):
        xdat1=json.loads(xdat)
        newrow['xdat']=xdat1
    newrows.append(newrow)
    #print(newrow)
rows=newrows
with open(outhtml+'-orig.json','w') as outfile:
    json.dump(rows,outfile,indent=2)

datasets=getDatasets4plot(rows)
print('Retrieved datasets:',len(datasets))
ldata=len(datasets)
if (ldata<=0):
    print("---No data found---")
    sys.exit(2)

reacodes=getReacodes(datasets)
print('Reaction codes: ',len(reacodes),'\n')
#data1=prepareExforDataForPlot(datasets,lines=True,lwidth=0.5)
data1=prepareExforDataForPlot(datasets)

datasets00=getDatasets00(rows)
print('_____________Experts Correction datasets:',len(datasets00))
ii=0;datasets11=[]
for dataset in datasets00:
    #reload(corr_subr)
    rows11=corr_dataset(dataset,cursor)
    if (len(rows11)>0): datasets11=datasets11+rows11
    ii+=1
    print('Corr:'+str(ii)+') '+str(len(datasets11))+' '+' pt:'+str(len(rows11)))

rows=datasets11	#corrected datasets
datasets=getDatasets4plot(rows)
print('Corrected datasets:',len(datasets))
ldata=len(datasets)
if (ldata<=0):
    print("---No data found---")
    #sys.exit(2)
with open(outhtml+'-corr.json','w') as outfile:
    json.dump(rows,outfile,indent=2)

reacodes=getReacodes(datasets)
print('Corrected reacodes:',len(reacodes),'\n')
#data1+=prepareExforDataForPlot(datasets,lines=True,lwidth=0.5)
data1+=prepareExforDataForPlot(datasets,symBorder=True)

conn.close()


#_________________Retrieve ENDF_________________
data2=[]
reqLibs={
	'ENDF/B-VIII.0':"0,0,255"
	,'JENDL-5':"0,255,0"
#	,'JENDL-4.0':"0,255,0"
#	,'JEFF-3.3':"0,255,255"
	,'IAEA-Therapeutic':"255,0,0"
#	,'CENDL-3.2':"255,127,127"
#	,'BROND-3.1':"255,0,255"
#	,'TENDL-2019.s60':"127,127,127"
	}
#data2=getEndfDataForPlot(target,react,reqLibs,'',True)
e4datasets=webEndfDataForPlot_SIG(target,react,'',reqLibs,1e-6,1e3)
data2=prepareEndfDataForPlot(e4datasets,'',True)

#_________________Plot data from EXFOR and ENDF_________________
myOfflinePlot(data1+data2,'<b>Apply experts corrections from database</b> to EXFOR data: '+reacode
	+'<br><i>X4Pro, by V.Zerkin, IAEA-NDS, 2021-2022, ver.2022-11-09 //running:'+ct+'</i>'
	,'Incident energy (MeV)'
	,'Cross section (mb)'
	,legendInside=False
	,filename=outhtml
	)
print('\nProgram successfully completed')
