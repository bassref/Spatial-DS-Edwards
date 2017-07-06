"""

This program executes a query to find the top 3-5 clusters of volcanos and earthquakes.
Sample Queries: 1) volcanos 10 50
                2) earthquakes 20 100
"""
import os,sys
import math
from pymongo import MongoClient
from math import sin, cos, sqrt, atan2, radians
import pprint
import unicodedata 

# -*- encoding : utf-8 -*-
#             ^
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

    ''' 
    Calculate the distance between the two locations
    '''
    def get_distance(self, s_point, e_point ):

        # approximate radius of earth in km
        R = 6373.0 
        
        lon1 = s_point[1]
        lon2 = e_point[1]
        lat1 = s_point[0]
        lat2 = e_point[0]
        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c
        return distance

    #function to convert lat lon to x, y for plotting

        """
        Converts lists (polygons) of lat/lon pairs into pixel coordinates in order to do some 
        simple drawing using pygame. 
        """
        width = height = 1000

        self.mapWidth = width       # width of the map in pixels
        self.mapHeight = height     # height of the map in pixels
        self.mapLonLeft = -180.0    # extreme left longitude
        self.mapLonRight = 180.0    # extreme right longitude
        self.mapLonDelta = self.mapLonRight - self.mapLonLeft # difference in longitudes
        self.mapLatBottom = 0.0     # extreme bottom latitude
        self.mapLatBottomDegree = self.mapLatBottom * math.pi / 180.0 # bottom in degrees

    def convertGeoToPixel(self, lon, lat):
        """
        Converts lat/lon to pixel within a set bounding box
        Args:
            lon (float): longitude
            lat (float): latitude
        Returns:
            point (tuple): x,y coords adjusted to fit on print window
        """
        x = (lon - self.mapLonLeft) * (self.mapWidth / self.mapLonDelta)

        lat = lat * math.pi / 180.0
        self.worldMapWidth = ((self.mapWidth / self.mapLonDelta) * 360) / (2 * math.pi)
        self.mapOffsetY = (self.worldMapWidth / 2 * math.log((1 + math.sin(self.mapLatBottomDegree)) / (1 - math.sin(self.mapLatBottomDegree))))
        y = self.mapHeight - ((self.worldMapWidth / 2 * math.log((1 + math.sin(lat)) / (1 - math.sin(lat)))) - self.mapOffsetY)

        return (x, y)

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
    def calculate_initial_compass_bearing(self, pointA, pointB):
        """
        Calculates the bearing between two points.

        The formulae used is the following:
             theta= atan2(sin(delta long).cos(lat2),
                      cos(lat1).sin(lat2) - sin(lat1).cos(lat2).cos(delta long))

        :Parameters:
          - `pointA: The tuple representing the latitude/longitude for the
            first point. Latitude and longitude must be in decimal degrees
          - `pointB: The tuple representing the latitude/longitude for the
            second point. Latitude and longitude must be in decimal degrees

        :Returns:
          The bearing in degrees

        :Returns Type:
          float
        """
        if (type(pointA) != tuple) or (type(pointB) != tuple):
            raise TypeError("Only tuples are supported as arguments")

        lat1 = math.radians(pointA[0])
        lat2 = math.radians(pointB[0])

        diffLong = math.radians(pointB[1] - pointA[1])

        x = math.sin(diffLong) * math.cos(lat2)
        y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
                * math.cos(lat2) * math.cos(diffLong))

        initial_bearing = math.atan2(x, y)

        # Now we have the initial bearing but math.atan2 return values
        # from -180 deg to + 180 deg which is not what we want for a compass bearing
        # The solution is to normalize the initial bearing as shown below
        initial_bearing = math.degrees(initial_bearing)
        compass_bearing = (initial_bearing + 360) % 360

        return compass_bearing
    
     
     
    def choose_next_airport(self, next_airs, lon_dir, bearing, used_ap):
        filter1 = []
        #create a list of airports on the east with lowest level
        #print("long_dir %d" % lon_dir)
        if bearing <= 180:
            for ap in next_airs:
                prop_lng = float(ap[u'properties'][u'lng'])
                #print("<=180 %s" % ap[u'properties'][u'lng']) 
                if prop_lng > lon_dir and lon_dir != "":
                    filter1.append(ap)
        
        elif bearing > 180:
            for ap in next_airs:
                #print(">180 %s" % ap[u'properties'][u'lng'])
                prop_lng = float(ap[u'properties'][u'lng'])
                if prop_lng < lon_dir and prop_lng != "" and lon_dir != "":
                    filter1.append(ap)
        for a in filter1:
            if a[u'properties'][u'ap_iata'] in used_ap or a[u'properties'][u'ap_iata'] == "" :
                filter1.remove(a)
            
        level_key = lambda airport: airport[u'properties'][u'ap_level']      
        min_level = min(filter1, key=level_key)
        lowest_levels = [x for x in filter1 if x[u'properties'][u'ap_level'] == min_level[u'properties'][u'ap_level']]
        #lowest_level.append(min(filter1, key=lambda filter1: filter1[u'properties'][u'ap_level']))   
        #print("lowest level")
        #print(lowest_level)
        
        if len(lowest_levels) >1:
            elevation_key = lambda airport: airport[u'properties'][u'elevation']
            choice = min(lowest_levels, key=elevation_key)
            
        else:
            choice = lowest_levels[0]
            
        return choice
    



if __name__ == '__main__':
    mh = mongoHelper()
    used_ap = []
    next_ap = []
    loc_a = sys.argv[1]
    loc_b = sys.argv[2]
    miles = float(sys.argv[3])
    used_ap.append(loc_a)
    print("Begin at: %s" % loc_a)
    a_doc = mh.get_doc_by_keyword('airports', 'properties.ap_iata', loc_a)
    b_doc = mh.get_doc_by_keyword('airports', 'properties.ap_iata', loc_b)
    points = mh.get_latlon('airports', a_doc, b_doc)
    end_point = points[1]
    #end_point_lat = points[2]
    #end_point_lon = points[3]
    pointA = points[0]#(float(points[1]), float(points[0]))
    pointB = points[1]#(float(points[3]), float(points[2]))
    bearing = mh.calculate_initial_compass_bearing(pointA, pointB)
    #print("---bearing")
    #print(bearing)
    while pointA[0] != end_point[0] and pointA[1] != end_point[1]:
        begin = points[0]#(float(points[1]), float(points[0]))
        print(begin)
        #print(points)
        # get all volcanoes, earthquakes and cities within a 500 mile radius and longitude is less than a
        #print their names and location
        print("Features on the way:")
        volcs = mh.get_features_near_me('volcanoes', begin, miles)
        print("Volcanoes: ")
        for v in volcs:
            name = v[u'properties'][u'Name']
            country = v[u'properties'][u'Country']
            print("   %s in %s" %(name, country))
        #get the earthquakes
        earth = mh.get_features_near_me('earthquakes', begin, miles)
        print("Earthquakes: ")
        for e in earth:
            name = e[u'properties'][u'place']
            mag = e[u'properties'][u'mag']
            print("   Location: %s ,Magnitude: %s" %(name, mag))
        met = mh.get_features_near_me('meteroite', begin, miles)
        print("Meteroites: ")
        for m in met:
            name = c[u'properties'][u'City']
            country = c[u'properties'][u'Country']
            print("   %s in %s" %(name, country))
        city = mh.get_features_near_me('world_cities', begin, miles)
        print("Cities: ")
        for c in city:
            name = c[u'properties'][u'City']
            country = c[u'properties'][u'Country']
            print("    %s in %s" %(name, country))
        state = mh.get_features_near_me('state_borders', begin, miles)
        print("States:")
        for s in state:
            name = c[u'properties'][u'name']
            print("   The state of %s is close." % name)
        
        #get the next airport within 500 miles
        next_airs = mh.get_features_near_me('airports', begin, miles)
        #pp.pprint(next_airs)
        lon_dir = begin[0]
        choice = mh.choose_next_airport(next_airs, lon_dir, bearing, used_ap)
        choice_val = choice[u'properties'][u'ap_iata']
        used_ap.append(choice_val)
        print("")
        print("Next airport: %s" % choice_val)
        next_doc = mh.get_doc_by_keyword('airports', 'properties.ap_iata', choice_val)
        points = mh.get_latlon('airports', next_doc, b_doc)
        #print(points)
               
        
     

    # for earthquakes, volcanos, etc, plot the points in the 500 radius whose lon val 
    # is less than that of the airport
    """
    start_point = mh.convertGeoToPixel(float(dis_bet[1]), float(dis_bet[0]))
    end_point = mh.convertGeoToPixel(float(dis_bet[3]), float(dis_bet[2]))
    distance = mh.get_distance(start_point, end_point)
    """
