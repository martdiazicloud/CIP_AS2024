# importing
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

#### 0 - FUNCTIONS
''' the new_page_driver Function allows to navigate to the next web page'''
def new_page_driver():
    actions = ActionChains(driver)
    actions.click(next_page)
    actions.perform()
    url = driver.current_url
    driver.get(url)
    time.sleep(5)

''' the get_url Function allows to get the html structure of a web page and to store all the products links in a list'''
def get_url():
    page = driver.page_source  # extract page source and put in the memory --> possible to search the class we need
    soup = BeautifulSoup(page, 'html.parser')

    # find url within BeautifulSoup
    konserven = soup.find_all("a", class_="product-item-link")

    # Extract the URL from the tag
    for i in konserven:
        url = i['href']
        if url not in lista_url:
            lista_url.append(url)
    return lista_url

#### 1- GET URL OF PRODUCTS FOR INDIVIDUAL SCRAPING
# inizialize list of url
lista_url = []

### 1.1 From sortiment 'Konserven'
url = 'https://sortiment.lidl.ch/de/konserven#/'

# request approach & html with webdriver
# page 1
driver = webdriver.Chrome()  # browser to render the dynamic content
driver.get(url)
time.sleep(5)
# by pass cookies
cookie_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Zustimmen')]")))
cookie_button.click()
time.sleep(2)
# scrapping url
get_url()

# page 2
next_page = driver.find_element(By.XPATH, "//*[@id='maincontent']/div[2]/div[1]/button[2]")
new_page_driver()
get_url()

# page 3
next_page = driver.find_element(By.XPATH, "//*[@id='maincontent']/div[2]/div[1]/button[3]")
new_page_driver()
get_url()

# page 4
next_page = driver.find_element(By.XPATH, "//*[@id='maincontent']/div[2]/div[1]/button[4]")
new_page_driver()
get_url()

# page 5
next_page = driver.find_element(By.XPATH, "//*[@id='maincontent']/div[2]/div[1]/button[5]")
new_page_driver()
get_url()

# page 6
next_page = driver.find_element(By.XPATH, "//*[@id='maincontent']/div[2]/div[1]/button[6]")
new_page_driver()
get_url()

driver.quit()

### 1.2 From sortiment 'Saucen'
url = 'https://sortiment.lidl.ch/de/gewurze-ole/saucen'

# request approach & html with webdriver
# page 1
driver = webdriver.Chrome()  # browser to render the dynamic content
driver.get(url)
time.sleep(5)
# by pass cookies
cookie_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Zustimmen')]")))
cookie_button.click()
time.sleep(2)
# scrapping url
get_url()

# page 2
next_page = driver.find_element(By.XPATH, "//*[@id='maincontent']/div[2]/div[1]/button[2]")
new_page_driver()
get_url()

# page 3
next_page = driver.find_element(By.XPATH, "//*[@id='maincontent']/div[2]/div[1]/button[3]")
new_page_driver()
get_url()

driver.quit()

#### 2 - SCRAPING
# consider only url of Tomaten, sauces and Pesto
filtered_lista_url = [item for item in lista_url if 'omaten' in item or 'esto' in item or 'auce' in item]
filtered_lista_url

##### 2.1 - Initialize lists
lista_description = []
lista_title = []
lista_price = []
lista_brand = []
lista_grammage = []
lista_discount = []
date_scrapping = []
lista_unit = []

##### 2.2 - Individual scraping
for i in filtered_lista_url:
    driver = webdriver.Chrome()  # browser to render the dynamic content
    driver.get(i)

    # by pass cookies
    cookie_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Zustimmen')]")))
    cookie_button.click()
    time.sleep(2)

    # extract titles
    title_frame = driver.find_element(By.CLASS_NAME, 'base')
    if title_frame:
         title = title_frame.text
    lista_title.append(title)

    # extract descriptions
    description_frame = driver.find_elements(By.XPATH, '//*[@id="tab-description"]/div/div/p')
    if description_frame:
        description = description_frame[0].text.strip()
        lista_description.append(description)

    # extract prices
    price_frame = driver.find_element(By.CLASS_NAME, 'pricefield__price')
    if price_frame:
         price = price_frame.get_attribute('content')
         lista_price.append(price)

    # extract brand
    try:
        # Try to find the element with the class 'brand-name'
        brand_frame = driver.find_element(By.CLASS_NAME, 'brand-name')
        brand = brand_frame.text.strip()
    except NoSuchElementException:
        # If the element is not found, handle the exception
        brand = "not defined"
    lista_brand.append(brand)

    # extract grammage
    grammage_frame = driver.find_element(By.CLASS_NAME, 'pricefield__footer')
    if grammage_frame:
        grammage = grammage_frame.text.strip()
        if 'ml' in grammage:
            unit = 'ml'
        else:
            unit = 'g'
    else:
        grammage = "not defined"

    lista_grammage.append(grammage)
    lista_unit.append(unit)

    # extract discount
    try:
        # Try to find the element with discount
        discount_frame = driver.find_element(By.XPATH,
                                             '//*[@id="maincontent"]/div[3]/div/div[1]/div[1]/div[1]/div[2]/div[3]/span/span[1]/span/strong/span[2]/span/sup')
        discount = discount_frame.text.strip()
    except NoSuchElementException:
        # If the element is not found, handle the exception
        discount = "no discount"
    lista_discount.append(discount)

    # attach date scrapping
    current_date = datetime.now().strftime("%Y-%m-%d")
    date_scrapping.append(current_date)

driver.quit

# In the list 'Discount' replace '*' with 'no discount' in the whole list
for j in range(len(lista_discount)):
    if lista_discount[j] == '*':
        lista_discount[j] = 'no discount'


##### 3 - LIDL DATA FRAME
df_lidl = pd.DataFrame({"ID": [None] * len(filtered_lista_url)})
df_lidl["Competitor"] = "lidl"
df_lidl["Category"] = "Pasta Sauces"
df_lidl.insert(3, "Product_Description", lista_title)
df_lidl.insert(4, "Brand", lista_brand)
df_lidl.insert(5, "Regular_Price (CHF)", lista_price)
df_lidl.insert(6, "Grammage", lista_grammage)
df_lidl.insert(6, "Unit", lista_unit)
df_lidl.insert(7, "Link", filtered_lista_url)
df_lidl.insert(8, "Scraping_Date", date_scrapping)
df_lidl.insert(9, "Discount", lista_discount)

# 4 - EXPORTING
print(df_lidl)

df_lidl.to_csv('/Users/diazm/Documents/HSLU/05_AS2024/CIP/project/lidl.csv', index=False)