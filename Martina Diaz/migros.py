'''
Author: Martina Diaz
Title: migros.py
Description: Web scraping Pasta sauces products from Migros website

The script aims at scraping a list of features for all the product in the Migros website that belong
to the category "Pasta Sauces".

The following script is divided in 4 parts:
0. IMPORTING PACKAGES
1. GENERAL FUNCTIONS
2. URL LIST OF ALL PRODUCTS
3. INDIVIDUAL PRODUCT SCRAPING
4. DATA FRAME

The main principle of this script's structure is to provide an example of generalised functions
to scrape the products.

Warning: due to change in the website pages this script might not work.
'''


############################################
# 0 - IMPORTING PACKAGES
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import datetime


############################################
# 1 - GENERAL FUNCTIONS

# new_page_driver()
''' the new_page_driver Function allows to navigate to the next web page'''
def new_page_driver():
    actions = ActionChains(driver)
    actions.click(next_page)
    actions.perform()
    url = driver.current_url
    driver.get(url)
    time.sleep(5)

# get_url()
''' the get_url Function allows to get the html structure of a web page and to store all the products links in a list'''
def get_url():
    page = driver.page_source  # extract page source and put in the memory --> possible to search the class we need
    soup = BeautifulSoup(page, 'html.parser')

    # find url within BeautifulSoup
    konserven = soup.find_all("a", class_="product-show-details mdc-button mat-mdc-button mat-unthemed mat-mdc-button-base")

    # Extract the URL and price from the tag
    for i in konserven:
        url = i['href']
        if url not in lista_url:
            lista_url.append(url)
    return lista_url


############################################
# 2 - URL LIST OF ALL PRODUCTS

# 2.1 inizialize a list to collect the urls of each product
lista_url = []

# 2.2 Access to the sortiment 'Pasta saucen und pestos' on the website
url = 'https://www.migros.ch/de/category/pasta-wurzmittel-konserven/gewurze-saucen/pastasaucen-pestos'

# 2.3 request approach & html with webdriver
driver = webdriver.Chrome()  # browser to render the dynamic content
driver.get(url)
time.sleep(5)
get_url() # scrapping url

print(lista_url)
len(lista_url)

# 2.4 complete the url for each product
lista_url_complete=[]
for j in lista_url:
    url_complete = 'https://www.migros.ch/' + j
    lista_url_complete.append(url_complete)

lista_url_complete

# splitting the  list into chunks
'''due to the website settings and issues related to the IP address,
to avoid be blocked and end up in a maintenance-page announcement,
the list of all urls is split into chunks of maximum 10 items'''
lista_url_complete_select1 = lista_url_complete[0:10]
lista_url_complete_select2 = lista_url_complete[10:20]
lista_url_complete_select3 = lista_url_complete[20:30]
lista_url_complete_select4 = lista_url_complete[30:40]
lista_url_complete_select5 = lista_url_complete[40:50]
lista_url_complete_select6 = lista_url_complete[50:60]
lista_url_complete_select7 = lista_url_complete[60:70]
lista_url_complete_select8 = lista_url_complete[70:80]
lista_url_complete_select9 = lista_url_complete[80::]


############################################
# 3 - INDIVIDUAL PRODUCT SCRAPING

# 3.1 - Initialize lists to collect data
lista_description = []
lista_title = []
lista_price = []
lista_brand = []
lista_grammage = []
lista_discount = []
date_scraping = []
lista_unit = []

# 3.2 Unique function for data scraping
'''the function called 'partial_scrape' allows to extract the title, the brand, the price, the grammage,
the unit, the discount and the date of the scraping activity'''
def partial_scrape(lista):
    for i in lista:
        driver = webdriver.Chrome()  # browser to render the dynamic content
        driver.get(i)

        # extract Product_Description and Brand
        title_frame = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.TAG_NAME, 'h1')))
        if title_frame:
            title_complete = title_frame.text
            words = title_complete.split()
            # extract Brand (is the first word of the title of the item)
            brand = words[0]
            # extract Product_Description (is part of the title of the item)
            title_raw = ' '.join(words)
            title = title_raw.replace("· ","")

        lista_title.append(title)
        lista_brand.append(brand)

        # extract the regular price
        try:
            price_frame = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'actual')))
            price = price_frame.text.strip()
        except NoSuchElementException:
            # If the price is not found, handle the exception
            price = "not found"

        lista_price.append(price)

        # extract Grammage
        grammage_frame = driver.find_element(By.CSS_SELECTOR, "span.weight-priceUnit.product-detail")
        if grammage_frame:
            grammage_complete = grammage_frame.text.strip()
            words_g = grammage_complete.split()
            # extract Unit (is the last character)
            unit = ''.join([char for char in grammage_complete if char.isalpha()])
            # extract Grammage
            grammage = ''.join([char for char in grammage_complete if char.isdigit()])
        else:
            grammage = "not defined"
            unit = "not defined"

        lista_grammage.append(grammage)
        lista_unit.append(unit)

        # extract Discount
        try:
            discount_frame = driver.find_element(By.CSS_SELECTOR,
                                                 '#badge-PERCENTAGE_PROMOTION > span > span')
            discount = discount_frame.text.strip()
        except NoSuchElementException:
            # If the element is not found, handle the exception
            discount = "no discount"
        lista_discount.append(discount)

        current_date = datetime.now().strftime("%Y-%m-%d")
        date_scraping.append(current_date)

        driver.quit()

    return len(lista_title), len(lista_title)

# 3.2 Products scraping through function "partial_scrape"
'''due to the website setting, the individual scraping needs to be operated for maxium 10 items at time
to avoid be blocked and end up in a maintenance-page announcement'''

part1 = partial_scrape(lista_url_complete_select1)
part2 = partial_scrape(lista_url_complete_select2)
part3 = partial_scrape(lista_url_complete_select3)
part4 = partial_scrape(lista_url_complete_select4)
part5 = partial_scrape(lista_url_complete_select5)
part6 = partial_scrape(lista_url_complete_select6)
part7 = partial_scrape(lista_url_complete_select7)
part8 = partial_scrape(lista_url_complete_select8)
part9 = partial_scrape(lista_url_complete_select9)


############################################
# 4 DATA FRAME
'''creation of the data frame, insertion of the scraped data and export into .csv file'''

# 4.1 Uploading data into the data frame
df_migros = pd.DataFrame({"ID": range(len(lista_title))})  # creating the data frame
df_migros["Competitor"] = "Mirgos"  # a unique value for the Competitor
df_migros["Category"] = "Pasta Sauces"  # a unique value for the Category

# extracting the values of the other fields from the lists
df_migros.insert(3, "Product_Description", lista_title)
df_migros.insert(4, "Brand", lista_brand)
df_migros.insert(5, "Regular_Price (CHF)", lista_price)
df_migros.insert(6, "Grammage", lista_grammage)
df_migros.insert(7, "Unit", lista_unit)
df_migros.insert(8, "Link", lista_url_complete)
df_migros.insert(9, "Scraping_Date", date_scraping)
df_migros.insert(10, "Discount", lista_discount)

# 4.2 Exporting the database into csv file
df_migros.to_csv('/Users/diazm/Documents/HSLU/05_AS2024/CIP/project/migros.csv', index=False)





