"""
 ***********************************************************************************
 * Copyright (C) 2021-2023 International Atomic Energy Agency (IAEA)               *
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

def retrieve1entry(cursor,Entry):
    #version-0 was: x4entry:=x4subents[1,...]
    #version-1 with x4entry:=x4subent1 + x4subent[2,...]
    arr1=[]
    sql=str("SELECT Subent,updated,jx4z FROM x4pro_x4z"
	+" where Subent like '"+Entry+"%' order by Subent")
    print('\t--------Retrieve Subentries from X4Pro using SQL:\n\t'+sql)
    try:
        cursor.execute(sql)
        rows=cursor.fetchall()
    except Exception as ex:
        print("___1___execute-SQL error: ", ex)
        return arr1
    print('\tRetrieved rows:'+str(len(rows)))
    return rows


def adapt0entry(rows,Entry,outEverySubent=False):
    #version-0: entry:{meta,subents:[sub1,sub2,...]}
    x4entry={}
    x4entry['ENTRY']=Entry
    x4entry['compiled']='?'
    x4entry['x4dbVersion']='?'
    x4entry['year']=0
    x4entry['a1']=''
    x4subents=[]
    x4entry['x4subents']=x4subents
    for row in rows:
        Subent=row['Subent']
        updated=row['updated']
        jx4z=row['jx4z']
        x4sub=json.loads(jx4z)
        if Subent.endswith('001'):
            x4entry['compiled']=x4sub['compiled']
            x4entry['x4dbVersion']=x4sub['x4dbVersion']
        x4subents.append(x4sub);
        if outEverySubent:
            filename='in/'+Subent+'.json'
            with open(filename,'w') as outfile:
                outfile.write(jx4z)
    return x4entry

def adapt1entry(rows,Entry):
    #version-1:
    #- entry:{meta,sub1,subents:[sub2,...]}
    #- added to entry.meta: year, author1, reference, title
    #- no BIB: keywords moved to subent level
    x4sub1=None
    x4entry={}
    x4entry['ENTRY']=Entry
    x4subents=[]
    x4entry['compiled']='?'
    x4entry['x4dbVersion']='?'
    x4entry['year']=0
    x4entry['a1']=''
    x4entry['ref']=''
    x4entry['title']=''
    nsub=0
    for row in rows:
        Subent=row['Subent']
        updated=row['updated']
        jx4z=row['jx4z']
        try:
            x4sub=json.loads(jx4z)
	    #move keywords from x4sub.BIB to x4sub
	    #preserv the same position in x4sub for COMMON and DATA
            BIB=x4sub.get('BIB')
            COMMON=x4sub.get('COMMON')
            DATA=x4sub.get('DATA')
            if (BIB    is not None): del x4sub['BIB']
            if (COMMON is not None): del x4sub['COMMON']
            if (DATA   is not None): del x4sub['DATA']
            if (BIB    is not None): x4sub=dict(list(x4sub.items())+list(BIB.items()))
            if (COMMON is not None): x4sub['COMMON']=COMMON;
            if (DATA   is not None): x4sub['DATA']=DATA;
        except Exception as ex:
            print("___1___JSON-error: ",ex)
            return None
        if Subent.endswith('001'):
            x4entry['compiled']=x4sub['compiled']
            x4entry['x4dbVersion']=x4sub['x4dbVersion']
            x4sub1=x4sub
        else: x4subents.append(x4sub);
        nsub+=1
    x4entry=dict(list(x4entry.items()) + list(x4sub1.items()))
    del x4entry['SUBENT'] #remove::"SUBENT": "10020001"
    del x4entry['isub'] #remove::"isub":1
    x4entry['x4subents']=x4subents

    try:
        authors=x4entry['AUTHOR'][0]['x4codes']
        x4entry['a1']=authors[0]['ini']+authors[0]['nam']
    except Exception as ex:
        print("\tWarning: read 1st AUTHOR:",ex)

    try:
        refs=x4entry['REFERENCE'][0]['x4codes']
        x4entry['year']=refs[0]['year']
        x4entry['ref1']=refs[0]['shortRef']
    except Exception as ex:
        print("\tWarning: read 1st REFERENCE:",ex)

    try:
        title=x4entry['TITLE'][0]['x4freetext']
        title=' '.join(title)
        x4entry['title']=' '.join(title.split())
    except Exception as ex:
        print("\tWarning: read TITLE:",ex)

    return x4entry


print("Program: export2couchdb3.py, ver. 2023-03-29")
print("Author:  V.Zerkin, IAEA-NDS, Vienna, 2021-2023")
print("Purpose: Export EXFOR Entries from X4Pro to CouchDB\n")
ct=str(datetime.datetime.now())[:19]
print("Running: "+ct+"\n")

react="25-MN-55(N,A)23-V-52,,SIG" #example-1

reCreateDB=False #CouchDB for export: insert/replace documents
reCreateDB=True #CouchDB for export: replace whole database
user2='exfor'    #CouchDB:user
passw2='exfor'   #CouchDB
dbname = "zv-exfor-001"

outdir='out/'
if not os.path.exists(outdir): os.makedirs(outdir)
if not os.path.exists('in/'):  os.makedirs('in/') #needed only for test by adapt0entry()

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

    rows=retrieve1entry(cursor,Entry)
    if rows is None: continue

    x4entry1=adapt1entry(rows,Entry) #version-1
#    x4entry1=adapt0entry(rows,Entry,outEverySubent=True) #version-0
    if x4entry1 is None: continue
    print('\t--------Entry:'+Entry+' adapted. Compiled:'+str(x4entry1.get('compiled'))
	+', Subentries:'+str(len(x4entry1['x4subents']))
	+', year:'+str(x4entry1.get('year'))+', author1:'+x4entry1.get('a1')
	)

    filename=outdir+Entry+'.json'
    print('\tSaving to the file: '+filename)
    with open(filename,'w') as outfile:
        json.dump(x4entry1,outfile,indent=2)

    x4entry1['_id']=x4entry1['ENTRY']
    doc_id,doc_rev=db.save(x4entry1)
    print("\tDocument successfully saved in CouchDB: doc_id="+doc_id+" doc_rev="+doc_rev)
    ii+=1
    if (ii>=12): break #save only 1st 12 docs

conn.close()
print('\nProgram successfully completed')
