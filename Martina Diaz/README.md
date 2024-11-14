Author: Martina Diaz

**Contents**

This repository contains the files .py developed to scrap the products in the category "Pasta Sauces."
These files are named **lidl.py** and **migros.py**. Both scripts are divided into the following parts:

0. IMPORTING PACKAGES
1. GENERAL FUNCTIONS
2. URL LIST OF ALL PRODUCTS
3. INDIVIDUAL PRODUCT SCRAPING
4. DATA FRAME
The data frames **lidl.csv** and **migros.csv** are created from the respective Python script.

The file **pasta_sauces_dataframes.py** includes functions and steps to merge and clean the data frames according to the following structure:
0. IMPORTING PACKAGES
1. IMPORTING THE DATA FRAMES
2. CLEANING AND FORMATTING THE DATA FRAMES
3. CALCULATION OF THE DISTANCE FROM AVERAGE PRICE
4. EXPORTING THE DATA FRAMES
5. PLOTS

Chapter 3 includes the additional section of the data frame to calculate the distance of the Regular_Price/Unit from the average price/unit.
This analysis allows us to get, at first glance, the positive or negative difference of the price in percentage and to visualize the outliers.

The outputs of the script include the file **pasta_sauces_merged.csv** and plots in .png format showing the products' price/unit distance from the average price.

**How to run the code**

In order to run the code, the following steps are required:
1. run **lidl.py**
2. run **migros.py**
3. run **pasta_sauces_dataframes.py**

___Remarks___: the scraping scripts at points 1 and 2 are implemented according to the website structure dated 01.11.2024. 
Changes in the websites might affect the functionality of the scripts.
Additional remarks and comments are posted in the scripts.
