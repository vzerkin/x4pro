import os
import sys
import sqlite3
import time
import datetime
import json
import csv

print("Program: data-err.py, ver. 2024-12-16")
print("Author:  V.Zerkin, v.zerkin@gmail.com, Vienna, 2024")
print("Purpose: execute SQL command on SQLite\n"
      "         to find EXFOR datasets with DATA-ERR<0\n")

ct=str(datetime.datetime.now())[:19]
print("Running: "+ct+"\n")



dbFileName='../../x4sqlite1.db'
url='file:'+dbFileName+'?mode=ro'
print("___getConnSQLite:",url)
try:
    conn=sqlite3.connect(url,uri=True)
    conn.row_factory=sqlite3.Row
except sqlite3.Error as error:
    print("___0___sqlite3.connect.Error:\n",error)
    sys.exit(1)

cursor=conn.cursor()

sql1="""
SELECT distinct substr(x4.DatasetID,1,5) as Entry
 ,x4.DatasetID,idat
 ,json_extract(x4.xdat,'$.DATA') as DATA
 ,json_extract(x4.xdat,'$.DATA-ERR') as `DATA-ERR`
-- ,printf("%.3f",100*json_extract(x4.xdat,'$.DATA')/json_extract(x4.xdat,'$.DATA-ERR')) as `errPercent`
 ,h4.units,x4.xdat
FROM x4pro_x4data as x4
 inner join x4pro_hdr as h4 on h4.DatasetID=x4.DatasetID
where json_extract(x4.xdat,'$.DATA-ERR') is not null
 and json_extract(x4.xdat,'$.DATA-ERR') <0
 and h4.hdr='DATA-ERR'
"""

print("SQL:\n"+sql1)

t0=time.perf_counter()
try:
    cursor.execute(sql1)
    rows=cursor.fetchall()
except Exception as ex:
    print("___1___execute-SQL error: ", ex)
    rows=[]
t1=time.perf_counter()
conn.close()
x4time=t1-t0
print("\nEXFOR SQL executed: "+str(round(x4time,3))+"sec")

print('rows:',len(rows))
ldata=len(rows)
if (ldata<=0):
    print("---No data found---")
    sys.exit(2)

cols=[]
if len(rows)>0: row=rows[0]; cols=row.keys()
print('cols:',len(cols),list(cols))

datasets=[]
ii=0
for row in rows:
    dataset={}
    dataset['Entry']=row['Entry']
    dataset['DatasetID']=row['DatasetID']
    dataset['idat']=row['idat']
    dataset['DATA']=row['DATA']
    dataset['DATA-ERR']=row['DATA-ERR']
    dataset['units']=row['units']
    dataset['xdat']=json.loads(row['xdat'])
    datasets.append(dataset);
    print('  '+str(ii)+')\trow:',tuple(row))
    ii+=1
#print('datasets:',list(datasets))
#print('datasets:',json.dumps(datasets,indent=2))

out="data-err"
#_________________Output datasets_________________
print('\n---Save datasets to JSON file:',out+'.json')
with open(out+'.json','w') as outfile:
    json.dump(datasets,outfile,indent=2)

#out index of data to CSV file: selected columns only
cols=[	'Entry'
	,'DatasetID'
	,'idat'
	,'DATA'
	,'DATA-ERR'
	,'units'
#	,'xdat'
	]

outfile=out+".csv"
print('\n---Save datasets to CSV file:',outfile)
with open(outfile, "w", newline="") as ff:
    writer=csv.DictWriter(ff,fieldnames=cols,extrasaction='ignore')
    writer.writeheader()
    writer.writerows(datasets)

print('\nProgram successfully completed')
