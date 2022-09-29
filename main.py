# Importing modules
from bs4 import BeautifulSoup
import requests
import pandas as pd
import lxml

# This is the url that we are going to scrape
URL = 'https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors/page/'

# scraping logic
all_majors = []
for n_page in range(1, 35):
    url = URL + str(n_page)
    response = requests.get(url)
    website = response.text
    soup = BeautifulSoup(website, "lxml")
    majors = soup.findAll(name='span', class_='data-table__value')
    major_row = []
    for major in majors:
        price = major.text
        if '$' in price and ',' in price:
            price = price.replace("$", "")
            price = price.replace(",", "")
            price = int(price)
        major_row.append(price)
        if len(major_row) == 6:
            all_majors.append(major_row)
            major_row = []

# Creating the dataframe
majors_df = pd.DataFrame(all_majors,
                         columns=['Rank', 'Major', 'Degree Type', 'Early Career Pay', 'Mid-Career Pay', '% High Meaning'])

# Exporting the dataframe to a csv file
majors_df.to_csv('college-salary-report.csv', index=False)
