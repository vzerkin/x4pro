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
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import matplotlib.cm as cm
import numpy as np

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


print("Program: me0mpl3d.py, ver. 2022-11-09")
print("Author:  V.Zerkin, IAEA-NDS, Vienna, 2021-2022")
print("Purpose: Retrieve and plot EXFOR mass-energy distribution\n")

flagShow=True
if (len(sys.argv)>1) and (sys.argv[1]=='show=0'): flagShow=False

target="U-235";react="n,f"
xtype='linear';ytype='linear'
quant="mass,prFrg"

plotTitle="92-U-235(N,F)MASS,PR/FRG,NU/TKE";
outhtml=target.replace('-','')+react.replace(',','')+'-fy.html'

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




fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
X,Y=np.meshgrid(arrMass,arrEne)
Z = np.array(arrCounts)
print(X)
print(Y)
print(Z)
#ax.yaxis.set_ticks_position('both')
surf=ax.plot_surface(X,Y,Z)
#surf=ax.plot_surface(X,Y,Z,cmap=cm.jet)
plt.gcf().set_size_inches(12,8)
plt.title('Matplotlib. EXFOR #21095008: 92-U-235(N,F)MASS,PR/FRG,NU/TKE:Counts')
plt.xlabel('Atomic Mass')
plt.ylabel('TKE: Total kinetic energy (MeV)')
plt.legend()
#fig.colorbar(surf, shrink=0.5, aspect=5)
plt.savefig('me0mpl3d.pdf')
plt.savefig('me0mpl3d.png')
if flagShow:
    print('\nPress Q to exit...')
    plt.show()
