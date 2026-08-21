"""
 **********************************************************************
 * Copyright: (C) 2021-2022 International Atomic Energy Agency (IAEA) *
 * Author: Viktor Zerkin, V.Zerkin@iaea.org, (IAEA-NDS)               *
 **********************************************************************
"""

def getRef1(cursor,DatasetID):
    shortRef=""
    Subent001=DatasetID[:5]+'001'
    sql=("select"
	+" json_extract(jx4z,'$.BIB.REFERENCE[0].x4codes[0].shortRef') as shortRef "
	+" from x4pro_x4z"
	+" where Subent like '"+Subent001+"'")
    print("___1___SQL:\n"+sql)
    try:
        rows=cursor.execute(sql)
    except Exception as ex:
        #print("___1___execute-SQL error: ", ex)
        return shortRef
    for row in rows:
        shortRef=', '+row[0]
    return shortRef

#_________________Output EXFOR datasets_________________
def outR33Datasets(datasets,filename='temp',plotTitle='',ct='',cursor=None):
    if not filename.endswith('.r33dat'): filename=filename+'.r33dat'
    my_file=open(filename,'w')
    if (len(datasets)>1): my_file.write("#"+str(len(datasets))+" "+ct+" "+plotTitle+"\n\n\n")
    ii=0
    for dataset in datasets:
        ii+=1
        if (len(datasets)>1):
            my_file.write("#"+str(ii)+"_"*66+"\n")
        my_file.write("Comment:      //Data converted from X4Pro "+ct+"\n")
        my_file.write("              //Program da1ei_leg.py by V.Zerkin, IAEA, 2022-11-30\n")
        my_file.write("              //EXFOR: "+str(dataset['DatasetID'])+"\n")
        my_file.write("              //X4Reaction: "+dataset['Reacode']+"\n")
        my_file.write("\n")
        my_file.write("Version:      R33\n")
        my_file.write("x4Number:     "+str(dataset['DatasetID'])+"\n")
        if (cursor is not None): str1=getRef1(cursor,dataset['DatasetID'])
        else: str1=""
        my_file.write("Source:       "+dataset['x4lbl']+str1+"\n")
        my_file.write("Units:        mb\n")
        if (dataset['LEG_CM']!=0): my_file.write("cm:           0 1 1 #Ene Theta Data\n")
        my_file.write("Theta:        "+str(dataset['ang'])+"\n")
        lx=len(dataset['x'])
        my_file.write("Data:\n")
        for i2 in range(0,lx,1):
            x=dataset['x'][i2]
            dx=dataset['dx'][i2]
            y=dataset['y'][i2]
            dy=dataset['dy'][i2]
            if (y>0) and (dy>0): str1="\t#dy(%)="+str(round(dy/y*100,1))
            else: str1=""
            my_file.write("%-11.2f,%-9.2f,%-11.6g,%-9.4g%s\n" % (x,dx,y,dy,str1))
        my_file.write("EndData:\n\n\n")
    my_file.close()
