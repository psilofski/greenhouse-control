#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as sql
from datetime import datetime
import time
import os

i=0;
filelist = []
print "select database:"
for file in os.listdir("./"):
    if file.endswith(".db"):
        filelist.append(file)
        print '[' + repr(i) + ']' + file
        i += 1

s = int(raw_input("Choose db: "))

dbfile = filelist[s]


#-------------------------------------------------------------------
con = sql.connect(dbfile)

with con:    
    
    cur = con.cursor()    
    cur.execute("SELECT * FROM envir")

    rows = cur.fetchall()

    for row in rows:
        print row