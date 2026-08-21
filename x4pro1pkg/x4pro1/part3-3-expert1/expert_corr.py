from importlib import reload
import corr_subr

def corr_dataset(rows,cursor):
    newrows=[]
    if len(rows)<=0: return newrows
    row=rows[0]
    DatasetID=row['DatasetID']
    print("___________corr_dataset:::"+DatasetID+' ldat:'+str(len(rows)))
    load_corr_subr('corr_subr.py',DatasetID,cursor,row)
    reload(corr_subr)
    for row in rows:
#        str0=DatasetID+' En='+str(row['En'])+'	y0='+str(round(row['y'],5))+'	dy='+str(round(row['dy'],5))
        str0=DatasetID+' En='+str(row['En'])+'	y0='+str(round(row['y'],5))
        ierr=corr_subr.corr_point(row)
        if ierr>0:
            newrows.append(row);
            row['corrected']=1
            str0=str0+'	y1='+str(round(row['y'],5))+'	dy1='+str(round(row['dy'],5))
            print("___________corr_data:::"+str0)
    return newrows

def load_corr_subr(file_py,DatasetID,cursor,datarow):
    """
    my_file=open(file_py,'w')
    my_file.write("#Dataset:"+DatasetID+"\n")
    my_file.write("def corr_point(row):\n")
    my_file.write("    return 0 #unchanged\n")
    my_file.close()
    """
    sql="\
SELECT strcorr,author from x4pro_expertcorr \n\
 WHERE (DatasetID like '"+DatasetID+"')        \n\
 ORDER BY fileDate desc                        \n\
"
    #return
    try:
        rows=cursor.execute(sql)
        rows=cursor.fetchall()
    except Exception as ex:
        print("___1___execute-SQL error: "+str(ex)+"\n"+sql)
        rows=[]

    strcorr=''
    if len(rows)>0:
        row=rows[0]
        strcorr=row['strcorr']
        author=row['author']
        datarow['corr_author']=author
    else:
        strcorr="\
def corr_point(row):\n\
    return 0 #unchanged\n\
"

    my_file=open(file_py,'w')
    my_file.write("#Dataset:"+DatasetID+"\n")
    my_file.write(strcorr)
    my_file.write("\n")
    my_file.close()
    print("________load_corr_subr:::"+DatasetID+"\n"+strcorr)
