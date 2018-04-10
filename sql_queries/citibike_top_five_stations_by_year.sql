#legacySQL

# find top 5 (start) stations of each year by number of trips
# RANK() is used to rank by number of trips 

# show only the top 5 stations of each year based on results of inner query
SELECT *
FROM
  (
  # for each year, rank each station by number of trips that originate from it
  SELECT start_station_name, YEAR(starttime) AS trip_year, 
    COUNT(*) AS num_trip, RANK() OVER(PARTITION BY trip_year ORDER BY num_trip DESC) trip_rank
  FROM 
    [bigquery-public-data:new_york.citibike_trips],
    [citibike_tripdata.tripdata_2016_10_to_2017_12]
  GROUP BY start_station_name, trip_year
  )
WHERE trip_rank <= 5
ORDER BY trip_year, trip_rank