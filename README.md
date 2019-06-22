# Citibike Trip Analysis Project

### Overview

The purpose of this project is primarily for me to experiment with big data tools such as Google BigQuery and Apache Spark. Below you will find documentation regarding the steps I took in performing my data analysis.

## Data Gathering and Setup

I decided to use the Google Cloud Platform as my platform of choice for working with Citibike trip data. A nice feature about GCP was that they were already hosting a public dataset for Citibike trips from July 2013 (earliest reporting) to September 2016. To expand on this, I pulled newer data (including Jersey City data) from the [Citibike S3 bucket](https://s3.amazonaws.com/tripdata/index.html) and uploaded it onto Google Cloud Storage. Afterwards, I made a dataset from the csv files to run queries on them using Google BigQuery.

### Pulling Data

I pulled zip files and unzipped them using [get_tripdata.py](get_tripdata.py). Afterwards, I uploaded the csv files to my personal bucket.

## Analysis

Analysis of Citibike trips can be found in the [notebooks](notebooks) directory.

For a quick look at general trends in Citibike ridership, take a look at [General Trends Analysis](notebooks/General_Trends_Analysis.ipynb).

For an analysis of the stations that trips start at, take a look at [Start Stations](notebooks/Start_Stations.ipynb)

To see a predictive model of Citibike trips using an Ordinary Least Squares linear regression approach, please take a look at [Citibike Predict Trips 79 R2 Revised](notebooks/Citibike_Predict_Trips_79_R2_Revised.ipynb). The model uses station data, weather information, and date information to predict the number of trips on a given day. The data is split into a training set and testing set, and certain features with widely varying ranges such as tempurature and precipitation are scaled.

## Other

For a look at the SQL queries I used on Google BigQuery for aggregating data, take a look at [SQL Queries](sql_queries).

For a look at the Python scripts I used for gathering and cleaning data, take a look at [Citibike Python](citibike_python). This will also include unused files such as one running Dijkstra's algorithm on all stations to find the shortest paths between all stations based on average time.
