Instructions for queries
"""
Rephael Edwards
Query 1

This query returns all the features along the wayfrom one airport to another while passing through other airports.
Sample queries: DFW GVA 1000

Query#2
This query returns the nearest volcano and earthquake based on a point.
The user enters the feature, key, key value, number of records tobe returned, radius and the location as lon,lat
Sample query:1) query2.py volcano altitude 5000 min 5 2005 138,33
            2) query2.py earthquake magnitude 3 max 4 500 141,37

This program executes a query to find the top 3-5 clusters of volcanos and earthquakes.
The user enters the feature (volcanos or earthquakes), min # of points for a cluster , distance parameter for the db scan
Sample Queries: 1) volcanos 10 50
                2) earthquakes 20 100

