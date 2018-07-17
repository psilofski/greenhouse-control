#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as sql
from datetime import datetime
import time
import os
import cgi
import cgitb; cgitb.enable()  # for troubleshooting

# i=0;
# filelist = []
# print "select database:"
# for file in os.listdir("./"):
    # if file.endswith(".db"):
        # filelist.append(file)
        # print '[' + repr(i) + ']' + file
        # i += 1

# s = int(raw_input("Choose db: "))

# dbfile = filelist[s]
dbfile = './data/calendar.db'
print "Content-type: text/html\r\n"

#-------------------------------------------------------------------
con = sql.connect(dbfile)

with con:        
    # con.row_factory = sql.Row  #I want to get a dictionary
    entries = []
    cur = con.cursor()    
    cur.execute("SELECT * FROM envir")
    for entry in cur.fetchall():
        entries.append(list(entry))

    # https://stackoverflow.com/questions/3121979/how-to-sort-list-tuple-of-lists-tuples
for entry in entries:
    entry[1] = datetime.strptime(entry[1], '%d/%m/%Y')	#string to date object

entries = sorted(entries, key=lambda tup: tup[1])[::-1]    

print """ <table style="font-size:80%; border-collapse: collapse;"> """    
for entry in entries:
    row = {
        'regDate': entry[1].strftime('%a%d%b'),
        'subject': entry[2],
        'comments': entry[3],
        'regColor': entry[4],
        }
    
    print """ 
<tr style=" border-bottom: 1px dotted silver;">
<td style="color:%s; font-weight:bold;"> %s</td>
<td style="font-weight:bold; text-align: center;">%s</td> 
<td style="">%s</td>
</tr>
    """ % (row['regColor'], row['regDate'], row['subject'], row['comments'])
print """</table>"""          
