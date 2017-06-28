import pprint as pp
import os,sys
import json
import collections

f = open("C:\\Users\\Esther\\Documents\\VisualDS\\Spatial-DS-Edwards\\Assignments\\Program_4\\WorldData\\earthquakes-1960-2017.json", "r")

data = f.read()

data = json.loads(data)

all_earthquakes = []
n = 0

for key in data.keys():
    #member is the list of dictionaries
    member = data[key]
    earthDict = collections.OrderedDict()
    for m in member:
        earthDict["type"] = "Feature"
        earthDict["properties"] = m
        info =  m["geometry"]["coordinates"]
        lat = info[0]
        lon = info[1]
        del earthDict["properties"]["geometry"]
        earthDict["geometry"] = {}
        earthDict["geometry"]["type"]="Point"
        earthDict["geometry"]["coordinates"] = [ lon, lat]
        while n < 1000:
            all_earthquakes.append(earthDict)
            n+=1

#pp.pprint(all_earthquakes)

out = open("C:\\Users\\Esther\\Documents\\VisualDS\\Spatial-DS-Edwards\\Assignments\\Program_4\\geo_json\\earthquakes.geojson","w")

out.write(json.dumps(all_earthquakes, sort_keys=False,indent=4, separators=(',', ': ')))

out.close()