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
from mn55na_sub import *
from auto_corr  import *
from rweb11     import *
from x4out      import *
from exfor2plot import * #plot by plotly/matplotlib
from endf2plot  import *

print("Program: mn55na.py, ver. 2022-11-09")
print("Author:  V.Zerkin, IAEA-NDS, Vienna, 2021-2022")
print("Purpose: Automatic correction of EXFOR cross sections according to new Standard CS\n")
ct=str(datetime.datetime.now())[:19]
print("Running: "+ct+"\n")

target="Mn-55";react="n,a"
quant=",sig"
plotTitle=target+'('+react+')'+quant;
outhtml='auto1'
annot=('<b><sup>55</sup>Mn'+'('+react+')'+quant+'</b>',15,12.5)

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

newrows=rows2dicts(rows) #conv list of objects into list of dictionaries
rows=newrows
with open('mn55na-0pt.json','w') as outfile:
    json.dump(rows,outfile,indent=2)

datasets=getDatasets4plot(rows) #Datasets for plotting
print('datasets:',len(datasets))
ldata=len(datasets)
if (ldata<=0):
    print("---No data found---")
    sys.exit(2)

reacodes=getReacodes(datasets)
print('reacodes:',len(reacodes),'\n')
outX4Datasets(datasets,'mn55na-0ds.json')
data1=prepareExforDataForPlot(datasets,msize=8,groupReac=False,lines=False)


datasets00=getDatasets00(rows) #Datasets: retrieved rows
print('_____________datasets00:',len(datasets00))
ii=0;datasets11=[]
for dataset in datasets00:
    #reload(corr_subr)
    rows11=auto_corr_dataset(dataset)
    if (len(rows11)>0): datasets11=datasets11+rows11
    ii+=1
    print(str(ii)+') '+str(len(datasets11))+' '+' pt:'+str(len(rows11)))

rows=datasets11
datasets=getDatasets4plot(rows)
print('datasets:',len(datasets))
ldata=len(datasets)
if (ldata<=0):
    print("---No corrections of data---")
    #sys.exit(2)
with open('mn55na-1pt.json','w') as outfile:
    json.dump(rows,outfile,indent=2)

reacodes=getReacodes(datasets)
print('reacodes:',len(reacodes),'\n')
outX4Datasets(datasets,'mn55na-1ds.json')
data1+=prepareExforDataForPlot(datasets,msize=8,groupReac=False,lines=False,lblPrefix='auto-',symBorder=True)

conn.close()


#_________________Retrieve ENDF_________________
data2=[]
reqLibs={
	'ENDF/B-VIII.0':"0,0,255"
#	,'JENDL-4.0':"0,255,0"
	,'JENDL-5':"255,127,0"
#	,'JEFF-3.3':"0,255,255"
#	,'CENDL-3.2':"255,0,0"
	,'CENDL-3.2':"0,0,255"
#	,'CENDL-3.2':"196,196,196"
#	,'BROND-3.1':"255,0,255"
#	,'TENDL-2019.s60':"127,127,127"
	}
#data2=getEndfDataForPlot(target,react,reqLibs,'',True)
e4datasets=webEndfDataForPlot_SIG(target,react,'',reqLibs,1e-6,1e3)
data2=prepareEndfDataForPlot(e4datasets,'',True)

#_________________Plot data from EXFOR and ENDF_________________
myOfflinePlot(data1+data2,'<b>Automatic correction</b> of EXFOR cross sections: '+plotTitle
	+'<br><i>X4Pro, by V.Zerkin, IAEA-NDS, 2021-2022, ver.2022-11-09 //running:'+ct+'</i>'
	,'Incident energy (MeV)'
	,'Cross section (mb)'
#	,legendInside=False
#	,xtype='log'
#	,ytype='log'
	,filename=outhtml
	,annot1=annot
	)
print('\nProgram successfully completed')
