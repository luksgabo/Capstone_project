# %%
# Web scraping from Wikipedia
wiki_url = 'https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches'
static_url = "https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/91.0.4472.124 Safari/537.36"
}

# %%
# import required packages
import numpy as np, datetime as dt
import requests
from bs4 import BeautifulSoup
import re, unicodedata, pandas as pd
# %%
#  Helper function
def save_to_dict(launch_dict, row_id, elems):

    # Date value
    date_time = elems[columns_name.index("Date and time ( UTC )")-1]
    date_time = ' '.join(list(date_time.strings)[:2])
    date_time = dt.datetime.strptime(str(date_time), "%B %d, %Y %H:%M")

    launch_dict['Date and time ( UTC )'].append(date_time)
    launch_dict['Date'].append(date_time.date())
    launch_dict['Time'].append(date_time.time())

    # Booster version
    booster_version = elems[columns_name.index("Version, booster")-1]
    try:
        booster_version = ' '.join(booster_version.strings)
        booster_version = re.sub('[\xa0] ', '-', booster_version).replace(' ‑ ', '-')
    except:
        booster_version = None
        
    launch_dict['Version, booster'].append(booster_version)
    launch_dict['Version Booster'].append(booster_version)

    # Launch Site
    site = elems[columns_name.index('Launch site')-1]

    if site.strings:
        launch_site = ''.join(site.strings)
    else:
        launch_site = None

    launch_dict['Launch site'].append(launch_site)

    # Payload
    payload = elems[columns_name.index('Payload')-1]
    if payload.strings:
        payload = ''.join(payload.strings)
    else:
        payload = None

    launch_dict['Payload'].append(payload)

    # Payload Mass
    payload_mass = elems[columns_name.index('Payload mass')-1]

    if payload_mass.strings:
        payload_mass = ''.join(payload_mass.strings)
        payload_mass = re.sub('[\xa0]', ' ', payload_mass)
        payload_mass = payload_mass[:payload_mass.find('kg')+2]
    else:
        payload_mass = None

    launch_dict['Payload mass'].append(payload_mass)
    
    # Orbit
    orbit = elems[columns_name.index('Orbit')-1]

    if orbit.strings:
        orbit = ''.join(orbit.strings)
    else:
        orbit = None

    launch_dict['Orbit'].append(orbit)

    # Customer
    customer = elems[columns_name.index('Customer')-1]

    if customer.strings:
        customer = ''.join(customer.strings)
    else:
        customer = None

    launch_dict['Customer'].append(customer)

    # Launch outcome
    launch_outcome = elems[columns_name.index('Launch outcome')-1]

    if launch_outcome.strings:
        launch_outcome = ''.join(launch_outcome.strings)
    else:
        launch_outcome = None

    launch_dict['Launch outcome'].append(launch_outcome)

    # Booster landing
    booster_landing = elems[columns_name.index('Booster landing')-1]

    if booster_landing.strings:
        booster_landing = ''.join(booster_landing.strings)
    else:
        booster_landing = None

    launch_dict['Booster landing'].append(booster_landing)

def extract_column_from_header(row):
    """
    Return the landing status from the input HTML table cell
    """
    if row.br:
        row.br.replace_with(' ')

    for a_tag in row.find_all('a'):
        a_tag.replace_with(a_tag.get_text())

    if row.sup:
        row.sup.extract()

    column_name = ' '.join(row.stripped_strings)

    # Filter the digit and empty names
    if not (column_name.strip().isdigit()):
        return column_name.strip()

# %%
# Request the Falcon9 Launch Wiki HTML
response = requests.get(wiki_url, headers=headers)
print('status code:', response.status_code)

# %%
# Create a beautifulsoup object
soup = BeautifulSoup(response.text, features="html.parser", )
print(soup.title)
# %%
# Extract all columns/variable names from the HTML
html_tables = soup.find_all('table')

# using the third table which is the first launch table
first_launch_table = html_tables[2]
# print(first_launch_table)

columns_name = []
for th in first_launch_table.find_all('tr')[0].find_all('th'): # all headers in first row
    columns_name.append(extract_column_from_header(th))

print(columns_name)
# %%
# Create dataframe from HTML table
launch_dict = {k: [] for k in columns_name}

# Add some new columns
launch_dict['Version Booster']=[]
launch_dict['Booster landing']=[]
launch_dict['Date']=[]
launch_dict['Time']=[]

# Parsing into dict
# Extract each table of class "wikitable plainrowheaders collapsible sticky-header"
for table_number, table in enumerate(soup.find_all('table',
    attrs={'class':"wikitable plainrowheaders collapsible sticky-header"}) ):
    # get table row
    print('\ntable', table_number)
    for row in table.find_all("tr"):
        # check if it is a row
        if row.th and row.th['scope']=='row':
            # get number for Flight No.
            flight_number = row.th.string.strip()
            try:
                row_id = int(flight_number)
            except:
                row_id = str(flight_number)

            # print(flight_number)
            # get row elements
            elems = row.find_all('td')
            # if the row's elements match the number of columns ( minus "Flight No.")
            if len(elems) == 9:                
                save_to_dict(launch_dict, row_id, elems)
                # Flight Number 
                launch_dict['Flight No.'].append(row_id)
                # print(launch_dict['Flight No.'])

# %%
# Creating data frame from dictionary
df = pd.DataFrame({ key:pd.Series(value) for key, value in launch_dict.items() })

# %% Checking Data frame
# df.head()
# df.sample(5)
# df.info()
# df.describe(include='all')

# %%
# Save to csv
df.to_csv('spacex_web_scraped.csv', index=False)
# %%
