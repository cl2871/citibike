import os
import csv
import requests


def get_zipcodes():

    # grabs postal codes for each station via Google geocoding API by latitude and longitude
    # number of unknown postal codes after pulling data is small (1 entry), can manually look up

    # see below for example json response
    # https://developers.google.com/maps/documentation/geocoding/intro#reverse-example

    key = os.environ["Google_API"]
    input_path = r"C:\Users\Chris\Desktop\Code_Practice\citibike\citibike_stations.csv"
    output_path = r"C:\Users\Chris\Desktop\Code_Practice\citibike\citibike_stations_updated.csv"

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

                # if latitude and longitude are not 0 or null (station not available)
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

if __name__ == "__main__":
    get_zipcodes()

