from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime, time, timedelta
import time
from random import randrange
import csv

def get_event_row(columns, extract_to_date):
        columns = row.find_all("td")

        #extract the event_id, useful for future deep scraping
        event_id = columns[0].find("input")
        event_id = str(event_id)
        sizem = len(event_id)
        loc_value = event_id.find('value')
        event_id = event_id[loc_value: sizem-1]
        event_id = event_id[event_id.find('"')+1:]
        event_id = event_id[:event_id.find('"')]
                
        magnitude = columns[1].find(text=True)
        datetime = columns[2].find(text=True)
        
        #control for stop scraping
        current_year = datetime[0:4]
        current_month = datetime[5:7]
        if (extract_to_date == current_year + '-' + current_month):
            event_id = '-break'

        latitude = columns[3].find(text=True)
        longitude = columns[4].find(text=True)
        region = columns[5].find(text=True)
        depth = columns[6].find(text=True)
        auth = columns[7].find(text=True)
        seismic_event=[event_id,magnitude,datetime,latitude,longitude,region,depth,auth]

        return seismic_event

def create_csv_file(event_list, extract_to_date):
    current_date = datetime.now()
    name_csv = str(current_date.year) + '-' + str(current_date.month) + '_' + extract_to_date + '.csv'
    name_csv = 'seismic_events_' + name_csv
    events_counter = 0

    with open(name_csv, 'w') as csvfile:
        filewriter = csv.writer(csvfile)
        for seismic_event in event_list:
            filewriter.writerow(seismic_event)
            events_counter = events_counter + 1
    return events_counter

#main 

#geckodriver is required and must be in PATH
browser = webdriver.Firefox()

#open target URL
browser.get('http://www.seismicportal.eu/')

dropdown = browser.find_element_by_xpath("//select/option[text()= 'Show 100 per page']")
dropdown.click()

browser.forward()

#get the HTML soup
soup = BeautifulSoup(browser.page_source, 'html5lib')

#extract data last year from current month
extract_to_date = '2018-08'#not included
keep_extracting = True
event_list=[]
#add headers to event_list
seismic_event=['Event ID', 'Magnitude','Datetime UTC','Latitude','Longitude','Region','Depth(KM', 'Auth']
event_list.append(seismic_event)

while keep_extracting:

    table = soup.find("table")
    tbody = table.find("tbody")
    rows = tbody.find_all("tr")

    for row in rows:

        columns = row.find_all("td")

        seismic_event = get_event_row(columns,extract_to_date) #getting data of current seismic event
        event_list.append(seismic_event)
        print (seismic_event)
        if (seismic_event[0] == '-break'):
            keep_extracting = False
            break
        
        
    browser.implicitly_wait(4)
    browser.find_element_by_link_text("Next »").click()        
    time.sleep(randrange(5,6))
    browser.forward()        
    soup = BeautifulSoup(browser.page_source, 'html5lib')       

number_events = create_csv_file(event_list, extract_to_date)      
print('Task finished, ' + str(number_events) + ' seismic events succesfully scraped')
