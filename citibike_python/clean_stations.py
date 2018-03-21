import csv


def remove_bad_latitude_longitude():

    input_path = "../data/queried_data/citibike_trips_by_end_stations_2017.csv"
    output_path = "../data/workspace/citibike_trips_by_end_stations_2017_clean.csv"

    with open(input_path, "r") as stations_file:
        with open(output_path, "w", newline='') as output_file:

            # readers and writers; note: newline='' needed for Windows due to extra carriage return
            reader = csv.reader(stations_file)
            writer = csv.writer(output_file)

            # write header
            writer.writerow(next(reader))

            for row in reader:

                name = row[1]
                latitude = row[2]
                longitude = row[3]

                # if both latitude and longitude are not 0 and not a special station (station available)
                if float(latitude) and float(longitude) and name[:2] != '8D':

                    writer.writerow(row)


if __name__ == "__main__":
    remove_bad_latitude_longitude()