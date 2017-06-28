import pprint as pp
import os,sys
import json
import collections
from collections import namedtuple

Country = namedtuple('Country', ('type, id, properties, geometry'))

f = open("C:\\Users\\Esther\\Documents\\VisualDS\\Spatial-DS-Edwards\\Assignments\\Program_4\\WorldData\\countries_edited.json","r")

data = f.read()

data = json.loads(data)

all_countries = []

#count = 0

for d in data:
    feat_list = d["features"]
    for count in range(1000, len(feat_list)-1):
        del feat_list[count]



out = open("C:\\Users\\Esther\\Documents\\VisualDS\\Spatial-DS-Edwards\\Assignments\\Program_4\\geo_json\\countries.geojson","w")

out.write(json.dumps(data, sort_keys=False,indent=4, separators=(',', ': ')))

out.close()

