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
import math
sys.path.append('./')
sys.path.append('../')
import dbConn
from rx4da_ei   import *
from rx4leg_ei  import *
from rweb12     import *
from x4out      import *
from r33out     import *
from exfor2plot import * #plot by plotly/matplotlib
from endf2plot  import *

print("Program: da1ei_leg.py, ver. 2023-06-08")
print("Author:  V.Zerkin, IAEA-NDS, Vienna, 2021-2023")
print("Purpose: Retrieve and plot EXFOR/ENDF angular distributions\n")
ct=str(datetime.datetime.now())[:19].replace(' ',':')
print("Running: "+ct+"\n")

quant=",da"
adeg=165
xtype='log'; xrange=None; ytype='log'; yrange=None
nexample='default'
annot=None

target="Li-6";react="p,he3";e4react="p,*"
#x4sqlparam=" and (An>=140 and An<=140.5) and (En>=14.1e6 and En<=14.2e6)"
#x4sqlparam=" and (An>=164 and An<=165)"
#e4webparam="&an=164&mf=4&mt=40002&zap=1001"
xrange=[100,4000]; yrange=[0.35,30]
annot=('<b><sup>6</sup>Li'+'('+react+')'+quant+'</b>',750,15)

#target="O-16";react="n,el";e4react="n,*";xrange=[2800,5300];yrange=[4,2000];annot=None
#target="B-11";react="n,el";e4react="n,*";xrange=[65,6500];yrange=[55,1100];annot=None
#target="Fe-0";react="n,el";e4react="n,*";xrange=None;yrange=None;annot=None
#target="Fe-0";react="n,el";e4react="n,*";xrange=[4,11e3];yrange=[15,6000];annot=None

x4sqlparam=(" and (An>="+str(adeg-1)+" and An<="+str(adeg+1)+")")
e4webparam=("&an="+str(adeg)+"&mf=4&mt=40002&zap=1001")

outhtml='da1ei_leg2da'

print("---Retrieve EXFOR data from SQL database---")
conn=dbConn.getConnSQLx4db()
if conn is None:
    print("___0___No connection...")
    sys.exit(1)
print("Connected to: ["+dbConn.dbType+"]")

cursor=dbConn.getCursor(conn)

sql=getX4SqlSearchDA_Ei(target,react,x4sqlparam)
print("SQL:\n"+sql)

plotTitle=target+'('+react+')'+quant;

try:
    cursor.execute(sql)
    rows=cursor.fetchall()
except Exception as ex:
    print("___1___execute-SQL error: ", ex)
    rows=[]

datasets=getDatasets4plot(rows,fx=1e-3)
print('datasets:',len(datasets))
ldata=len(datasets)
if (ldata<=0):
    print("---No data found---")
#    sys.exit(2)

reacodes=getReacodes(datasets,1) #reacodes with #points >9
print('reacodes:',len(reacodes),'\n')
datasets=getReacodes2Datasets(reacodes) #filter only large datasets

#_________________Output EXFOR datasets_________________
outX4Datasets(datasets,outhtml)

#_________________Preparing EXFOR data for plot_________________
data1=prepareExforDataForPlot(datasets,msize=7,groupReac=len(reacodes)>1,lines=True,lwidth=0.9)



print("---Retrieve [,DA,,LEG] from EXFOR SQL database---")
x4ei=''
sql=getX4SqlSearch_DA_LEG(target,react,x4ei)
print("SQL:\n"+sql)
try:
    cursor.execute(sql)
    rows=cursor.fetchall()
except Exception as ex:
    print("___1___execute-SQL error: ", ex)
    rows=[]
print("\nEXFOR SQL executed. Rows:"+str(len(rows)))

legDatasets=rows2leg(rows)
with open(outhtml+'_leg.json','w') as outfile: json.dump(legDatasets,outfile,indent=2)
datasets2=calcLegDatasets2da4plot(adeg,legDatasets,fx=1e-3)
#datasets2=calcLegDatasets2da4plot(165,legDatasets,fx=1e-3,noCM=True)
#datasets2=calcLegDatasets2da4plot(165,legDatasets,fx=1e-3,fy=1e3*0.7)
#with open(outhtml+'_leg.json2','w') as outfile: json.dump(legDatasets,outfile,indent=2)
outR33Datasets(datasets2,outhtml,plotTitle=plotTitle,ct=ct,cursor=cursor)
data1+=prepareExforDataForPlot(datasets2,msize=8,lblPrefix='Leg2DA:',lines=True,lwidth=0.8,symBorder=True)


conn.close()




#_________________Retrieve ENDF_________________
data2=[]
reqLibs={'ENDF/B-VIII.0':"0,0,190"
	,'JENDL-5':"0,190,0"
#	,'JEFF-3.3':"0,255,255"
#	,'CENDL-3.2':"255,0,0"
#	,'CENDL-2':"255,127,127"
#	,'BROND-3.1':"255,0,255"
#	,'BROND-2.2':"255,0,255"
	,'ENDF/B-V':"0,127,255"
#	,'JENDL-3.2':"255,127,0"
#	,'ENDF/B-V':"0,127,127"
#	,'TENDL-2019':"127,127,127"
	,'IBA-EVAL':"0,0,192"
	}
#data2=getSigmacalcDataForPlot('sc1c12aa130.json')
e4datasets=webEndfDataForPlot_DADE(target,e4react,e4webparam,reqLibs,1e-3,1e3/(4*math.pi))
data2=prepareEndfDataForPlot(e4datasets,'',True,lwidth=2.8)

#_________________Plot data from EXFOR and ENDF_________________
#myOfflinePlot(data2+data1
myOfflinePlot(data1+data2
	,'Plot EXFOR/ENDF angular distributions d\u03c3/d\u03a9(E,\u03B8): '+plotTitle
	+'<br><i>X4Pro, by V.Zerkin, IAEA-NDS, 2021-2022, ver.2022-12-07 //running:'+ct+'</i>'
	,'Incident energy (keV)'
	,'Cross section (mb/sr)'
	,xtype=xtype,ytype=ytype
	,xrange=xrange,yrange=yrange
#	,legendInside=False
	,filename=outhtml
	,annot1=annot
	)
print('\nProgram successfully completed')
