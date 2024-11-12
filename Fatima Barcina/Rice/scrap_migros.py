
"""\
Title: "Rice Migros Web Scraping "
by Fátima Barcina Arias (CIP_Group:03)
Date: Fall Semester 2024 (November 2024)
"""
from bs4 import BeautifulSoup
import csv
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from datetime import datetime
import re  # To use regular expressions for extracting quantities and units from product details.

def get_data_from_selenium(driver):
    url = "https://www.migros.ch/en"
    driver.get(url)
    time.sleep(5)  # Wait for 5 seconds to allow the page to load

    # Handle cookie consent or other popups (if present)
    try:
        cookie_button = driver.find_element(By.XPATH, "//button[text() = 'Accept all cookies']")
        cookie_button.click()
        time.sleep(2)  # Wait for the popup to close
    except:
        print("No cookie consent popup found")

    driver.switch_to.window(driver.window_handles[0])  # Ensure remain in the correct window after closing cookies popup

    # Find and click the "Pasta, condiments & canned food" link
    link_section = driver.find_elements(By.LINK_TEXT, 'Pasta, condiments & canned food')
    link_section[0].click()
    time.sleep(5)
    # Ensure remain in the correct window
    driver.switch_to.window(driver.window_handles[0])
    # Find and click the "Rice" link
    link_rice = driver.find_elements(By.LINK_TEXT, 'Rice')
    link_rice[0].click()
    time.sleep(5)
    driver.switch_to.window(driver.window_handles[0])  # Ensure remain in the correct window
    # Get the HTML content of the current page
    html_page = driver.page_source
    soup = BeautifulSoup(html_page, 'lxml')  # Parse the HTML with BeautifulSoup and return the parsed object
    return soup

def scrap_products(soup):
    products_to_return = []
    counter = 1  # ID
    pattern = r'(\d+)\s*(kg|g)'
    scraping_date = datetime.now().strftime("%d/%m/%Y")  # Get scraping date format dd/mm/yyyy

    products_from_selenium = soup.find_all('div', class_='show-product-detail')
    for product in products_from_selenium:
        # Check if there is a discount
        discount_element = product.find('span', class_='product-badge badge-promo')
        if discount_element:
            discount = discount_element.find('span', class_='ng-star-inserted').text.strip()
        else:
            discount = 'No Discount'

        # Extract the price
        price_element = None

        # Discounted price (class="actual")
        if discount_element:
            price_element = product.find('span', class_='actual')

        # Normal price (class="actual ng-star-inserted")
        if not price_element:
            price_element = product.find('span', class_='actual ng-star-inserted')

        if price_element:
            price = price_element.text.strip()
            #  Clean the price to remove    unwanted    characters
            price = re.sub(r'[^\d.,]', '', price)  # Remove    any    non - numeric    characters except commas and dots
            price = price.replace(',', '.')  # Convert commas    to    dots    for decimal format consistency
            price = float(price)  # Convert to float to standardize format
            price = f"{price:.2f}"  # Format to two decimal places
        else:
            price = None

        # Extract description (general description concatenated with the particular description with space)
        description = None
        description_parent_div = product.find('span', class_='desc ng-star-inserted')
        description_children = description_parent_div.find_all('span', class_='ng-star-inserted')
        for description_child in description_children:
            if not description:
                description = ""
            description = description + description_child.text.strip() + " "
        if description:
            description = description.strip()

        # Extract brand or set to default if not found
        brand_element = product.find('span', class_='name ng-star-inserted')
        brand = None
        if brand_element:
            brand = brand_element.text.strip()
        # Extract grammage and unit (Weight of package as    ex.: "1 kg" or "500 g")
        grammage_element = product.find('span', class_ = 'weight-priceUnit ng-star-inserted')
        if grammage_element:
            grammage_text = grammage_element.text.lower().strip()
            # Use regular expressions to extract numbers and    units(kg, g, etc.)
            match = re.match(r'%s' % pattern, grammage_text)
            if match:
                grammage = f"{float(match.group(1)):.2f}"  # Extract the number(grammage) and format it with 2 decimal
                unit = match.group(2)  # Extract the unit (kg or g)
            elif grammage_text.__contains__('x'): # Special case: Fix for cases as 8x125g
                    unit = grammage_text.split('x')[1].strip()
                    weight = float(grammage_text.split('x')[0].strip())
                    weight_and_unit_special = re.match(pattern, unit)
                    weight = weight * float(weight_and_unit_special.group(1).strip())
                    grammage = f"{weight:.2f}"
                    unit = weight_and_unit_special.group(2).strip()
            else:
                grammage = 'N/A'
                unit = 'N/A'
        else:
            grammage = 'N/A'
            unit = 'N/A'

        # Extract product link
        product_link_element = product.find('a', href=True)
        if product_link_element:
            base_url = "https://www.migros.ch"  # Assign the    base    URL    of    the    website
            product_link = base_url +  product_link_element['href']  # Build the full URL
        else:
            product_link = None

        # Append extracted data to the list
        products_to_return.append({
            'ID': counter,
            'Competitor': 'Migros',
            'Category': 'Rice',
            'description': description,
            'brand': brand,
            'price(CH)': price,
            'grammage': grammage,
            'unit': unit,
            'product_link': product_link,
            'scraping_date': scraping_date,
            'discount': discount,
        })
        counter += 1  # Increment the counter after each product for ID

    return products_to_return


def main():
    csv_file = "RiceOfMigros.csv"
    driver = webdriver.Chrome()  # Start the Selenium WebDriver
    soup = get_data_from_selenium(driver)  # Get the parsed HTML content from the webpage
    product_list = scrap_products(soup)  # Scrape the product details

    # Write the scraped product details into a CSV file
    with open(csv_file, 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file)
        # Write the CSV headers
        writer.writerow(['ID', 'Competitor', 'Category',
                         'Description', 'Brand', 'Price', 'Grammage', 'Unit', 'Product Link', 'Scraping Date', 'Discount']) # Write CSV headers
        for product in product_list:
            writer.writerow(product.values()) ## Write each product's details to a row

    # Print the result
    print(f"\n.- Scrapped url: {driver.current_url}")
    print(f"\n.- {len(product_list)} products added in {csv_file}")
    print("\nProgram finished")

    driver.quit() # Close the browser


if __name__ == '__main__':
    main()