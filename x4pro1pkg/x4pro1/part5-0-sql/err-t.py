import os
import sys
import sqlite3
import time
import datetime
import json
import csv

print("Program: err-t.py, ver. 2024-12-16")
print("Author:  V.Zerkin, v.zerkin@gmail.com, Vienna, 2024")
print("Purpose: execute SQL command on SQLite\n"
      "         to find EXFOR datasets with ERR-T<=0\n")

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
SELECT distinct substr(DatasetID,1,5) as Entry
,DatasetID,idat
,json_extract(x4.xdat,'$.ERR-T') as `ERR-T`
,xdat
FROM x4pro_x4data as x4
where json_extract(x4.xdat,'$.ERR-T') is not null
and json_extract(x4.xdat,'$.ERR-T') <=0
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

datasets=[]
ii=0
for row in rows:
    dataset={}
    dataset['Entry']=row['Entry']
    dataset['DatasetID']=row['DatasetID']
    dataset['idat']=row['idat']
    dataset['ERR-T']=row['ERR-T']
    dataset['xdat']=json.loads(row['xdat'])
    datasets.append(dataset);
#print('datasets:',list(datasets))
print('datasets:',json.dumps(datasets,indent=2))

out="err-t"
#_________________Output datasets_________________
print('\n---Save datasets to JSON file:',out+'.json')
with open(out+'.json','w') as outfile:
    json.dump(datasets,outfile,indent=2)

#out index of data to CSV file: selected columns only
cols=[	'Entry'
	,'DatasetID'
	,'idat','ERR-T'
#	,'xdat'
	]

outfile=out+".csv"
print('\n---Save datasets to CSV file:',outfile)
with open(outfile, "w", newline="") as ff:
    writer=csv.DictWriter(ff,fieldnames=cols,extrasaction='ignore')
    writer.writeheader()
    writer.writerows(datasets)

print('\nProgram successfully completed')
