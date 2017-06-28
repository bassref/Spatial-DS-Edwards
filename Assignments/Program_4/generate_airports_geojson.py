import pprint as pp
import os,sys
import json
import collections


f = open("C:\\Users\\Esther\\Documents\\VisualDS\\Spatial-DS-Edwards\\Assignments\\Program_4\\WorldData\\airports.json","r")

data = f.read()

data = json.loads(data)

all_airports = []

n = 0

for k,v in data.items():
    gj = collections.OrderedDict()
    gj['type'] = "Feature"
    gj['properties'] = v
    lat = v['lat']
    lon = v['lon']
    del gj['properties']['lat']
    del gj['properties']['lon']
    gj["geometry"] = {}
    gj["geometry"]["type"]="Point"
    gj["geometry"]["coordinates"] = [
          lon,
          lat
        ]
    while n < 1000:
      all_airports.append(gj)
      n+=1

out = open("C:\\Users\\Esther\\Documents\\VisualDS\\Spatial-DS-Edwards\\Assignments\\Program_4\\geo_json\\airports.geojson","w")

out.write(json.dumps(all_airports, sort_keys=False,indent=4, separators=(',', ': ')))

out.close()