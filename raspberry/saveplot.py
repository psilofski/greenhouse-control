#!/usr/bin/python

import time
tm0 = time.time()  ######################################################

import cgi
import cgitb; cgitb.enable()  # for troubleshooT2g
from datetime import date, timedelta, datetime
# from pymongo.connection import Connection
import matplotlib
matplotlib.use( 'Agg' )
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec  #http://stackoverflow.com/questions/5083763/python-matplotlib-change-the-relative-size-of-a-subplot
from matplotlib import dates

## from matplotlib.dates import num2date, date2num
from threading import Lock
import numpy
import sqlite3 as sql

from os import path
datatree = path.dirname(path.realpath(__file__)) + '/data/'
dbfile = datatree + 'logger.db'
axesfile = datatree + 'Temperatures.png'
curaxesfile = datatree + 'Ttoday.png'

tm1 = time.time()  ###############################################################
print 'libraries loaded: ',  ############################################
print tm1-tm0

lock = Lock()

form = cgi.FieldStorage()

def nonnegative(foo):
    if foo < 0:
        foo = 0
    return foo
    
try:
    step = int(form.getvalue('step'))
except TypeError:
    step = 1  #days to plot
    axesfile = curaxesfile

try:
    pg = int(form.getvalue('pg'))
except KeyError:
    pg = 1
except TypeError:
    pg = 1

# connection = Connection("localhost")
# db = connection.home
def Tok(T):
	if T<85 and T>-127:
		return 1
	else:
		return 0

def dumpErrors(val, limitup, limitdown):
    i = 0;
    for T in val:
	if T > limitup or T < limitdown or T == 0.0:
	    val[i] = numpy.nan
#		val[i] = val[i-1]
        i=i+1
    return val

servertime = []
T1 = []
T2 = []
T3 = []
T4 = []
Tnight = []
Tday = []
Tmorning = []
humidity = []
light = []
soil = []
today = datetime.now()
fromdate = today - timedelta(step*pg)
uptodate = today - timedelta( step*(pg-1) )
startepoch = int(time.mktime( fromdate.timetuple() ))
endepoch = int(time.mktime( uptodate.timetuple() ))
# loggerCursor = db.GHdevelopment.find( {'servertime': { '$gte': fromdate, '$lte': uptodate} } )
conn = sql.connect(dbfile)
with conn:
    conn.row_factory = sql.Row  #I want to get a dictionary
    curs = conn.cursor()
    curs.execute( "SELECT * FROM envir WHERE servertime BETWEEN ? AND ?", (startepoch,endepoch,) )
    rows = curs.fetchall()

for entry in rows:
    try:
        T1.append(float(entry['Tdigital1']))
    	Tn2 = float(entry['Tdigital2']) 
        T2.append(Tn2)
        T3.append(float(entry['Tdigital3']))
    	Tn4 = float(entry['Tdigital4']) 
        T4.append(Tn4)
        servertime.append( datetime.fromtimestamp(entry['servertime']) )
        humidity.append(float(entry['Humidity']))
        light.append(float(entry['Light']))
        soil.append(float(entry['Soil']))

    	Troom = Tn4 ## (Tn2*Tok(Tn2)+Tn4*Tok(Tn4))/(Tok(Tn2)+Tok(Tn4)) ##T4 is where they sense T
        if Tok(Troom):
            if light[-1] > 50:
                Tday.append(Troom)
            else:
                Tnight.append(Troom)
            try:  #status was added later...
    			if int(entry['status']) > 999:	## morning true is 1bbb in status
    				Tmorning.append(Troom)
            except TypeError:
                pass

    except KeyError:
        pass

print 'data extracted: ',  ############################################
tm2 = time.time()
print tm2-tm1
#print T1[-1], T2[-1], T3[-1], T4[-1]
Tmday = numpy.mean(Tday)
Tmnight = numpy.mean(Tnight)
Tmmorning = numpy.mean(Tmorning)
ADT = numpy.mean(Tday+Tnight)
DIF = Tmday - Tmnight
CAB = Tmmorning - Tmnight
#print Tmday, Tmnight

T1 = dumpErrors(T1, 70, -70)
T2 = dumpErrors(T2, 70, -70)
T3 = dumpErrors(T3, 70, -70)
T4 = dumpErrors(T4, 70, -70)
humidity = dumpErrors(humidity, 100, 1)


if servertime != []:
	date = datetime.strftime(uptodate, '%d/%m')
	servertime = dates.date2num(servertime)
	
	params = {'legend.fontsize': 9,
			  'legend.linewidth': 2,
			  'font.size': 11}
	matplotlib.rcParams.update(params)
	
	with lock: #better-> http://sjohannes.wordpress.com/2010/06/11/using-matplotlib-in-a-web-application/
			ax = plt.figure(figsize=(8.0, 3.5)) #inches   
			gs = gridspec.GridSpec(3, 1, height_ratios=[1,3,6])

			l1 = plt.subplot(gs[2])
			l1.yaxis.tick_right()
			# l1 = ax.add_subplot(gs[0])
			# putT2g makers on line
			#    markers_on = [12, 20, 30, 19] 
			#    l1.plot(servertime[markers_on], T1[markers_on], 'rD')        
			l1.plot_date(servertime, T1, '-', label=r'T1')
			l1.plot_date(servertime, T2, '-', label=r'T2')       
			# l1.plot_date(servertime, T3, '-', label=r'T3')  #Roof T (1)
			l1.plot_date(servertime, T4, '-', label=r'T4')
			l1.set_ylabel("$Temp$ C")
			l1.set_xlabel("hr")
			# l1.legend(('$low$', '$high$', '$roof$', '$mid$'), loc=0)  #for Roof T (1)
			l1.legend(('$low$', '$high$', '$mid$'), loc=0)
		#http://stackoverflow.com/questions/5498510/creaT2g-graph-with-date-and-time-in-axis-labels-with-matplotlib
		#    l1.xaxis.set_major_locator(dates.HourLocator())
			l1.xaxis.set_major_formatter(dates.DateFormatter('%H'))
			plt.grid()
			plt.xticks(rotation=10)
			
			l3 = plt.subplot(gs[1])
			l3.yaxis.tick_right()
			# l3 = ax.add_subplot(gs[1])
			l3.plot_date(servertime, humidity, '-')
			l3.set_ylabel("$Hum$ %")
			l3.xaxis.set_major_locator(plt.NullLocator())
			
			l4 = plt.subplot(gs[0])
			l4.yaxis.tick_right()
			l4.xaxis.tick_top()
			# l4 = ax.add_subplot(gs[2])
			l4.plot_date(servertime, light, '-')
			l4.plot_date(servertime, soil, '-') #plotting Soil
			l4.set_ylabel("$Light$")
			l4.yaxis.set_major_locator(plt.NullLocator())
			l4.xaxis.set_major_locator(dates.DayLocator())
			l4.xaxis.set_major_formatter(dates.DateFormatter('%d/%m/%y'))
			
		#    ax.autofmt_xdate() # If you have dates
			plt.grid()
			if step > 10:
				plt.xticks(rotation=60)		
			
			print 'will save file now: ',  ###################################3
			tm3 = time.time()
			print tm3-tm2
			
			plt.savefig(axesfile, format='png', transparent=True)
			
			print 'file saved: ',  ###################################3
			tm4 = time.time()
			print tm4-tm3
			
else:
	date = datetime.strftime(today, '%d/%m')


print "Content-type: text/html\r\n"


#print '<img src="./data/T1_T2_t.png" />'

#nextpg = pg+1
#<p>%s</p>
#<a target href="home.py?pg=%s&step=%s">Previous...</a>
#<br/>
print """
<Tday>%s</Tday>
<ADT>%s</ADT>
<DIF>%s</DIF>
<CAB>%s</CAB>
<uptodate>%s</uptodate>
<page>%s</page>
<step>%s</step>
<res>%s</res>
""" % (round(Tmday,1), round(ADT,1), round(DIF,1), round(CAB,1), date, pg, step, 1)

#print 'T1=', T1, ';'
#print 'T2=', T2, ';'
#print 'servertime=', servertime          
        


