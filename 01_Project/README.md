### IMPORTANT

<b>THE PARQUET FILE IS NOT IN THE DIRECTORY SINCE IT IS TOO LARGE TO STORE ON GITHUB.</b>

It stores the record of taxi data. To run the code you will need to download Yellow Taxi's Trip Records for January 2024 (It's a Parquet file).
You can do this at https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page.
Keep the file in the same directory as the notebook.


### Project Overview: Taxi Patterns in New York City

This project focuses on analyzing taxi data in New York City to uncover key patterns and insights.
By examining various aspects such as peak times, airport fees,
and busy days, the project aims to provide a comprehensive understanding of taxi operations and passenger behavior.


Additionally, the project uses Parquet files instead traditional CSV files.
Since they are more efficient for large volumes of data, I had to figure out how to process them.

### Files

The code is contained in the "01_Project.ipynb" file

To read it in an easy way try using the PDF version.


The taxi_zone_lookup.csv file is a csv table that correlates to LocationID in the Parquet file.










