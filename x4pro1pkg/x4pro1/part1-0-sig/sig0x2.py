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
import sqlite3
import time
import datetime
import json
import plotly
from plotly.graph_objs import Scatter, Layout 
import plotly.graph_objects as go

dbType='?'
def getConnSQLx4db(fileName='../../x4sqlite1.db'):
    url='file:'+fileName+'?mode=ro'
    conn=getConnSQLite(url)
    return conn

def getConnSQLite(url):
    global dbType;
    print("___getConnSQLite:",url)
    try:
        conn=sqlite3.connect(url,uri=True)
        conn.row_factory=sqlite3.Row
        dbType='sqlite3'
    except sqlite3.Error as error:
        print("___0___sqlite3.connect.Error:\n",error)
        conn=None
    return conn

def getCursor(conn):
    global dbType;
    cursor=conn.cursor()
    return cursor


def getX4SqlSearchCS(target,react):
    print('\n___getX4SqlSearchCS: ['+target+'] ['+react+']')
    sql=str(""
	+"select *                          \n"
	+"from sig1                         \n"
	+"where (Target like '"+target+"')  \n"
	+"  and (Reaction like '"+react+"') \n"
	)

    #print("SQL:\n"+sql)
    return sql

def getDatasets4plot(rows,fx=1e-6,fy=1e3):
    lx=len(rows)
    datasets=[]
    ii=0; lastDatasetID=''; lastDataset={}
    print('\n___getDatasets from datapoints:',len(rows))
    for row in rows:
        fullCode=row['fullCode']; DatasetID=row['DatasetID']; iPoint=row['iPoint']
        YearRef1=row['YearRef1']; Author1Ini=row['Author1Ini']; Author1=row['Author1'];
        xx=row['En'];  yy=row['Sig'];  dyy=row['dSig'];  dxx=row['dEn']
        if xx is None: continue;
        if yy is None: continue;
        if Author1Ini is not None: Author1=Author1Ini+Author1
        if DatasetID!=lastDatasetID:
            lastDataset={}
            lastDataset['DatasetID']=DatasetID
            lastDataset['Reacode']=fullCode
            lastDataset['x4lbl']=str(YearRef1)+', '+str(Author1)
            x=[];     lastDataset['x']=x
            y=[];     lastDataset['y']=y
            dy=[];    lastDataset['dy']=dy
            dx=[];    lastDataset['dx']=dx
            datasets.append(lastDataset);
            lastDatasetID=DatasetID
            print('DS:'+str(len(datasets))+') '+str(fullCode)+' #'+str(DatasetID)+' '+str(YearRef1)+','+Author1)
        xx=float(xx)*fx; xx=round(xx,7)
        yy=float(yy)*fy; yy=round(yy,7)
        if dyy is not None: dyy=float(dyy)*fy; dyy=round(dyy,7)
        if dxx is not None: dxx=float(dxx)*fx; dxx=round(dxx,7)
        x.append(xx);
        y.append(yy);
        dy.append(dyy)
        dx.append(dxx)
        ii+=1
        print(' pt:'+str(ii)+'/'+str(lx)+') '+str(fullCode)+' '+str(DatasetID)+' '+str(YearRef1)+' '+Author1+" x:"+str(xx)+" y:"+str(yy)+" dy:"+str(dyy)+" dx:"+str(dxx))
    return datasets

def getReacodes(datasets):
    lx=len(datasets)
    Reacodes=[]
    ii=0; lastReacodeStr='---'; lastReacode={}
    print('\nDatasets:',len(datasets))
    for dataset in datasets:
        Reacode=dataset['Reacode']
        if Reacode!=lastReacodeStr:
            lastReacode={}
            lastReacode['Reacode']=Reacode
            lastReacode['datasets']=[]
            Reacodes.append(lastReacode)
            lastReacodeStr=Reacode
            print(str(len(Reacodes))+') '+str(Reacode))
        lastReacode['datasets'].append(dataset);
        ii+=1
        #print('\tDataset:'+str(ii)+'/'+str(lx)+') '+str(Reacode)+' '+str(dataset['DatasetID']))
    return Reacodes



print("Program: sig0x2.py, ver. 2022-11-09")
print("Author:  V.Zerkin, IAEA-NDS, Vienna, 2021-2022")
print("Purpose: Retrieve and plot EXFOR cross sections\n")

ct=str(datetime.datetime.now())[:19]
print("Running: "+ct+"\n")

target="Al-27";react="n,a"
xtype='linear';ytype='linear'
quant=",sig"

outhtml=target.replace('-','')+react.replace(',','')+'-2'

print("---Retrieve EXFOR data from SQL database---")
conn=getConnSQLx4db()
if conn is None:
    print("___0___No connection...")
    sys.exit(1)
print("Connected to: ["+dbType+"]")

cursor=getCursor(conn)

sql=getX4SqlSearchCS(target,react)
print("SQL:\n"+sql)

plotTitle=target+'('+react+')'+quant;

t0=time.perf_counter()
try:
    cursor.execute(sql)
    rows=cursor.fetchall()
except Exception as ex:
    print("___1___execute-SQL error: ", ex)
    rows=[]
t1=time.perf_counter()
conn.close()
x4time=t1-t0
print("\nEXFOR SQL executed: "+str(round(x4time,3))+"sec")

datasets=getDatasets4plot(rows)
print('datasets:',len(datasets))
ldata=len(datasets)
if (ldata<=0):
    print("---No data found---")
    sys.exit(2)

reacodes=getReacodes(datasets)
print('Reaction codes:',len(reacodes),'\n')

#_________________Output EXFOR datasets_________________
with open(outhtml+'.json','w') as outfile:
    json.dump(datasets,outfile,indent=2)

#_________________Preparing EXFOR data for plot_________________
data1=[]; ii=0; iir=0
for reacode in reacodes:
    iir+=1
    for dataset in reacode['datasets']:
        error_y=dict(type='data',array=dataset['dy'],visible=True,thickness=0.9)
        error_x=dict(type='data',array=dataset['dx'],visible=True,thickness=0.9)
        tr=Scatter(x=dataset['x'],y=dataset['y'],error_y=error_y,error_x=error_x
	,text=dataset['x4lbl']
	,name=str(ii+1)+') '+dataset['x4lbl']+' pt:'+str(len(dataset['x']))+' #'+dataset['DatasetID']
	,marker_symbol=str(ii%33)
	,marker_size=8
	,mode="markers"
,legendgroup='exGrp'+str(iir)
,legendgrouptitle_text=""+dataset['Reacode']
	)
        data1.append(tr)
        ii+=1
        print('Plot:'+str(ii)+'/'+str(ldata)+') #'+str(dataset['DatasetID'])+' '+str(dataset['x4lbl'])+' pt:'+str(len(dataset['x'])))

#_________________Plot data from EXFOR_________________
plot1={}
plot1['data']=data1
xaxis=dict(title='Incident energy (MeV)',showline=True,linecolor='black',ticks='outside',showgrid=True,gridcolor='#aaaaaa',type=xtype)
yaxis={'title':'Cross section (mb)','showline':True,'linecolor':'black'#,'type':'log'
	,'showgrid':True, 'gridcolor':'#aaaaaa','ticks':'outside','type':ytype
	,'zeroline':True, 'zerolinecolor':'#dddddd'#, 'zerolinewidth':0.1
}
plot1['layout']=Layout(title='EXFOR cross sections \u03c3(E): '+plotTitle
	+'<br><i>X4Pro, by V.Zerkin, IAEA-NDS, 2021-2022, ver.2022-11-09 //running:'+ct+'</i>'
	,xaxis=xaxis,yaxis=yaxis
	,plot_bgcolor='white'
	,legend=dict(traceorder="grouped")
)

how2plot=2
if how2plot==1:
    plotly.offline.plot(plot1,filename=outhtml+'.html')
elif how2plot==2:
    fig=go.Figure(data=plot1['data'],layout=plot1['layout'])
    fig.write_html(outhtml+'.html')
    fig.show()

print('\nProgram successfully completed')
