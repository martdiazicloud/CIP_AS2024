'''
Author: Martina Diaz
Title: "pasta_sauces_dataframes.py"
Description: Data frame of 'Pasta-sauce' category products from Lidl and Migros websites

This script aims at merge the data frames obtained by scraping Lidl and Migros websites.
It contains all products found in the two competitors' webpages under the categories 'pasta sauces' and 'pesto'.
The final output is a dataframe exported in "csv" format ready to be merged with other product categories
scraped by the other group members to answer the research questions:
Which supermarket has the most competitive prices?
Which competitor offers more brand across distinct categories?
How much more expensive are own brands compared to traditional brands for each competitor?

The following script is divided in 4 parts:
0. Importing packages
1. Importing the data frame
2. Cleaning and formatting the data frame
3. Exporting the data frame
'''

# 0 - IMPORTING PACKAGES
import pandas as pd
import numpy as np
import os
import re

# 1 - IMPORTING THE DATAFRAMES

## 1.1 Define file path and extension of file to import
path = '/Users/diazm/Documents/HSLU/05_AS2024/CIP/project'
extension = '.csv'

## 1.2 Create a list of CSV File Names available in the directory
'''It will fetch the data frames exported by the webscraping processes'''
files = [file for file in os.listdir(path) if file.endswith(extension)]

## 1.3 Import CSV files into Pandas
dfs = []
for file in files:
    df = pd.read_csv(os.path.join(path, file))
    dfs.append(df)

## 1.4 Concatenate the Data Frames into one
df = pd.concat(dfs, ignore_index=True)
type(df)

# 2 - CLEANING AND FORMATTING THE DATA FRAME

## 2.1 Delete ID column
df.drop(columns=['ID'])

## 2.2 Cleaning Grammage and Unit column
'''In these columns there are different format of strings.
The following operations have the goal to extract the quantity of a unit for each product, reporting it under "Grammage",
and to set the values of "Unit" to "g" and "ml" according to the product unit measurements.'''

for i in range(len(df)):
    # regex to extract the grammage from strings like "pro 265g | 100g = 0.67 CHF"
    if df.loc[i, 'Competitor'] == 'lidl':
        match = re.search(r'pro (\d+)(?:g|ml)', df.loc[i, 'Grammage'])
        if match:
            df.loc[i, 'Grammage'] = match.group(1)
    # regex to extract the grammage from strings like "2x700ml | 1L = 4.28 CHF"
    if df.loc[i, 'Competitor'] == 'lidl':
        match = re.search(r'(\d+)x(\d+)(?:g|ml)', df.loc[i, 'Grammage'])
        if match:
            quantity = int(match.group(1))
            per_unit = int(match.group(2))
            total_grammage = quantity * per_unit
            df.loc[i, 'Grammage'] = total_grammage
    # Cleaning cases with gx
    if df.loc[i, 'Unit'] != 'g' and df.loc[i, 'Unit'] != 'ml':
        df.loc[i, 'Unit'] = 'g'

## 2.3 Formatting 'Discount' and calculating 'Actual_Price'
'''The following phases are needed to make the calculation of the Actual Price
for each product according to the discount active for the products at the date
of the scraping.'''

## 2.3.1 Replace "no discount" with 1.0 (no discount effect) and convert discount percentages into decimal factors
df['Discount'] = df['Discount'].replace('no discount', '100%').astype(str).str.replace('%', '', regex=False)
df['Discount'] = pd.to_numeric(df['Discount'], errors='coerce')/100

## 2.3.2 Cleanin 'Regular Price' values
df['Regular_Price (CHF)'] = pd.to_numeric(df['Regular_Price (CHF)']
                                           .astype(str)
                                           .str.replace('–', '00', regex=False),
                                           errors='coerce').fillna(0.00)

## 2.3.3 Calculate "Actual_Price (CHF)" based on "Discount" percentage
df['Actual_Price (CHF)'] = np.where(
    df['Discount'] == 1.0,                 # Condition: no discount
    df['Regular_Price (CHF)'],             # Then: set to regular price
    df['Regular_Price (CHF)'] * (1 - df['Discount']))  # Else: apply discount

df['Actual_Price (CHF)'] = df['Actual_Price (CHF)'].round(2)  # Round the result to 2 decimal places

df.loc[df['Discount'] == 1.0, 'Discount'] = 'no discount'  # Restore '1.0' with 'no discount'

## 2.3.4 Deleting products that not correspond to "pasta sauce" or "pesto"
keywords = ['Braten', 'Sriracha', 'Heinz', 'Thomy', 'Bohnen', 'Chili', 'Soja', 'Knorr']  # List of keywords to filter out
pattern = '|'.join(keywords)  # Matches any of the keywords
df = df[~df['Product_Description'].str.contains(pattern, case=False, na=False)]  # Filter out rows

## 2.3.5 Manual correction for "Brand" values with case-insensitive replacement
'''This step is necessary because some Brand labels that are composed of more than one word
have been split in the webscraping process leading to incomplete Brand names.
Once selected the cases to correct, a regex for case-insensitive (?i) and fixed start ^ and end $ 
of the string is used to avoid affecting other Brands that contains the same sequence of characters.'''

brand_replacements = {
    "(?i)^la$": "La Molisana",
    "(?i)^bon$": "Bon Chef",
    "(?i)^aus$": "Aus der Region",
    "(?i)^da$": "Da Emilio",
}

df['Brand'].replace(to_replace=brand_replacements, regex=True, inplace=True)


# 3 - EXPORTING THE DATAFRAME
''' It is important to save the data frame in "csv" format in a subfolder to avoid importing
it when running this script again, since it will import or "csv" files available in the directory selected
at the beginning of this script.'''

print(df.to_string())  # Visualize the data frame for final check
df.to_csv('/Users/diazm/Documents/HSLU/05_AS2024/CIP/project/merged_dfs/pasta_sauces_merged.csv', index=False)  #save