import json
import urllib2

start=0
limit=3
i=0
while i<3:
    print i
    link="http://data.cityofnewyork.us/resource/erm2-nwe9.json?$limit=%d&$offset=%d"%(limit,start)
    res = json.load(urllib2.urlopen(link))
    start+=1
    i+=1
    print json.dumps(res, indent=4, sort_keys=True)

