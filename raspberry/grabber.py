#!/usr/bin/python

import cgi
import cgitb; cgitb.enable()  # for troubleshooT2g
import urllib2

form = cgi.FieldStorage()
print "Content-type: text/html\r\n"

try:
    url = form.getvalue('url')
    print urllib2.urlopen(url).read(1000)  # ALWAYS specify a max size (in bytes). See [url]http://sebsauvage.net/python/snyppets/#bound_read[/url]
except:
    pass
