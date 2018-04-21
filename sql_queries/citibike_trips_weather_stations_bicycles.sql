#standardSQL

/* 
  Will display the following information by day:
    - date information
    - aggregate trip information such as number of trips (num_trip) and average trip duration (avg_trip)
    - weather information such as temperature and snowfall
    - monthly operating report information such as average number of monthly stations and bicycles
        note: not daily data
  
  trip_date, day_of_week, trip_month, trip_year, num_trip, avg_trip, temp, stations
*/

# Get date, trip, weather, reports data; join reports data on month-year concatenation
SELECT trips_and_weather.*, reports.stations, reports.bicycles
FROM
  (
    # Get date, trip, and weather data; join weather data on date
    SELECT trips_by_date.trip_date AS trip_date, EXTRACT(DAYOFWEEK FROM trips_by_date.trip_date) AS day_of_week, 
      EXTRACT(MONTH FROM trips_by_date.trip_date) AS trip_month, EXTRACT(YEAR FROM trips_by_date.trip_date) AS trip_year,
      trips_by_date.num_trip AS num_trip, trips_by_date.avg_trip AS avg_trip, 
      weather.avg_temperature AS temp, weather.precipitation AS prec, weather.snowfall AS snowfall
    FROM
      (
        # Get aggregate trip data grouped by date
        SELECT EXTRACT(DATE FROM starttime) AS trip_date, COUNT(tripduration) AS num_trip, AVG(tripduration) AS avg_trip 
        FROM
          (
            (
              SELECT starttime, tripduration FROM
              `bigquery-public-data.new_york.citibike_trips`
            )
            UNION ALL
            (
              SELECT starttime, tripduration FROM
              `citibike_tripdata.tripdata_2016_10_to_2017_12`
            )
            UNION ALL
            (
              SELECT starttime, tripduration FROM
              `citibike_tripdata.tripdata_jc_2015_09_to_2017_12`
            )
          )
        GROUP BY trip_date ORDER BY trip_date
      ) AS trips_by_date
      
    JOIN `weather.laguardia_20130701_20171231` AS weather
    ON trips_by_date.trip_date = weather.date
  ) AS trips_and_weather
  
JOIN `operating_reports.reports_2013_07_to_2017_12` AS reports
ON CONCAT(CAST(trips_and_weather.trip_month AS STRING), CAST(trips_and_weather.trip_year AS STRING)) 
  = CONCAT(CAST(EXTRACT(MONTH FROM reports.date) AS STRING), CAST(EXTRACT(YEAR FROM reports.date) AS STRING))
