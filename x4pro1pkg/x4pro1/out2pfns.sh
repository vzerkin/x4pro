set -x

cd part2-B-pfns

ls --format=single-column */*.png   >qq0
#ls --format=single-column */*.*.png >>qq0
ls --format=single-column */**.png   >qq0
#grep -v html qq0>qq1
#grep html qq0>qq01
cat qq0|grep html|grep -v "part1\-8\-reac"|grep -v "part2\-8\-sig1par">qq01

sort -u qq01>qq1
#exit

cat >out1.html <<EOF
<html>
<head>
<style>
a { text-decoration: none;}
</style>
<style type="text/css" media="print">
@page {
  @bottom-right {
    content: counter(page) " of " counter(pages);
  }
}
</style>
EOF

cat >>out1.html <<EOF
<script language=javascript>
var dirMap=new Map([
EOF

    filenames="./content.txt"
    ii=0
    for name in $filenames; do
	if [ -f $name ]; then
	    ext=${name##*.}
	    dir=$(dirname "${name}")
	    str1=`cat "$dir/content.txt" 2>/dev/null|head -n 1`
	    echo "---read--- $dir $str1"
	    if [ $ii -gt 0 ] ; then
		echo "	,[\"$dir\",\"$str1\"]" >>out1.html
	    else
		if [ "$dir" = "." ] ; then
		    echo "	['out00',\"$str1\"]" >>out1.html
		else
		    echo "	[\"$dir\",\"$str1\"]" >>out1.html
		fi
	    fi
	    ii=$(($ii+1))
	fi
    done

cat >>out1.html <<EOF
    ]);
</script>
EOF

cat >>out1.html <<EOF
<script language=javascript>
var pngMap=new Map([
	 ["out00/pfns233u00_0th.html.png"	,"<sup>233</sup>U(n<sub>thermal</sub>,f) PFNS-ratio to Mxw. (T=1.34MeV)"]
	,["out00/pfns239pu00_0th.html.png"	,"<sup>239</sup>Pu(n<sub>thermal</sub>,f) PFNS-ratio to Mxw.distr. (T=1.32MeV)"]
	,["out00/pfns239pu00_0th138.html.png"	,"<sup>239</sup>Pu(n<sub>thermal</sub>,f) PFNS-ratio to Mxw.distr. (T=1.382MeV)"]
	,["out00/pfns238u14_3.html.png"		,"<sup>238</sup>U(n<sub>14.3MeV</sub>,f) PFNS-ratio to Mxw. (T=1.32MeV)"]
	,["out00/pfns239pu01_45.html.png"	,"<sup>239</sup>Pu(n<sub>1.45MeV</sub>,f) PFNS-ratio to Mxw. (T=1.32MeV)"]
	,["out00/fig12-vs-x4pro.png"		,"<sup>235</sup>U(n<sub>15MeV</sub>,f) PFNS-ratio to Mxw. (T=1.32MeV)"]
	,["out00/zabs2mxw233u_t.html.png"	,"Converting of abs.[PR,NU/DE] to Mxw.ratio in EXFOR"]
EOF

cat >>out1.html <<EOF
    ]);
</script>
EOF


cat >>out1.html <<EOF
<script language=javascript>
var num=0;
var prevDir='';
    function out1(filename,comment) {
	var ii,nowDir='',shortHelp='',str1='',shortHelpPng;
	var str=filename.replace(/ /g,'');
	var hh=600;
	if (typeof comment=='undefined') comment='';
	shortHelpPng=pngMap.get(str);
	if (typeof shortHelpPng!='undefined') comment=' &nbsp; <i>'+shortHelpPng+'</i>';
//	comment=' &nbsp; <i>['+filename+']</i>';
	if (filename.indexOf('couchdb')>=0) hh=760;
	num++;
	ii=filename.lastIndexOf('/');
	if (ii>0) nowDir=filename.substring(0,ii);
	ii=nowDir.lastIndexOf('/');
	if (ii>0) nowDir=nowDir.substring(0,ii);
	document.write('<div style="page-break-inside:avoid;">');
	if (nowDir!=prevDir) {
	    str1=nowDir+'/';
	    shortHelp=dirMap.get(nowDir);
	    if (typeof shortHelp!='undefined') str1+=' &nbsp; <i>'+shortHelp+'</i>';
	    document.write('<div style="font-size:16pt;color:#fff;background-color:#44f;padding-left:10px;margin-bottom:4px;">'+str1+'</div>');
	    prevDir=nowDir;
	}
        document.write('<div style="padding-top:3px">');
        document.write('<span style="font-size:20pt;font-family:calibry;color:#a0a;'
	+'border:1px solid #aaa;border-bottom:none;border-radius:6px 6px 0 0;margin-bottom:-1px;margin-left:10px;position:relative;'
	+'padding-left:9px;padding-right:2px;background-color:#fff;">'
	+num+') '+str+'</span><span style="font-size:14pt;margin-left:4px;color:blue;">'+comment+'</span>');
        document.write('</div>');
        document.write('<div style="border:1px solid #aaa;display:table;">');
        document.write('<img src="'+str+'" height='+hh+'>');
        document.write('</div><br>');
	document.write('</div>');
    }
</script>
</head>
<body bgcolor="#ddddff">
<big><big><b>X4Pro. Plotting PFNS - EXFOR versus ENDF.</b></big></big>
EOF

echo "<br>Generated: `date +%F,%T`<br>">>out1.html

cat >>out1.html <<EOF
<script language="javascript">
EOF


#cat qq1 |awk '{print "out1(\""$0"\");"}'>>out1.html
cat qq1 |awk '{printf("    out1(\"%-44s\");\n", $0)}'>>out1.html
#echo "myplot1.png" |awk '{printf("    out1(\"%-44s\",\"%s\");\n",$0)}'>>out1.html

#echo '    out1("myplot1.png","Interactive plot: EXFOR:ETA + ENDF:MT452,18,102,MF1,3,31,33");'>>out1.html
echo '    out1("out00/fig12-vs-x4pro.png","Interactive plot: EXFOR:ETA + ENDF:MT452,18,102,MF1,3,31,33");'>>out1.html

cat >>out1.html <<EOF
</script>

<hr>
<font face="helvetica" size="1">
  Created by <a HREF="mailto:v.zerkin@gmail.org">V.Zerkin</a>, 09-Aug-2026<br>
  <script language="javascript">  document.write(" Last updated: "+document.lastModified) </script>
</font>

</body>
</html>
EOF

#cp -p out1.html out2plotly.html

set +x

#move line up: out00zv/da1ei-ex2.png
#    out1("part2-3-da1ei/out00/da1ei-ex2.png           ");
#    out1("part2-3-da1ei/out00zv/da1ei-ex2.png         ");

echo ""
echo "Move line down"
echo "16) part2-3-da1ei/out00/da1ei-ex2.png"
echo "to make"
echo "17) part2-3-da1ei/out00/da1ei-ex2.png"
rm qq0 qq1 qq01
