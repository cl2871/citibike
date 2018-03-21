## Helpful Resources

https://github.com/phelps-sg/python-bigdata/blob/master/README.md

## Other (to be fixed)

https://data.cityofnewyork.us/City-Government/2010-Census-Tracts/fxpq-c8ku/data
http://data.jerseycitynj.gov/dataset/jersey-city-census-tract-polygon
https://www.census.gov/geo/maps-data/data/cbf/cbf_tracts.html


Note: Carto uses PostGreSql syntax

```
SELECT a.* FROM cb_2016_34_tract_500k a, jerseycitytract b
WHERE a.geoid = b.geoid
```

create 11-digit geoid and map income

```
SELECT *, '36' || LPAD(boro_ct2010, 9, '0') as geoid FROM table_2010_census_tracts
```
```
SELECT a.*, b.hd01_vd01 FROM table_2010_census_tracts a, acs_16_5yr_b19013 b
WHERE a.geoid = b.geo_id2
```

```
select a.cartodb_id,
       ST_Difference(
         a.the_geom_webmercator,
         b.the_geom_webmercator
       ) as the_geom_webmercator
from cb_2016_34_tract_500k a,
     tl_2016_34017_areawater b
```

Color Ramping w/ Turbo Carto (put into CartoCss)
https://carto.com/blog/styling-with-turbo-carto/

```
#layer {
	polygon-fill: ramp([hd01_vd01], colorbrewer(YlGn), quantiles(5));
  	polygon-opacity: 0.6;
	line-width: 0.5;
	line-color: #FFF;
	line-opacity: 0.5;
}
```

Work on this below query later. Note: based on [this](https://gist.github.com/ramiroaznar/c461a399eb20ae7392ff77badfea3ce2)

```
WITH
    start_station as (
		SELECT cartodb_id, start_station_id, start_station_latitude, start_station_longitude, FROM routes_2017_top_30
    ),
    end_station as (
      	SELECT cartodb_id, end_station_id, end_station_latitude, end_station_longitude, FROM routes_2017_top_30
    )
SELECT start_station.cartodb_id, r.shape as the_geom, r.length, r.duration
FROM start_station, end_station, cdb_route_point_to_point(origin.the_geom, destiny.the_geom, 'car') r 
```


## Weather 

https://www.climate.gov/maps-data/dataset/past-weather-zip-code-data-table

station:
"USW00014732","LA GUARDIA AIRPORT, NY US","40.7792","-73.88"