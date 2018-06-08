#!/usr/bin/env python 

import json
from urllib2 import urlopen

url = 'http://192.168.218.124:1985/api/v1/summaries'
try:
    rawtext = urlopen(url,timeout=15).read()
    jsonStr = json.loads(rawtext)
    for item in jsonStr[u'data'][u'self']:
        print item,jsonStr[u'data'][u'self'][item]
    for item1 in jsonStr[u'data'][u'system']:
        print item1,jsonStr[u'data'][u'system'][item1]
except:
    print 'do not get data'
