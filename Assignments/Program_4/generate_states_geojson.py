import pprint as pp
import os,sys
import json
import collections

f = open("C:\\Users\\Esther\\Documents\\VisualDS\\Spatial-DS-Edwards\\Assignments\\Program_4\\WorldData\\state_borders.json", "r")

data = f.read()

data = json.loads(data)
n = 0

all_state_boarders = []


for d in data:
    stateDict = collections.OrderedDict()
    #member = d[key]
    stateDict["type"] = "Feature"
    stateDict["properties"] = d.copy() #set the whole dictionary as the properties
    del stateDict["properties"]["coordinates"]
    #for firstList in d["coordinates"]: #coordinates is a list with a 2nd list with 3rd lists of coordinates
    stateDict["geometry"] = {}
    stateDict['geometry']['type']="Polygon"
    stateDict['geometry']['coordinates'] = d["coordinates"] 
    while n < 1000:
        all_state_boarders.append(stateDict)
        n+=1


out = open("C:\\Users\\Esther\\Documents\\VisualDS\\Spatial-DS-Edwards\\Assignments\\Program_4\\geo_json\\states.geojson","w")

out.write(json.dumps(all_state_boarders, sort_keys=False,indent=4, separators=(',', ': ')))

out.close()
    



