import os
import sys
import sqlite3
import time
import datetime
import json
import csv

print("Program: exec1sql.py, ver. 2024-12-16")
print("Author:  V.Zerkin, v.zerkin@gmail.com, Vienna, 2024")
print("Purpose: execute one SQL command on SQLite database.")
print("Operations:\n"
     +"         - connect to SQLite data file;\n"
     +"         - execute SQL command;\n"
     +"         - read retrieved data rows to list of dicts\n"
     +"           extracting data (incl.JSON) from row to dict;\n"
     +"         - save result in JSON file and CSV file for EXCEL.\n"
     )
ct=str(datetime.datetime.now())[:19]
print("Running: "+ct+"\n")

sql1=""
out="tmp1"

if (len(sys.argv)<=1):
    print("Please, define SQL file\n\t$ python -B exec1sql.py sql1.sql")
    sys.exit(1)

if sys.argv[1]!='':
    with open(sys.argv[1]) as f: sql1=f.read()
if (len(sys.argv)>2) and (sys.argv[2]!=''): out=str(sys.argv[2])

dbFileName='../../x4sqlite1.db'
url='file:'+dbFileName+'?mode=ro'
print("---getConnSQLite:",url)
try:
    conn=sqlite3.connect(url,uri=True)
    conn.row_factory=sqlite3.Row
except sqlite3.Error as error:
    print("___0___sqlite3.connect.Error:\n",error)
    sys.exit(1)

cursor=conn.cursor()

print("\n---SQL:"+sql1)

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
print("---SQL executed: "+str(round(x4time,3))+"sec")

print('\n---Retrieved from the database')
print('rows:',len(rows))
ldata=len(rows)
if (ldata<=0):
    print("---No data found---")
#    sys.exit(2)

cols=[]
for colinfo in cursor.description:
    print("---colinfo---",colinfo)
    cols.append(colinfo[0]) #column name

datasets=[]
ii=0
for row in rows:
    print('  '+str(ii)+')\trow:',tuple(row))
    dataset={}
    for col in cols:
        val=row[col]
        #print('   '+str(ii)+')\tcol:',col,'\ttype(value):',type(val),'\tvalue:',val)
        try: val=json.loads(val)	#try to convert JSON to dict
        except Exception as ex: pass	#do nothing if it is not JSON column
        dataset[col]=val
    datasets.append(dataset);
    #print('['+str(ii)+'] dataset:\n',json.dumps(dataset,indent=4))
    ii+=1
print('\n---Collected datasets:',len(datasets))
#print('---Collected datasets:',json.dumps(datasets,indent=2))

#_________________Output datasets_________________
print('\n---Save datasets to JSON file:',out+'.json')
with open(out+'.json','w') as outfile:
    json.dump(datasets,outfile,indent=2)

outfile=out+".csv"
print('\n---Save datasets to CSV file:',outfile)
with open(outfile, "w", newline="") as ff:
    writer=csv.DictWriter(ff,fieldnames=cols,extrasaction='ignore')
    writer.writeheader()
    writer.writerows(datasets)

print('\nProgram successfully completed')
