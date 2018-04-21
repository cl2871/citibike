#legacySQL

SELECT HOUR(starttime) AS hour, COUNT(tripduration) AS num_trip, AVG(tripduration) AS avg_trip  
FROM 
  [bigquery-public-data:new_york.citibike_trips],
  [citibike_tripdata.tripdata_2016_10_to_2017_12],
  [citibike_tripdata.tripdata_jc_2015_09_to_2017_12]
GROUP BY hour ORDER BY hour