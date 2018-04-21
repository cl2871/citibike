#legacySQL

SELECT start_station_id, start_station_name, start_station_latitude, start_station_longitude,
COUNT(tripduration) AS num_trip, AVG(tripduration) AS avg_trip 
FROM 
  [bigquery-public-data:new_york.citibike_trips],
  [citibike_tripdata.tripdata_2016_10_to_2017_12],
  [citibike_tripdata.tripdata_jc_2015_09_to_2017_12] 
GROUP BY start_station_id, start_station_name, start_station_latitude, start_station_longitude ORDER BY num_trip DESC