import os
import sys
import sqlite3
import time
import datetime
import json
import csv

#-------------------------------------------------------------------------------
def main():
    print("Program: exec2sql1.py, ver. 2025-01-13")
    print("Author:  V.Zerkin, v.zerkin@gmail.com, Vienna, 2024-2025")
    print("Purpose: execute one SQL command on SQLite database.")
    print("Operations:\n"
         +"         - connect to SQLite data file\n"
         +"         - read SQL commands from a SQL-file\n"
         +"         - execute SQL command\n"
         +"         - read retrieved data rows to list of dicts\n"
         +"           extracting data (incl.JSON) from row to dict;\n"
         +"         - save result in JSON file and CSV file for EXCEL.\n"
    )
    ct=str(datetime.datetime.now())[:19]
    print("Running: "+ct+"\n")

    sqls=[]
    sql1=""
    out="tmp1"

    if (len(sys.argv)<=1):
        print("Please, define SQL file\n\t$ python -B exec2sql1.py sql1.sql")
        sys.exit(1)

    if sys.argv[1]!='':
        with open(sys.argv[1], "r") as ff:
            sql1=""
            for line in ff:
                #print(str(len(sqls))+" ["+line.rstrip()+"]")
                #if line.rstrip().startswith(";") or line.rstrip().endswith(");"):
                if line.rstrip().startswith(";") or line.rstrip().endswith(";"):
                    sql1+=line.rstrip()
                    #print("__________SQL__________",len(sqls))
                    #print(sql1)
                    sqls.append(sql1)
                    sql1=""
                else:
                    if len(sql1)<=0 and line.rstrip()=="": continue
                    sql1+=line.rstrip()+"\n"
            if sql1!="":
                #print("----------SQL----------",len(sqls))
                #print(sql1)
                if sql1!="": sqls.append(sql1)
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

    ii=0
    print('\n---Execute SQL commands:',len(sqls))
    for sql1 in sqls:
        cols,datasets=execute1sql(conn,sql1)
        #print('\n'+str(ii)+')---Collected datasets:'+str(len(datasets))+'\n\tcols='+str(cols))
        #print('---Collected datasets:',json.dumps(datasets,indent=2))
        ii+=1

    print('\n---Save datasets to JSON file:',out+'.json')
    with open(out+'.json','w') as outfile:
        json.dump(datasets,outfile,indent=2)

    outfile=out+".csv"
    print('\n---Save datasets to CSV file:',outfile)
    with open(outfile, "w", newline="") as ff:
        writer=csv.DictWriter(ff,fieldnames=cols,extrasaction='ignore')
        writer.writeheader()
        writer.writerows(datasets)

    conn.close()

#-------------------------------------------------------------------------------
def execute1sql(conn,sql1,printSql=False):
    #printSql=True
    cursor=conn.cursor()
    if printSql: print("\n---SQL:[\n"+sql1+"\n]")
    t0=time.perf_counter()
    try:
        cursor.execute(sql1)
        rows=cursor.fetchall()
    except Exception as ex:
        print("___1___execute-SQL error: ", ex)
        print(sql1)
        rows=[]
    t1=time.perf_counter()
    x4time=t1-t0
    print("\n\n===SQL executed: "+str(round(x4time,3))+"sec")
    ldata=len(rows)
    if (ldata<=0):
        print("---No data found---")
#        sys.exit(2)
    cols=[]
    for colinfo in cursor.description:
        if printSql: print("---colinfo---",colinfo)
        cols.append(colinfo[0]) #column name
    print('---Retrieved from the database'+' cols:'+str(len(cols))+' rows:'+str(len(rows))+'\n\tcols:'+str(cols))

    datasets=[]
    ii=0
    print('\trows:['+str(len(rows))+']')
    for row in rows:
        print('row-'+str(ii)+':\t',tuple(row))
        dataset={}
        for col in cols:
            val=row[col]
            #print('   '+str(ii)+')\tcol:',col,'\ttype(value):',type(val),'\tvalue:',val)
            try: val=json.loads(val)		#try to convert JSON to dict
            except Exception as ex: pass	#do nothing if it is not JSON column
            if col=='comment2': val=val.split('\r\n')
            dataset[col]=val
        datasets.append(dataset);
        #print('['+str(ii)+'] dataset:\n',json.dumps(dataset,indent=4))
        ii+=1
    #print('\n---Collected datasets:',len(datasets))
    #print('---Collected datasets:',json.dumps(datasets,indent=2))
    return cols,datasets

#-------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
    print('\nProgram successfully completed')
