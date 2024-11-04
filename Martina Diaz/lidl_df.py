'''
Author: Martina Diaz
Title: Data frame of 'Pasta-sauce' category products from Lidl website

The script aims at scraping a list of features for all the product in the Lidl website that belong
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
df_import = pd.read_csv('lidl.csv')
df = pd.DataFrame(df_import)

# 2 - Cleaning and formatting the data

## 2.2 Cleaning Grammage column

# Extract the digits before 'g' using regex
df['Grammage'] = df['Grammage'].str.extract(r'pro (\d+)(?:g|ml)')[0]

## 2.3 Formatting 'Discount' and calculating 'Actual_Price'
'''The following phases are needed to make the calculation of the Actual Price
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

# List of keywords to filter out
keywords = ['Braten', 'Sriracha', 'Heinz', 'Thomy', 'Bohnen', 'Chili', 'Soja', 'Knorr']

# Create a regex pattern that matches any of the keywords
pattern = '|'.join(keywords)  # This creates a pattern like 'Braten|Sriracha|Heinz|...'

# Filter out rows where 'Product_Description' contains any of the keywords
df = df[~df['Product_Description'].str.contains(pattern, na=False)]


# 3 - Exporting the data frame
print(df.to_string()) # Visualize the data frame
df.to_csv('/Users/diazm/Documents/HSLU/05_AS2024/CIP/project/lidl_cleaned.csv', index=False)