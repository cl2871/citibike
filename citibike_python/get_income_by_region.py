import os
import csv
import requests

""" ---- Overview ----
    
    This file utilizes a station's latitude and longitude to identify the geographic region it is located in.
    Afterwards, the median income of the geographic region can be mapped to a given station.
    
    Note: zip codes code is deprecated, census tracts are more reliable for population statistics
    
    --- Zip Codes ---
    
    > get_zip_codes()                               get zip codes for each station
    > collect_median_income_by_zip_code()           map income to a station via its zip code
    
    --- Census Tracts ---
    
    > get_zip_codes()                               get census tracts for each station
    > collect_median_income_by_census_tract()       map income to a station via its census track
    
"""


def get_zip_codes():

    """Generates a csv file that maps zip code to station data.

    Grabs postal codes for each station via Google's geocoding API by latitude and longitude.
    The number of unknown postal codes after pulling data is small (1 entry); can manually look up.

    See below for an example json response
    https://developers.google.com/maps/documentation/geocoding/intro#reverse-example

    Returns:
        Nothing
    """

    key = os.environ["Google_API"]
    input_path = "../data/workspace/citibike_stations.csv"
    output_path = "../data/workspace/citibike_stations_zipcodes.csv"

    with open(input_path, "r") as stations_file:
        with open(output_path, "w", newline='') as output_file:

            # readers and writers; note: newline='' needed for Windows due to extra carriage return
            reader = csv.reader(stations_file)
            writer = csv.writer(output_file)

            # skip header row
            next(reader, None)
            writer.writerow(['station_id', 'name', 'latitude', 'longitude', 'zipcode', 'capacity'])

            for row in reader:

                # station info
                station_id = row[0]
                name = row[1]
                latitude = row[3]
                longitude = row[4]
                capacity = row[7]

                # TODO: ignore testing stations (stations related to 8D Technologies)
                # if latitude and longitude are not 0 (station available)
                if float(latitude) and float(longitude):

                    # retrieve zip code of station using Google's geocoding API
                    request = "https://maps.googleapis.com/maps/api/geocode/json?latlng=" \
                              + latitude + "," + longitude + "&result_type=postal_code" + "&key=" + key
                    response = requests.get(request).json()

                    # get a result if there are any
                    if response["results"]:
                        zipcode = response["results"][0]["address_components"][0]["short_name"]
                    else:
                        zipcode = "UNKNOWN"

                    # display bad values and append data to output file
                    if len(str(zipcode)) != 5 and zipcode != "UNKNOWN":
                        print("Unexpected Value:", zipcode, "for latlng", str(latitude), ",", str(longitude))
                    elif zipcode == "UNKNOWN":
                        print("Unknown Zipcode for latlng:", str(latitude), ",", str(longitude))
                        writer.writerow([station_id, name, latitude, longitude, zipcode, capacity])
                    else:
                        writer.writerow([station_id, name, latitude, longitude, zipcode, capacity])


def read_income_path_zip_code(path, hashmap):

    """Reads in income data from file and maps income for each zip code.

    Key: zip code, Value: income
    """

    with open(path, "r") as income_file:
        reader = csv.reader(income_file)

        # skip 2 header rows
        next(reader, None)
        next(reader, None)

        for row in reader:
            zipcode = row[1]
            income = row[3]
            hashmap[zipcode] = income


def collect_median_income_by_zip_code():

    """Generates a csv file that maps median income to station data by zip code.

    References
    https://factfinder.census.gov/
    https://www.reddit.com/r/datasets/comments/3lfttu/recent_median_household_income_by_us_zip_code/

    Steps for downloading median income data using Census Bureau website:
    advanced search > geographies > 5 digit zip code tabulation area > new york (and new jersey) > add to selections
    table B19013 > 2016 ACS 5-year estimates > download (use), uncheck merge annotations and data into same file

    Returns:
        Nothing
    """

    # map for zip code to median income
    hashmap = dict()

    # renamed the unzipped folders (NY and NJ)
    income_ny_path = "../data/income_data/ACS_16_5YR_B19013_NY/ACS_16_5YR_B19013.csv"
    income_nj_path = "../data/income_data/ACS_16_5YR_B19013_NJ/ACS_16_5YR_B19013.csv"

    input_path = "../data/workspace/citibike_stations_zipcodes.csv"
    output_path = "../data/workspace/citibike_stations_and_income.csv"

    # populate hashmap with zip code keys and income values
    read_income_path_zip_code(income_ny_path, hashmap)
    read_income_path_zip_code(income_nj_path, hashmap)

    with open(input_path, "r") as input_file:
        with open(output_path, "w", newline='') as output_file:

            # readers and writers; note: newline='' needed for Windows due to extra carriage return
            reader = csv.reader(input_file)
            writer = csv.writer(output_file)

            # skip header row
            next(reader, None)
            writer.writerow(['station_id', 'name', 'latitude', 'longitude', 'zipcode', 'income', 'capacity'])

            for row in reader:

                zipcode = row[4]
                capacity = row[5]

                if zipcode in hashmap:
                    income = hashmap[zipcode]
                else:
                    income = "UNKNOWN"

                writer.writerow([row[0], row[1], row[2], row[3], zipcode, income, capacity])


def get_census_tracts():

    """Generates a csv file that maps zip code to station data.

    Grabs the census tract for each station via the FCC's geo API by latitude and longitude.
    https://geo.fcc.gov/api/census/

    NOTE: block_fips is a unique identifier for a census block (has state, county, tract, and block ids)
    e.g. 360470543001000  ->  36      047         054300      1000
                              ^ state ^ county    ^ tract     ^ block

    Returns:
        Nothing
    """

    input_path = "../data/workspace/citibike_stations.csv"
    output_path = "../data/workspace/citibike_stations_census_tracts.csv"

    with open(input_path, "r") as stations_file:
        with open(output_path, "w", newline='') as output_file:

            # readers and writers; note: newline='' needed for Windows due to extra carriage return
            reader = csv.reader(stations_file)
            writer = csv.writer(output_file)

            # skip header row
            next(reader, None)
            writer.writerow(['station_id', 'name', 'latitude', 'longitude', 'census_tract', 'capacity'])

            for row in reader:

                # station info
                station_id = row[0]
                name = row[1]
                latitude = row[3]
                longitude = row[4]
                capacity = row[7]

                # if latitude and longitude are not 0 (station available)
                if float(latitude) and float(longitude):

                    # retrieve zip code of station using the FCC's geo API
                    request = "https://geo.fcc.gov/api/census/area?lat=" \
                              + latitude + "&lon=" + longitude + "&format=json"
                    response = requests.get(request).json()

                    # get a result if there are any
                    if response["results"]:
                        block_fips = response["results"][0]["block_fips"]
                        census_tract = block_fips[:11]
                    else:
                        census_tract = "UNKNOWN"

                    # display bad values and append data to output file
                    if len(census_tract) != 11 and census_tract != "UNKNOWN":
                        print("Unexpected Value:", census_tract, "for lat,lon:", str(latitude), ",", str(longitude))
                    elif census_tract == "UNKNOWN":
                        print("Unknown Census Tract for lat,lon:", str(latitude), ",", str(longitude))
                        writer.writerow([station_id, name, latitude, longitude, census_tract, capacity])
                    else:
                        writer.writerow([station_id, name, latitude, longitude, census_tract, capacity])


def read_income_path_census_tract(path, hashmap):

    """Reads in income data from file and maps income for each census tract.

    Key: census tract, Value: income
    """

    with open(path, "r") as income_file:
        reader = csv.reader(income_file)

        # skip 2 header rows
        next(reader, None)
        next(reader, None)

        for row in reader:
            census_tract = row[1]
            income = row[3]
            hashmap[census_tract] = income


def collect_median_income_by_census_tract():

    """Generates a csv file that maps median income to station data by census tract.

    https://factfinder.census.gov/

    Steps for downloading median income data using Census Bureau website:
    advanced search > geographies > census tract > new york (and new jersey) > all census tracts > add to selections
    table B19013 > 2016 ACS 5-year estimates > download (use), uncheck merge annotations and data into same file

    Returns:
        Nothing
    """

    # map for census tract to median income
    hashmap = dict()

    # renamed the unzipped folder for census tract
    income_census_path = "../data/income_data/ACS_16_5YR_B19013_Census_Tract/ACS_16_5YR_B19013.csv"
    input_path = "../data/workspace/citibike_stations_census_tracts.csv"
    output_path = "../data/workspace/citibike_stations_census_tracts_and_income.csv"

    read_income_path_census_tract(income_census_path, hashmap)

    with open(input_path, "r") as input_file:
        with open(output_path, "w", newline='') as output_file:

            # readers and writers; note: newline='' needed for Windows due to extra carriage return
            reader = csv.reader(input_file)
            writer = csv.writer(output_file)

            # skip header row
            next(reader, None)
            writer.writerow(['station_id', 'name', 'latitude', 'longitude', 'census_tract', 'income', 'capacity'])

            for row in reader:

                census_tract = row[4]
                capacity = row[5]

                if census_tract in hashmap:
                    income = hashmap[census_tract]
                else:
                    income = "UNKNOWN"

                writer.writerow([row[0], row[1], row[2], row[3], census_tract, income, capacity])


if __name__ == "__main__":
    get_census_tracts()
    collect_median_income_by_census_tract()
