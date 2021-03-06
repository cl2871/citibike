import csv


def find_missing_dates():

    """Find missing dates in the first file compared to a second file.

    Example:
    Discrepancy:  2016-01-27 2016-01-23
    Discrepancy:  2016-01-27 2016-01-24
    Discrepancy:  2016-01-27 2016-01-25
    Discrepancy:  2016-01-27 2016-01-26

    The first file is missing dates for Jan 23, 24, 25, and 26.
    The first and second file will share dates again starting at Jan 27.

    Note: this assumes that the second file has all the dates you need

    Returns:
        Nothing
    """

    missing_dates = []

    path_1 = "../data/workspace/citibike_trips_by_date.csv"
    path_2 = "../data/weather_data/20130701_20171231_clean.csv"

    with open(path_1, "r") as file_1:
        with open(path_2, "r") as file_2:

            reader_1 = csv.reader(file_1)
            reader_2 = csv.reader(file_2)

            # skip headers
            next(reader_1, None)
            next(reader_2, None)

            row_1 = next(reader_1, None)
            row_2 = next(reader_2, None)

            while row_1 is not None and row_2 is not None:

                date_1 = row_1[0]
                date_2 = row_2[0]

                if date_1 != date_2:
                    print("Discrepancy: ", date_1, date_2)
                    missing_dates.append(date_2)
                    row_2 = next(reader_2, None)

                else:
                    row_1 = next(reader_1, None)
                    row_2 = next(reader_2, None)

            print("\nMissing: ", missing_dates)
            print("Total Missing: ", len(missing_dates))

if __name__ == "__main__":
    find_missing_dates()
