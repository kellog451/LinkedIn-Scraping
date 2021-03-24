import csv
import urllib.request
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import requests
import _warnings
from time import sleep
from random import randint
from warnings import warn
from IPython.core.display import clear_output

# specifies the path to the chromedriver.exe

driver = webdriver.Chrome('/Users/imaki/Desktop/x88/chromedriver')
# ('/Users/imaki/Desktop/chromedriver')
# ('/Users/imaki/Desktop/x87/chromedriver')

with open('Extracted_csv/BankingLinks.csv') as f:
    reader = csv.reader(f)
    data = list(reader)

LinkArray = []

# add about to the links to target about page.
for list in data:
    for number in list:
        x = str(number) + 'about/'
        LinkArray.append(x)


# login method from LinkedLinks file.
def login():
    theurl = 'https://www.linkedin.com/checkpoint/rm/sign-in-another-account?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin'

    # driver.get method() will navigate to a page given by the URL address
    driver.get(theurl)

    # locate email form by_class_name
    username = driver.find_element_by_id('username')

    # send_keys() to simulate key strokes
    username.send_keys('imakitm@gmail.com')

    # locate password form by_class_name
    password = driver.find_element_by_id('password')

    # send_keys() to simulate key strokes
    password.send_keys('cSavEz37XEDrgQ5')

    # locate submit button by_xpath
    log_in_button = driver.find_element_by_xpath('//*[@type="submit"]')

    # .click() to mimic button click
    log_in_button.click()


login()  # login to linkedIn

# Define Company Data Lists.
Company_Names = []
Websites = []
Phones = []
Industry = []
Company_Size = []
HQs = []
Company_Type = []
Founded = []
Specialties = []
Location = []

# Preparing the monitoring of the loop
start_time = time.time()
num_of_requests = 0

num_of_links = 901

while num_of_links < 1000:

    # Control loop by ↓
    # Pause the loop by random secs to simulate human behavior.

    sleep(randint(5, 10))

    driver.get(LinkArray[num_of_links])
    thepage = driver.page_source

    # Monitor the num_of_requests
    num_of_requests += 1
    elapsed_time = time.time() - start_time
    print('Request:{}; Frequency: {} num_of_requests/s'.format(num_of_requests, num_of_requests / elapsed_time))
    clear_output(wait=True)

    # parse html page.
    soup = BeautifulSoup(thepage, 'lxml')

    # get the main div containing the data you need by id
    main_container = soup.find('section', class_='artdeco-card p4 mb3')

    # print(main_container)
    # two title class options, check for either
    main_title_check = soup.find('h1', class_='org-top-card-summary__title t-24 t-black t-bold truncate')
    main_title_check2 = soup.find('h1', class_='org-top-card-summary__title t-24 t-black truncate')

    if main_title_check is not None:
        title_check = main_title_check['title']
        main_title = title_check
        Company_Names.append(main_title)

    if main_title_check2 is not None:
        title_check2 = main_title_check2['title']
        main_title2 = title_check2
        Company_Names.append(main_title2)

    if main_title_check2 is None and main_title_check is None:
        Company_Names.append(" ")

    main_website_links = main_container.find_all('a', class_='link-without-visited-state ember-view')

    main_website_check = main_container.find('a', class_='link-without-visited-state ember-view')

    if main_website_check is not None:
        main_website = main_website_check['href']
        Websites.append(main_website)
    else:
        Websites.append(" ")

    if len(main_website_links) < 2:
        contact = " "
    else:
        contact = main_website_links[-1].find('span', attrs={'dir': 'ltr'}).text

    size_check = main_container.find('dd', class_='org-about-company-module__company-size-definition-text t-14 '
                                                  't-black--light mb1 fl')

    size_check2 = main_container.find('dd', class_='org-about-company-module__company-size-definition-text t-14 '
                                                   't-black--light mb5')

    if size_check is not None:
        size = size_check.text
        Company_Size.append(size.strip())
    elif size_check2 is not None:
        size = size_check2.text
        Company_Size.append(size.strip())
    else:
        Company_Size.append(" ")

    # get all dd html tags
    info = main_container.find_all('dd', class_='org-page-details__definition-text t-14 t-black--light t-normal')
    customArray = [pt.get_text().strip() for pt in info]

    # arrays with possible matches
    type_maybes = ["Privately", "Privately Held", "Public Company", "Held", "Self-Employed", "Educational Institution",
                   "Proprietorship", "Sole Proprietorship", "Nonprofit", "Partnership"]

    hq_maybes = ["Melbourne", "Victoria", "Cairns", "Queensland", "Gold", "Coast", "QLD", "Brisbane", "Sydney",
                 "Canberra", "Armidale", "Ballina", "Balranald", "Batemans Bay", "Bathurst", "Bega", "Bourke",
                 "Bowral", "Broken Hill", "Byron Bay", "Camden", "Campbelltown", "Perth", "Australia", "Larapinta",
                 "Kings Park", "NSW", "Hills", "Laverton", "North", "Victoria", "Adelaide", "SA", "Brisbane", "Mitcham",
                 "Surrey Hills", "Ascot Park", "Baldivis", "WA", "Denmark", "Belrose", "South", "Wales", "NY",
                 "Western Australia", "St Leonards", "Osborne", "HINDMARSH", "Fortitude Valley", "Ingleburn",
                 "Loganholme", "Mount", "Saint", "Thomas", "Caringbah", "Hackham", "Fremantle", "Forrest", "ACT",
                 "Hawthorn", "VIC", "Meadowbrook", "Artarmon", "SUBIACO", "Vic", "Kewdale", "Western Australia",
                 "Mandurah", "Melrose Park", "South Australia", "Belmont", "Burleigh Heads", "Qld", "Malaga", "Garbutt",
                 "Glynde", "Flinders Park", "Craigieburn", "Murarrie", "Cottesloe", "Sydney, NSW", "Utrecht"]

    spec_maybes = ["Banking", "accounting", "accounts", "Training", "banking", "Reporting", "Compliance",
                   "Financial", "Management", "Charities", "Social" "Enterprises", "Governance",
                   "Tax", "Business", "Service",  "Investment", "Reports", "Payment", "Cash", "Accounts",
                   "Payable", "Auditing", "Fee", "Advisory", "Capital", "Planning", "Audit",
                   "Wealth", "Operations", "Lending", "Strategy", "Valuation", "rate", "loans",
                   "Commercial", "Asset", "Finance", "Insurance", "Bankieren"]

    founded_maybes = [str(x) for x in range(1800, 2021)]

    # company details

    Phones.append(contact.strip())
    Industry.append('Banking')

    for x in customArray:
        if any(y in x for y in type_maybes):
            if len(x.split()) < 3:
                hold_type = x
        if any(y in x for y in hq_maybes):
            if x.count(",") + 1 < 4:
                hold_HQs = x
        if any(y in x for y in spec_maybes):
            if not 'http://' in x:
                hold_Spec = x
        if any(y in x for y in founded_maybes):
            if len(x) == 4:
                hold_Year = x

    try:
        Company_Type.append(hold_type)
        hold_type = ""
    except NameError:
        Company_Type.append(" ")

    try:
        HQs.append(hold_HQs)
        hold_HQs = ""
    except NameError:
        HQs.append(" ")

    try:
        if hold_Spec == 'Banking':
            Specialties.append(" ")
            hold_Spec = " "
        else:
            Specialties.append(hold_Spec)
            hold_Spec = " "
    except NameError:
        Specialties.append(" ")

    try:
        Founded.append(hold_Year)
        hold_Year = ""
    except NameError:
        Founded.append(" ")

    location_check = soup.find('p', class_='t-14 t-black--light t-normal break-words')
    # print(location.strip())
    if location_check is not None:
        location = location_check.text
        Location.append(location.strip())
    else:
        Location.append(" ")

    # monitor
    # print(customArray[num_of_links])
    print(LinkArray[num_of_links])
    num_of_links += 1

import pandas as pd

ourdata = pd.DataFrame({
    'Company Name': Company_Names,
    'Website': Websites,
    'Phone': Phones,
    'Industry': Industry,
    'Company Size': Company_Size,
    'HQ': HQs,
    'Type': Company_Type,
    'Founded': Founded,
    'Location': Location,
    'Specialities': Specialties
})

print(ourdata)

ourdata.to_csv("Extracted_csv/BankingData.csv", mode='a', index=False, header=False)
