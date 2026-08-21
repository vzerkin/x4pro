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
from rx5legrs   import *
from rweb12     import *
from x4out      import *
from exfor2plot import * #plot by plotly/matplotlib
from endf2plot  import *

print("Program: da1an.py, ver. 2022-11-15")
print("Author:  V.Zerkin, IAEA-NDS, Vienna, 2021-2022")
print("Purpose: Retrieve and plot EXFOR/ENDF angular distributions\n")
ct=str(datetime.datetime.now())[:19]
print("Running: "+ct+"\n")

target="Cu-0";react="n,el";quant=",da"
#x4ei=' and (En>1.46e6 and En<=1.5e6)'
ei=1.48e6
x4ei=' and (En>='+str(ei-0.02e6)+' and En<='+str(ei+0.02e6)+')'
x4ei=' and (En>=0.2e6 and En<=0.4e6)'
x4ei=' and (En=1.8e3 or En=0.253e6 or (En>=1.46e6 and En<=1.5e6))'
x4ei=' and (En=0.253e6 or (En>=1.46e6 and En<=1.5e6))'
#x4ei=' and (En=0.253e6)'

e4ei='&ei='+str(ei)
e4ei='&ei=1.8e3,0.253e6,1.5e6'
e4ei='&ei=0.253e6,1.5e6'
#e4ei='&ei=0.253e6'


annot=None
#annot=('<b><sup>nat</sup>Cu(n,el)</b>',35,0.37)



plotTitle=target+'('+react+')'+quant;
outhtml='legrs2da'
outhtml=target.replace('-','')+react.replace(',','')+'_da'

print("---Preparing connection to EXFOR SQL database---")
conn=dbConn.getConnSQLx4db()
if conn is None:
    print("___0___No connection...")
    sys.exit(1)
print("Connected to: ["+dbConn.dbType+"]")

cursor=dbConn.getCursor(conn)

print("---Retrieve [,DA] from EXFOR SQL database---")
#sql=getX4SqlSearch_DA_e(target,react,' and (En=5e6)')
sql=getX4SqlSearch_DA_e(target,react,x4ei)
print("SQL:\n"+sql)

try:
    cursor.execute(sql)
    rows=cursor.fetchall()
except Exception as ex:
    print("___1___execute-SQL error: ", ex)
    rows=[]

datasets=getDatasets4plot(rows)
print('datasets:',len(datasets))
ldata=len(datasets)
if (ldata<=0):
    print("---No data found---")
    #sys.exit(2)

reacodes=getReacodes(datasets)
print('reacodes:',len(reacodes),'\n')

#_________________Output EXFOR datasets_________________
outX4Datasets(datasets,outhtml+'_x4da')
#_________________Preparing EXFOR data for plot_________________
data1=prepareExforDataForPlot(datasets,msize=10,groupReac=len(reacodes)>1,lines=True,lwidth=0.8)



print("---Retrieve [,DA,,LEG/RS] from EXFOR SQL database---")
#x4ei=''
sql=getX4SqlSearch_DA_LEGRS(target,react,x4ei)
print("SQL:\n"+sql)
try:
    cursor.execute(sql)
    rows=cursor.fetchall()
except Exception as ex:
    print("___1___execute-SQL error: ", ex)
    rows=[]
print("\nEXFOR SQL executed. Rows:"+str(len(rows)))

legrsDatasets=rows2legrs(rows)
#outX4Datasets(legrsDatasets,outhtml+'_leg')
datasets2=calcLegrsDatasets2da4plot(legrsDatasets)
outX4Datasets(legrsDatasets,outhtml+'_legda')
reacodes=getReacodes(datasets2)
data1+=prepareExforDataForPlot(datasets2,msize=6,lblPrefix='Leg2DA:',lines=True,lwidth=0.8,symBorder=True)

conn.close()

#sys.exit(2)

#_________________Retrieve ENDF_________________
data2=[]
reqLibs={'ENDF/B-V':"0,0,255"
	,'CENDL-3.2':"255,0,0"
	,'JENDL-3.2':"0,255,0"
##	,'JEF-2.2':"0,255,255"
#	,'BROND-2.2':"255,0,255"
	}
#e4ei='&ei=0.25e6,1.5e6'
e4datasets=webEndfDataForPlot_DADE(target,react,e4ei,reqLibs)
data2=prepareEndfDataForPlot(e4datasets,'',True)

#_________________Plot data from EXFOR and ENDF_________________
myOfflinePlot(data1+data2,'Calculate angular distributions d\u03c3/d\u03a9(E,\u03B8) from LEG/RS: '+plotTitle
	+"<br>(Legendre coefficient L[0] is absent and cross section should be found in the same Entry)"
	+'<br><i>X4Pro, by V.Zerkin, IAEA-NDS, 2021-2022, ver.2022-11-15 //running:'+ct+'</i>'
	,'Angle (deg)'
	,'Cross section (b/sr)'
	,xtype='linear',ytype='log'
	,filename=outhtml
	,legendInside=False
	,xstep30=True
	,annot1=annot
	)
print('\nProgram successfully completed')
