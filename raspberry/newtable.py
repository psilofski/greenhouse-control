#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as sql
from datetime import datetime
import time

dbfile = './data/logger.db'

print "this is first test"

Controller = 'Controller'
loggertime = '165/165 165:165:85'
# servertime = datetime.strftime(datetime.now(),'%F %R')
servertime = int(time.time())  # seconds since epoch
Soil = 500
Light = 700
Humidity = 65
Tanalog = 20.31
Tdigital1 = 18.1
Tdigital2 = 20.00
Tdigital3 = 22.00
Tdigital4 = 24.06
        
conn = sql.connect(dbfile)
curs = conn.cursor()

curs.execute("DROP TABLE IF EXISTS envir")
curs.execute("CREATE TABLE envir(Id INTEGER PRIMARY KEY, Controller TEXT, loggertime TIMESTAMP, servertime TIMESTAMP, Soil INTEGER, Light INTEGER, Humidity INTEGER, Tanalog FLOAT, Tdigital1 FLOAT, Tdigital2 FLOAT, Tdigital3 FLOAT, Tdigital4 FLOAT);")
curs.execute("INSERT INTO envir VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (Controller, loggertime, servertime, Soil, Light, Humidity, Tanalog, Tdigital1, Tdigital2, Tdigital3, Tdigital4,))
conn.commit()


#-------------------------------------------------------------------
con = sql.connect(dbfile)

with con:    
    
    cur = con.cursor()    
    cur.execute("SELECT * FROM envir")

    rows = cur.fetchall()

    for row in rows:
        print row