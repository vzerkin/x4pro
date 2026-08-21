#!/bin/bash
#X4Pro-Demo, V.Zerkin@iaea.org, 2022-08-09
echo "Setup: SQLite, Plotly"
set -x
cp dbConn-sqlite.py     dbConn.py
cp endf2plot-plotly.py  endf2plot.py
cp exfor2plot-plotly.py exfor2plot.py
ls -la	dbConn-sqlite.py     dbConn.py    \
	endf2plot-plotly.py  endf2plot.py \
	exfor2plot-plotly.py exfor2plot.py
