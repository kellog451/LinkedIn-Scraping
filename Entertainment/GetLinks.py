# ------------------------------------------------------------------#
# ------ Getting All Australian Company LinkedIn Account Links -----#
# ------------------------------------------------------------------#
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from time import sleep
from random import randint
from IPython.core.display import clear_output

# specifies the path to the chromedriver.exe
driver = webdriver.Chrome('/Users/imaki/Desktop/chromedriver')


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


login()

"""driver.get('https://www.linkedin.com/search/results/companies/?companyHqGeo=%5B%22101452733%22%5D&industry=%5B%2219'
           '%22%5D&keywords=fashion&origin=FACETED_SEARCH')"""

driver.get('https://www.linkedin.com/search/results/companies/?companyHqGeo=%5B%22100506852%22%5D&industry=%5B%2228'
           '%22%5D&keywords=australia&origin=FACETED_SEARCH')

thepage = driver.page_source

soup = BeautifulSoup(thepage, 'lxml')

# Define Lists.
Company_links = []

# get main container
main_div = soup.find('ul', class_='reusable-search__entity-results-list list-style-none')

# get each company container
company_item = main_div.findAll('li', class_='reusable-search__result-container')

if company_item is not None:
    # loop to get all links
    i = 0
    while i < len(company_item):
        link_ID = company_item[i].find('a', class_='app-aware-link')['href']
        Company_links.append(link_ID)
        # increment counter
        i += 1
else:
    print("What!!!!!!!!!!")

# Preparing variables to monitor loop
start_time = time.time()
num_of_requests = 0


page = 2
while page < 20:
    # get the url
    pg = str(page)

    url = 'https://www.linkedin.com/search/results/companies/?companyHqGeo=%5B%22100506852%22%5D&industry=%5B%2228%22' \
          '%5D&keywords=australia&origin=FACETED_SEARCH&page=' + pg + ' '

    # Control loop by ↓
    # Pause the loop by random secs to simulate human behavior.
    sleep(randint(8, 15))

    driver.get(url)
    the_new_page = driver.page_source

    # Monitor the num_of_requests
    num_of_requests += 1
    elapsed_time = time.time() - start_time
    print('Request:{}; Frequency: {} num_of_requests/s'.format(num_of_requests, num_of_requests / elapsed_time))
    clear_output(wait=True)

    soup2 = BeautifulSoup(the_new_page, 'lxml')

    # get main div
    main_div = soup2.find('ul', class_='reusable-search__entity-results-list list-style-none')

    # get each company container
    company_item = main_div.findAll('li', class_='reusable-search__result-container')

    if company_item is not None:
        # loop to get all links
        i = 0
        while i < len(company_item):
            link_ID = company_item[i].find('a', class_='app-aware-link')['href']
            Company_links.append(link_ID)
            # increment counter
            print(link_ID)
            i += 1
    else:
        print("What!!!!!!!!!!")

    page += 1

import pandas as pd

companies = pd.DataFrame({
    'Company LinkedIn': Company_links
})

print(companies)

# companies.to_csv('companyLinks.csv')
companies.to_csv('Extracted_csv/EntLinks2.csv', mode='a', header=None, index=None)
