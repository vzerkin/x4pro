"""
 ***********************************************************************************
 * Copyright (C) 2021-2023 International Atomic Energy Agency (IAEA)               *
 * Copyright (C) 2023-2024 Viktor Zerkin (NRDC), v.zerkin@gmail.com                *
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
from x4out      import *
from rx4dae_e2  import *
from rweb12     import *
from exfor2plot import * #plot by plotly/matplotlib
from endf2plot  import *

print("Program: dae1eo.py, ver. 2024-09-02")
print("Author:  V.Zerkin, IAEA-NRDC, Vienna, 2021-2024")
print("Purpose: Retrieve and plot EXFOR/ENDF double differential cross sections\n")
ct=str(datetime.datetime.now())[:19]
print("Running: "+ct+"\n")

quant=",dae"
target="F-19";react="n,x";prod="n"

x4sqlparam=" and (An=45) and (En>=14.1e6 and En<=14.2e6)"
e4webparam="&ei=14.15e6&an=45&mf=6&mt=5&zap=1"
#x4sqlparam=" and (An=145) and (En>=13.4e6 and En<=13.9e6)"
#e4webparam="&ei=1.34e7&an=145&mf=6&mt=5&zap=1"

plotTitle=target+'('+react+prod+')'+quant;
outhtml='dae1eo'

print("---Retrieve EXFOR data from SQL database---")
#conn=dbConn.getConnSQLite('file:../x4sqlite1.db?mode=ro')
conn=dbConn.getConnSQLx4db()
if conn is None:
    print("___0___No connection...")
    sys.exit(1)
print("Connected to: ["+dbConn.dbType+"]")

cursor=dbConn.getCursor(conn)

sql=getX4SqlSearch_DAE_e2(target,react,prod,x4sqlparam)
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

reacodes=getReacodes(datasets,1)
print('reacodes:',len(reacodes),'\n')

#_________________Output EXFOR datasets_________________
outX4Datasets(datasets,outhtml)

#_________________Preparing EXFOR data for plot_________________
data1=prepareExforDataForPlot(datasets,msize=8,groupReac=len(reacodes)>1,lines=True,lwidth=0.8,symBorder=True)

#_________________Retrieve ENDF_________________
data2=[]
reqLibs={'ENDF/B-VIII.0':"0,0,255"
	,'JENDL-5':"255,127,0"
#	,'JEFF-3.3':"0,255,255"
#	,'CENDL-3.2':"255,0,0"
#	,'BROND-3.1':"255,0,255"
	,'ENDF/B-V':"127,0,127"
#	,'TENDL-2019':"127,127,127"
	}
e4datasets=webEndfDataForPlot_DADE(target,"n,*",e4webparam,reqLibs,1e-6,1e9)
data2=prepareEndfDataForPlot(e4datasets,'',True,lwidth=3,showAuth=True)


#_________________Plot data from EXFOR and ENDF_________________
myOfflinePlot(data1+data2,'EXFOR/ENDF double differential cross sections: '+plotTitle
	+'<br><i>X4Pro, by V.Zerkin, IAEA-NRDC, 2021-2024, ver.2024-09-02 //run:'+ct+'</i>'
	,'Outgoing energy (MeV)'
	,'Cross section (mb/sr/MeV)'
	,xtype='linear',ytype='log'
	,yrange=[0.01,100]
	,legendInside=False
	,filename=outhtml
	)
print('\nProgram successfully completed')
