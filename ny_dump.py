import json
import urllib2
import re

start = 1113 #id=570 is missed
limit = 500
i = 0
counter = 0
f = open('ny_dump','a')
#f = open('ny_list','w')

while True:
    link = "http://data.cityofnewyork.us/resource/j9m9-eu6n.json?$limit=%d&$offset=%d"%(limit,start)
    res = json.load(urllib2.urlopen(link))
    start += limit
    i += len(res)
    #print json.dumps(res, indent=4, sort_keys=True)
    '''
    field for each dataset:
    1.agency
    2.available
    3.behind_schedule
    4.dataset (name)
    5.dataset_description
    6.link/url

    1456 are informative
    '''
    for d in res:
        info = []
        l = d['link']['url'].split('/')
        catalog = l[3]
        identifier = l[-1]
        info.append(d['agency'])
        info.append(d['dataset'])
        if 'dataset_description' in d:
            info.append(d['dataset_description'])
        else:
            info.append('')
        info.append(catalog)
        info.append(identifier)
        info = [l.encode(encoding='UTF-8') for l in info]
        for l in info:
            #l = l.replace('\n','')
            l = re.sub('(\n|,)',' ',l)
            f.write(l + ',')
        link = "http://data.cityofnewyork.us/resource/%s.json?$limit=1&$offset=0"%identifier
        print link
        try:
            counter+=1
            item = json.load(urllib2.urlopen(link))
        except Exception as e:
            print 'id %s got Err %d'%(identifier, e.code)
        else:
            print 'id', counter, 'done...'
            if item:
                item = item[0].keys()
                item = [l.encode(encoding='UTF-8') for l in item]
                item = sorted(item)
                f.write(",".join(item))
        f.write('\n')
        #print l[3], l[-1]
        #print json.dumps(d, indent=4, sort_keys=True)

    if len(res)<limit:
        break

print i, 'items fectched'


f.close()
