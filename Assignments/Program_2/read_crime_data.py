import pprint as pp
import os, sys

#get working path
DIRPATH = os.path.dirname(os.path.realpath(__file__))

keys = []
crimes = []
bronx_crimes = []


got_keys = False
with open(DIRPATH+ '/../NYPD_CrimeData/filtered_crimes_bronx.csv') as f:
    for line in f:
        line = line.strip().split(',')
        if not got_keys:
            keys = line
            print(keys)
            got_keys = True
            continue

        crimes.append(line)
for crime in crimes:
    bronx_crimes.append((crime[19],crime[20]))
    print(bronx_crimes[0])
