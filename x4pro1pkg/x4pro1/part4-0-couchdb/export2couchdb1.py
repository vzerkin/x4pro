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
import couchdb
sys.path.append('./')
sys.path.append('../')
import dbConn

def sql2list1(cursor,sql):
    arr1=[]
    try:
        cursor.execute(sql)
        rows=cursor.fetchall()
    except Exception as ex:
        print("___1___execute-SQL error: ", ex)
        return arr1
    #print('\nrows:',len(rows))
    for row in rows:
        dd=row[0]
        arr1.append(dd);
    return arr1

def retrieve1entry(cursor,Entry,out0dir='in/'):
    #version-0 was: x4entry:=x4subents[1,...]
    #version-1 with x4entry:=x4subent1 + x4subent[2,...]
    sql=str("SELECT Subent,updated,jx4z FROM x4pro_x4z"
	+" where Subent like '"+Entry+"%' order by Subent")
    print('\t--------Retrieve Subentries from X4Pro using SQL:\n\t'+sql)
    x4sub1=None
    x4entry={}
    x4entry['x4entry']=Entry
    x4subents=[]
#    x4entry['x4subents']=x4subents
    x4entry['compiled']='?'
    x4entry['x4dbVersion']='?'
    try:
        cursor.execute(sql)
        rows=cursor.fetchall()
    except Exception as ex:
        print("___1___execute-SQL error: ", ex)
        return arr1
    print('\tRetrieved rows:'+str(len(rows)))
    if out0dir is not None: #output Entries as [sub1,sub2,...] in original retrieved JSON text
        filename=out0dir+Entry+'.json'
        print('\tSaving retrieved {Subent.JSON} to the file: '+filename)
        f = open(filename,'w')
        f.write('[\n')
    isub=0
    for row in rows:
        Subent=row['Subent']
        updated=row['updated']
        jx4z=row['jx4z']
        if out0dir is not None:
            if isub>0: f.write(',')
            f.write(jx4z)
        try:
            x4sub=json.loads(jx4z)
        except Exception as ex:
            print("___1___JSON-error: ",ex)
            return None
        if Subent.endswith('001'):
            x4entry['compiled']=x4sub['compiled']
            x4entry['x4dbVersion']=x4sub['x4dbVersion']
            x4sub1=x4sub
        else: x4subents.append(x4sub);
        isub+=1
    if out0dir is not None:
        f.write(']\n')
        f.close()
#    x4entry=x4sub1
#    x4entry['x4entry']=Entry
    x4entry=dict(list(x4entry.items()) + list(x4sub1.items()))
    del x4entry['SUBENT'] #remove::"x4subent": "10020001"
    x4entry['x4subents']=x4subents
    return x4entry



print("Program: export2couchdb1.py, ver. 2023-03-27")
print("Author:  V.Zerkin, IAEA-NDS, Vienna, 2021-2023")
print("Purpose: Export EXFOR Entries from X4Pro to CouchDB\n")
ct=str(datetime.datetime.now())[:19]
print("Running: "+ct+"\n")

react="25-MN-55(N,A)23-V-52,,SIG" #example-1

reCreateDB=False #CouchDB for export: insert/replace documents
#reCreateDB=True #CouchDB for export: replace whole database
user2='exfor'    #CouchDB:user
passw2='exfor'   #CouchDB
dbname = "zv-exfor-001"

outdir='out/'
if not os.path.exists(outdir): os.makedirs(outdir)
if not os.path.exists('in/'):  os.makedirs('in/')

print("---Retrieve EXFOR data from SQL database---")
conn=dbConn.getConnSQLx4db()
if conn is None:
    print("___0___No connection...")
    sys.exit(1)
print("Connected to: ["+dbConn.dbType+"]")

cursor=dbConn.getCursor(conn)

#example-1:
sql=("select distinct ENTRY.Entry\n"
	+" from REACODE\n"
	+" inner join REACSTR on REACSTR.ReacodeID=REACODE.ReacodeID\n"
	+" inner join SUBENT on REACODE.SubentID=SUBENT.SubentID\n"
	+" inner join ENTRY on ENTRY.EntryID=SUBENT.EntryID\n"
	+" where (REACODE.fullCode='"+react+"')\n"
	+" order by ENTRY.Entry"
	)
#example-2:
sql="select distinct Entry from ENTRY order by Entry"
#example-3:
sql="select distinct substr(Subent,1,5) as Entry from x4pro_x4z order by Entry"
print('SQL command:\n'+sql)
Entries=sql2list1(cursor,sql)
print('Exporting Entries: '+str(len(Entries)))

print("---Store EXFOR data in NoSQL database CouchDB---")

couchserver=couchdb.Server('http://localhost:5984/')
couchserver.resource.credentials=(user2,passw2)
print("---Listing databases")
for i,nam in enumerate(couchserver):
    print('------'+str(i+1)+') database name: '+nam)

if dbname in couchserver:
    db = couchserver[dbname]
    print("Database already exists: "+dbname)
    flagNewDB=False
    if (reCreateDB):
        del couchserver[dbname]
        print("Database deleted: "+dbname)
        db = couchserver.create(dbname)
        print("Database successfully created: "+dbname)
else:
    db = couchserver.create(dbname)
    print("Database successfully created: "+dbname)
    flagNewDB=True

ii=0
print("---List of documents in "+dbname)
for docid in db.view('_all_docs'):
    id = docid['id']
    print('------'+str(ii+1)+') id:'+id)
    ii+=1

ii=0
for Entry in Entries:
    print('export------'+str(ii+1)+") Entry:"+Entry)
    docs=db.view('_all_docs')
    doc_id=Entry
    doc=db.get(doc_id)
    if (doc is not None):
        print('\t--------DocID:'+doc_id+' exists in CouchDB. Removing from CouchDB...')
        del db[doc_id]

    x4entry1=retrieve1entry(cursor,Entry)
    if x4entry1 is None: continue
    print('\t--------Entry:'+Entry+' retrieved. Compiled:'+str(x4entry1['compiled'])
	+', Subentries:'+str(len(x4entry1['x4subents'])))

    filename=outdir+Entry+'.json'
    print('\tSaving to the file: '+filename)
    with open(filename,'w') as outfile:
        json.dump(x4entry1,outfile,indent=2)

    x4entry1['_id']=x4entry1['x4entry']
    doc_id,doc_rev=db.save(x4entry1)
    print("\tDocument successfully saved in CouchDB: doc_id="+doc_id+" doc_rev="+doc_rev)
    ii+=1
    if (ii>=12): break #save only 1st 12 docs

conn.close()
print('\nProgram successfully completed')
