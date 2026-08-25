! ***********************************************************************************
! * Copyright (C) 2021-2022 International Atomic Energy Agency (IAEA)               *
! *-----------------------------------------------------------------------------    *
! * Permission is hereby granted, free of charge, to any person obtaining a copy    *
! * of this software and associated documentation files (the "Software"), to deal   *
! * in the Software without restriction, including without limitation the rights    *
! * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell       *
! * copies of the Software, and to permit persons to whom the Software is furnished *
! * to do so, subject to the following conditions:                                  *
! *                                                                                 *
! * The above copyright notice and this permission notice shall be included in all  *
! * copies or substantial portions of the Software.                                 *
! *                                                                                 *
! * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR      *
! * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,        *
! * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE     *
! * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER          *
! * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,   *
! * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN       *
! * THE SOFTWARE.                                                                   *
! *                                                                                 *
! *-----------------------------------------------------------------------------    *
! *   AUTHOR:                                                                       *
! *   Viktor Zerkin, PhD                                                            *
! *   e-mail: V.Zerkin@iaea.org                                                     *
! *   International Atomic Energy Agency                                            *
! *   Nuclear Data Section, P.O.Box 100                                             *
! *   Wagramerstrasse 5, Vienna A-1400, AUSTRIA                                     *
! *   Phone: +43 1 2600 21714; Fax: +43 1 26007                                     *
! *                                                                                 *
! ***********************************************************************************
!
!gfortran f1.f sql1sub.c sqlite3.c -o f1
!gfortran f1.f sql1sub.c sqlite3.c -o f1.exe -pthread -ldl
!
	program f1
	character*512  dbname
	character*512  outfile/'sql1tmp.dat'/
	character*4096 sql
!
        write (*,*) 'Program: f1.f (ver.2022-12-22)'
        write (*,*) 'by V.Zerkin, IAEA-NDS, 2021-2022'

	dbname='../../x4sqlite1.db'
	ierr=ix4lite_open(trim(dbname)//char(0)) !add 0 for C-subr.
	if (ierr.ne.0) then
	    write(*,*) 'Can''t open database ',trim(dbname),' err=',ierr
	    stop
	endif
	write (*,'(a,a/)') ' Open database: ',trim(dbname)

	sql='select Entry,YearRef1,Author1 '//char(10)
     1  //' from ENTRY where Entry like ''F%'' '//char(10)
     1  //' limit 8'
	write(*,'(a/1x,a/)') ' SQL command:',trim(sql)

	sql=trim(sql)//char(0)
	outfile=trim(outfile)//char(0)
	ipnt=ix4lite_exec(sql,outfile)
	if (ierr.lt.0) then
	    write (*,*) 'SQL error ierr=',ipnt
	else
	    write (*,*) 'SQL executed OK: ',ipnt,'rows'
	endif

	call read_data(outfile,ipnt)
!
	call ix4lite_close()

	write(*,'(/a)') 'Program completed successfully'
	stop
	end

	subroutine read_data(infile,ipnt)
	character(len=*) infile
	character*132 nam,line
	character*5   Entry
	character*4   sYear
	character*12  Author1
	write (*,*) 'Read data points:',ipnt
	nin=100
	open(unit=nin,file=infile,status='old',err=9999)
	iipnt=0
	do
	    read(nin,'(a12,a)',end=8888) nam,line
	    if (nam.eq.'//EOF')      exit
	    if (nam.eq.'$Entry')     Entry=line
	    if (nam.eq.'$YearRef1')  read(line,'(i11)') iYear
	    if (nam.eq.'$YearRef1')  sYear=line
	    if (nam.eq.'$Author1')   Author1=line
	    if (nam(1:4).eq.'####') then !--- Begin of new Row
		iipnt=iipnt+1
		Entry=''
		iYear=0
		sYear='----'
		Author1=''
		cycle
	    endif
	    if (nam.eq.'//') then !--- End of Row
		write(*,*) iipnt,Entry,' ',sYear,',',Author1
	    endif
	enddo
8888	close(nin)
9999	return
	end
