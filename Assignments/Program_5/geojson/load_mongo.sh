mongo rephie --eval "db.dropDatabase()"
mongoimport --db rephie --collection airports       --type json --file airports.geojson        --jsonArray
mongoimport --db rephie --collection countries      --type json --file countries.geojson       --jsonArray
mongoimport --db rephie --collection meteorites     --type json --file meteorite.geojson       --jsonArray
mongoimport --db rephie --collection volcanos       --type json --file volcanos.geojson        --jsonArray
mongoimport --db rephie --collection earthquakes    --type json --file earthquakes.geojson     --jsonArray
mongoimport --db rephie --collection cities         --type json --file world_cities.geojson    --jsonArray
mongoimport --db rephie --collection states         --type json --file state_borders.geojson   --jsonArray
mongoimport --db rephie --collection terrorism      --type json --file globalterrorism.geojson --jsonArray