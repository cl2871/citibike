#legacySQL

# Will display routes ("station_a to station_b"), related station information, and aggregate data for 2017

SELECT 
  CONCAT(start_station_name, " to ", end_station_name) AS route, 
  start_station_id, start_station_latitude, start_station_longitude,
  end_station_id, end_station_latitude, end_station_longitude,
  COUNT(tripduration) AS num_trip, AVG(tripduration) AS avg_trip
FROM 
  [bigquery-public-data:new_york.citibike_trips],
  [citibike_tripdata.tripdata_2016_10_to_2017_12], 
  [citibike_tripdata.tripdata_jc_2015_09_to_2017_12]
WHERE YEAR(starttime) = 2017
GROUP BY route, start_station_id, start_station_latitude, start_station_longitude,
  end_station_id, end_station_latitude, end_station_longitude 
ORDER BY num_trip DESC