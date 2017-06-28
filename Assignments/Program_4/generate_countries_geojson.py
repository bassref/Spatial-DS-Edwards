import pprint as pp
import os,sys
import json
import collections


f = open("C:\\Users\\Esther\\Documents\\VisualDS\\Spatial-DS-Edwards\\Assignments\\Program_4\\WorldData\\countries.geo.json","r")

data = f.read()

data = json.loads(data)

all_airports = []

n = 0

json_object = f.load(raw)
