import pprint as pp
import os,sys
import json
import collections

f = open("C:\\Users\\Esther\\Documents\\VisualDS\\Spatial-DS-Edwards\\Assignments\\Program_4\\WorldData\\world_volcanos.json", "r")

data = f.read()

data = json.loads(data)

all_volcanos = []
n = 0

for v in data:
    volcDict = collections.OrderedDict()
    volcDict["type"] = "Feature"
    volcDict["properties"] = v
    if v["Lat"] != "" and v["Lon"] != "":
        lat = float(v["Lat"])
        lon = float(v["Lon"])
    del volcDict["properties"]["Lat"]
    del volcDict["properties"]["Lon"]
    volcDict["geometry"] = {}
    volcDict["geometry"]["type"]="Point"
    volcDict["geometry"]["coordinates"] = [
        lon,
        lat
    ]
    while n < 1000:
        all_volcanos.append(volcDict)
        n+=1

out = open("C:\\Users\\Esther\\Documents\\VisualDS\\Spatial-DS-Edwards\\Assignments\\Program_4\\geo_json\\volcanos.geojson","w")

out.write(json.dumps(all_volcanos, sort_keys=False,indent=4, separators=(',', ': ')))

out.close()