# import required modules
import sys, os, requests, csv, time, shutil
from datetime import date
from datetime import datetime
from selenium.webdriver.chrome.options import Options
import retailer

VERSION = '0.1'
retailers = ['costco', 'lowes', 'overstock', 'sams', 'target', 'walmart']

start_range = '0'
end_range = '0'
run_all_rows = False

if (len(sys.argv)<3):
    print('Too few arguments.  Syntax is: python retailer-scrape.py [RETAILER] X-Y|all')
    print('where [RETAILER] is one of: ')
    print(*retailers, sep=', ')
    print('and X-Y|[all] is a range of rows to run, such as 1-100, or the word all to run all rows')
    sys.exit()
elif (len(sys.argv)>3):
    print('Too many arguments.  Syntax is: python retailer-scrape.py [RETAILER] X-Y|all')
    print('where [RETAILER] is one of: ')
    print(*retailers, sep=', ')
    print('and X-Y|[all] is a range of rows to run, such as 1-100, or the word all to run all rows')
    sys.exit()
    
if sys.argv[2] == 'all':
    run_all_rows = True
    start_range = '1' 
elif '-' in sys.argv[2]:
    start_range, end_range = sys.argv[2].split('-')
    if start_range == '':
        start_range = '0'
    if end_range == '':
        end_range = '0'
else:
    print('Argument 2 must be a range of rows to run, such as 1-100, or the word all to run all rows')
    sys.exit()

print(start_range)
print(end_range)
print(run_all_rows)
print(sys.argv[2])
print(start_range != '0')
print(end_range != '0')
print(sys.argv[2] != 'all')

if ((len(sys.argv)==3) and (sys.argv[1] not in retailers) and ( (sys.argv[2] == 'all') or ( (start_range != '0') and (end_range != '0') ) ) ):
    print('Argument 1 must match one of the following retailers: ')
    print(*retailers, sep=', ')
    sys.exit()
elif ((len(sys.argv)==3) and (sys.argv[1] not in retailers) and (sys.argv[2] != 'all') and (start_range != '0') and (end_range !='0')):
    print('Argument 1 must match one of the following retailers: ')
    print(*retailers, sep=', ')
    print('Argument 2 must be a range of rows to run, such as 1-100, or the word all to run all rows')
    sys.exit()
elif ((len(sys.argv)==3) and (sys.argv[1] in retailers) and (sys.argv[2] != 'all') and ( (start_range == '0') or (end_range == '0'))):
    print('Argument 2 must be a range of rows to run, such as 1-100, or the word all to run all rows')
    sys.exit()
elif ((len(sys.argv)==3) and (sys.argv[1] in retailers) and ( (sys.argv[2] == 'all') or ( (start_range != '0') and (end_range !='0') ) ) ):
    print('PASS')
    retailer_name = sys.argv[1]
else:
    print('Unknown error.')
    sys.exit()

# print the time so we can calculate approximately how long this is taking to run
print('\n' + 'Start time: ')
startDateTime = datetime.now()
print(startDateTime)

# process input file name
csvInput = 'input-' + retailer_name + '.csv'

try:
    # use the start time to rename the input file
    shutil.copyfile('input-' + retailer_name + '.csv', 'input-'+ retailer_name + '-' + startDateTime.strftime('%Y%m%d') + '-' + startDateTime.strftime('%H%M%S') + '.csv')
    # os.rename(csvInput, 'input-'+ retailer_name + '-' + startDateTime.strftime('%Y%m%d') + '-' + startDateTime.strftime('%H%M%S') + '.csv')
    csvInput = 'input-'+ retailer_name + '-' + startDateTime.strftime('%Y%m%d') + '-' + startDateTime.strftime('%H%M%S') + '.csv'
except FileNotFoundError:
    print('\n' + 'ERROR: Could not find CSV input file named \"input-' + retailer_name + '.csv\"')
    print('in same directory as this script')
    sys.exit()
 

# define output file name
csvOutput = 'output-'+ retailer_name + '-' + startDateTime.strftime('%Y%m%d') + '-' + startDateTime.strftime('%H%M%S') + '.csv'

# prepare options object to pass to browser (to specify user agent)
options = Options()

# open input file in read-only mode to count rows
try:
    csvInputFileObj = open(csvInput, 'r')
    csvReader = csv.reader(csvInputFileObj)
    global input_row_count
    input_row_count = sum(1 for row in csvReader)
    csvInputFileObj.close()
except FileNotFoundError:
    print('\n' + 'ERROR 1: Could not open input file')
    sys.exit()

print('\n' + 'retailer-scrape.py: Version ' + VERSION)
print('\n' + 'Activated for ' + retailer_name)
print('\n' + 'Input file found.')

# open input file again in read-only mode (list of Item Numbers or whatever the search term will be should be in Column A, no header) to start reading data
try:
    csvInputFileObj = open(csvInput, 'r')
    csvReader = csv.reader(csvInputFileObj)
except FileNotFoundError:
    print('\n' + 'ERROR 2: Could not open input file')
    sys.exit()

# open output file in read/write mode
csvOutputFileObj = open(csvOutput, 'w', newline='')
csvWriter = csv.writer(csvOutputFileObj)
print('\n' + 'Output file ready.')

# update the shell/console with a status message to indicate we've made it past the file open stage and will be launching browser activities
print('\n' + 'Attempting to launch browser and connect to website...')

#### jump to retailer module/function ### pass csvWriter, csvReader, ...?
retailer.write_csv_output_header(retailer_name, csvWriter)
count = retailer.scrape_site(retailer_name, csvReader, csvWriter, options, start_range, end_range)

# print the time so we and calculate how long this is taking to run
print('\n' + 'End time: ')
endTime = datetime.now().time()
print(endTime)
startTime = startDateTime.time()
print('\n' + 'Total time: ')
totalTime = datetime.combine(date.min, endTime) - datetime.combine(date.min, startTime)
print(totalTime)
print('\n' + 'Number of items:')
print(count)
print('\n' + 'Seconds per item: ')
print(totalTime/count)

# open log file in read/write mode
OutputLog = 'log-'+ retailer_name + '-' + startDateTime.strftime('%Y%m%d') + '-' + startDateTime.strftime('%H%M%S') + '.txt'
OutputFileObj2 = open(OutputLog, 'w')
OutputFileObj2.write('Start time: %s \n' % startTime)
OutputFileObj2.write('End time: %s \n' % endTime)
OutputFileObj2.write('Total time: %s \n' % totalTime)
OutputFileObj2.write('Number of items: %s \n' % count)
# OutputFileObj2.write('Seconds per item: %s \n' % totalTime/count)
OutputFileObj2.close()
print('\n' + 'Log file saved.')


# close the input and output files                        
csvOutputFileObj.close()
csvInputFileObj.close()

# rename the output file with the current date and time
# endDateTime = datetime.now()
# os.rename(csvOutput, 'output-'+ retailer_name + '-' + endDateTime.strftime('%Y%m%d') + '-' + endDateTime.strftime('%H%M%S') + '.csv')
