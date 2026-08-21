"""
 *******************************************************************************
 * Copyright: (C) 2021-2023 International Atomic Energy Agency (IAEA)          *
 * Copyright: (C) 2023-2026 Viktor Zerkin, Vienna, Austria                     *
 * Author: Viktor Zerkin, v.zerkin@gmail.com, IAEA(1999-2023), NRDC(1996-2026) *
 *******************************************************************************
"""

import sys
sys.path.append('./')
sys.path.append('../')
import dbConn
import datetime

def wgetdb_exec(cursor,sql):
    rows=[]
    try:
        cursor.execute(sql)
        rows=cursor.fetchall()
    except Exception as ex:
        print("---wgetdb_exec---error-execute SQL: ", ex)
        return None
    return rows

def wgetdb_execupdate(cursor,sql):
    try:
        cursor.execute(sql)
    except Exception as ex:
        print("---wgetdb_execupdate---error-execute SQL: ", ex)
        return -1
    return 0

def wgetdb_get(url0,prog,params,debug=False):
    cmd=prog+params
    print('---wgetdb_get:'+cmd)
    conn=dbConn.getConnSQLx4db()
    if conn is None:
        print("----wgetdb_get: No connection to DB...")
        return -1
    print("Connected to: ["+dbConn.dbType+"]")
    cursor=dbConn.getCursor(conn)
    sql="select * from wget_cache where cmd='"+cmd+"'"
    rows=wgetdb_exec(cursor,sql)
    if rows is None: return None
    lx=len(rows)
    txt=None
    print('\n---wgetdb_get---retrieved from wget_cache rows:',len(rows))
    print('---wgetdb_get---sql: '+sql)
    for row in rows:
        txt=row['txt']
        if txt is None: break
        break
    conn.close()
    return txt

def wgetdb_put(url0,prog,params,txt,debug=False):
    #print('---wgetdb_put---')
    print('---wgetdb_put:'+url0)
    conn=dbConn.getConnSQLx4db()
    if conn is None:
        print("----wgetdb_put: No connection to DB...")
        return -1
    print("Connected to: ["+dbConn.dbType+"]")
    cursor=dbConn.getCursor(conn)
#tst    iupd=wgetdb_execupdate(cursor,"drop table wget_cache")
    rows=wgetdb_exec(cursor,"select count(*) from wget_cache")
    if rows is None:
        sql="""create table wget_cache (
	 url varchar(255) null
	,cmd varchar(255) null
	,datim datetime
	,txt text null
	,primary key (cmd)
        )"""
        iupd=wgetdb_execupdate(cursor,sql)
        rows=wgetdb_exec(cursor,"select count(*) from wget_cache")
        if rows is None:
            return -2

    cmd=prog+params
    sql="delete from wget_cache where cmd='"+cmd+"'"
    iupd=wgetdb_execupdate(cursor,sql)

    ct=str(datetime.datetime.now())[:19]
    sql="insert into wget_cache(url,cmd,datim,txt) values ("+\
	"\n'"+url0+"'"+"\n,'"+cmd+"'"+"\n,'"+ct+"'"+"\n,'"+txt+"'"+")"
    iupd=wgetdb_execupdate(cursor,sql)
#    print("\n\n\n---SQL---\n"+sql)
    conn.commit()
    conn.close()
    return 0
