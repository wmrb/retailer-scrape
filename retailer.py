from selenium import webdriver
from itertools import islice
import time, random

def write_csv_output_header(retailer_name, csvWriter):

    # Write retailer-specific header rows in Excel output file
    if (retailer_name == 'costco'):

        # write the Costco header row in the Excel output file
        csvWriter.writerow([
            'Costco Item Number / Search Term',
            'Price'
        ])

    elif (retailer_name == 'lowes'):

        # write the Lowe's header row in the Excel output file
        csvWriter.writerow([
            'Lowes Item Number / Search Term',
            'Price'
        ])

    elif (retailer_name == 'overstock'):

        # write the Overstock header row in the Excel output file
        csvWriter.writerow([
            'Overstock Item Number / Search Term',
            'Price'
        ])

    elif (retailer_name == 'sams'):

        # write the Sam's header row in the Excel output file
        csvWriter.writerow([
            'Sams Item Number / Search Term',
            'Price'
        ])

    
    elif (retailer_name == 'target'):

        # write the Target header row in the Excel output file
        csvWriter.writerow([
            'Target Item Number / Search Term',
            'Price',
            'Sold Out?'            
        ])

    elif (retailer_name == 'walmart'):

        # write the Walmart header row in the Excel output file
        csvWriter.writerow([
            'Search Term',
            'Product Title',
            'Price',
            'Sold By',
            'Walmart Number'
        ])


def scrape_site(retailer_name, csvReader, csvWriter, options, start_range, end_range):

    user_agent_list = [
    #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    #Firefox
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)'
    ]
    user_agent = random.choice(user_agent_list)
    
    # for each row in the input file, go to retailer's website search url for the Item Number in question,
    # find the text within proper class/x-path, and save/write it to the output file

    count = 0

    try:
        
        while True: # see below - this for loop will continue until 

            for row in islice(csvReader,int(start_range)-1,None): 

                options.add_argument(f'user-agent={user_agent}')
                        
                # launch new instance of Chrome with selenium - could use .Firefox() if desired
                # need to make sure to have chromedriver.exe (Chrome) or geckodriver.exe (Firefox) in same folder as this script
                print(options)
                browser = webdriver.Chrome(chrome_options=options)
                browser.implicitly_wait(5) # Sets the timeout to implicitly wait for an element to be found or a command to complete.
                browser.set_page_load_timeout(30) # added 3/5/19  - Sets the amount of time to wait for a page load to complete before throwing an exception.
                
                # assume item number or other search term is in column A (row[0]) of input file
                itemnumber = row[0]
                
                # print a status update for the user and perform the actual search in the browser instance
                print('\n' + 'Looking for %s...' % (itemnumber))

                if (retailer_name == 'costco'):
                    browser.get('https://www.costco.com/CatalogSearch?dept=All&keyword=' + itemnumber)
                    try:    
                        elem = browser.find_element_by_xpath('//*[@id="math-table"]/div[2]/div/span[1]')
                        print('\n' + 'Found price for ' + itemnumber + ': ' + elem.text)
                        csvWriter.writerow([itemnumber,elem.text])
                    except:
                        print('\n' + 'Could not find price for %s' % (itemnumber))
                        csvWriter.writerow([itemnumber,'Could not find price'])
                
                elif (retailer_name == 'lowes'):
                    browser.get('https://www.lowes.com/search?searchTerm=' + itemnumber)
                    try:    
                        elem = browser.find_element_by_xpath("//span[@itemprop='price']")
                        print('\n' + 'Found price for ' + itemnumber + ': ' + elem.get_attribute('content'))
                        csvWriter.writerow([itemnumber,elem.get_attribute('content')])
                    except:
                        print('\n' + 'Could not find price for %s' % (itemnumber))
                        csvWriter.writerow([itemnumber,'Could not find price'])
                        
                elif (retailer_name == 'overstock'):
                    browser.get('https://www.overstock.com/search?keywords=' + itemnumber)
                    try:
                        elem_oos_found = False;
                        elem_oos = browser.find_element_by_xpath(".//span[@class='message danger out-of-stock-label']")
                        elem_oos_found = True;
                    except:
                        print('\n' + 'No out of stock message')
                    try:    
                        elem = browser.find_element_by_xpath(".//span[@class='monetary-price-value']")
                        print('\n' + 'Found price for ' + itemnumber + ': ' + elem.get_attribute("content"))
                        if (elem_oos_found == False):
                            csvWriter.writerow([itemnumber,elem.get_attribute("content")])
                        elif (elem_oos_found == True):
                            csvWriter.writerow([itemnumber,elem.get_attribute("content"),elem_oos.get_attribute("content")])
                    except:
                        print('\n' + 'Could not find price for %s' % (itemnumber))
                        csvWriter.writerow([itemnumber,'Could not find price'])                    
                
                elif (retailer_name == 'sams'):
                    browser.get('https://www.samsclub.com/sams/search/searchResults.jsp?searchTerm=' + itemnumber)
                    try:    
                        elem = browser.find_element_by_xpath("//span[@class='Price-group']/span[@class='visuallyhidden']")
                        print('\n' + 'Found price for ' + itemnumber + ': ' + elem.text)
                        formatted_text = elem.text.replace('PRICE ','')
                        csvWriter.writerow([itemnumber,formatted_text])
                    except:
                        print('\n' + 'Could not find price for %s' % (itemnumber))
                        csvWriter.writerow([itemnumber,'Could not find price'])


                #################################################################
                ####################                         ####################
                ####################   T A R G E T . C O M   ####################
                ####################                         ####################
                #################################################################
                        
                            
                elif (retailer_name == 'target'):

                    rowdata = [itemnumber]
                    # print('rowdata: ')
                    # print(*rowdata)

                    try:
                        
                        browser.get('https://www.target.com/s?searchTerm=' + itemnumber)

                        # if the page loads, try to find and click on the first search result:
                        
                        try:

                            elem_search_result = browser.find_element_by_xpath("//a[@data-test='product-title']")

                            elem_search_result.click()
                            
                            # introduce a delay to let the search load before clicking on the result, although browser.implicitly_wait(30) is supposed to handle this so not entirely sure why it seems to help
                            time.sleep(2)
                            

                            try:    

                                elem_product_price = browser.find_element_by_xpath(".//span[@data-test='product-price']")
                                rowdata.append(elem_product_price.text)
                                print('\n' + 'Found price for ' + itemnumber + ': ' + elem_product_price.text)

                            except:

                                elem_product_price.text = ""
                                rowdata.append(elem_product_price.text)
                                print('\n' + 'Could not find price for %s' % (itemnumber))
                            

                            try:

                                # elem_oos_found = False;
                                # elem_oos = browser.find_element_by_xpath(".//span[@class='h-text-orangeDark']")
                                # elem_oos_found = True;
                                
                                elem_oos = browser.find_element_by_xpath(".//span[@class='h-text-orangeDark']")
                                rowdata.append(elem_oos.text)
                                print('\n' + 'Found Out of Stock text for ' + itemnumber + ': ' + elem_oos.text)

                            except:
                                
                                elem_oos = ""
                                rowdata.append(elem_oos)
                                print('\n' + 'Item appears to be in stock')


                            csvWriter.writerow(rowdata)
                            rowdata=[]

                            
                        # Exception for elem_search_result.click():

                        except:
                            
                            if ("no results found" in browser.page_source):
                                    
                                rowdata.append("No results")

                            else:

                                rowdata.append("Unknown error")

                            print('\n' + 'No results or other error for %s' % (itemnumber))

                            csvWriter.writerow(rowdata)


                    # Exception for initial .get() page load:
                    
                    except:

                        print('\n' + 'Page did not load within 15 seconds for: %s' % (itemnumber))
                        rowdata.append("Page did not load within 15 seconds")
                        csvWriter.writerow(rowdata)
                        
                #################################################################
                #################################################################
                ###############      end of target.com block      ###############
                #################################################################
                #################################################################
                        
                #################################################################
                ####################                         ####################
                ####################  W A L M A R T . C O M  ####################
                ####################                         ####################
                #################################################################
                        
                elif (retailer_name == 'walmart'):

                    rowdata = [itemnumber]
                    # print('rowdata: ')
                    # print(*rowdata)   
                    
                    try:

                        browser.get('https://www.walmart.com/search/?query=' + itemnumber)

                        # if the page loads, try to find and click on the first search result:
                    
                        try:    

                            # test_page_loaded = True
                            
                            elem_search_result = browser.find_element_by_xpath("//div[@class='search-result-productimage listview']")

                            elem_search_result.click()
                            # introduce a delay to let the search load before clicking on the result, although browser.implicitly_wait(30) is supposed to handle this so not entirely sure why it seems to help:
                            time.sleep(2)

                            # test_search_result_clicked = True


                            try:

                                elem_title = browser.find_element_by_xpath("//h1[@class='prod-ProductTitle no-margin font-normal heading-a']")
                                rowdata.append(elem_title.get_attribute('content'))
                                print('\n' + 'Found Product Title for ' + itemnumber + ': ' + elem_title.get_attribute('content'))

                            except:
                                
                                elem_title = "Could not find Product Title"
                                rowdata.append(elem_title)
                                print('\n' + 'Could not find Product Title for ' + itemnumber)
                                

                            try:    

                                elem_price = browser.find_element_by_xpath(".//span[@class='price-characteristic']")
                                rowdata.append(elem_price.get_attribute('content'))
                                print('\n' + 'Found Price for ' + itemnumber + ': ' + elem_price.get_attribute('content'))
                                
                            except:
                                
                                elem_price = "Could not find Price"
                                rowdata.append(elem_price)
                                print('\n' + 'Could not find Price for ' + itemnumber)

                                
                            try:

                                elem_seller = browser.find_element_by_xpath(".//a[@class='seller-name']")
                                rowdata.append(elem_seller.text)
                                print('\n' + 'Found Sold By for ' + itemnumber + ': ' + elem_seller.text)
                                
                            except:

                                elem_seller = "Could not find Sold By"
                                rowdata.append(elem_seller)
                                print('\n' + 'Could not find Sold By for ' + itemnumber)


                            try:                           
                            
                                elem_walmart_number = browser.find_element_by_xpath(".//div[@class='valign-middle secondary-info-margin-right copy-mini display-inline-block wm-item-number']")
                                elem_walmart_number_text = elem_walmart_number.get_attribute('aria-label').replace("Walmart Number: ","")
                                rowdata.append(elem_walmart_number_text)
                                print('\n' + 'Found Walmart Number for ' + itemnumber + ': ' + elem_walmart_number_text)
                                
                            except:

                                elem_walmart_number = "Could not find Walmart Number"
                                rowdata.append(elem_walmart_number)
                                print('\n' + 'Could not find Walmart Number for ' + itemnumber)
                            
                           
                            csvWriter.writerow(rowdata)
                            rowdata=[]


                        # Exception for elem_search_result.click():

                        except:
                            
                            if (browser.find_element_by_xpath("//span[@class='zero-results-message message active message-warning message-block']")):
                                    
                                rowdata.append("No results")

                            else:

                                rowdata.append("Unknown error")

                            print('\n' + 'No results or other error for %s' % (itemnumber))

                            csvWriter.writerow(rowdata)


                    # Exception for initial .get() page load:
                    
                    except:

                        print('\n' + 'Page did not load within 15 seconds for: %s' % (itemnumber))
                        rowdata.append("Page did not load within 15 seconds")
                        csvWriter.writerow(rowdata)

                #################################################################
                #################################################################
                ###############     end of walmart.com block      ###############
                #################################################################
                #################################################################
  

                # introduce another delay to avoid querying the site too quickly, although this seems to run slowly enough that it might not matter:
                time.sleep(random.randint(1,5))

                # close this browser instance so we don't end up with a bunch of open browser windows to close after this script runs
                browser.quit()

                # go to next row in input file on next time through for loop
                count = count + 1

                print(count)
                print(end_range)
                print(start_range)
                
                if count == ((int(end_range) - int(start_range)) + 1):

                    return count

            return count

    except KeyboardInterrupt:

        return count

    return count
