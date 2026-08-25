"""
 *********************************************************************************
 * Copyright: (C) 2024-2025 Viktor Zerkin, Vienna, Austria                       *
 * Author: Viktor Zerkin, v.zerkin@gmail.com, IAEA (1999-2023), NRDC (1996-2025) *
 *********************************************************************************
"""

#sqlite3 -header -box ../../x4sqlite1.db <sql1x4evalscore.sql >sql1x4evalscore.txt

import os
import sys
sys.path.append('./')
sys.path.append('../')
import dbConn

def get_x4evalscores(conn):
#    print('\n---get_x4evalscores from X4Pro database...')
    sql1="""select x4evalscore.fileID,x4evalscore.DatasetID
	 ,x4evalscore.author
	 ,x4evalscore_file.myComment
	 ,x4evalscore.itype
	 ,x4evalscore.accepted
	 ,x4evalscore.evalflag
	 ,x4evalscore.comment2
	from x4evalscore
	 left join x4evalscore_file on x4evalscore_file.fileID=x4evalscore.fileID
	order by x4evalscore.itype,x4evalscore.DatasetID
	"""
    #print("SQL:[\n"+sql1+"]")
    dict1={}

    #cursor=conn.cursor()
    cursor=dbConn.getCursor(conn)
    print("\n---SQL:[\n"+sql1+"\n]")
    try:
        cursor.execute(sql1)
        rows=cursor.fetchall()
    except Exception as ex:
        print("___2___execute-SQL error: ", ex)
        print(sql1)
        return dict1
    print("===SQL executed. Rows:"+str(len(rows)))

    for row in rows:
        obj1={}
        DatasetID=row['DatasetID']
        #obj1['DatasetID']=DatasetID
        obj1['author']   =row['author']
        obj1['myComment']=row['myComment']
        obj1['itype']    =row['itype']
        obj1['accepted'] =row['accepted']
        obj1['evalflag'] =row['evalflag']
        comment2         =row['comment2']
        if comment2 is not None: comment2=comment2.split('\r\n')
        obj1['comment2'] =comment2
        arrFlags=dict1.get(DatasetID)
        if arrFlags is None:
            arrFlags=[]
            dict1[DatasetID]=arrFlags
        arrFlags.append(obj1)
#    print("===x4evalscores:"+str(len(dict1))+" datasets")

    return dict1
