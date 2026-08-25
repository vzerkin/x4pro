"""
 *******************************************************************************
 * Copyright: (C) 2025-2026 Viktor Zerkin, Vienna, Austria                     *
 * Author: Viktor Zerkin, v.zerkin@gmail.com, IAEA(1999-2023), NRDC(1996-2026) *
 * License:  MIT License (MIT)                                                 *
 *******************************************************************************
"""

import sys
sys.path.append('./')
sys.path.append('../')
import dbConn

def executeSql(dbConn,conn,sql,verbose=False):
    if verbose: print("---SQL:\n"+sql)
    cursor=dbConn.getCursor(conn)
    try:
        cursor.execute(sql)
        rows=cursor.fetchall()
    except Exception as ex:
        print("___1___execute-SQL error: ", ex)
        rows=[]
    return rows

def getStrFromSQL(dbConn,conn,sql,verbose=False):
    str1=''
    if verbose: print("---getStrFromSQL-SQL:",sql)
    rows=executeSql(dbConn,conn,sql)
    if len(rows)>0: str1=rows[0][0]
    if verbose: print("---getStrFromSQL-str:",str1)
    return str1

def execute1sql(dbConn,conn,sql,verbose=False,ttout=False):
    rows=[]
    cols=[]
    cursor=dbConn.getCursor(conn)
    if verbose: print("---SQL:\n"+sql)
    try:
        cursor.execute(sql)
        rows=cursor.fetchall()
        for colinfo in cursor.description:
            #print("---colinfo---",colinfo)
            cols.append(colinfo[0]) #column name
    except Exception as ex:
        print("___1___execute-SQL error: ", ex)
        rows=[]
    if ttout:
        print('\n---execute1sql---rows:',len(rows),' cols:',len(cols))
        irow=0
        for row in rows:
            irow+=1
#           print('row-'+str(irow)+':\t',tuple(row))
            print('\n----'+str(irow)+': '+str(row[0]))
            icol=0
            for col in cols:
                icol+=1
                val=row[col]
#               print('   '+str(irow)+'.'+str(icol)+':\t',col.ljust(16),' type(value):',type(val),'\tvalue:',val)
                if val is not None: print('    '+(str(irow)+'.'+str(icol)+':').ljust(10)+' ',col.ljust(16),' ',val)
    return rows,cols
