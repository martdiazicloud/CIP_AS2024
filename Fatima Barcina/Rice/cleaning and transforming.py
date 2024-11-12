"""
Title: "Rice Migros and Lidl: Data Cleaning and Transforming ""
author: Fátima Barcina Arias
date:  Fall Semester 2024 (November 2024)
"""

# 1. Import and set up
import pandas as pd     # Data manipulation (tables)
import os               # Interact with operating system
import matplotlib.pyplot as plt   #Basic plotting
import seaborn as sns             #Advanced plotting
from collections import Counter   #Count items
import re                         #Text pattern matching


#Set options:
pd.set_option('display.precision', 2)     #For floating show two decimals
pd.set_option('display.max_columns', 20)  #Set option to display 20 columns
pd.set_option('display.width', 1000)      #Sets option to display width to 1000 characters, preventing rows from wrapping onto multiple lines.
pd.set_option('display.max_colwidth', 30 ) #Set option column width
#pd.set_option('display.max_rows', None)     #Display all.
#pd.set_option('display.max_columns', None)
#pd.set_option('display.max_colwidth', None )

# 2. Load and Inspect Data: Load the datasets and perform initial checks
# Load the CSV files into a DataFrame, where df1=Migros y df2=Lidl
df1 = pd.read_csv('RiceOfMigros.csv', header=0)
df2= pd.read_csv('RiceOfLidl.csv', header=0)

# Inspection and Overview both DF from Webscraping:
print("\n Migros Rice Overview: ")
print(df1)
print(f"\n Number non-NA/null entries for each column: {df1.count()}")

print("\n Lidl Rice Overview: ")
print (df2)
print(f"\n Number non-NA/null entries for each column: {df2.count()}")

print("\n Info DF Migros:")
print(df1.info())
print("\n Info DF Lidl:")
print(df2.info())

# 3. Merge DataFrames: Combine the two datasets into a single DataFrame: df_rice
# Merge df1 and df2: Combine  vertically, with index reset
print("*"*50)
print("      Rice DF(Migros+Lidl): 'df_rice' ")
print("*"*50)
df_rice = pd.concat([df1, df2], axis=0).reset_index(drop=True)   #One DF: Migros and Lidl Rice

# 4. Check Data Types and Missing Values: Display data types and summarize missing values.
##Inspection:
print (f"\n Migros and Lidl Rice DF Overview: ")
print (df_rice.head)
#print(df_rice.tail)
print (f"\n Display 3 random rows: {df_rice.sample(3)}")

# Display data types of each column
print("\nData type of each column:")
data_types = df_rice.dtypes
print(data_types)

# General DataFrame info
print("\nDataFrame Info:")
df_info = df_rice.info()    #automatically print

#Missing values: NaN, Null, None
# Count of non-NA/null entries for each column
non_na_counts = df_rice.count()
print(f"\nNumber of non-NA/null entries for each column:\n{non_na_counts}\n")

# Boolean matrix of missing values (Not very practical for large DataFrames)
#missing_values_matrix = df_rice.isna()
#print("\nMissing Values Boolean Matrix:")
#print(missing_values_matrix)

## Check rows that contain missing values
print("\n Are there rows with NaN values?")
print(df_rice.isna().any(axis=1))

#5. Handle Missing Data: Fill missing values if needed and load 'df_rice_cleaned'(if this file is deleted> fill Nan with loop)
# Find and Fill Missing Data with dynamically input assistance; avoiding filling again NaN if the script run again
# For filling again the missing values: delete 'df_rice_cleaned.csv' and use input function for each NaN
# Path to the CSV file where the DataFrame will be saved with filled missing values.
csv_file_path = 'df_rice_cleaned.csv'

# Check if the CSV file already exists
if os.path.exists(csv_file_path):
    # Load the DataFrame from the CSV file
    df_rice = pd.read_csv(csv_file_path)
    print("\nLoaded DataFrame from existing CSV file.")
else:

    # Summary of the total number of missing values in each column (practical)
    missing_values_summary = df_rice.isna().sum()
    print("\nSummary of total number of missing values in each column:")
    print(missing_values_summary)

    # Check if there are any missing values
    if missing_values_summary.sum() == 0:
        print("\nNo missing values found in the DataFrame.")
    else:
        # Filtering rows with NaN values
        print(f"\n Row(s) with NaN value(s):")
        rows_with_nan = df_rice[df_rice.isna().any(axis=1)]
        print(rows_with_nan)

        # Loop through each row with NaN values and display the columns containing NaN
        for index, row in rows_with_nan.iterrows():
            nan_columns = row[row.isna()].index.tolist()  # Get columns with NaN in the current row
            print(f"\nRow {index} has NaN in columns: {nan_columns}")

        # Loop through each row with NaN values
        for index, row in rows_with_nan.iterrows():
            print("\nClick on the product link to check missing information in the following row:")
            print(row['Product Link'])  # Display the product link for you to review

            # Loop through each column that has NaN in the current row
            nan_columns = row[row.isna()].index.tolist()  # Columns with NaN in the current row
            for col in nan_columns:
                user_input = input(f"For row {index}, insert {col}: ")

                # Convert input to float if the column is expected to be numeric
                if df_rice[col].dtype in ['float64', 'int64']:
                    user_input = float(user_input)

                df_rice.loc[index, col] = user_input  # Fill the missing value in the DataFrame

            # Check the updated row
            print("\nCheck the updated row:")
            print(df_rice.loc[index])

        # Save the updated DataFrame to the CSV file
        df_rice.to_csv(csv_file_path, index=False)
        print("\nSaved updated DataFrame to CSV file.")

# Display the updated DataFrame with filled values
print("\nUpdated DataFrame with filled values:")
print(df_rice)

# Summary check for any remaining NaN values in each column
remaining_nans = df_rice.isna().sum()
print("\nSummary of remaining NaN values in each column:")
print(remaining_nans)


"""
#For filling missing values manually one by one, access specific row with missing value as example 43 'Brand':

print("\n Click in the product link to check the brand: ")
print(df_rice.iloc[43,:])
#Fill missing value
df_rice.loc[43, 'Brand'] = 'Ori di Langa'
print("\n Check the missing value: ")
print(df_rice.loc[43])

# Check for any remaining NaN values in the DataFrame
remaining_nans = df_rice.isna().sum()
print("\nSummary of remaining NaN values in each column:")
print(remaining_nans)

# Remove rows (no need it)
#As all the data are in the website Removing Rows are not need. In some missing values cases might be necessary:
# Remove rows that have NaN in any column
df_rice = df_rice.dropna()
print("\nDataFrame after removing rows with any NaN values:")
print(df_rice)

# Remove rows that have NaN in a specific column, for example, 'Brand'
df_rice = df_rice.dropna(subset=['Price'])
print("\nDataFrame after removing rows with NaN in 'Brand' column:")
print(df_rice)
"""

## Boolean matrix of null values (not very practical for large DataFrames)
#print("Null Values Boolean Matrix:")
#print(df_rice.isnull())

print("\n Any column  null values:")
print(df_rice.isnull().sum()) # Summarize null counts values by column

print("\nRow(s) with null values:")
rows_with_nulls = df_rice[df_rice.isnull().any(axis=1)]  #shows only the rows with missing vaule
print(rows_with_nulls)

print("\n Are there rows with Null values?")
print(df_rice.isnull().any(axis=1))                 #shows boolean check for null presence across rows

# 6. Check duplicates
# Check for any duplicated row:
if df_rice.duplicated().any():
    # Boolean Series indicating duplicated rows (only from second occurrence duplicates are marked as True)
    duplicate_rows = df_rice.duplicated()
    print("Duplicated rows:")
    print(duplicate_rows)

    # DataFrame showing only rows that are duplicates (excludes the first occurrence of each duplicate)
    duplicates_rows_df = df_rice[df_rice.duplicated()]
    print("\nSubsequent duplicated rows:")
    print(duplicates_rows_df)

    # DataFrame showing all duplicated rows (includes the first occurrence of each duplicate)
    all_duplicates = df_rice[df_rice.duplicated(keep=False)]
    print("\nAll duplicated rows (including first occurrences):")
    print(all_duplicates)
else:
    print("\nNo duplicate rows found!!")         #No duplicates in df_rice.

#in case delete duplicate rows (keeping first occurrence):
#df.drop_duplicates()

### Above is confirmed is NOT any row duplicate DF!.Might be interested to check only based on 2 columns
### Check for duplicates in combinations of columns: Brand, Description
duplicates_check = df_rice[df_rice.duplicated(subset=['Description', 'Brand'], keep=False)]
if not duplicates_check.empty:
    print("\nDuplicate rows found based on 'Description' and 'Brand':")
    print(duplicates_check[['Competitor', 'Description', 'Brand', 'Price', 'Grammage','Unit', 'Product Link']])
print("\nNo duplicates, rest of columns as Price and Product Link are different")

# 7. Data Cleaning and Transformation:

# Columns.
print("\nNames of columns: ")
print(df_rice.columns)

# Modified ID column to avoid duplicates from Lidl
df_rice['ID'] = df_rice.index + 1

# Define the new column order
columns_order = ['ID', 'Competitor', 'Category', 'Description', 'Brand', 'Price', 'Grammage', 'Unit', 'Discount',
                 'Product Link', 'Scraping Date']

# Reorder the DataFrame columns,  under my consideration
df_rice = df_rice[columns_order]
print("\nDataFrame with 'Discount' moved after 'Unit':")
print(df_rice)

print("\n Display some of columns: ")
print(df_rice.iloc[:,3:9])     #interested in Description, Brand, Price, Grammage, Unit, Discount

# New Columns:

## Add "Price per kg" column:                     #(group project: Actual_Price/Unit)
## Note:The price per kg at the moment of purchase (including the discount) is generally more relevant for consumers
## It is the amount consumer pay per kg when they buy the product, considering any ongoing discounts
df_rice['Price per Kg'] = df_rice.apply(lambda row: row['Price'] * (1000 / row['Grammage']) if row['Unit'] == 'g'
else row['Price'] / row['Grammage'], axis=1)

print("\nDataFrame with 'Price per Kg' column:")
print(df_rice[['Description', 'Brand', 'Price', 'Grammage', 'Unit', 'Price per Kg']])


## Add "Regular Price" column.                                          (Group Project: Regular_Price (CH))
## Calculate 'Regular Price' based on 'Price' and 'Discount Percentage' from webscraping
### Note: more relevant for consumer, Price at moment purchase than regular price (price without discount)
### as it is what consumer really pay and made the decision buy or not.
df_rice['Regular Price'] =df_rice['Price'] / (1 - pd.to_numeric(
    df_rice['Discount'].str.replace('%', ''), errors='coerce'
).fillna(0) / 100)
# Round to 2 decimal places
df_rice = df_rice.round(2)

print("\nDataFrame with 'Regular Price' column:")
print(df_rice[['Description', 'Price', 'Discount', 'Regular Price']])

## Add "Regular Price per kg" based on 'Regular Price' and 'Grammage'      (Group project: Regular_Price/Unit)
df_rice['Regular Price per Kg'] = df_rice.apply(lambda row: row['Regular Price'] * (1000 / row['Grammage'])
if row['Unit'] == 'g' else row['Regular Price'] / row['Grammage'],
    axis=1
)
print("\nDataFrame with 'Regular Price per Kg' column:")
print(df_rice[['Description', 'Regular Price', 'Grammage', 'Unit', 'Regular Price per Kg']])

## Add 'Discounted Price Difference' column: (the difference between Regular Price and Price)
df_rice['Discounted Price Difference'] = df_rice['Regular Price'] - df_rice['Price']
print("\nDataFrame with 'Discounted Price Difference' column:")
print(df_rice[['Description', 'Price', 'Regular Price', 'Discounted Price Difference']])

# Define the new column order, including "Discounted Price Difference"
columns_order = [
    'ID', 'Competitor', 'Category', 'Description', 'Brand',
    'Price', 'Discount', 'Regular Price', 'Grammage', 'Unit',
    'Price per Kg', 'Regular Price per Kg', 'Discounted Price Difference',
    'Product Link', 'Scraping Date'
]
# Reorder the DataFrame columns
df_rice = df_rice[columns_order]

print("\nDataFrame with reordered columns:")
print(df_rice)

#Check summary of the Df
df_rice.info()

# 8. Outlier Detection
# Statistics for all numeric columns
print("\nStatistics for all numeric columns:")
print(df_rice.describe())

print("\nInconsistency found: max data.")

print("\nCheck filter grammage =1000")
# Filter rows where "Grammage" is equal to 1000
grammage_1000 = df_rice[df_rice['Grammage'] == 1000]
print("\nRows with 'Grammage' equal to 1000:")
print(grammage_1000)
print("Check it. OK")#ok data compare website

# Find the row with the maximum "Price per Kg"
outlier_row = df_rice[df_rice['Price per Kg'] == df_rice['Price per Kg'].max()]
print("\nRow with the maximum 'Price per Kg':")
print(outlier_row)    #check data is correct 175g 8.90CHF is 5.09/100g  (50.90/kg)

## Find the row with 175g and 8.90 CHF to verify the price per kg
specific_product = df_rice[(df_rice['Grammage'] == 175) & (df_rice['Price'] == 8.90)]
# Display product details
print("\nProduct details for verification:")
print(specific_product[['Description', 'Brand', 'Price', 'Grammage', 'Price per Kg']]) #it is ok comparing with website

print("\ndata max is correct. Check it. (ingredients: truffle)\n")

# Add "Outlier" column to identify rows with Price per Kg above 20 CHF
df_rice['Outlier'] = df_rice['Price per Kg'] > 20  # Mark as True for values > 20
# Display a sample to check the "Outlier" column
print("\nSample of DataFrame with 'Outlier' column:")
print(df_rice[['Description', 'Price', 'Grammage', 'Price per Kg', 'Outlier']].sample(10))
# Filter rows where "Outlier" is True
outliers = df_rice[df_rice['Outlier'] == True]
# Display the rows with Outlier set to True
print("\nRows marked as Outliers (Price per Kg > 20 CHF):")
print(outliers[['Description', 'Brand', 'Price', 'Grammage', 'Price per Kg', 'Outlier']])
print("Already check it!")

# Important: Data Consistency: Converting 'g' to 'kg' for Standardized Units for next comparing steps
# Convert all 'g' entries to 'kg' by dividing by 1000 (data consistency: Scaling by 1000)
df_rice.loc[df_rice['Unit'] == 'g', 'Grammage'] = df_rice['Grammage'] / 1000
df_rice.loc[df_rice['Unit'] == 'g', 'Unit'] = 'kg'
print("\n Convert all 'g' entries to 'kg':")
print(df_rice)


# Outlier identify any negative number in numeric columns
# Identify numeric columns
numeric_columns = df_rice.select_dtypes(include=['float64', 'int64']).columns
# Create a "Negative Value Outlier" column to mark rows with negative values in numeric columns
df_rice['Negative Value Outlier'] = df_rice[numeric_columns].lt(0).any(axis=1)
# Display rows where "Negative Value Outlier" is True
negative_outliers = df_rice[df_rice['Negative Value Outlier'] == True]
print("\nRows marked as Negative Value Outliers (containing negative values in numeric columns):")
print(negative_outliers)


# Mean: Importance of means as a method of detecting outliers.
# Analysis of price variations that help in detecting potential outliers.
# The resulting columns are added to the dataframe.

# Note: For this section, mean calculations is used column 'Price' =Purchase Price (Actual_Price)
# as from my consideration is more relevant as consumer

# Calculate the Overall Average Price per kg for all rice in the Df
print("*"*50)
mean_price_per_kg_all = df_rice['Price per Kg'].mean()
print(f"\nOverall Average Price per Kg for all rice in the DataFrame: {mean_price_per_kg_all:.2f} CHF")

# Calculate the average Price per kg grouped by 'Competitor'
mean_price_per_kg_by_competitor = df_rice.groupby('Competitor')['Price per Kg'].mean()
print("\nAverage Price per Kg of rice by Competitor:")
print(mean_price_per_kg_by_competitor)
print("*"*50)

# Rice price comparing with mean(s) price per kg (Price- Mean)
## Create a column showing the variation of Price per Kg from the overall mean
df_rice['Var Price per Kg vs Overall Mean (%)'] = (
    ((df_rice['Price per Kg'] - mean_price_per_kg_all) / mean_price_per_kg_all) * 100).round(2)

# Create a column showing the variation of Price per Kg from the competitor-specific mean
df_rice['Mean Price per Kg (Competitor)'] = df_rice['Competitor'].map(mean_price_per_kg_by_competitor)  # Ensures that each product is compared to the correct competitor average for calculating price variation.
df_rice['Var Price per Kg vs Competitor Mean (%)'] = (
    ((df_rice['Price per Kg'] - df_rice['Mean Price per Kg (Competitor)'])
     / df_rice['Mean Price per Kg (Competitor)']) * 100).round(2)


# Display the DataFrame with the new columns
print("\nRice Price per Kg: Variation from Overall and Competitor Averages:")
print(df_rice[['Competitor', 'Description', 'Price per Kg', 'Var Price per Kg vs Overall Mean (%)',
               'Var Price per Kg vs Competitor Mean (%)']])

# Create a column showing the absolute difference from the overall mean  (more useful as consumer)
df_rice['Abs Diff Price per Kg vs Overall Mean'] = (df_rice['Price per Kg'] - mean_price_per_kg_all).round(2)

# Create a column showing the absolute difference from the competitor-specific mean
df_rice['Mean Price per Kg (Competitor)'] = df_rice['Competitor'].map(mean_price_per_kg_by_competitor) #ensures that each product is compared to the correct competitor average for calculating price variation.
df_rice['Abs Diff Price per Kg vs Competitor Mean'] = (df_rice['Price per Kg'] - df_rice['Mean Price per Kg (Competitor)']).round(2)

# Display the DataFrame with the new columns
print("\nRice Price per Kg: Absolute Difference from Overall and Competitor Averages:")
print(df_rice[['Competitor', 'Description', 'Price per Kg', 'Abs Diff Price per Kg vs Overall Mean',
               'Abs Diff Price per Kg vs Competitor Mean']])

# Outlier Detection and Validation for 'Price per Kg'
print("******** Outlier Detection and Validation for 'Price per Kg' ********")
# Define outliers using the Interquartile Range (IQR)
Q1 = df_rice['Price per Kg'].quantile(0.25)
Q3 = df_rice['Price per Kg'].quantile(0.75)
IQR = Q3 - Q1
print(f"IQR: {IQR:.2f},Q1: {Q1:.2f}, Q3:{Q3:.2f}")

# Define the outliers (factor *1.5)
low_outliers = df_rice['Price per Kg'] < (Q1 - 1.5 * IQR)
high_outliers = df_rice['Price per Kg'] > (Q3 + 1.5 * IQR)
iqr_outliers = df_rice[low_outliers | high_outliers]   #(|=or)
print("\nRows identified as outliers based on IQR for 'Price per Kg':")
print(iqr_outliers[['Competitor', 'Description', 'Price per Kg']])

# Check if 'Price per Kg' falls within an expected range
min_expected_price_per_kg = 1  # Example: 1 CHF
max_expected_price_per_kg = 30  # Example: 30 CHF
range_outliers = df_rice[(df_rice['Price per Kg'] < min_expected_price_per_kg)
                         | (df_rice['Price per Kg'] > max_expected_price_per_kg)]

print("\nRows with 'Price per Kg' outside the expected range:")
print(range_outliers[['Competitor', 'Description', 'Price per Kg']])
print("According website is ok. Check it!")
print("*****************************************************************")

# 9. Visualizations:
# helpful for identifying outliers as well as providing insights into the data.
print("\n***** 6 Graphs and boxplot. Checking and understanding. ******")
#Graphs and boxplot
#1. Box Plot - Visualize Price per Kg by Competitor
plt.figure(figsize=(8, 6))
sns.boxplot(data=df_rice, x='Competitor', y='Price per Kg')
plt.title("Distribution of Price per Kg by Competitor")
plt.show()

#2. Histogram - Overall Distribution of Price per Kg
# Histogram of Price per Kg
plt.figure(figsize=(8, 6))
sns.histplot(df_rice['Price per Kg'], bins=20, kde=True)
plt.title("Histogram of Price per Kg")
plt.xlabel("Price per Kg")
plt.ylabel("Frequency")
plt.show()

#3. Scatter Plot - Price vs. Price per Kg
# Scatter plot of Price vs. Price per Kg (pricing coherence)
plt.figure(figsize=(8, 6))
plt.scatter(df_rice['Price'], df_rice['Price per Kg'])
plt.title("Scatter Plot of Price vs. Price per Kg")
plt.xlabel("Price (CHF)")
plt.ylabel("Price per Kg (CHF)")
plt.show()

#4. Bar Plot - Average Price per Kg by Competitor
# Bar plot of average Price per Kg by Competitor
mean_price_per_kg_by_competitor = df_rice.groupby('Competitor')['Price per Kg'].mean()
mean_price_per_kg_by_competitor.plot(kind='bar', color=['blue', 'orange'], figsize=(8, 6))
plt.title("Average Price per Kg by Competitor")
plt.xlabel("Competitor")
plt.ylabel("Average Price per Kg (CHF)")
plt.show()

#5. Highlight Outlier in Scatter Plot
# Highlight the outlier in scatter plot
plt.figure(figsize=(8, 6))
plt.scatter(df_rice['Price'], df_rice['Price per Kg'], color='blue')
plt.xlabel("Price (CHF)")
plt.ylabel("Price per Kg (CHF)")
plt.title("Scatter Plot of Price vs. Price per Kg with Outlier Highlighted")
# Highlighting the specific outlier row
outlier = df_rice[df_rice['Price per Kg'] == 50.86]
plt.scatter(outlier['Price'], outlier['Price per Kg'], color='red', label='Risotto con Tartufo')
plt.legend()
plt.show()

#6. Horizontal Bar Plot- Product count by 'Brand' and 'Competitor'
# Group by 'Competitor' and 'Brand', then count the number of occurrences for each brand
brand_counts = df_rice.groupby(['Competitor', 'Brand']).size().reset_index(name='Product Count')
#Sorting brand counts in descending order by 'Product Count'
brand_counts_sorted = brand_counts.sort_values(by='Product Count', ascending=False)

plt.figure(figsize=(12, 8))
for competitor in brand_counts_sorted['Competitor'].unique():
    competitor_data = brand_counts_sorted[brand_counts_sorted['Competitor'] == competitor]
    color = 'orange' if competitor == 'Migros' else 'blue'
    plt.barh(competitor_data['Brand'], competitor_data['Product Count'],color=color, label=competitor)

plt.xlabel("Number of Products")
plt.ylabel("Brand")
plt.title("Number of Products by Brand for Each Supermarket (Sorted)")
plt.legend(title="Supermarket")
plt.tight_layout()
plt.show()

print("**End of Graph visualization**")


# 10. Categorical variables
# Descriptive statistics of the rice dataset
print("***** Overview of Categorical Variables *****\n")
print("\nDescriptive Statistics (Including Categorical Variables):")
print(df_rice.describe(include='all'))  #statistics for categorical and numerical columns

# Check the data and better understanding.Insights and Observations.
print("\n*** Insights and Observations Categorical Variables for this dataset***\n:")

# Competitor Analysis
# print("Directly from table: 2 competitors. Migros offers 66 products, therefore Lidl offers 10 products"). #ok
# Calculate the percentage of products from Migros
total_products = df_rice['Competitor'].count()
migros_count = df_rice['Competitor'].value_counts().get('Migros', 0)   #if not found, return 0
migros_percentage = (migros_count / total_products) * 100

print("\n1. 'Competitor' Analysis:")
print("- There are two competitors: Migros and Lidl")
print(f"- Migros offers {migros_count} products, representing {migros_percentage:.2f}% of the total data.")
print(f"- Lidl offers {total_products - migros_count} products, highlighting a smaller variety available on their site.")

# Category Analysis
print("\n2. Category Analysis:")
print("- All entries belong to the 'Rice' category, confirming a rice-specific dataset.")

# Description Analysis
print("\n3. Description Analysis:")
print("- Based on the descriptive statistics table, there are 68 unique product descriptions in the dataset.")
print("- The most common description is 'Basmati rice,' appearing 4 times.")

# Brand Analysis
print("\n4. Brand Analysis:")
print("- There are 24 unique brands, with 'Mister Rice Bio' appearing most frequently (13 times).")
print("- This indicates 'Mister Rice Bio' is a prominent brand in the dataset.")

# Discount Analysis
print("\n5. Discount Analysis:")
print("- Based on the descriptive statistics table, there are 2 unique discount values in the dataset.")
print("- The most common discount status is 'No Discount,' appearing 70 times. Therefore 6 products with discount")
#find out the discount types
unique_discounts = df_rice['Discount'].unique()
print("Unique discount types:")
print(unique_discounts)

# Unit and Grammage Analysis
print("\n6. Unit and Grammage Analysis:")
print("- The unit of measurement is consistently 'kg,' indicating that all data is standardized in units.")
print("- No further unit conversions are necessary.")

# Product Link Analysis
print("\n7. Product Link Analysis:")
print("- Each product has a unique link, suggesting each row represents a unique product.")

# Scraping Date
print("\n8. Scraping Date:")
print("- Only one unique scraping date ('07/11/2024') is present, indicating all data was collected on the same day.")


print("\nApart from the info summarize table above, the next info provides a clear view and add \nclarity on product variety, brand presence, and data consistency, supplementing the general statistics.")

# Summary of unique values, most frequent entries, and value counts.
# Identify categorical columns:
categorical_columns = df_rice.select_dtypes(include=['object']).columns  #object as categorical variable
categorical_columns = categorical_columns.drop('Product Link')   #drop Product Link categorical variable
# Display information for each categorical column
# Loop through each Categorical Column: Loop over each column in categorical_columns and provides a summary for each.
print("\nCategorical Data Summary:")
for col in categorical_columns:
    print(f"\nColumn: {col}")
    print(f"Unique Values: {df_rice[col].nunique()}")     #shows number of distint values
    print(f"Most Frequent Value: {df_rice[col].mode()[0]} (Count: {df_rice[col].value_counts().iloc[0]})") #most common value/mode , select first mode using [0] in case multiple; count sorted by freq, getting the first row
    print("Value Counts:")
    print(df_rice[col].value_counts().head(10))  # Show top 10

# Product Proportions, Price Analysis, and Leading Brands by Competitor
# Calculate proportions of each competitor: proportion of products offered by each competitor as %.
competitor_proportions = df_rice['Competitor'].value_counts(normalize=True) * 100
print("\nCompetitor Proportions (%):")
print(competitor_proportions)

# Products counts by Competitor and Category
product_counts = df_rice.groupby(['Competitor', 'Category']).size().reset_index(name='Product Count')
print("\nProduct Counts by Competitor and Category:")
print(product_counts)

# Calculate Minimum and Maximum Price per kg by competitor
price_range_per_kg = df_rice.groupby('Competitor')['Price per Kg'].agg(['min', 'max']).round(2)  #agg:multiple aggregation functions in a single line
print("\nPrice Range per Kg by Competitor:")
print(price_range_per_kg)

# Quartile Distribution of Price per kg for each Competitor
price_quartiles = df_rice.groupby('Competitor')['Price per Kg'].describe()[['25%', '50%', '75%']].round(2)
print("\nQuartile Distribution of Price per Kg for Each Competitor:")
print(price_quartiles)

#Top 5 most common products by description
common_products = df_rice['Description'].value_counts().head(5)
print("\nTop 5 Most Common Products by description:")
print(common_products)

# Average price per kg of top brands grouped by competitor: Average Price per Kg of the top 5 most frequent brands, grouped by competitor.
top_brands = df_rice['Brand'].value_counts().head(5).index  # Adjust '5'  for more brands if needed
brand_price_comparison = df_rice[df_rice['Brand'].isin(top_brands)].groupby(['Brand', 'Competitor'])['Price per Kg'].mean().round(2)
print("\nAverage Price per Kg of Top Brands by Competitor:")
print(brand_price_comparison)

# Top 5 most frequent brands within each competitor’s product list
# Count the occurrences of each brand per competitor and select the top 5
top_brands_by_competitor = (
    df_rice.groupby(['Competitor', 'Brand']).size()
    .reset_index(name='Frequency')
    .sort_values(['Competitor', 'Frequency'], ascending=[True, False])
    .groupby('Competitor').head(5)
    .reset_index(drop=True)  # Reset index
)
print("\nTop 5 Most Frequent Brands by Competitor:")
print(top_brands_by_competitor)

# Get a list of top brands
top_brands_list = top_brands_by_competitor['Brand'].unique()

# Calculate the average price per kg for  top brands within each competitor
brand_price_comparison = (
    df_rice[df_rice['Brand'].isin(top_brands_list)]
    .groupby(['Brand', 'Competitor'])['Price per Kg']
    .mean().round(2))

print("\nAverage Price per Kg of Top Brands within each Competitor:")
print(brand_price_comparison)

# Column 'Description' Analysis
# Description containing “Jasmin” (column 'Description')
# Basmati rice and Jasmine rice as most common products by description:

# Filter rows where 'Description' contains "Basmati" (case-insensitive)
basmati_rice = df_rice[df_rice['Description'].str.contains("Basmati", case=False, na=False)]
# Count occurrences of "Basmati" descriptions per competitor
basmati_count_by_competitor = basmati_rice['Competitor'].value_counts().reset_index()
basmati_count_by_competitor.columns = ['Competitor', 'Count']
print("\nCount of Basmati Rice by Competitor:")
print(basmati_count_by_competitor)
# Calculate average price per kg for descriptions containing "Basmati" by competitor
basmati_price_by_competitor = basmati_rice.groupby('Competitor')['Price per Kg'].mean().round(2)
print("\nAverage Price per Kg of Basmati Rice by Competitor:")
print(basmati_price_by_competitor)

# Filter rows where 'Description' contains "Jasmin" (case-insensitive)
jasmin_rice = df_rice[df_rice['Description'].str.contains("Jasmin", case=False, na=False)]
# Count occurrences of "Jasmin" descriptions per competitor
jasmin_count_by_competitor = jasmin_rice['Competitor'].value_counts().reset_index()
jasmin_count_by_competitor.columns = ['Competitor', 'Count']
print("\nCount of Jasmin Rice by Competitor:")
print(jasmin_count_by_competitor)
# Calculate average price per kg for descriptions containing "Jasmin" by competitor
jasmin_price_by_competitor = jasmin_rice.groupby('Competitor')['Price per Kg'].mean().round(2)
print("\nAverage Price per Kg of Jasmin Rice by Competitor:")
print(jasmin_price_by_competitor)

# 'Description' column: analyzing the text data in the Description column
# Concatenate all descriptions into one large text, then split into individual words
all_descriptions = " ".join(df_rice['Description']).lower()  # Convert to lowercase to make the search case-insensitive
words = re.findall(r'\b\w+\b', all_descriptions)  # Extract words

# Count word occurrences
word_counts = Counter(words)

# Display the most common words
common_words = word_counts.most_common(20)  # Adjust the number to show more or fewer common words
print("\nMost common words in product descriptions:")
for word, count in common_words:
    print(f"{word}: {count}")

# Define keywords to analyze
keywords = ["long", "langkornreis", "basmati", "bio", "jasmine"]

# Create a DataFrame to store occurrences of each keyword in `Description` by Competitor
keyword_counts_by_competitor = pd.DataFrame()

for keyword in keywords:
    # Filter rows that contain the keyword in `Description`
    contains_keyword = df_rice['Description'].str.contains(keyword, case=False, na=False)

    # Count occurrences of the keyword by Competitor
    keyword_count = df_rice[contains_keyword].groupby('Competitor').size().reset_index(name=f'{keyword}_count')

    # Merge results with the main DataFrame
    if keyword_counts_by_competitor.empty:
        keyword_counts_by_competitor = keyword_count
    else:
        keyword_counts_by_competitor = keyword_counts_by_competitor.merge(keyword_count, on='Competitor', how='outer')

# Display occurrences of each keyword by Competitor
print("\nKeyword Occurrences by Competitor in Descriptions:")
print(keyword_counts_by_competitor.fillna(0))  # Fill NaN with 0 for clarity

# Calculate average price per kg for products containing each keyword by Competitor
keyword_price_comparison = {}

for keyword in keywords:
    contains_keyword = df_rice['Description'].str.contains(keyword, case=False, na=False)
    avg_price_per_kg = df_rice[contains_keyword].groupby('Competitor')['Price per Kg'].mean().round(2)
    keyword_price_comparison[keyword] = avg_price_per_kg

# Display average price per kg for products with each keyword by Competitor
print("\nAverage Price per Kg for Products Containing Keywords by Competitor:")
for keyword, avg_price in keyword_price_comparison.items():
    print(f"\nKeyword: {keyword}")
    print(avg_price)


# 11. Save Transformed Data
print("*****Create .csv  *******")
#1. ALL columns: Save 'df_rice' with all transformations and added columns to a final CSV file with ALL columns: overview
#df_rice.to_csv("RiceCleanedAndTransformed.csv", index=False)
#print("\nFinal DataFrame with all transformations saved as 'RiceCleanedAndTransformedAll.csv'")
#df3 = pd.read_csv('RiceCleanedAndTransformedAll.csv', header=0)
#df3.info()
#print(df3)

# 2.Save 'df_rice' with just some selected columns of all cleaning and transforming process
# Define the columns to keep, excluding as 'Outlier' and 'Negative Value Outlier' columns
# According to the whole process of this Cleaning and Transforming script, included only some selected columns in CSV
selected_columns = [
    'ID', 'Competitor', 'Category', 'Description', 'Brand', 'Price', 'Discount', 'Regular Price',
    'Grammage', 'Unit', 'Price per Kg', 'Regular Price per Kg', 'Discounted Price Difference',
    'Product Link', 'Scraping Date',
    'Var Price per Kg vs Overall Mean (%)', 'Var Price per Kg vs Competitor Mean (%)',
    'Abs Diff Price per Kg vs Overall Mean', 'Abs Diff Price per Kg vs Competitor Mean'
]

# Select the specified columns from df_rice and round to 2 decimal places where applicable
df_rice_new = df_rice[selected_columns].round(2)

# Save the selected DataFrame to a new CSV file with the filename ending in "d"
df_rice_new.to_csv("RiceData_Cleaned_Transformed.csv", index=False)
print("\nSelected columns saved as 'RiceData_Cleaned_Transformed.csv'")

# Load the new CSV to verify and display its structure
df_verified = pd.read_csv("RiceData_Cleaned_Transformed.csv")
df_verified.info()
print(df_verified)


#3.For Group Project:
# Adapt to common column names and column order for group project
# Rename the necessary columns for the group project
df_rice = df_rice.rename(columns={
    'Description': 'Product_Description',
    'Regular Price': 'Regular_Price (CHF)',
    'Product Link': 'Link',
    'Scraping Date': 'Scraping_Date',
    'Price': 'Actual_Price (CHF)',
    'Regular Price per Kg': 'Regular_Price/Unit',
    'Price per Kg': 'Actual_Price/Unit',
    'Var Price per Kg vs Overall Mean (%)': 'Deviation % Actual_Price/Unit from Overall Mean',
    'Var Price per Kg vs Competitor Mean (%)': 'Deviation % Actual Price/Unit from Competitor Mean',
    'Abs Diff Price per Kg vs Overall Mean': 'Abs Deviation Actual Price/Unit from Overall Mean',
    'Abs Diff Price per Kg vs Competitor Mean': 'Abs Deviation Actual Price/Unit from Overall Mean'
})

# Select only the columns needed for the group project, ordered
df_selected = df_rice[['ID', 'Competitor', 'Category', 'Product_Description', 'Brand',
                       'Regular_Price (CHF)', 'Grammage', 'Unit', 'Link', 'Scraping_Date',
                       'Discount', 'Actual_Price (CHF)', 'Regular_Price/Unit', 'Actual_Price/Unit',
                       'Deviation % Actual_Price/Unit from Overall Mean',
                       'Deviation % Actual Price/Unit from Competitor Mean',
                       'Abs Deviation Actual Price/Unit from Overall Mean',
                       'Abs Deviation Actual Price/Unit from Overall Mean']].round(2)


df_selected.to_csv("RiceData_Cleaned_Transformed_GroupProject.csv", index=False)
print("\nSelected columns saved as 'RiceData_Cleaned_Transformed_GroupProject.csv'")

# Load the new CSV for the group project to verify and display its structure
df_group_project = pd.read_csv("RiceData_Cleaned_Transformed_GroupProject.csv")
df_group_project.info()
print(df_group_project)


print("*"*20)
print("\n13. END OF SCRIPT\n")
print("*"*20)
