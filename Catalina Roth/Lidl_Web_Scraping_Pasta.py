# Import necessary packages
from selenium import webdriver
from selenium.webdriver.chrome.service import Service               # To control and interact with web browser
from webdriver_manager.chrome import ChromeDriverManager            # To manage the ChromeDriver
from selenium.webdriver.common.by import By                         # Allows locating elements on the web page
from selenium.webdriver.support.ui import WebDriverWait             # Set explicit wait times
from selenium.webdriver.support import expected_conditions as EC    # Used with WebDriverWait to specify conditions
from selenium.webdriver.chrome.options import Options               # Setting options for the Chrome browser
import os                                                           # Locate the desktop path
from bs4 import BeautifulSoup
import time
import random
from datetime import datetime
import pandas as pd

# Set up options for ChromeDriver
options = Options()

# Initialize ChromeDriver
try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    print("ChromeDriver installed and browser opened.")
except Exception as e:
    print(f"Error initializing ChromeDriver: {e}")

# Initialize WebDriverWait (20 seconds)
wait = WebDriverWait(driver, 20)

# Go directly to the pasta section
pasta_section_url = 'https://sortiment.lidl.ch/de/catalogsearch/result/index/?cat=142&q=pasta'
driver.get(pasta_section_url)
print("Navigating to Lidl pasta section.")

# Handle the cookie consent (ablehnen button)
try:
    # Wait for the products to be loaded
    ablehnen_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Ablehnen')]"))
    )
    ablehnen_button.click()
    print("Clicked the 'Ablehnen' button.")
except Exception as e:
    print(f"Error handling cookie consent: {e}")

# Function to click the "Weitere Produkte laden" button
try:
    # Wait for the products to be loaded
    weitere_produkte_button = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'primary.amscroll-load-button-new')))

    # Scroll into view to ensure that the current product is visible in the browser window
    driver.execute_script("arguments[0].scrollIntoView(true);", weitere_produkte_button)

    # Give the page a moment to load
    time.sleep(1)

    # Click the "Weitere Produkte" button
    weitere_produkte_button.click()
    print("Clicked the 'Weitere Produkte laden' button.")

except Exception as e:
    print(f"Error clicking the 'Weitere Produkte laden' button: {e}")

    # If the above method fails, try using JavaScript to click
    try:
        driver.execute_script("arguments[0].click();", weitere_produkte_button)
        print("Clicked the 'Weitere Produkte laden' button using JavaScript.")
    except Exception as js:
        print(f"Error clicking the 'Weitere Produkte laden' button using JavaScriptS: {js}")

time.sleep(5)

# Initialize an empty list to store all product data
product_data = []

# Get the current date
current_date = datetime.now().strftime('%Y-%m-%d')

# List to collect all products links
product_links = []

while True:
    try:
        # Wait for the product elements to be loaded
        wait.until(EC.presence_of_element_located((By.XPATH, '//li[@class="item product product-item"]')))

        # Loop through the products on the current page
        product_elements = driver.find_elements(By.XPATH, '//li[@class="item product product-item"]')

        # Extract links to product pages
        for product_element in product_elements:
            try:
                product_link_element = product_element.find_element(By.XPATH, './/a[@class="product-item-link"]')
                product_link = product_link_element.get_attribute('href')
                if product_link not in product_links:
                    product_links.append(product_link)
            except Exception as e:
                print(f"Error extracting product link: {e}")

        # Try to click "Weitere Produkte laden" button to load more products
        try:
            # Wait for the product elements to be loaded
            weitere_produkte_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'primary.amscroll-load-button-new')))
            driver.execute_script("arguments[0].click();", weitere_produkte_button)
            time.sleep(5)
        except Exception:
            print("No more products to load.")
            break  # Break the loop if the button is not found
    except Exception as e:
        print(f"Error extracting product links: {e}")
        break

# Visit each product link and extract details
product_counter = 0

for product_link in product_links:
    if product_counter >= 100:  # Stop after scraping 100 products
        break

    try:
        # Get product link
        driver.get(product_link)

        # Wait for the product details page to load
        wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="product-info-main"]')))

        # Extract product details from the product page
        product_name = driver.find_element(By.XPATH, '//h1[@class="page-title"]').text
        regular_price = driver.find_element(By.XPATH, './/strong[@class="pricefield__price"]').text
        product_grammage = driver.find_element(By.XPATH, './/span[@class="pricefield__footer"]').text

        # Find the actual price
        try:
            actual_price = driver.find_element(By.XPATH, ".//div[@class='m-price__price']").text
        except Exception:
            actual_price = regular_price

        # Extract brands using BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        try:
            product_brand_element = soup.find('p', class_='brand-name')
            product_brand = product_brand_element.text if product_brand_element else "Unknown"
        except Exception:
            product_brand = "No Brand"

        # Increment product counter and store product data in a dictionary
        product_counter += 1
        product_data.append({
            'ID': product_counter,
            'Competitor': 'Lidl',
            'Category': 'Pasta',
            'Product_Description': product_name,
            'Product_Brand': product_brand,
            'Product_Grammage': product_grammage,
            'Regular_Price': regular_price,
            'Actual_Price': actual_price,
            'Link': product_link,
            'Scraping_Date': current_date
        })

        print(f'Extracted information from product {product_counter}: {product_name}')

        # Random delay to avoid getting blocked
        time.sleep(random.uniform(1, 3))

    except Exception as e:
        print(f"Error extracting details for product: {e}")

# Convert to DataFrame and save
df_lidl = pd.DataFrame(product_data)
desktop_path = os.path.expanduser("~/Desktop/Lidl_Scraping_2.csv")
df_lidl.to_csv(desktop_path, index=False)

print("Scraping completed!.")
print(df_lidl)

# Close the browser
driver.quit()
