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
import datetime
sys.path.append('./')
sys.path.append('../')
import dbConn
from rx5da      import *
from rweb12     import *
from x4out      import *
from exfor2plot import * #plot by plotly or matplotlib
from endf2plot  import *

print("Program: da1an.py, ver. 2025-01-24")
print("Author:  V.Zerkin, Vienna, 2021-2024")
print("Purpose: Retrieve and plot EXFOR/ENDF angular distributions\n")
ct=str(datetime.datetime.now())[:19]
print("Running: "+ct+"\n")

quant=",da"
yrange=None
annot=None

target="Fe-54";react="n,el"
x4ei=' and (En>=4.9e6 and En<=5.1e6)'
e4ei='&ei=5e6'

target="O-16";react="n,el";quant=",da"
ei=14.1e6
target="Pb-204";ei=8e6#;ei=14e6
#target="Cr-52";ei=6e6
#target="Al-27";ei=6e6#;ei=14.6e6;#ei=26e6
#target="Fe-56";ei=14e6
#target="U-238";ei=14e6#ei=8e5;#ei=14e6
#target="U-235";ei=4e6
#target="pu-239";ei=4e6
target="Mn-55";ei=3.4e6
#target="Ni-58";ei=7.5e6
#target="Fe-54";ei=6e6
#x4ei=' and (En>13.9e6 and En<14.2e6)'
#e4ei='14.1e6'

target="O-16";react="n,el";ei=14.1e6;yrange=[2.1,1400];annot=('<b><sup>16</sup>O(n,el)</b>',105,150)
#target="Pb-204";ei=2.53e6#4.6e6
#target="Mn-55";react="n,el";ei=3.4e6;annot=('<b><sup>55</sup>Mn(n,el)</b>',120,263)

x4ei=' and (En>'+str(ei-0.2e6)+' and En<'+str(ei+0.2e6)+')'
#x4ei=' and (En>'+str(ei-0.1e6)+' and En<'+str(ei+0.1e6)+')'
e4ei='&ei='+str(ei)
e4ei+='&dy'

plotTitle=target+'('+react+')'+quant;
outhtml='da1an'

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

fy=1e3;yunits='mb/sr'
datasets=getDatasets4plot(rows,fy=fy)
print('datasets:',len(datasets))
ldata=len(datasets)
if (ldata<=0):
    print("---No data found---")
#    sys.exit(2)

reacodes=getReacodes(datasets)
print('reacodes:',len(reacodes),'\n')

#_________________Output EXFOR datasets_________________
outX4Datasets(datasets,'x4'+outhtml)

#_________________Preparing EXFOR data for plot_________________
data1=prepareExforDataForPlot(datasets,msize=8,groupReac=len(reacodes)>1,lines=True,lwidth=0.8,symBorder=True)

#_________________Retrieve ENDF_________________
data2=[]
reqLibs={
#	'ENDF/B-VIII.0':"0,0,255",
#	'ENDF/B-VII.1':"0,0,255",
#	'ENDF/B-VIII.1':"0,127,127",
	'JENDL-5':"255,0,0",
#	'JENDL-4.0':"255,0,0",
#	'TENDL-2021':"0,127,0",
#	'TENDL-2019.s60':"63,63,63",
#	'TENDL-2019.s60':"0,127,0",
#	'TENDL-2014':"0,0,127",
#	'JEFF-3.1':"0,255,255",
#	'JEFF-3.2':"0,255,255",
#	'CENDL-3.2':"255,0,0",
#	'BROND-3.1':"255,0,255",
	'INDEN-Oct2022':"0,0,255"
	}
#data2=getEndfDataForPlot_DA_A(target,react,e4ei,reqLibs,'',True)
e4datasets=webEndfDataForPlot_DADE(target,react,e4ei,reqLibs,fy=fy)
data2=prepareEndfDataForPlot(e4datasets,'',True,lwidth=3,showAuth=True)
with open('e4datasets.json','w') as outfile:
    json.dump(e4datasets,outfile,indent=2)

my_file=open('e4datasets.txt','w')
my_file.write("#Datasets: "+str(len(e4datasets))+" "+plotTitle+" "+ct+"\n")
ii=0
for dataset in e4datasets:
    ii+=1
    my_file.write("#EndfSectID: "+str(dataset['DatasetID'])+" "+plotTitle+"\n")
    my_file.write("#Label: "+dataset['x4lbl']+"\n")
    my_file.write("#     Ang(deg)   DA(mb/sr)    dDA(mb/sr)     dDA(%)\n")
    lx=len(dataset['x'])
    for i2 in range(0,lx,1):
        #str1=str(dataset['x'][i2])+"\t"+str(dataset['y'][i2]);
        str1="{:<10}".format(dataset['x'][i2])+" {:<12}".format(dataset['y'][i2])
        if (dataset['idy']>0):
            #str1+="\t"+str(dataset['dy'][i2])
            str1+=" {:<14}".format(dataset['dy'][i2])
            #if (dataset['dy'][i2]!=0): str1+="\t"+str(round(dataset['dy'][i2]/dataset['y'][i2]*100,2))+"%"
            if (dataset['dy'][i2]!=0): str1+=" "+str(round(dataset['dy'][i2]/dataset['y'][i2]*100,2))
        my_file.write("{:<5}".format(i2+1)+" "+str1+"\n")
    my_file.write("#//\n")
my_file.close()


#_________________Plot data from EXFOR and ENDF_________________
myOfflinePlot(data1+data2,'EXFOR/ENDF angular distributions d\u03c3/d\u03a9(E,\u03B8): '+plotTitle
	+'  EXFOR-datasets:'+str(len(datasets))
	+'<br><i>X4Pro, by V.Zerkin, IAEA-NRDC, 2021-2025, ver.2025-01-24 //run:'+ct+'</i>'
	,'Angle (deg)'
	,'Cross section ('+yunits+')'
	,xtype='linear',ytype='log'
	,yrange=yrange
	,filename=outhtml
	,xstep30=True
	,annot1=annot
	)
print('\nProgram successfully completed')
