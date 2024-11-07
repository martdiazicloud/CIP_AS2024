# Import Packages
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#######################################################################
##################         DATA CLEANING MIGROS       #################
#######################################################################

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
    df.loc[df['Grammage'] == 1, 'Unit'] = 'Kg'
    return df

# Function to convert gr to kg
def convert_grammage_to_kg(df):
    # Transform Grammage to float
    df['Grammage'] = df['Grammage'].astype(float)

    # Apply conversion
    df.loc[df['Unit'] == 'g', 'Grammage'] = round(df.loc[df['Unit'] == 'g', 'Grammage'] / 1000, 3)

    # update the Unit to Kg
    df['Unit'] = 'kg'
    return df

# Function to calculate the Price/Unit
def price_per_unit(df, column_price):
    df['Price/Unit'] = round(df[column_price] / df['Grammage'], 2)
    return df['Price/Unit']

# Call clean_price function to clean the columns of the dataset
clean_price(df_migros_cleaned)

# Call clean_product_description function to clean the columns of the dataset
clean_product_description(df_migros_cleaned)

# Call clean_grammage function to clean the columns of the dataset
clean_grammage(df_migros_cleaned)

# Call conversion_grammage_tp_kg function to convert gr to kg
convert_grammage_to_kg(df_migros_cleaned)

# Calculate the Discount %
df_migros_cleaned['Discount'] = (
    ((df_migros_cleaned['Regular Price (CH)'] - df_migros_cleaned['Actual Price (CH)'])
     / df_migros_cleaned['Regular Price (CH)']) * 100
).round(0).astype(int).astype(str) + '%'

# Replace '0%' with 'no discount'
df_migros_cleaned['Discount'] = df_migros_cleaned['Discount'].replace('0%', 'no discount')

# Calling Function Price per Unit to calculate Regular_Price/ KG and Actual_Price/KG
df_migros_cleaned['Regular_Price/Unit'] = price_per_unit(df_migros_cleaned, 'Regular Price (CH)')
df_migros_cleaned['Actual_Price/Unit'] = price_per_unit(df_migros_cleaned, 'Actual Price (CH)')

# Arrange order of columns
df_migros_cleaned = df_migros_cleaned[['ID', 'Competitor', 'Category', 'Product_Description', 'Brand', 'Regular Price (CH)',
                               'Grammage', 'Unit', 'Link', 'Scraping_Date', 'Discount', 'Actual Price (CH)',
                                       'Regular_Price/Unit', 'Actual_Price/Unit']]

# Rename columns
df_migros_cleaned = df_migros_cleaned.rename(columns={'Regular Price (CH)': 'Regular_Price (CHF)',
                                                      'Actual Price (CH)': 'Actual_Price (CHF)'})


#######################################################################
##################         DATA CLEANING lIDL       #################
#######################################################################

# Open CSV file
df_lidl = pd.read_csv("~/Desktop/Lidl_Scraping_Pasta.csv", encoding='utf-8')
print(df_lidl.head())

# Create DataFrame df_lidl_cleaned
df_lidl_cleaned = df_lidl.copy()

# Function to clean Price column
def clean_price(df):
    # Extract the price value as a decimal number and convert to float
    df['Regular_Price'] = df['Regular_Price'].str.extract(r'(\d+\.\d+)').astype(float)
    df['Actual_Price'] = df['Actual_Price'].str.extract(r'(\d+\.\d+)').astype(float)
    return df

# Function to clean Product Description
def clean_product_description(df):
    df['Product_Description'] = (df['Product_Description'].str.replace('Ã¶', 'ö', regex=False)
                                 .str.replace('Ã¼', 'ü', regex=False)
                                 .str.replace('Ã¤', 'ä', regex=False))
    return df

# Function to clean Grammage
def clean_grammage(df):
    # Extract the numeric value and the unit (either 'g' or 'k')
    df[['Grammage', 'Unit']] = df['Product_Grammage'].str.extract(r'(\d+)(g|k)')

    # Delete Product_Grammage Column
    del df['Product_Grammage']

    return df

# Apply the cleaning functions to df_lidl_cleaned
df_lidl_cleaned = clean_price(df_lidl_cleaned)
df_lidl_cleaned = clean_product_description(df_lidl_cleaned)
df_lidl_cleaned = clean_grammage(df_lidl_cleaned)

# Calculate the Discount %
df_lidl_cleaned['Discount'] = (
    ((df_lidl_cleaned['Regular_Price'] - df_lidl_cleaned['Actual_Price'])
     / df_lidl_cleaned['Regular_Price']) * 100
).round(0).astype(int).astype(str) + '%'

# Replace '0%' with 'no discount'
df_lidl_cleaned['Discount'] = df_lidl_cleaned['Discount'].replace('0%', 'no discount')

# Call conversion_grammage_tp_kg function to convert gr to kg
convert_grammage_to_kg(df_lidl_cleaned)

# Calling Function Price per Unit to calculate Regular_Price/ KG and Actual_Price/KG
df_lidl_cleaned['Regular_Price/Unit'] = price_per_unit(df_lidl_cleaned, 'Regular_Price')
df_lidl_cleaned['Actual_Price/Unit'] = price_per_unit(df_lidl_cleaned, 'Actual_Price')



# Arrange order of columns
df_lidl_cleaned = df_lidl_cleaned[['ID', 'Competitor', 'Category', 'Product_Description', 'Product_Brand', 'Regular_Price',
                                   'Grammage', 'Unit', 'Link', 'Scraping_Date', 'Discount', 'Actual_Price',
                                   'Regular_Price/Unit', 'Actual_Price/Unit']]

# Rename columns in df_lidl_cleaned
df_lidl_cleaned = df_lidl_cleaned.rename(columns={'Product_Brand': 'Brand',
                                                  'Regular_Price': 'Regular_Price (CHF)',
                                                  'Actual_Price': 'Actual_Price (CHF)'})


###################################################################################
##################         EXPLORATORY DATA ANALYSIS PART        ##################
###################################################################################

# Look for Missing Values and data Type
print("Info Variables Migros:")
df_migros_cleaned.info() # Migros

print("")

print("Info Variables Lidl:")
df_lidl_cleaned.info()   # Lidl

''' CREATE BOXPLOT TO DETECT OUTLIERS '''

# Function to create Boxplot
def boxplot(df, name):
    # Numerical variables
    vars = ['Regular_Price (CHF)', 'Actual_Price (CHF)']

    # Set up subplots
    fig, axes = plt.subplots(1, 2, figsize=(8, 5))

    # Flatten axes array into 1D for easy iteration
    axes = axes.flatten()

    # Plot a boxplot for each numerical variable
    for i, var in enumerate(vars):
        sns.boxplot(data=df, y=var, ax=axes[i], palette='coolwarm')

    # Add main title
    plt.suptitle(f'Boxplots for Price Variables in {name}  ', fontsize=10, y=0.95)

        # Display Boxplot
    box_plot = plt.show()

# Calling Boxplot Function
boxplot(df_migros_cleaned, 'Migros')
boxplot(df_lidl_cleaned, 'Lidl')


###################################################################################
##################        CREATE COLUMN OF INTEREST        #########################
###################################################################################

''' A Column named " Private Label Product" is created in order to compare its price with third brands'''

def column_interest(df, brands, category, retail):

    df_label_brand = brands
    df['Private_Label_Product'] = df['Brand'].apply(lambda x: 'Yes' if x in df_label_brand else 'No')

    # Save to CSV
    df = df.to_csv(f"~/Desktop/{retail}_cleaned_{category}.csv", index = False)

    return df

# Calling the column of interest function
column_interest(df_lidl_cleaned, ['Combino', 'Italiamo'], 'Pasta', 'Lidl')
column_interest(df_migros_cleaned, ['M-Classic', 'Migros Bio'], 'Pasta', 'Migros')
