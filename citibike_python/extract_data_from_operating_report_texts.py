import calendar
import csv
import string
import re


def collect_data_from_operating_reports():

    """Collects data from operating report text files

    Will generate a csv with the following information (header then data):
        date        stations    bicycles    miles
        (YYYY-MM)   (int)       (int)       (float)

    NOTE: Missing information will be represented as "NULL"

    Returns:
         Nothing
    """

    target = "../data/operating_reports/text_files/"
    output_path = "../data/workspace/citibike_operating_reports_data.csv"

    with open(output_path, "w", newline='') as output_file:

        writer = csv.writer(output_file)

        # header
        writer.writerow(['date', 'stations', 'bicycles', 'miles'])

        # operating reports from July 2013 to December 2017
        for year in range(2013, 2018):
            for month in range(1, 13):

                # start at July 2013
                if year == 2013 and month < 7:
                    continue

                # date_format_a example:            2017_01_January
                # date_format_standard example:     2017-01
                date_format_a = str(year) + "_" + '{:02d}'.format(month) + "_" + calendar.month_name[month]
                date_format_standard = str(year) + "-" + '{:02d}'.format(month)
                file_name = target + date_format_a + ".txt"

                # extract data and write content
                content = extract_text_contents(file_name)
                writer.writerow([date_format_standard] + content)

                print(date_format_a, "done")


def extract_text_contents(file_name):

    """Extracts data from operating report text files

    Will return an array with the following information:
        stations    bicycles    miles
        (int)       (int)       (float)

    NOTE: Missing information will be represented as "NULL"

    Returns:
         Nothing
    """

    with open(file_name, 'r', encoding="utf8") as text_file:

        # extract text, clean up spacing, ignore content in parentheses or brackets
        content = text_file.read()
        content = content.replace("\n", "")
        content = re.sub("[\(\[].*?[\)\]]", "", content)

        # str.maketrans() and translate() are used to remove punctuations
        #translator = str.maketrans('', '', string.punctuation)
        #content = content.translate(translator)
        # ^above code left unused to preserve the period in a floating point value

        # split by white space and remove punctuation from right of a word
        words = content.split()
        words = [word.rstrip(string.punctuation) for word in words]

        # find number of active stations using "____ active" pattern
        stations_indices = [i for i, word in enumerate(words) if word == "active"]
        stations = "NULL"
        for stations_index in stations_indices:
            stations = words[stations_index - 1]
            temp = words[stations_index - 1]
            try:
                # less than 1000 stations as of end of 2017
                if int(temp.replace(',', '')) < 1000:
                    stations = int(temp.replace(',', ''))
                    break
            except ValueError:
                pass

        # find number of bicycles available/used
        try:
            # attempt to get number of bicycles using "average fleet size was ____" pattern
            fleet_index = content.index("average fleet size was ") + 23
            new_content = content[fleet_index:]
            bicycles = new_content.split(' ')[0].rstrip(string.punctuation)
            bicycles = int(bicycles.replace(',', ''))

        except ValueError:

            try:
                # attempt to get number of bicycles using "average bike fleet last month was ____" pattern
                fleet_index = content.index("average bike fleet last month was ") + 34
                new_content = content[fleet_index:]
                bicycles = new_content.split(' ')[0]
                bicycles = int(bicycles.replace(',', ''))

            except ValueError:

                # get number of bicycles using "____ bicycles" and "bikes was ____" patterns

                # indices to check
                bicycles_indices = [i for i, word in enumerate(words) if word == "bicycles"]
                bikes_indices = [i for i, word in enumerate(words) if word == "bikes"]

                # find any valid values for "____ bicycles"
                bicycles = 0
                for bicycles_index in bicycles_indices:
                    temp = words[bicycles_index - 1]
                    try:
                        # between 3000 to 15000 as of end of 2017
                        if 3000 < int(temp.replace(',', '')) < 15000:
                            bicycles = int(temp.replace(',', ''))
                            break
                    except ValueError:
                        pass

                # find any valid values for "bikes was ____"
                bikes = 0
                for bikes_index in bikes_indices:
                    temp = words[bikes_index + 2]
                    try:
                        # between 3000 to 15000 as of end of 2017
                        if 3000 < int(temp.replace(',', '')) < 15000:
                            bikes = int(temp.replace(',', ''))
                            break
                    except ValueError:
                        pass

                if not bicycles or 0 < bikes <= bicycles:
                    bicycles = bikes

                if bikes == 0 and bicycles == 0:
                    bicycles = "NULL"

        # find number of miles travelled
        try:
            miles_index = words.index("miles")
            miles = words[miles_index - 1]
            miles = float(miles.replace(',', ''))
        except:
            miles = "NULL"

        return [stations, bicycles, miles]


if __name__ == "__main__":
    collect_data_from_operating_reports()
