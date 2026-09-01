/*    Program:         ggsub.js
      Author:          Viktor Zerkin, v.zerkin@gmail.com
      Created:         2025-01-23
      Last modified:   2025-01-17
      Distribution:    2026-09-01
      Project:         X4Pro2
      License:         MIT
*/
function trim1(a){return a.replace(/^\s\s*/,"").replace(/\s\s*$/,"")}function str2int(c,b){var a;a=parseInt(""+c);if(a=="NaN"){a=b}return a}function str2float(c,b){var a;a=parseFloat(""+c);if(a=="NaN"){a=b}return a}function float2ene(a){var b;ff=a;if(ff<0.01){b=""+ff.toExponential(2);b=b.replace(/e\+/g,"e")}else{ff=a.toPrecision(3);b=""+ff;b=b.replace(/e\+/g,"e")}if(b.indexOf("e")<0){if(b.indexOf(".")>0){b=b.replace(/0+$/,"").replace(/\.+$/,"")}}b=b.replace(/0e/g,"e");b=b.replace(/0e/g,"e");return b}function float2enep(a,b){var c;ff=a;if(ff<0.01){c=""+ff.toExponential(2);c=c.replace(/e\+/g,"e")}else{ff=a.toPrecision(b);c=""+ff;c=c.replace(/e\+/g,"e")}if(c.indexOf("e")<0){if(c.indexOf(".")>0){c=c.replace(/0+$/,"").replace(/\.+$/,"")}}c=c.replace(/0e/g,"e");c=c.replace(/0e/g,"e");return c}function x4downloadCSV(b){var c=x4getDataCSV(b);var a=x4getFilenameCSV();downloadCSV(c,a)}function downloadCSV(c,a){var b=document.createElement("a");b.setAttribute("href","data:text/csv;charset=utf-8,"+encodeURIComponent(c));b.setAttribute("download",a);b.style.display="none";document.body.appendChild(b);b.click();document.body.removeChild(b)};