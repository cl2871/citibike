import calendar
import urllib.request


def retrieve_operating_reports():

    """Retrieves Citibike operating reports

    Will save pdf files in target path.
    Several will have to be manually downloaded (see below).

    # April 2016:
    # "https://drive.google.com/file/d/0Bxxodixj2nQ_VnJjLUFiSWZuNHJzRUFTQS1laGNSZl9ZM2U0/view"
    # May 2016:
    # "https://drive.google.com/file/d/0Bxxodixj2nQ_ZlJ1aWp6TWVQQm5WdHFLa2lmZll4S0tselRF/view"
    # July 2016
    # "https://drive.google.com/file/d/0BzE9-ar20jzmVlBXNFdoRjFHelU/view"
    # August 2016
    # "https://drive.google.com/file/d/0BzE9-ar20jzmdEh1NHJvSnhlenc/view"
    # September 2016
    # "https://drive.google.com/file/d/0BzE9-ar20jzmZ3dBVGRNVkYzbDA/view"

    Returns:
         Nothing
    """

    target = "../data/operating_reports/pdf_files/"

    # operating reports from July 2013 to December 2017
    for year in range(2013, 2018):
        for month in range(1, 13):

            # start at July 2013
            if year == 2013 and month < 7:
                continue

            # main format used is date_format_a, date_format_b is used for later pdfs but I use date_format_a
            date_format_a = str(year) + "_" + '{:02d}'.format(month) + "_" + calendar.month_name[month]
            date_format_b = calendar.month_name[month] + "-" + str(year)

            # retrieve pdf files, several will need to be manually downloaded

            if year == 2014 and month == 4:
                urllib.request.urlretrieve("https://d21xlh2maitm24.cloudfront.net/nyc/" +
                                           "April-2014-Citi-Bike-Monthly-Report_FINAL.pdf",
                                            target + date_format_a + ".pdf")

            elif year == 2016 and month in [4, 5, 7, 8, 9]:
                # special case, need to manually download, see above
                pass

            elif year < 2016 or year == 2016 and month <= 5:
                urllib.request.urlretrieve("https://s3.amazonaws.com/citibike-regunits/pdf/" + date_format_a
                                       + "_Citi_Bike_Monthly_Report.pdf", target + date_format_a + ".pdf")

            else:
                urllib.request.urlretrieve("https://d21xlh2maitm24.cloudfront.net/nyc/" + date_format_b +
                                           "-Citi-Bike-Monthly-Report.pdf", target + date_format_a + ".pdf")

            print(date_format_a, "done")


if __name__ == "__main__":
    retrieve_operating_reports()
