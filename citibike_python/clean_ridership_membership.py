import csv
import os


def aggregate_data():

    # aggregates data from ridership and membership csv files
    # note: I named the files based on the year-month they represent (e.g. 201601_201603.csv for 2016 Q1)

    # data issues:
    #   12/25/2014, 12/27/2014, 12/29/2014 manually cleaned
    #   9/19/2015 annual membership and 24-passes values appear combined, manually fixed
    #   certain dates have outages (reporting 0's)
    #   last day of 7-day pass is 5/18/16
    #   2013 Q4 (10/2013 to 12/2013) file is missing 7-day pass information

    input_dir = "../data/ridership_membership_data/"
    output_path = "../data/workspace/citibike_ridership_membership_data.csv"

    with open(output_path, "w", newline='') as output_file:

        writer = csv.writer(output_file)
        writer.writerow(['date', 'trips', 'miles', 'annual_members', '24_hour_passes', '3_day_passes', '7_day_passes'])

        for item in os.listdir(input_dir):
            file_name = input_dir + item
            with open(file_name, "r") as input_file:

                reader = csv.reader(input_file)

                # skip header row
                next(reader, None)

                for row in reader:

                    # TODO: need to find data for 2013 Q4 for 7-day passes or write 0's, current code will break
                    # different months have different formats
                    if item[:4] in ["2013", "2014"]:
                        writable = [row[0], row[1], row[3], row[5], row[7], 0, row[8]]
                    elif item[:4] == "2015" or item[:6] == "201601":
                        writable = [row[0], row[1], row[3], row[5], row[6], 0, row[7]]
                    elif item[:6] == "201604":
                        writable = [row[0], row[1], row[3], row[5], row[6], row[7], row[8]]
                    elif item[:4] == "2016":
                        writable = [row[0], row[1], row[3], row[5], row[6], row[7], 0]
                    elif item[:4] == "2017":
                        writable = [row[0], row[1], row[2], row[3], row[4], row[5], 0]

                    writer.writerow(writable)


if __name__ == "__main__":
    aggregate_data()
