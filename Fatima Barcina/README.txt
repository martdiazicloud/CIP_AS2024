Title: "Rice Migros and Lidl: Data Collecting and Data Cleaning and Transforming "
by Fátima Barcina Arias (CIP_Group:03)
Date: Fall Semester 2024 (November 2024)

Websites Scraped:
https://www.migros.ch/en
https://www.lidl.ch/
Rice Webscraping from two competitors, starting from the initial webpage link and
navigating through multiple links until reaching the Rice sections.

Files:
"scrap_lidl.py": Script for web scraping Lidl.
"scrap_migros.py": Script web scraping Migros.
"RiceOfLidl.csv": Resulting CSV file from Lidl rice web scraping. Used in "cleaning and transforming.py"
"RiceOfMigros.csv": Resulting CSV file from Migros rice web scraping. Used in "cleaning and transforming.py"
"cleaning and transforming.py": Script that merger the two previous CSV files,data cleaning, inspection,
and transforming.
"df_rice_cleaned.csv": Intermediate CSV file created after merging and filling missing values,
as an outcome of organized method has been implemented to fill missing fields column by column,
using the "input" function. Saving this file avoids repeating the NaN filling
step every time the script runs entirely.
"RiceData_Cleaned_Transformed.csv": Final cleaned and transformed file with column names chosen
based on my practical considerations.
"RiceData_Cleaned_Transformed_GroupProject.csv": Final file created with standardized column names,
among others, after group team agreement. File used in the following steps for Group Project.


Some relevant Key Challenges:
-Navigating Responsive Elements: Rice category on Lidl’s website involved navigating elements, like
"Sortiment" button, which would sometimes disappear based on the window size.
This responsiveness complicated the web scraping, as key links became hidden when
the window was narrow. To solve this, if the button is hidden due to the window width,
the script uses an alternative approach by accessing the sitemap at the page’s footer.
-Brand  field Extraction: on Lidl's  website  the brand only appeared after clicking into each
individual product page. The script extracts brand information from each product page
Without doing so, the field would return  a high rate of NaN.
- Special case in Lidl´s web scraping, weight normally appeared as number followed by unit
(250g) but occasionally as a multiplication( 2x500g), which the initial scraping code not recognize,
resulting missing values. The Lidl web scraping script addresses this special case to prevent NaN values.
-cookies
-discount supermarket website updating : no se pudieron testear ciertos elementos como los descuentos de forma continua
durante el desarrollo

Goal:Fulfill the requirements of the project in each phase. Learning through this real-world
web scraping by using Beautiful Soup and Selenium,followed by data cleaning, inspection and transformation
with pandas.
My aim was to apply a wide range of  tools and methods in this practical case in an organized, structured and
consistent way throughout the project.
