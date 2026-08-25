/*
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
 */

//gcc -c sql1sub.c

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "sqlite3.h"

static int irec=0;
static sqlite3 *db=NULL;
static const char* data="Callback function called";
static FILE *outFile=NULL;
static char sErrMsg[512];

static int callback(void *data, int argc, char **argv, char **azColName)
{
    int i;
    irec++;

    if (outFile!=NULL) fprintf(outFile,"#### %d\n",irec);
    else printf("#%d	%s\n",irec,(const char*)data);
   
    for (i=0; i<argc; i++) {
	if (outFile!=NULL) {
	    if (argv[i]!=NULL) fprintf(outFile,"$%-10s %s\n",azColName[i], argv[i]);
	}
	else
	printf("	%-10s : %s\n", azColName[i], argv[i] ? argv[i] : "NULL");
    }

    if (outFile!=NULL) fprintf(outFile,"//\n");
    else printf("\n");
   
    return 0;
}

int ix4lite_open_(const void *filename)
{
    int ierr;
    if (db!=NULL) sqlite3_close(db);

    irec=0;
    ierr=sqlite3_open_v2(filename,&db,SQLITE_OPEN_READONLY,NULL);
    if (ierr!=0) {
//	fprintf(stderr, "Can't open database: %s\n",sqlite3_errmsg(db));
	sprintf(sErrMsg,"Can't open database: %s\n",sqlite3_errmsg(db));
    } else {
//	fprintf(stderr,"Opened database successfully\n");
    }

    return ierr;
}

int ix4lite_close_()
{
    int ierr;
    if (db!=NULL) sqlite3_close(db);
    return 0;
}

int ix4lite_exec_(char *sql,const void *filename)
{
    int ierr;
    char *zErrMsg=0;
    if (db==NULL) return -3;

    if (strcmp(filename,"tt")!=0) {
	outFile=fopen(filename,"w");
	if (outFile==NULL) {
            fprintf(stderr,"Can not open output file [%s]\n",(char *)filename);
	    return -2;
	}
    }

    //Execute SQL statement
    ierr=sqlite3_exec(db, sql, callback, (void*)data, &zErrMsg);
   
    if (ierr!=SQLITE_OK) {
	sprintf(sErrMsg,"SQL error: %s\n",zErrMsg);
	printf("SQL error: %s\n",zErrMsg);
	sqlite3_free(zErrMsg);
	return -1;
    }

    if (outFile!=NULL) {
//	fprintf(outFile,"////\n");
	fprintf(outFile,"//EOF\n");
	fclose(outFile);
    }

    return irec;
}

void getErrMsg_(char *errMsg)
{
    sprintf(errMsg,"%s",sErrMsg);
}
