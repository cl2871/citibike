#legacySQL

# Get date, trip, and weather data; join weather data on date
SELECT trips_by_date.trip_date AS date, dayofweek(trips_by_date.trip_date) AS day_of_week, 
  month(trips_by_date.trip_date) AS month, year(trips_by_date.trip_date) AS year,
  trips_by_date.num_trip AS num_trip, trips_by_date.avg_trip AS avg_trip, weather.avg_temperature AS temp
FROM
  (
    # Get aggregate trip data grouped by date
    SELECT CAST(DATE(starttime) AS DATE) AS trip_date, COUNT(tripduration) AS num_trip, AVG(tripduration) AS avg_trip 
    FROM 
      [bigquery-public-data:new_york.citibike_trips],
      [citibike_tripdata.tripdata_2016_10_to_2017_12],
      [citibike_tripdata.tripdata_jc_2015_09_to_2017_12] 
    GROUP BY trip_date ORDER BY trip_date
  ) AS trips_by_date
  
JOIN [weather.laguardia_20130701_20171231] AS weather
ON trips_by_date.trip_date = weather.date