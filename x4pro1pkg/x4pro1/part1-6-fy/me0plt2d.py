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
import plotly
from plotly.graph_objs import Scatter,Layout,Contour
sys.path.append('./')
sys.path.append('../')
import dbConn

def sql2x(cursor,sql):
    arr1=[]
    try:
        cursor.execute(sql)
        rows=cursor.fetchall()
    except Exception as ex:
        print("___1___execute-SQL error: ", ex)
        return arr1
    #print('\ndatapoints:',len(rows))
    for row in rows:
        dd=row[0]
        arr1.append(dd);
    #print('\n___sql2x::sql:',sql,'\ndatasets:',len(rows))
    return arr1

def sql2z(cursor,sql,x,y):
    z=[]
    for iy in range(len(y)):
        xx=[]
        for ix in range(len(x)):
            xx.append(0);
        z.append(xx)
    try:
        cursor.execute(sql)
        rows=cursor.fetchall()
    except Exception as ex:
        print("___2___execute-SQL error: ", ex)
        return z
    print('\ndatapoints:',len(rows))
    for row in rows:
        xx=row[0]
        yy=row[1]
        zz=row[2]
        ix=x.index(xx)
        iy=y.index(yy)
        z[iy][ix]=zz
        #print(' xx:'+str(xx)+' ix:'+str(ix)+' yy:'+str(yy)+' iy:'+str(iy)+' zz:'+str(zz))
    return z


print("Program: me0plt2d.py, ver. 2022-11-09")
print("Author:  V.Zerkin, IAEA-NDS, Vienna, 2021-2022")
print("Purpose: Retrieve and plot EXFOR mass-energy distribution)\n")
ct=str(datetime.datetime.now())[:19].replace(' ',':')
print("Running: "+ct+"\n")

target="U-235";react="n,f"
xtype='linear';ytype='linear'
quant="mass,prFrg"

plotTitle="92-U-235(N,F)MASS,PR/FRG,NU/TKE";
outhtml=target.replace('-','')+react.replace(',','')+'-tke'

print("---Retrieve EXFOR data from SQL database---")
#conn=dbConn.getConnSQLite('file:../x4sqlite1.db?mode=ro')
conn=dbConn.getConnSQLx4db()
if conn is None:
    print("___0___No connection...")
    sys.exit(1)
print("Connected to: ["+dbConn.dbType+"]")

cursor=dbConn.getCursor(conn)

sql="""select distinct json_extract(xdat,'$.MASS') as Mass
from x4pro_x4data where DatasetID='21095008'
order by Mass
"""
arrMass=sql2x(cursor,sql)

sql="""
select distinct json_extract(xdat,'$.E') as E
from x4pro_x4data where DatasetID='21095008'
order by E
"""
arrEne=sql2x(cursor,sql)

print('Mass:',len(arrMass),' Energy:',len(arrEne))

sql="""
select json_extract(xdat,'$.MASS') as Mass
 ,json_extract(xdat,'$.E') as E
 ,json_extract(xdat,'$.MISC') as Counts
 from x4pro_x4data
 where DatasetID='21095008'
 order by E,Mass
"""
arrCounts=sql2z(cursor,sql,arrMass,arrEne)

with open('me0plt2d.json','w') as outfile:
    json.dump({"x":arrMass,"y":arrEne,"z":arrCounts}
	,outfile,indent=2)

#colorscale = [[0,'white'], [0.5, '#a0a'], [1, '#bb0']]
colorscale =[
  [0.,'rgb(255,255,255)']
, [10./4209,'rgb(220,220,255)']
, [20./4209,'rgb(0,2,132)']
, [100./4209,'rgb(0,10,138)']
, [200./4209,'rgb(0,16,141)']
, [500./4209,'rgb(0,35,154)']
, [1000./4209,'rgb(0,92,184)']
, [1500./4209,'rgb(0,205,233)']
, [2000./4209,'rgb(90,255,168)']
, [2500./4209,'rgb(234,234,0)']
, [3000./4209,'rgb(234,0,0)']
, [1,'rgb(130,0,0)']
]
#20 100 500 1000 2000 3000 4000 4209

data3=[]
tr=Contour(x=arrMass,y=arrEne,z=arrCounts
	,name='Matrix: '+str(len(arrMass))+'x'+str(len(arrEne))
	,line=dict(smoothing=0.85)
#	,line=dict(smoothing=0.05)
#	,colorscale='Hot'
#	,colorscale='Jet'#'Edge'#'turbo'#'RdYlGn'#'spectral'#'piyg'#'balance'#'Edge'#'Jet'#'rdbu'#https://plotly.com/python/builtin-colorscales/      'Picnic'
,colorscale=colorscale
        ,contours=dict(
            coloring ='heatmap',
            #coloring ='lines',
            showlabels = True, # show labels on contours
            labelfont = dict( # label font properties
                size = 10,
                color = 'white'
                #color = 'black'
            )
	  )
#,zmin=-1,zmax=1,zmid=0
#,zmin=-0.8,zmax=1,zmid=0
	)
data3.append(tr)

xaxis=dict(title='Atomic Mass',showline=True,linecolor='black',ticks='outside'
#	,type='log'
#	,showgrid=True,gridcolor='#aaaaaa'
)
yaxis={'title':'TKE: Total kinetic energy (MeV)','showline':True,'linecolor':'black','ticks':'outside'
#	,'type':'log'
}
layout1=Layout(title='EXFOR #21095008: '+plotTitle+' //Counts'
	+'<br><i>X4Pro, by V.Zerkin, IAEA-NDS, 2021-2023, ver.2023-06-08 //running:'+ct+'</i>'
	,xaxis=xaxis,yaxis=yaxis
	,plot_bgcolor='rgba(200,200,200,0.1)'
)

plotly.offline.plot({'data':data3,'layout':layout1},filename='me0x.html')
