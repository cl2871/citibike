#legacySQL

SELECT MONTH(starttime) AS trip_month, YEAR(starttime) AS trip_year, COUNT(tripduration) AS num_trip, AVG(tripduration) AS avg_trip 
FROM 
  [bigquery-public-data:new_york.citibike_trips],
  [citibike_tripdata.tripdata_2016_10_to_2017_12],
  [citibike_tripdata.tripdata_jc_2015_09_to_2017_12] 
GROUP BY trip_month, trip_year ORDER BY trip_year, trip_month