import pprint as pp
import os,sys
import collections


f = open( )
data = f.read()
data  = 



for k,v in data.items():
    gj = collections.OrderedDict()
    gj['type'] = "Feature"
    gj['properties'] = v
    lat = v['lat']
    lon = v['lon']
    del gj['properties']['lat']
    del gj['properties']['lon']
    gj["geometry"] = {}
    gj["geometry"]["type"] = 'Point'
    


