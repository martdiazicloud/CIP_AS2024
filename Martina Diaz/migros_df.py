'''
Author: Martina Diaz
Title: Data frame of 'Pasta-sauce' category products from Migros website

The script aims at scraping a list of features for all the product in the Migros website that belong
to the category Pasta sauces and Pesto.

The following script is divided in 4 parts:
0. Importing packages
1. Importing the data frame
2. Cleaning and formatting the data frame
3. Exporting the data frame
'''

# 0 - IMPORTING PACKAGES
import pandas as pd
import numpy as np

# 1 - IMPORTING THE DATAFRAME
df_import = pd.read_csv('migros.csv')
df = pd.DataFrame(df_import)

# 2 - Cleaning and formatting the data

## 2.1 Cleaning 'Regula_Price (CHF)' column and set float format
df['Regular_Price (CHF)'] = df['Regular_Price (CHF)'].map(lambda x: x.replace('–','00')) # cleaning
df['Regular_Price (CHF)'] = df['Regular_Price (CHF)'].astype(float).fillna(0.00) # float format

## 2.2 Cleaning Grammage column
df['Unit'] = df['Unit'].map(lambda x: x.replace('x',''))

## 2.3 Formatting 'Discount' and calculating 'Actual_Price'
'''The following phases are needed to make the calculation of the 'Actual Price'
for each product according to the discount active for the products at the date
of the scraping'''

### 2.3 - Step 1: Replace "no discount" with 1.0 (no discount effect) and remove % for calculations
df['Discount'] = df['Discount'].replace('no discount', '100%')  # Make "no discount" 100%
df['Discount'] = df['Discount'].str.replace('%', '').astype(float) / 100  # Convert to decimal format

### 2.3 - Step 2: Calculate "Actual_Price (CHF)" based on "Discount" percentage
df['Actual_Price (CHF)'] = np.where(
    df['Discount'] == 1.0,                 # Condition: no discount
    df['Regular_Price (CHF)'],             # Then: set to regular price
    df['Regular_Price (CHF)'] * (1 - df['Discount']))  # Else: apply discount

df['Actual_Price (CHF)'] = df['Actual_Price (CHF)'].round(2) # Round the result to 2 decimal places

### 2.3 - Step 3: Replace 1.0 in 'Discount' with 'no discount'
df.loc[df['Discount'] == 1.0, 'Discount'] = 'no discount'


## 2.4 Manual correction for Brand with case-insensitive replacement
'''This step is necessary because some Brands are composed of more than 1 word
and have been split in the process of web scraping'''

df['Brand'].replace(to_replace="(?i)la", value="La Molisana", regex=True, inplace=True)
df['Brand'].replace(to_replace="(?i)bon", value="Bon Chef", regex=True, inplace=True)
df['Brand'].replace(to_replace="(?i)aus", value="Aus der Region", regex=True, inplace=True)
df['Brand'].replace(to_replace="(?i)da", value="Da Emilio", regex=True, inplace=True)

# 3 - Exporting the data frame
print(df.to_string()) # Visualize the data frame
df.to_csv('/Users/diazm/Documents/HSLU/05_AS2024/CIP/project/migros_cleaned.csv', index=False)
