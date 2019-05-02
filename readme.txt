retailer-scrape.py


RUNNING THE SCRIPT:

from the command line, enter:
python retailer-scrape [SITENAME]

where [SITENAME] is one of the following:
costco
lowes
overstock
sams
target
walmart


DEPENDENCIES:

input.csv is expected in same directory as retailer-scrape.py and is a csv file containing search terms (typically retailer item numbers) in Column A with no header.


OUTPUT: 

An output file containing results will be generated and saved in the same folder as retailer-scrape.py and input.csv and will contain the search terms and other data from the retailer site.  The file name will contain the name of the retailer and the date and time the script finished executing.
