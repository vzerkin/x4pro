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
sys.path.append('./')
sys.path.append('../')
import dbConn
from rx4fye     import *
from e4subr     import *
from x4out      import *
from exfor2plot import * #plot by plotly/matplotlib
from endf2plot  import * #plot by plotly/matplotlib

print("Program: fy1e.py, ver. 2024-09-02")
print("Author:  V.Zerkin, IAEA-NRDC, Vienna, 2021-2024")
print("Purpose: Cumulative fission yield from EXFOR/ENDF:")
print("         retrieve list of datasets, filter data by product,")
print("         download fy.json, extract data, plot by Plotly")

if (len(sys.argv)<=1):
    print('Examles:')
    print('	python -B fy1e.py Pu-239 Mo-99')
    print('	python -B fy1e.py u-235 kr-85-m log log ')
    print('	python -B fy1e.py u-235 cd-115-g log log')
    print('')
    sys.exit(0)

flagEndf=True
#flagEndf=False

ct=str(datetime.datetime.now())[:19]
print("Running: "+ct+"\n")

target="U-235";product='Cd-115-g';
product='Mo-99';
react="n,f"
quant="cum,fy"

xtype='linear';ytype='linear'
#ytype='log'; xtype='log'
xrange=None; yrange=None
annot=None

#xrange=[71,161];yrange=[0.00025,0.088]
#annot=('<b><sup>235</sup>U(n,f)<sup>115g</sup>Cd</b>',1.8,0.15)

if (len(sys.argv)>1) and (sys.argv[1]!=''): target=str(sys.argv[1])
if (len(sys.argv)>2) and (sys.argv[2]!=''): product=str(sys.argv[2])
if (len(sys.argv)>3) and (sys.argv[3]=='log'): xtype='log'
if (len(sys.argv)>4) and (sys.argv[4]=='log'): ytype='log'


plotTitle=target+'('+react+')'+product+','+quant;
outhtml=target.replace('-','')+'-'+react.replace(',','')+'-'+product.replace('-','')+'-cumFY'

print("---Retrieve EXFOR data from SQL database---")
conn=dbConn.getConnSQLx4db()
if conn is None:
    print("___0___No connection...")
    sys.exit(1)
print("Connected to: ["+dbConn.dbType+"]")

cursor=dbConn.getCursor(conn)

sql=getX4SqlSearchFY_ene(target,product)
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
    print("---No EXFOR data found---")
#    sys.exit(2)

#print('---datasets[0]=',datasets[0])
if len(datasets)>0: plotTitle=datasets[0]['Reacode'].replace('ELEM/MASS',datasets[0]['prod'].upper())

reacodes=getReacodes(datasets)
print('Reaction codes:',len(reacodes),'\n')

outX4Datasets(datasets,'exfor-'+outhtml)

data1=prepareExforDataForPlot(datasets,msize=8,groupReac=len(reacodes)>1,lines=True,lwidth=0.5,symBorder=True)

#_________________Retrieve ENDF_________________
data2=[]
reqLibs={'ENDF/B-VIII.0':"0,0,255"
	,'JEFF-3.3'	:"0,127,0"
	,'JENDL-5'	:"255,0,0"
#	,'BROND-3.1'	:"255,0,255"
	,'ENDF/B-V'	:"127,127,127"
#	,"JEF-2.2"	:"0,127,127"
#	,"JENDL-3.2"	:"127,127,0"
#	,"JENDL-3.3"	:"127,0,127"
	}
if flagEndf:
    print('\nRetrieve list of sections from ENDF...')
    list1=get_elist_fy(target,'n,cum_FY')
    print('Retrieved list of ENDF sections:'+str(len(list1)))
    if len(list1)<=0: print("---No ENDF data---")
    with open('e4list.json','w') as outfile: json.dump(list1,outfile,indent=2)

    edss=[];ii=0;iok=0
    for sect1 in list1:
        LibName=sect1['LibName']
        if reqLibs.get(LibName) is None: continue
        if sect1.get('SectID') is None: continue
        ii+=1
        print("   section:"+str(ii)+"/"+str(len(list1))+"/ok:"+str(iok)
		+" SectID:"+str(sect1['SectID'])+' '+sect1['Targ']
		+" Lib:"+sect1['LibName']+' AUTH:['+sect1['AUTH']+']')
        txt=get_e4fy(sect1['SectID'])
#        with open('endf-'+str(iok)+'.fy.json','w') as wfile: wfile.write(txt)
        with open('endf-'+str(sect1['SectID'])+'.fy.json','w') as wfile: wfile.write(txt)
        ds=e4fy2json(txt)
        ds1=e4fy2prod2data(ds,product)
        if len(ds1['x'])<=0: continue
        ds1['x4lbl']=sect1['LibName']
        ds1['AUTH']=sect1['AUTH']
        ds1['myColor']=reqLibs.get(sect1['LibName'])
        ds1['DatasetID']=sect1['SectID']
        print('   Prod:'+product+'\t En:'+str(ds1['x']))
        print('\t\t FY:'+str(ds1['y']))
        print('\t\tdFY:'+str(ds1['dy']))
        edss.append(ds1)
        iok+=1
    data2=prepareEndfDataForPlot(edss,'',True,autocolor=False,lwidth=2,showAuth=True)


myOfflinePlot(data1+data2,'EXFOR/ENDF cumulative fission yield FY(E): <b>'+plotTitle+'</b>'
	+'<br><i>X4Pro, by V.Zerkin, IAEA, 2021-2024, ver.2024-09-02 //run:'+ct+'</i>'
	,'Incident Energy (MeV)'
	,'Cumulative Fission Yield (%)'
	,xtype=xtype,ytype=ytype
	,filename=outhtml
	,xrange=xrange
	,yrange=yrange
	,annot1=annot
	)
print('\nProgram successfully completed')
