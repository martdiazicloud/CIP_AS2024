"""\
Title: "Rice Lidl Web Scraping "
by Fátima Barcina Arias (CIP_Group:03)
Date: 07.11.204

website: https://www.lidl.ch
"""


import csv
import re
import time
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


def get_data_from_selenium(driver):
    url = "https://www.lidl.ch/"
    driver.get(url)
    time.sleep(4)  # Wait for 4 seconds to allow the page to load

    # Handle cookie consent or other popups (if present)
    try:
        cookie_button = driver.find_element(By.XPATH, "//button[text() = 'Zustimmen']")
        cookie_button.click()
        time.sleep(2)  # Wait for the popup to close
    except:
        print("No cookie consent popup found")

    driver.switch_to.window(driver.window_handles[0]) # Ensure remain in the correct window after closing cookies popup

    # Find and click the "Sortiment" link
    link_section = driver.find_elements(By.LINK_TEXT, 'Sortiment')
    # If it is found, just click on it
    if link_section is not None and link_section != []:
        link_section[0].click()
    # If not (window width maybe too small and responsiveness hide it) just get it from sitemap at the bottom
    else:
        # special way to do click, as in a narrow window not only sortiment is hidden, but also the "scroll-up"
        # button can overlay the deployable clickable button for the sitemap
        sortiment_section = driver.find_element(By.XPATH,
                                      '//*[@id="__nuxt"]/div[2]/div/div[3]/footer/div[3]/div/div[1]/div[1]/label/img')
        driver.execute_script("arguments[0].click();", sortiment_section)
        time.sleep(1)
        link_section = driver.find_elements(By.LINK_TEXT, 'Sortiment')
        link_section[0].click()

    time.sleep(4) # Wait until Sortiment loads
    driver.switch_to.window(driver.window_handles[0]) # Ensure remain in the correct window

    # Find and click the "Pasta & Reis" link
    pasta_reis_link = driver.find_element(By.XPATH, '//*[@id="maincontent"]/div[4]/div/div[2]/div/div/article[10]/a')
    driver.execute_script("arguments[0].click();", pasta_reis_link)
    time.sleep(4)

    driver.switch_to.window(driver.window_handles[0])  # Ensure remain in the correct window

    # Find and click the "Rice" link
    link_rice = driver.find_element(By.XPATH, "//*[@id='narrow-by-list']/div[1]/div[2]/ul/li[16]/ul/li[2]/a")
    # If the link exists, then click on it
    if link_rice is not None and link_rice != []:
        driver.execute_script("arguments[0].click();", link_rice)
    # If it does not exist, then go to filter and click on Reis filter
    else:
        filter_button = driver.find_element(By.XPATH, '/html/body/div[2]/main/div[2]/div[2]/div/div[1]/div[1]/button')
        filter_button.click()
        time.sleep(4)
        # And now click on Reis doing the same as before
        driver.switch_to.window(driver.window_handles[0])
        link_rice = driver.find_element(By.XPATH, '//*[@id="narrow-by-list"]/div[1]/div[2]/ul/li[16]/ul/li[2]/a')
        driver.execute_script("arguments[0].click();", link_rice)

    time.sleep(4) # Wait until it loads

    driver.switch_to.window(driver.window_handles[0])  # Ensure remain in the correct window
    html_page = driver.page_source
    soup = BeautifulSoup(html_page, 'lxml')
    return soup


def scrap_products(soup, driver):
    pattern = r'(\d+\.?\d*)\s?(\w+)'  #regular expression for measurements or quantities
    products_to_return = []
    counter = 1  # for ID
    scraping_date = datetime.now().strftime("%d/%m/%Y")  # Get scraping date format dd/mm/yyyy

    products_from_selenium = soup.find_all('div', class_='product details product-item-details')
    for product in products_from_selenium:

        #Get product link:
        product_link = product.find('a')['href']

        # Get product page in Selenium in order to obtain the brand
        driver.get(product_link)
        time.sleep(4)  # Wait for 4 seconds to allow the page to load
        html_product_page = driver.page_source
        specific_product_soup = BeautifulSoup(html_product_page, 'lxml')
        brand = specific_product_soup.find('p', class_='brand-name').text

        # Get the remaining item details from product
        description = product.find('strong', class_='product name product-item-name').text.strip()
        #prepartion_time = product.find('div', class_='product description product-item-description').text.strip()
        weight_and_unit = product.find('span', class_='pricefield__footer').text.strip()
        weight_and_unit = weight_and_unit.split('|')[0].replace('pro ', '').replace(',','.').strip()
        weight_and_unit_split = re.match(pattern, weight_and_unit)
        weight = float(weight_and_unit_split.group(1).strip())
        weight = f"{weight:.2f}"
        unit = weight_and_unit_split.group(2).strip()


        if unit.__contains__('x'): #  Fix for cases as 8x125g (Special case)
            unit = unit.split('x')[1].strip()
            weight_and_unit_special = re.match(pattern, unit)
            weight = float(weight) * float(weight_and_unit_special.group(1).strip())
            weight = f"{weight:.2f}"
            unit = weight_and_unit_special.group(2).strip()


        price = float(
            product.find('strong', class_='pricefield__price').text.replace('–', '0').replace('*CHF', '').strip())
        discount_element = product.find('span', class_='pricefield__header')
        if discount_element is not None:
            discount = discount_element.text.replace('-', '').replace(' ', '').strip()
        else:
            discount = 'No Discount'

        products_to_return.append({
            'ID': counter,
            'competitor': 'Lidl',
            'category': 'Rice',
            'description': description,
            'brand': brand,
            'price': price,
            'weight': weight,
            'unit': unit,
            'discount': discount,
            'product_link': product_link,
            'scrapping_date': scraping_date


        })
        counter += 1  # Increment the counter after each product for ID

    return products_to_return


def main():
    csv_file = "RiceOfLidl.csv"
    driver = webdriver.Chrome()  # Start the Selenium WebDriver
    soup = get_data_from_selenium(driver)  # Get the parsed HTML content from the webpage
    product_list = scrap_products(soup, driver)  # Scrape the product details
    # Write the scraped product details into a CSV file
    with open(csv_file, 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file)
        # Write the CSV headers
        writer.writerow(
            ['ID', 'Competitor', 'Category', 'Description', 'Brand', 'Price', 'Grammage', 'Unit','Discount',
             'Product Link',  'Scraping Date' ])  # Write CSV headers
        for product in product_list:
            writer.writerow(product.values())  ## Write each product's details to a row
    # Print the result
    print(f"\n.- Scrapped url: {driver.current_url}")
    print(f"\n.- {len(product_list)} products added in {csv_file}")
    print("\nProgram finished")
    driver.quit()  # Close the browser


if __name__ == '__main__':
    main()

