import json
import urllib2

start=0
limit=1000
i=0
while True:
    link="http://data.cityofnewyork.us/resource/j9m9-eu6n.json?$limit=%d&$offset=%d"%(limit,start)
    res = json.load(urllib2.urlopen(link))
    start+=limit
    i+=len(res)
    print json.dumps(res, indent=4, sort_keys=True)
    if len(res)<limit:
        break

print i, 'lines fectched'
