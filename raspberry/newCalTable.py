#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as sql
from datetime import datetime
import time

dbfile = './data/calendar.db'

print "this is first test"

# servertime = datetime.strftime(datetime.now(),'%F %R')
servertime = int(time.time())  # seconds since epoch
regDate = '02/03/2014'
subject = 'welcome!'
comments = 'this is written during db creation'
regColor = 'yellow'
        
conn = sql.connect(dbfile)
curs = conn.cursor()

curs.execute("DROP TABLE IF EXISTS envir")
curs.execute("CREATE TABLE envir(Id INTEGER PRIMARY KEY, regDate TIMESTAMP, subject TEXT, comments TEXT, regColor TEXT, servertime TIMESTAMP);")
# curs.execute("INSERT INTO envir VALUES (NULL, ?, ?, ?, ?, ?)", (regDate, subject, comments, regColor, servertime,))
conn.commit()


#-------------------------------------------------------------------
con = sql.connect(dbfile)

with con:    
    
    cur = con.cursor()    
    cur.execute("SELECT * FROM envir")

    rows = cur.fetchall()

    for row in rows:
        print row