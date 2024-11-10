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

Moreover, an additional individual analysis calculates the distance from the average price for the
products in the category "PAsta Sauces". The results are plotted in different format to obtain different insights.

The following script is divided in 4 parts:
0. IMPORTING PACKAGES
1. IMPORTING THE DATA FRAMES
2. CLEANING AND FORMATTING THE DATA FRAMES
3. CALCULATION OF THE DISTANCE FROM AVERAGE PRICE
4. EXPORTING THE DATA FRAMES
5. PLOTS
'''

# 0 - IMPORTING PACKAGES
import pandas as pd
import numpy as np
import os
import re
import matplotlib.pyplot as plt

# 1 - IMPORTING THE DATAFRAMES

# 1.1 Define file path and extension of file to import
path = '/Users/diazm/Documents/HSLU/05_AS2024/CIP/project'
extension = '.csv'

# 1.2 Create a list of CSV File Names available in the directory
'''It will fetch the data frames exported by the webscraping processes'''
files = [file for file in os.listdir(path) if file.endswith(extension)]

# 1.3 Import CSV files into Pandas
dfs = []
for file in files:
    df = pd.read_csv(os.path.join(path, file))
    dfs.append(df)

# 1.4 Concatenate the Data Frames into one
df = pd.concat(dfs, ignore_index=True)
type(df)

# 2 - CLEANING AND FORMATTING THE DATA FRAME

# 2.1 Re-set ID column
df['ID'] = range(len(df))

# 2.2 Cleaning Grammage and Unit column
'''In these columns there are different format of strings.
The following operations have the goal to extract the quantity of a unit for each product, reporting it under "Grammage",
and to set the values of "Unit" to "g" and "ml" according to the product unit measurements.
In the final step g and ml are converted respectively in Kg and L.
Entries where the unit is not specified are dropped from the dataframe.'''

for i in range(len(df)):
    if df.loc[i, 'Competitor'] != 'lidl':
        df.loc[i, 'Competitor'] = 'Migros'
    # regex to extract the grammage from strings like "pro 265g | 100g = 0.67 CHF"
    if df.loc[i, 'Competitor'] == 'lidl':
        match = re.search(r'pro (\d+)(?:g|ml)', df.loc[i, 'Grammage'])
        if match:
            df.loc[i, 'Grammage'] = match.group(1)
    # regex to extract the grammage from multiple packages like "2x700ml | 1L = 4.28 CHF"
    if df.loc[i, 'Competitor'] == 'lidl':
        match = re.search(r'(\d+)x(\d+)(?:g|ml)', df.loc[i, 'Grammage'])
        if match:
            quantity = int(match.group(1))
            per_unit = int(match.group(2))
            total_grammage = quantity * per_unit
            df.loc[i, 'Grammage'] = total_grammage
    # Converting g into Kg and ml in L
    if df.loc[i, 'Unit'] == 'Stück':
        df.drop(df[df['Unit'] == 'Stück'].index, inplace=True)  # eliminate rows without specified unit
    elif df.loc[i, 'Unit'] != 'g' and df.loc[i, 'Unit'] != 'ml' or df.loc[i, 'Unit'] == 'g':
        df.loc[i, 'Unit'] = 'Kg'
    else:
        df.loc[i, 'Unit'] = 'L'

# convert quantities: g in Kg and ml in L
df['Grammage'] = pd.to_numeric(df['Grammage'], errors='coerce')/1000

# 2.3 Formatting 'Discount' and calculating 'Actual_Price'
'''The following steps are needed to make the calculation of the Actual Price
for each product according to the discount active for the products at the date
of the scraping.'''

# 2.3.1 Replace "no discount" with 1.0 (no discount effect) and convert discount percentages into decimal factors
df['Discount'] = df['Discount'].replace('no discount', '100%').astype(str).str.replace('%', '', regex=False)
df['Discount'] = pd.to_numeric(df['Discount'], errors='coerce')/100

# 2.3.2 Cleanin 'Regular Price' values
df['Regular_Price (CHF)'] = pd.to_numeric(df['Regular_Price (CHF)']
                                           .astype(str)
                                           .str.replace('–', '00', regex=False),
                                           errors='coerce').fillna(0.00)

# 2.3.3 Calculate "Actual_Price (CHF)" based on "Discount" percentage
df['Actual_Price (CHF)'] = np.where(
    df['Discount'] == 1.0,                 # Condition: no discount
    df['Regular_Price (CHF)'],             # Then: set to regular price
    df['Regular_Price (CHF)'] * (1 - df['Discount']))  # Else: apply discount

df['Actual_Price (CHF)'] = df['Actual_Price (CHF)'].round(2)  # Round the Actual_Price to 2 decimal places

df.loc[df['Discount'] == 1.0, 'Discount'] = 'no discount'  # Restore '1.0' with 'no discount'
df.loc[df['Discount'] != 'no discount', 'Discount'] = (df['Discount'] * 100).astype(str)+'%'  # Restore discount in percentage


# 2.3.4 Deleting products that not correspond to "pasta sauce" or "pesto"
keywords = ['Braten', 'Sriracha', 'Heinz', 'Thomy', 'Bohnen', 'Chili', 'Soja', 'Knorr']  # List of keywords to filter out
pattern = '|'.join(keywords)  # Matches any of the keywords
df = df[~df['Product_Description'].str.contains(pattern, case=False, na=False)]  # Filter out rows

# 2.3.5 Manual correction for "Brand" values with case-insensitive replacement
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

# 2.4 Adding Regular_Price/Unit and Actual_Price/Unit
df['Regular_Price/Unit'] = (df['Regular_Price (CHF)']/df['Grammage']).round(3)
df['Actual_Price/Unit'] = (df['Actual_Price (CHF)']/df['Grammage']).round(3)

# 3 - New column information: distance from average price
'''The distance of the Regular_Price/Unit from the average price/unit allows to get at a first glance
the positive or negative difference of the price in percentage.
The calculation allows also to visualize the outliers.'''

average_price = df['Regular_Price/Unit'].mean()
df['Distance_average_price'] = (((df['Regular_Price/Unit']-average_price)/average_price)*100).round(2).astype(str)+'%'

# 4 - EXPORTING THE DATAFRAME
''' It is important to save the data frame in "csv" format in a subfolder to avoid importing
it when running this script again, since it will import or "csv" files available in the directory selected
at the beginning of this script.'''

## 4.1 Ordering columns according to group project
df = df[['ID', 'Competitor', 'Category', 'Product_Description', 'Brand', 'Regular_Price (CHF)', 'Grammage', 'Unit', 'Link', 'Scraping_Date', 'Discount', 'Actual_Price (CHF)', 'Regular_Price/Unit', 'Actual_Price/Unit', 'Distance_average_price']]

## 4.2 Visualize & exporting
print(df.to_string())  # Visualize the data frame for final check
df.to_csv('/Users/diazm/Documents/HSLU/05_AS2024/CIP/project/merged_dfs/pasta_sauces_merged.csv', index=False)  # save



# 5. PLOTS

# Convert Distance_average_price back to numeric for plotting (remove '%')
df['Distance_average_price_numeric'] = pd.to_numeric(df['Distance_average_price'].str.replace('%', ''), errors='coerce')

# 5.1 Histogram
plt.figure(figsize=(10, 6))
n, bins, patches = plt.hist(df['Distance_average_price_numeric'], bins=20, color='skyblue', edgecolor='black')

# Adding labels to each bar
for i in range(len(patches)):
    # Compute the position for each label
    height = n[i]
    plt.text(patches[i].get_x() + patches[i].get_width() / 2, height, f'{int(height)}',
             ha='center', va='bottom', fontsize=10, color='black')
plt.title('Distribution of Distance from Average Price')
plt.xlabel('Distance from Average Price (%)')
plt.ylabel('Frequency')
plt.savefig('distance_average_price_histogram.png', dpi=300, bbox_inches='tight')
plt.show()
plt.close()

# 5.2 Box plot
import matplotlib.pyplot as plt

# Calculate summary statistics
median = df['Distance_average_price_numeric'].median()
q1 = df['Distance_average_price_numeric'].quantile(0.25)
q3 = df['Distance_average_price_numeric'].quantile(0.75)
min_val = df['Distance_average_price_numeric'].min()
max_val = df['Distance_average_price_numeric'].max()

# Identify outliers based on the interquartile range (IQR)
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr
outliers = df[(df['Distance_average_price_numeric'] < lower_bound) | (df['Distance_average_price_numeric'] > upper_bound)]

# Plot boxplot
plt.figure(figsize=(8, 6))
plt.boxplot(df['Distance_average_price_numeric'], vert=False, patch_artist=True)
plt.title('Box Plot of Distance from Average Price')
plt.xlabel('Distance from Average Price (%)')

# Annotate the median
plt.text(median, 1.1, f'Median: {median:.2f}', ha='center', va='bottom', fontsize=8, color="purple", rotation=90)

# Annotate Q1 and Q3
plt.text(q1, 1.1, f'Q1: {q1:.2f}', ha='center', va='bottom', fontsize=8, color="green", rotation=90)
plt.text(q3, 1.1, f'Q3: {q3:.2f}', ha='center', va='bottom', fontsize=8, color="green", rotation=90)

# Annotate min and max (whiskers)
plt.text(min_val, 0.9, f'Min: {min_val:.2f}', ha='center', va='top', fontsize=8, color="red", rotation=90)
plt.text(max_val, 0.9, f'Max: {max_val:.2f}', ha='center', va='top', fontsize=8, color="red", rotation=90)

# Annotate outliers
for outlier in outliers['Distance_average_price_numeric']:
    plt.text(outlier, 1.1, f'{outlier:.2f}', ha='center', va='bottom', fontsize=8, color="blue", rotation=90)

# Save and show plot
plt.savefig('distance_average_price_box.png', dpi=300)
plt.show()
plt.close()


# 5.3 Bar plot

# Sort by Distance_average_price_numeric for clarity in the plot
df_sorted = df.sort_values('Distance_average_price_numeric', ascending=False)

plt.figure(figsize=(12, 8))
plt.bar(df_sorted.index, df_sorted['Distance_average_price_numeric'], color='orange')
plt.title('Distance from Average Price per Item')
plt.xlabel('Item Index')
plt.ylabel('Distance from Average Price (%)')
plt.xticks(rotation=90)  # Rotate item labels if necessary
plt.savefig('distance_average_price_bar.png', dpi=300, bbox_inches='tight')
plt.show()
plt.close()