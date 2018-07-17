#!/usr/bin/python
 
import cgi
import cgitb; cgitb.enable()  # for troubleshooting
from datetime import datetime, timedelta
import time
import sqlite3 as sql

dbfile = './data/calendar.db'


def record_transaction(post):
##    validate_dbpost(post)
    regDate = post['regDate']
    subject = post['subject']
    comments = post['comments']
    regColor = post['regColor']
    servertime = post['servertime']
	
    try:
        conn = sql.connect(dbfile)
        with conn:
            curs = conn.cursor()
            curs.execute("INSERT INTO envir VALUES (NULL, ?, ?, ?, ?, ?)", (regDate, subject, comments, regColor, servertime,))
        # conn.commit()
        # conn.close()
        
    # except KeyError:
        # pass
    except sql.Error, e:
        return "SQL Error: " + e.args[0] 
	
    return post	
		
if __name__=="__main__":
    
    form = cgi.FieldStorage()

##    data={}
##    for key in f.keys():
##        data[key]=f[key].value

    data = {'regDate': form.getvalue("regDate"),
            'comments': form.getvalue("comments"),
            'regColor': form.getvalue("regColor"),
            'subject': form.getvalue("subject")
            }
		
    data['servertime'] = int(time.time())   #seconds till epoch
    res = record_transaction(data)
    

    #


    print "Content-type: text/html\r\n"
    print res
