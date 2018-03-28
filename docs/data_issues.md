# Data Issues and Other Notes

## Citibike Trip Data Issues

Below are some issues present in the Citibike trip data files.

### 2015 Data Issues

The csv files for the months of 01/2015 to 03/2015 follow different formatting. In particular, there are no quotes around each item and the timestamp format is different (e.g. 3/1/2015 0:11 instead of the usual 4/1/2015 00:00:23). Luckily Google has handled this in their public dataset.

### Usertype Null Values

Several trips from 10/01/2016 to 03/31/2017 have null values for usertype. This seems to be system-wide as 663 Citibike (start) stations in NY and NJ report trips with missing values.

Below are relevant queries in legacy SQL.

```SQL
SELECT year(starttime) as trip_year, month(starttime) as trip_month, day(starttime) as trip_day,
  count(tripduration) as num_trip, avg(tripduration) as avg_trip
FROM 
  [citibike_tripdata.tripdata_2016_10_to_2017_12],
  [citibike_tripdata.tripdata_jc_2015_09_to_2017_12] 
WHERE usertype IS NULL
GROUP BY trip_day, trip_month, trip_year ORDER BY trip_year, trip_month, trip_day
```

```SQL
SELECT start_station_id, start_station_name,
  count(tripduration) as num_trip, avg(tripduration) as avg_trip
FROM 
  [citibike_tripdata.tripdata_2016_10_to_2017_12],
  [citibike_tripdata.tripdata_jc_2015_09_to_2017_12] 
WHERE usertype IS NULL
GROUP BY start_station_id, start_station_name ORDER BY num_trip DESC
```

### Unusual Stations

At least within the 2017 trip data, there are some stations that have fairly unusual locations (latitude and longitude outside expected operational area). These stations have names starting with "8D" and are assumed to be testing stations for [8D Technologies](https://www.motivateco.com/bike-share-leaders-motivate-and-8d-technologies-announce-merger/). I have ignored these in my start stations map. 

### Dates With No Trip Data

There are 8 days with no available trip data.

- '2016-01-23', '2016-01-24', '2016-01-25', '2016-01-26', '2017-02-09', '2017-03-14', '2017-03-15', '2017-03-16'

## Citibike Ridership and Membership Data Issues

### Undefined Data

Below dates have spacing instead of commas, leading to "undefined" values. Manual fix: spacing is replaced with commas and "undefined" values are deleted.
- 12/25/2014, 12/27/2014, 12/29/2014

Below date appears to have values for annual membership and 24-hour passes combined. Manual fix: insert comma between 147199 and 4256 and delete "undefined".
- 9/19/2015

### 3-Day and 7-Day Passes

Citibike switches from offering 7-day passes to 3-day passes. 5/18/2016 is the last day that 3-day passes are offered.

## Google Public Dataset

In general, Google's public dataset has been very useful. That said, their trip data coverage is only from 07/2013 to 09/2016. Additionally, Google has changed the gender field from int values to string representation (unknown, male, female). Moreover, their station data is kept somewhat up to date, which proves problematic as information for past stations is not present. 