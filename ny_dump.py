import json
import urllib2
import re


def _decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv

def _decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv

start = 558#id=570 is missed
#558\569\ in new dumping missing
limit = 500
i = 0
counter = start
f = open('ny_dump_new','a')
#f = open('ny_list','w')

while True:
    link = "http://data.cityofnewyork.us/resource/j9m9-eu6n.json?$limit=%d&$offset=%d"%(limit,start)
    res = json.load(urllib2.urlopen(link), object_hook=_decode_dict)
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
        #print json.dumps(d, indent=4, sort_keys=True)
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
        #info = [l.encode(encoding='UTF-8') for l in info]
        #print info
        for l in info:
            #l = l.replace('\n','')
            l = re.sub('(\n|,)',' ',l)
            f.write(l + ',')
        link = "http://data.cityofnewyork.us/resource/%s.json?$limit=2&$offset=0"%identifier
        print 'dumping...', identifier
        try:
            counter+=1
            item = json.load(urllib2.urlopen(link), object_hook=_decode_dict)
        except Exception as e:
            print 'id %s got Err %d'%(identifier, e.code)
        else:
            print 'id', counter, 'done...'
            #print json.dumps(item, indent=4, sort_keys=True)
            if item:
                d = item[0]
                if len(item)>1:
                    for k,v in item[1].items():
                        d[k] = str(d.get(k)).replace('\n', ' ')+'<<'+str(v).replace('\n', ' ')
                    #print d
                f.write(",".join(['%s<<%s'%(k,v) for k,v in d.items()]))
                #item = item[0].keys()
                #item = [l.encode(encoding='UTF-8') for l in item]
                #item = sorted(item)
                #f.write(",".join(item))
        f.write('\n')
        #print l[3], l[-1]
        #print json.dumps(d, indent=4, sort_keys=True)

    if len(res)<limit:
        print '>>>>>>>done dumping<<<<<<<'
        break

print i, 'items fectched'


f.close()
