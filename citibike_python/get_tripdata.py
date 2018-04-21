import gzip
import shutil
import urllib.request
import os
import zipfile

"""Downloads Citibike trip data as zip files then unzips them.

Downloads NY trip data for October 2016 to December 2017 and NJ trip data for September 2015 to December 2017.
The function retrieve_gz_data() is not utilized but is included below for downloading Google gzip files for 
July 2013 to September 2016.
"""


def retrieve_gz_data():

    """Retrieves trip data from Google's public dataset as gzip files.

    Downloads trip data from July 2013 to September 2016

    To extract gz file, use the following command in the directory:
    gunzip -k *.gz;

    Returns:
        Nothing
    """

    target = "../tripdata/gz/tripdata"

    for i in range(35):
        form = '{:012d}'.format(i)

        # retrieve data from bucket and store in directory
        urllib.request.urlretrieve("https://storage.googleapis.com/citibike_tripdata/tripdata" + form + ".gz",
                                   target + form + ".gz")


def retrieve_citibike_data():

    """Retrieves trip data from Citibike's S3 buckets as zip files.

    Downloads trip data from October 2016 to December 2017

    Returns:
        Nothing
    """

    target = "../tripdata/zip/citibike_tripdata_"

    for year in range(2016, 2018):
        for month in range(1, 13):

            if year == 2016 and month < 10:
                continue

            date_format = str(year) + '{:02d}'.format(month)

            # retrieve data from citibike's s3 buckets and store in zip directory
            if year < 2017:
                urllib.request.urlretrieve("https://s3.amazonaws.com/tripdata/" + date_format +
                                           "-citibike-tripdata.zip", target + date_format + ".zip")
            else:
                urllib.request.urlretrieve("https://s3.amazonaws.com/tripdata/" + date_format +
                                           "-citibike-tripdata.csv.zip", target + date_format + ".csv.zip")
            print(str(year) + "-" + str(month) + " done")


def retrieve_citibike_jc_data():

    """Does same thing as retrieve_citibike_data() but for Jersey City data

    Downloads trip data from September 2015 to December 2017.
    """

    target = "/tripdata/zip/citibike_tripdata_jc_"

    for year in range(2015, 2018):
        for month in range(1, 13):

            if year == 2015 and month < 9:
                continue

            date_format = str(year) + '{:02d}'.format(month)

            # retrieve data from citibike's s3 buckets and store in zip directory
            # note: JC-201708 is missing a dash
            if year == 2017 and month == 8:
                urllib.request.urlretrieve(
                    "https://s3.amazonaws.com/tripdata/JC-" + date_format + " citibike-tripdata.csv.zip",
                    target + date_format + ".csv.zip")
            else:
                urllib.request.urlretrieve(
                    "https://s3.amazonaws.com/tripdata/JC-" + date_format + "-citibike-tripdata.csv.zip",
                    target + date_format + ".csv.zip")
            print(str(year) + "-" + str(month) + " done")


def unzip_citibike_data():

    """Unzips Citibike zip files for both NY and JC.

    Returns:
        Nothing
    """

    zip_dir = "../tripdata/zip/"
    csv_dir = "../tripdata/csv/"
    extension = ".zip"

    # for each zip file in zip_dir extract data to csv_dir
    for item in os.listdir(zip_dir):
        if item.endswith(extension):

            # create zipfile object and extract
            file_name = zip_dir + item
            with zipfile.ZipFile(file_name, "r") as zip_ref:
                zip_ref.extractall(csv_dir)
                print(item + " done")
                #os.remove(file_name)


if __name__ == "__main__":
    retrieve_citibike_data()
    retrieve_citibike_jc_data()
    unzip_citibike_data()
