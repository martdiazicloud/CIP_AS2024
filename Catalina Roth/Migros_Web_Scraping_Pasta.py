# Import necessary packages
from selenium import webdriver                                      # To control and interact with web browser
from selenium.webdriver.chrome.service import Service               # To manage the ChromeDriver
from webdriver_manager.chrome import ChromeDriverManager            # Installation for the ChromeDriver
from selenium.webdriver.common.by import By                         # Allows locating elements on the web page
from selenium.webdriver.support.ui import WebDriverWait             # Set explicit wait times
from selenium.webdriver.support import expected_conditions as EC    # Used with WebDriverWait to specify conditions
from selenium.webdriver.chrome.options import Options               # Setting options for the Chrome browser
import os                                                           # Locate the desktop path
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import time
import random


''' Functions for data cleaning and grammage extraction'''

# Function to clean the product description
def clean_product(product_description):
    cleaned_text = product_description.replace('Â·', '').replace('·', '').strip()
    return cleaned_text

# Function to extract the unit measurement from the grammage
def extract_unit_measurement(grammage):
    return grammage[-1:]  # For example: Kg, g

# Function to extract the value measurement from the grammage
def extract_value_measurement(grammage):
    return grammage[:-1]  # For example: 500, 400

# Set up options for ChromeDriver
options = Options()

# Initialize ChromeDriver
try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    print("ChromeDriver installed and browser opened.")
except Exception as e:
    print(f"Error initializing ChromeDriver: {e}")

# Initialize WebDriverWait (10 seconds)
wait = WebDriverWait(driver, 10)

# Go directly to the pasta section
pasta_section_url = 'https://www.migros.ch/en/category/pasta-condiments-canned-food/pasta-rice-semolina-grain/pasta'
driver.get(pasta_section_url)
print("Navigating to Migros pasta section.")

# Wait for the product elements to be loaded
try:
    wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="name ng-star-inserted"]')))
    print("Product elements loaded successfully.")
except Exception as e:
    print(f"Error loading product elements: {e}")

# Click on the "See all products" button if it is available
try:
    see_all_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//div[@class="zoomer seatbelt ng-star-inserted"]')))
    see_all_button.click()
    print("Clicked the 'See all products' button.")
except Exception as e:
    print(f"Error clicking the 'See all products' button: {e}")

# Initialize an empty list to store all product data
product_data = []

# Get the current date
current_date = datetime.now().strftime('%Y-%m-%d')

# Loop to extract all products on the page
while True:
    # Wait for the product elements to be loaded
    wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="name ng-star-inserted"]')))

    # Extract brands using BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    brands_elements = soup.find_all('span', class_='name ng-star-inserted')
    product_brands = [brand.text for brand in brands_elements]

    # Loop through the products on the current page
    product_elements = driver.find_elements(By.XPATH, '//span[@class="name ng-star-inserted"]')

    for i in range(len(product_elements)):
        # Ensure the index is within range
        if i >= len(product_elements):
            print(f"Index {i} is out of range for product_elements.")
            break

        # Find all products_elements again to ensure an up-to-date list of elements
        product_elements = driver.find_elements(By.XPATH, '//span[@class="name ng-star-inserted"]')
        if i < len(product_elements):  # Ensure the index is within range
            product_element = product_elements[i]

            # Scroll into view to ensure that the current product is visible in the browser window
            driver.execute_script("arguments[0].scrollIntoView();", product_element)

            # Click on the product
            try:
                driver.execute_script("arguments[0].click();", product_element)
                print(f"Clicked on product {i + 1}: {product_brands[i]}")

                # Wait for product details to be loaded
                wait.until(EC.presence_of_element_located(
                    (By.XPATH, '//h1[contains(@id,"product-detail") and contains(@class,"ng-star-inserted")]')))

                # Extract product details
                product_name = driver.find_element(By.XPATH, '//h1[contains(@id,"product-detail") and contains(@class,"ng-star-inserted")]').text
                actual_price = driver.find_element(By.XPATH, '//span[@class="actual"]').text
                regular_price = driver.find_element(By.XPATH, "//span[@data-cy[contains(., 'original-price')]]").text
                product_grammage = driver.find_element(By.XPATH, '//span[@class="weight-priceUnit product-detail"]').text
                product_link = driver.current_url

                # Extract the value of the grammage with the function above
                weight_value = extract_value_measurement(product_grammage)

                # Extract unit measurement with the function above
                unit_measurement = extract_unit_measurement(product_grammage)

                # Clean the name of the description's product
                product_name = clean_product(product_name)

                # Store product data
                product_data.append({
                    'ID': len(product_data) + 1,
                    'Competitor': 'Migros',
                    'Category': 'Pasta',
                    'Product_Description': product_name,
                    'Brand': product_brands[i],
                    'Actual Price (CH)': actual_price,
                    'Regular Price (CH)': regular_price,
                    'Grammage': weight_value,
                    'Unit': unit_measurement,
                    'Link': product_link,
                    'Scraping_Date': current_date
                })

            except Exception as e:
                print(f"Error extracting details for product {i + 1}: {e}")

            # Return to the product listing
            driver.get(pasta_section_url)

            # Wait for product details to be loaded
            wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="name ng-star-inserted"]')))
        else:
            print(f"Unable to fetch product element at index {i}.")
            break

        # Random delay to avoid getting blocked
        time.sleep(random.uniform(1, 3))

    # Check if there is a "Next" button to load more products
    try:
        next_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="next"]')))
        if "disabled" in next_button.get_attribute("class"):
            print("No more products to load.")
            break
        next_button.click()
        print("Clicked the 'Next' button to load more products.")
    except Exception as e:
        print(f"Error clicking the 'Next' button: {e}")
        break

# Convert to DataFrame and save
df_migros = pd.DataFrame(product_data)
desktop_path = os.path.expanduser("~/Desktop/Migros_Scraping_Pasta.csv")
df_migros.to_csv(desktop_path, index=False)

print("Scraping completed!.")
print(df_migros)

# Close the browser
driver.quit()

