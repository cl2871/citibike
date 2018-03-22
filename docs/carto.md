# Map Visualizations Using Carto

Carto is an online platform for generating map visualizations through location data. Its software is built on PostGIS and PostgreSQL (so note the different SQL syntax).

## [Color Ramping w/ Turbo Carto](https://carto.com/blog/styling-with-turbo-carto/)

I decided to upload the information I had for Citibike (start) stations in 2017 (start_station_id, start_station_latitude, start_station_longitude, num_trips). Below is CSS code for highlighting stations in different colors. The stations are divided into 5 quantiles based on their number of trips (num_trip). To use this, go to a layer's style tab, toggle from values to CartoCSS, and then paste this code.

```CSS
#layer {
  marker-width: 7;
  marker-fill: ramp([num_trip], (#fcc5c0, #fa9fb5, #f768a1, #c51b8a, #7a0177), quantiles(5));
  marker-fill-opacity: 0.9;
  marker-allow-overlap: true;
  marker-line-width: 1;
  marker-line-color: #FFFFFF;
  marker-line-opacity: 1;
}
```