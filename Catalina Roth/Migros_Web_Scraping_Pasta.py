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

#######################################################################
##################         WEB SCRAPING PART         ##################
#######################################################################

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

#######################################################################
##################         CLEANING DATA PART        ##################
#######################################################################

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Open CSV file
df_migros = pd.read_csv("~/Desktop/Migros_Scraping_Pasta.csv", encoding='utf-8')
print(df_migros.head())

# Create DataFrame df_migros_cleaned
df_migros_cleaned = df_migros.copy()

# Functions for cleaning data

# Function to clean Price column
def clean_price(df):
    df['Regular Price (CH)'] = (df['Regular Price (CH)']
                                .str.replace('–', '', regex=False)
                                .str.replace('â€“', '', regex=False)
                                .astype(float))

    df['Actual Price (CH)'] = (df['Actual Price (CH)']
                                .str.replace('–', '', regex=False)
                                .str.replace('â€“', '', regex=False)
                                .astype(float))
    return df

# Function to clean Product Description
def clean_product_description(df):
    df['Product_Description'] = (df['Product_Description'].str.replace('Ã¤', 'Ä', regex=False)
                                 .str.replace('Â', '', regex=False))
    return df

# Function to clean Grammage
def clean_grammage(df):
    df['Grammage'] = (df['Grammage'].str.replace('k', '', regex=False)
                      .astype(int))

    # Update Unit column to 'k' where Grammage was originally '1k'
    df.loc[df['Grammage'] == 1, 'Unit'] = 'k'
    return df

# Call clean_price function to clean the columns of the dataset
clean_price(df_migros_cleaned)

# Call clean_product_description function to clean the columns of the dataset
clean_product_description(df_migros_cleaned)

# Call clean_grammage function to clean the columns of the dataset
clean_grammage(df_migros_cleaned)

# Calculate the Discount %
df_migros_cleaned['Discount'] = (
    ((df_migros_cleaned['Regular Price (CH)'] - df_migros_cleaned['Actual Price (CH)'])
     / df_migros_cleaned['Regular Price (CH)']) * 100
).round(0).astype(int).astype(str) + '%'

# Arrange order of columns
df_migros_cleaned = df_migros_cleaned[['ID', 'Competitor', 'Category', 'Product_Description', 'Brand', 'Regular Price (CH)',
                               'Grammage', 'Unit', 'Link', 'Scraping_Date', 'Discount', 'Actual Price (CH)']]

# Rename columns
df_migros_cleaned = df_migros_cleaned.rename(columns={'Regular Price (CH)': 'Regular_Price (CH)',
                                                      'Actual Price (CH)': 'Actual_Price (CH)'})

###################################################################################
##################         EXPLORATORY DATA ANALYSIS PART        ##################
###################################################################################

# Look for Missing Values and data Type
df_migros_cleaned.info()

''' CREATE BOXPLOT TO DETECT OUTLIERS '''

# Numerical variables
vars = ['Regular_Price (CH)', 'Actual_Price (CH)']

# Set up subplots
fig, axes = plt.subplots(1, 2, figsize=(8, 5))

# Flatten axes array into 1D for easy iteration
axes = axes.flatten()

# Plot a boxplot for each numerical variable
for i, var in enumerate(vars):
    sns.boxplot(data=df_migros_cleaned, y=var, ax=axes[i], palette='coolwarm')

# Add main title
plt.suptitle('Boxplots for Price Variables', fontsize=13, y=1.02)

# Display plot
plt.show()

###################################################################################
##################        CREATE COLUMN OF INTEREST        #########################
###################################################################################

''' A Column named " Private Label Product" is created in order to compare its price with third brands'''

df_label_brand = ['M-Classic', 'Migros Bio']
df_migros_cleaned['Private_Label_Product'] = df_migros_cleaned['Brand'].apply(lambda x: 'Yes' if x in df_label_brand else 'No')

# Save to CSV
df_migros_cleaned.to_csv("~/Desktop/Migros_Cleaned_Pasta.csv", index = False)



