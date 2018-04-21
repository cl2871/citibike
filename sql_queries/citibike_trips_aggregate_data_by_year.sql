#legacySQL

SELECT COUNT(tripduration) AS num_trip, AVG(tripduration) AS avg_trip, COUNT(DISTINCT bikeid) AS num_bike,
  COUNT(DISTINCT start_station_id) AS num_start_station, COUNT(DISTINCT end_station_id) AS num_end_station,
  YEAR(starttime) AS trip_year
FROM 
  [bigquery-public-data:new_york.citibike_trips],
  [citibike_tripdata.tripdata_2016_10_to_2017_12],
  [citibike_tripdata.tripdata_jc_2015_09_to_2017_12]
GROUP BY trip_year ORDER BY trip_year