# Citibike Trip Analysis Project

### Overview

The purpose of this project is primarily for me to experiment with big data tools such as Google BigQuery and Apache Spark. Below you will find documentation regarding the steps I took in performing my data analysis.

## Data Gathering and Setup

I decided to use the Google Cloud Platform as my platform of choice for working with Citibike trip data. A nice feature about GCP was that they were already hosting a public dataset for Citibike trips from July 2013 (earliest reporting) to September 2016. To expand on this, I pulled newer data (including Jersey City data) from the [Citibike S3 bucket](https://s3.amazonaws.com/tripdata/index.html) and uploaded it onto Google Cloud Storage. Afterwards, I made a dataset from the csv files to run queries on them using Google BigQuery.

### Pulling Data

I pulled zip files and unzipped them using [get_tripdata.py](get_tripdata.py). Afterwards, I uploaded the csv files to my personal bucket.

## Analysis

[Citibike.ipynb](notebooks/Citibike.ipynb)

to be continued...
