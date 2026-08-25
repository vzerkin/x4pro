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
import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import matplotlib.cm as cm
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
import numpy as np
import matplotlib as mpl

sys.path.append('./')
sys.path.append('../')
import dbConn

def executeSQL(cursor,sql):
    try:
        cursor.execute(sql)
        rows=cursor.fetchall()
    except Exception as ex:
        print("___1___execute-SQL error: ", ex)
        return None
    return rows

def getDatasets4plot(rows,nmaxds=4):
    lx=len(rows)
    datasets=[]
    ii=0; lastDatasetID=''; lastDataset={}
    print('\n___getDatasets from datapoints:',len(rows))
    for row in rows:
        jFreeData=row['jFreeData']; DatasetID=row['DatasetID']
#        print(' pt:'+str(ii)+'/'+str(lx)+') DS:'+str(DatasetID)+' '+str(jFreeData))
        print('___Row:'+str(ii)+'/'+str(lx)+') DS:'+str(DatasetID))
        if jFreeData is not None:
            arr1=json.loads(jFreeData)
            for obj1 in arr1:
                print(str(ii)+'_______Marix::['+obj1['zname']+']')
                obj1['DatasetID']=DatasetID
                if (obj1['zunit']=='PER-CENT'): z2nodim(obj1['xarr'],obj1['yarr'],obj1['zarr'])
                datasets.append(obj1)
                ii+=1
#                if (ii>=2): break
#                if (ii>=1): break
                if (ii>=nmaxds): break
    return datasets

def z2nodim(x,y,z):
    for iy in range(len(y)):
        for ix in range(len(x)):
            z[iy][ix]=z[iy][ix]/100.


print("Program: covar1.py, ver. 2022-11-09")
print("Author:  V.Zerkin, IAEA-NDS, Vienna, 2021-2022")
print("Purpose: Retrieve and plot EXFOR Correlation matrices\n")

flagShow=True
if (len(sys.argv)>1) and (sys.argv[1]=='show=0'): flagShow=False

target="Am-241";react="n,2n"
xtype='linear';ytype='linear'
quant="sig"
DatasetID="23114002"

plotTitle="Covariance";
outhtml=target.replace('-','')+react.replace(',','')+'-'+quant
outhtml='covar1'

print("---Retrieve EXFOR data from SQL database---")
conn=dbConn.getConnSQLx4db()
if conn is None:
    print("___0___No connection...")
    sys.exit(1)
print("Connected to: ["+dbConn.dbType+"]")

cursor=dbConn.getCursor(conn)

sql="""SELECT DatasetID,jFreeData FROM x4pro_kw
 where Keyword='COVARIANCE' and jFreeData is not null
 and DatasetID='23114002'
"""
rows=executeSQL(cursor,sql)
if rows is None:
    sys.exit(1)
print('Retrieved rows:',len(rows))
if len(rows)<=0:
    print("---No data found---")
    sys.exit(2)

my_file=open(outhtml+'-jFreeData.json','w')
my_file.write(rows[0]['jFreeData'])
my_file.close()


datasets=getDatasets4plot(rows)
print('datasets:',len(datasets))
if len(datasets)<=0:
    print("---No data for plotting---")
    sys.exit(3)
for dataset in datasets:
    print('___Dataset:#'+str(dataset['DatasetID'])
	+' marix:'+str(len(dataset['xarr']))+'x'+str(len(dataset['yarr']))
	+' name:'+str(dataset['name']))
with open(outhtml+'.json','w') as outfile:
    json.dump(datasets,outfile,indent=2)

cmap1=plt.colormaps['hot']
cmap1=plt.colormaps['rainbow']
levels=[-1.,-0.8,-0.6,-0.4,-0.2,-0.1,0,0.1,0.2,0.4,0.6,0.8,1]
#levels = MaxNLocator(nbins=15).tick_values(z.min(), z.max())
levels = MaxNLocator(nbins=20).tick_values(-1.04,1.04)
#norm = BoundaryNorm(levels, ncolors=cmap1.N, clip=True)
#norm = mpl.colors.Normalize(vmin=-100, vmax=100)
norm = mpl.colors.Normalize(vmin=-1, vmax=1)

ndat=len(datasets)
nx=2
if ndat<2: nx=1
ny=(ndat+nx-1)//nx
#nx=ndat;ny=1
print('ndat:'+str(ndat)+'___subplots:'+str(nx)+'x'+str(ny))
#sys.exit(0)

#fig,(ax1,ax2)=plt.subplots(1,2,figsize=(12,5),sharex=True,sharey=True)
#fig,axs=plt.subplots(ny,nx,figsize=(6,4*ndat),sharex=True,sharey=True)
#fig,axs=plt.subplots(ny,nx,figsize=(5.2*nx,5),sharex=True,sharey=True)

fig = plt.figure(figsize=(5.2*nx,4.6*ny))
gs = fig.add_gridspec(nrows=ny,ncols=nx)
axs=[];ii=0
for dataset in datasets:
    ix=ii%nx
    iy=ii//nx
    ii+=1
    iii=(ny)*100+(nx)*10+ii
    print('ii='+str(ii)+' ix='+str(ix)+' iy='+str(iy)+' iii='+str(iii))
    #ax=fig.add_subplot(iii)
    if (ii>1): ax=plt.subplot(gs[iy,ix],sharex=ax0,sharey=ax0)
    else: ax=plt.subplot(gs[iy,ix])
    ax0=ax
    axs.append(ax)

if ny==1: top=0.87
else:     top=0.93
plt.subplots_adjust(left=0.07,right=0.85,bottom=0.06,top=top)

ii=0
for dataset in datasets:
    X,Y=np.meshgrid(dataset['xarr'],dataset['yarr'])
    Z=np.array(dataset['zarr'])
    Z=np.ma.masked_where(Z==0.,Z)
    cmap1.set_bad(color='#eef')
    #print(X);print(Y);print(Z)
    print('_1_Dataset:#'+str(dataset['DatasetID'])
	+' marix:'+str(len(dataset['xarr']))+'x'+str(len(dataset['yarr']))
	+' name:'+str(dataset['name']))
    ix=ii%nx
    iy=ii//nx
    print('ii='+str(ii)+' ix='+str(ix)+' iy='+str(iy))
    ax1=axs[ii]
    surf1=ax1.pcolormesh(X,Y,Z,cmap=cmap1,norm=norm
	,edgecolors='w',linewidth=0.01
	)
    ax1.set_xlabel(dataset['xname']+' ('+dataset['xunit']+')')
    ax1.set_ylabel(dataset['xname']+' ('+dataset['xunit']+')')
    ax1.xaxis.set_ticks_position('both')
    ax1.yaxis.set_ticks_position('both')
#    ax1.grid()
    ax1.set_title(dataset['zname']+' ('+dataset['zunit']+') '+dataset['comment'],fontsize=11)
#    fig.colorbar(surf1,ax=ax1,anchor=(.95,0.),fraction=0.05)
    ii+=1
if (ndat%nx)==0: left=0.88
else: left=0.48
if ny==1: top=0.76*0.75;bottom=0.064
else: top=0.79/ny*0.8;bottom=0.06
#color_bar_ax=fig.add_axes([left,0.1,0.2,top])

color_bar_ax=fig.add_axes([left,bottom,0.02,top])
fig.colorbar(surf1,cax=color_bar_ax)

fig.suptitle('EXFOR Covariance #'+DatasetID+' '+target+'('+react+')'+quant,fontsize=14)

plt.savefig('covar1.pdf')
plt.savefig('covar1.png')
if flagShow:
    print('\nPress Q to exit...')
    plt.show()
