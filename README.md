# Citibike Trip Analysis Project

### Overview

The purpose of this project is primarily for me to experiment with big data tools such as Google BigQuery and Apache Spark. Below you will find documentation regarding the steps I took in performing my data analysis.

## Data Gathering and Setup

I decided to use the Google Cloud Platform as my platform of choice for working with Citibike trip data. A nice feature about GCP was that they were already hosting a public dataset for Citibike trips from July 2013 (earliest reporting) to September 2016. To expand on this, I pulled newer data (including Jersey City data) from the [Citibike S3 bucket](https://s3.amazonaws.com/tripdata/index.html) and uploaded it onto Google Cloud Storage. Afterwards, I made a dataset from the csv files to run queries on them using Google BigQuery.

### Pulling Data

I pulled zip files and unzipped them using [get_tripdata.py](get_tripdata.py). Afterwards, I uploaded the csv files to my personal bucket.

Notes:
- 2015 data has inconsistencies such as with the timestamp format; luckily Google has handled this in their public dataset
- 10/2016 to 03/2017 has some null values for usertype
- Google's public dataset changed gender from int values to string representation (unknown, male, female) 

## Jupyter Notebook Setup

Google offers Apache Spark clusters through its Dataproc service, and I utilize this to present results and visualizations using a Jupyter Notebook. 

### [Install Google Cloud SDK](https://cloud.google.com/sdk/) 

The SDK provides command line access to Google's services.

```
gcloud init
```

### Create Dataproc Cluster

A cluster called datascience will be spun up using the below code. It will have Jupyter Notebook installed.

``` 
gcloud dataproc clusters create datascience --initialization-actions gs://dataproc-initialization-actions/jupyter/jupyter.sh
```

You could do the same thing on the [user interface](https://cloud.google.com/dataproc/docs/guides/create-cluster#using_the_console_name) but remember to add the jupyter path under initialization actions.

### [SSH Tunneling and SOCKS](https://cloud.google.com/dataproc/docs/concepts/accessing/cluster-web-interfaces)

Have 2 command line interfaces open. One will be for the SSH tunnel and the other will be for starting a browser session with SOCKS proxy settings (see link above for more info). 


SSH Tunnel:

```
gcloud compute ssh --zone=master-host-zone master-host-name -- -D 1080 -N
```
Notes: 
- use name of MASTER node (e.g. datascience-m for datascience)
- need Putty for Windows

SOCKS Proxy Session:

```
"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --proxy-server="socks5://localhost:1080" --host-resolver-rules="MAP * 0.0.0.0 , EXCLUDE localhost" --user-data-dir=/tmp/master-host-name
```
### Connecting to Dataproc Cluster

Using the browser opened with SOCKS proxy settings, you can directly connect to the cluster services via the below URLs (hadoop and jupyter notebook respectively).

http://datascience-m:8088
http://datascience-m:8123 

After connecting to the second URL, you can create a PySpark notebook and run Python commands.

Install libraries:
```
!pip install --upgrade pandas
!pip install --upgrade google-api-python-client
!pip install --upgrade seaborn
!pip install pandas-gbq -U
```

### Cleanup

Save the notebook and download it when finished. Run the below command to shut down the cluster to save money. 

```
gcloud dataproc clusters delete datascience
```

## Analysis

[Citibike.ipynb](Citibike.ipynb)

to be continued...

## Helpful Resources

https://github.com/phelps-sg/python-bigdata/blob/master/README.md