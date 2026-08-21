"""
 **********************************************************************
 * Copyright: (C) 2021-2022 International Atomic Energy Agency (IAEA) *
 * Author: Viktor Zerkin, V.Zerkin@iaea.org, (IAEA-NDS)               *
 **********************************************************************
"""

import os
import sys
import sqlite3

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
