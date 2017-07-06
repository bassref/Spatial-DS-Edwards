"""
Rephael Edwards
Query#2
This query returns the nearest volcano and earthquake based on a point.
The user enters the feature, key, key value, number of records tobe returned, radius and the location as lon,lat
Sample query:1) query2.py volcano altitude 5000 min 5 2005 138,33
            2) query2.py earthquake magnitude 3 max 4 500 141,37

"""
import os,sys
import math
from pymongo import MongoClient
from math import sin, cos, sqrt, atan2, radians
import pprint
import unicodedata 
import json, ast
from decimal import Decimal
pp = pprint.PrettyPrinter(indent=4)



class mongoHelper(object):
    def __init__(self):
        self.client = MongoClient()
        self.coord_list =[]
    
    '''
    Get the lat and lon for the locations given
    '''
    def get_latlon(self, collection, point_a, point_b):

        lat1 = point_a[0][u'properties'][u'lat'] 
        lon1 = point_a[0][u'properties'][u'lng']
        lat2 = point_b[0][u'properties'][u'lat']
        lon2 = point_b[0][u'properties'][u'lng']
        res = [(float(lon1), float(lat1)), (float(lon2), float(lat2))]
        
        return res
    def get_features_near_me(self,collection,point,radius,earth_radius=3963.2): #km = 6371
        """
        Finds "features" within some radius of a given point.
        Params:
            collection_name: e.g airports or meteors etc.
            point: e.g (-98.5034180, 33.9382331)
            radius: The radius in miles from the center of a sphere (defined by the point passed in)
        Usage:
            mh = mongoHelper()
            loc = (-98.5034180, 33.9382331)
            miles = 200
            feature_list = mh.get_features_near_me('airports', loc, miles)
        """
        x,y = point

        res = self.client['rephie'][collection].find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [x, y ] , radius/earth_radius ] } }} )
        
        return self._make_result_list(res)
        
    def get_doc_by_keyword(self,collection,field_name,search_key,like=True):
        """
        Finds "documents" with some keyword in some field.
        Params:
            collection_name: e.g airports or meteors etc.
            field_name: key name of the field to search. e.g. 'place_id' or 'magnitude' 
            search_key: The radius in miles from the center of a sphere (defined by the point passed in)
        Usage:
            mh = mongoHelper()
            feature_list = mh.get_doc_by_keyword('earthquakes','properties.type','shakemap')
            # Returns all earthquakes that have the word 'shakemap' somewhere in the 'type' field
        """
        if like:
            # This finds the records in which the field just "contains" the search_key
            res = self.client['rephie'][collection].find(({field_name : {'$regex' : ".*"+search_key+".*"}}))
        else:
            # This finds the records in which the field is equal to the search_key
            res = self.client['rephie'][collection].find({field_name : search_key})

        return self._make_result_list(res)

        
    def _make_result_list(self,res):
        """
        private method to turn a pymongo result into a list
        """
        res_list = []
        for r in res:
            res_list.append(r)

        return res_list
    
    def filtered_list(self, feature_list, field_name, field_value, min_or_max):
        
        filter_list = []
        
        for f in feature_list:
            key_value = f['properties'][field_name]
            if key_value !="" and field_value !="":            
                if min_or_max == 'min' and  float(key_value) >= float(field_value):
                    filter_list.append(f)
                elif min_or_max == 'max' and  float(key_value) <= float(field_value):
                    filter_list.append(f)
                elif min_or_max == "" and f['properties'][field_name] == field_value:
                    filter_list.append(f)                  
            """for f in feature_list:
            if min_or_max == 'minimum' and  float(f['properties'][field_name]) >= float(field_value):
                filter_list.append(f)
            elif min_or_max == 'maximum' and  float(f['properties'][field_name]) <= float(field_value):
                filter_list.append(f)"""    
        return filter_list
    
    def type_filter(self, feature_list, field_name, field_value):
        
        filter_list = []
        for f in feature_list:
            key_value = f[u'properties'][u'Type']
            if key_value == field_value:
                filter_list.append(f)
        
        return filter_list
        
    def country_filter(self, feature_list, field_name, field_value):
        
        filter_list = []
        
        for f in feature_list:
            key_value = f[u'properties'][u'Type']
            if key_value == field_value:
                filter_list.append(f)        
                
        return filter_list
        
     
 

if __name__ == '__main__':

    mh = mongoHelper()
    filtered_matches_list = []
    final_list = []
    matches = []
    count = 0
    header = '--------Query 2-----------'
    out = open("query2_output.txt", "w")
    out.write('--------Query 2-----------')
    
    if len(sys.argv) < 5:
        feature_list = ['volcanos', 'earthquakes', 'meteroite'] 
        radius = float(sys.argv[1])
        lon_lat = sys.argv[2]
        string_point = lon_lat.split(",")
        point_x = float(string_point[0])
        point_y = float(string_point[1])
        point = (point_x, point_y)
        max_results = 500
        for feature in feature_list:
            matches = mh.get_features_near_me(feature, point, radius)
            filtered_matches_list.append(matches)
        for filter in filtered_matches_list:
            if count < float(max_results) and count < len(filter):
                pp.pprint(filter[count])
                #out.write(json.dumps(filter[count], sort_keys=False,indent=4, separators=(',', ': ')))
                count+=1
            
    else:         
        feature = sys.argv[1]
        field = sys.argv[2]
        field_value = sys.argv[3]
        min_or_max = sys.argv[4]
        max_results = sys.argv[5]
        radius = float(sys.argv[6])
        lon_lat = sys.argv[7]
        
        string_point = lon_lat.split(",")
        point_x = float(string_point[0])
        point_y = float(string_point[1])
        point = (point_x, point_y)
        
        if feature == 'volcanos':
            cap_title = field.title()
            field_name = 'properties.'+cap_title 
            
            feature_list = mh.get_features_near_me(feature, point, radius)
            filtered_matches_list = mh.filtered_list(feature_list, cap_title, field_value, min_or_max)
        
        elif feature == 'earthquakes' or feature == 'meteorite':
            feature_list = mh.get_features_near_me(feature, point, radius)
            filtered_matches_list = mh.filtered_list(feature_list, field, field_value, min_or_max)
            
        #print results
        while (count < float(max_results) and count < len(filtered_matches_list)):
            match = filtered_matches_list[count]
            #out.write(json.dumps(matchsort_keys=False,indent=4, separators=(',', ': ')))
            pp.pprint(match)
            count+=1
        
    
    out.close()   
    
    
    