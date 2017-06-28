import pprint as pp
import os,sys
import json
import collections

f = open("C:\\Users\\Esther\\Documents\\VisualDS\\Spatial-DS-Edwards\\Assignments\\Program_4\\WorldData\\world_cities_large.json", "r")

data = f.read()

data = json.loads(data)

all_cities = []
n = 0

for key in data.keys():
    member = data[key]
    cityDict = collections.OrderedDict()
    for m in member:
        cityDict["type"] = "Feature"
        cityDict["properties"] = m
        lat = float(m["lat"])
        lon = float(m["lon"])
        del cityDict["properties"]["lat"]
        del cityDict["properties"]["lon"]
        cityDict["geometry"] = {}
        cityDict["geometry"]["type"]="Point"
        cityDict["geometry"]["coordinates"] = [
          lon,
          lat
        ]
        while n < 1000:
          all_cities.append(cityDict)
          n+=1

out = open("C:\\Users\\Esther\\Documents\\VisualDS\\Spatial-DS-Edwards\\Assignments\\Program_4\\geo_json\\city_locations.geojson","w")

out.write(json.dumps(all_cities, sort_keys=False,indent=4, separators=(',', ': ')))

out.close()

