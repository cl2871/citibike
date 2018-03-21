import csv


def clean_weather_data():

    # https://www.climate.gov/maps-data/dataset/past-weather-zip-code-data-table
    # daily summaries, July 1, 2013 to Dec 31, 2017, Stations, USW00014732

    # note: station USW00014732 is LA GUARDIA AIRPORT, NY US (40.7792, -73.88)
    # standard units used

    input_path = "../data/weather_data/20130701_20171231.csv"
    output_path = "../data/weather_data/20130701_20171231_clean.csv"

    with open(input_path, "r") as weather_file:
        with open(output_path, "w", newline='') as output_file:

            reader = csv.reader(weather_file)
            writer = csv.writer(output_file)

            # skip header row
            next(reader, None)
            writer.writerow(['date', 'avg_wind_speed', 'precipitation', 'snowfall', 'snow_depth','avg_temperature'])

            for row in reader:

                # weather info
                DATE = row[5]
                AWND = row[6]           # average wind speed
                PRCP = row[8]           # precipitation
                SNOW = row[9]           # snowfall
                SNWD = row[10]          # snow depth
                TAVG = row[11]          # average temperature

                writer.writerow([DATE, AWND, PRCP, SNOW, SNWD, TAVG])


if __name__ == "__main__":
    clean_weather_data()