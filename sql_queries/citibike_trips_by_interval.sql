#legacySQL

# Aggregate data in 3-hour intervals of a day

SELECT FLOOR(HOUR(starttime) / 3) AS interval, COUNT(tripduration) AS num_trips, AVG(tripduration) AS avg_trip 
FROM 
  [bigquery-public-data:new_york.citibike_trips],
  [citibike_tripdata.tripdata_2016_10_to_2017_12],
  [citibike_tripdata.tripdata_jc_2015_09_to_2017_12]
GROUP BY interval ORDER BY interval