# %% 
# Imports
import requests
import pandas as pd
import numpy as np
import datetime 

# %% 
# PD settings
# Setting this option will print all collumns of a dataframe
pd.set_option('display.max_columns', None)
# Setting this option will print all of the data in a feature
pd.set_option('display.max_colwidth', None)

# %%
# Helper functions
# Takes the dataset and uses the rocket column to call the API and append the data to the list
def getBoosterVersion(data):
    print('started getting data for BoosterVersion')
    fallback = {
        '5e9d0d95eda69955f709d1eb': 'Falcon 1',
        '5e9d0d95eda69973a809d1ec': 'Falcon 9',
        '5e9d0d95eda69974db09d1ed': 'Falcon Heavy'
    }
    for x in data['rocket']:
        if x:
            try:
                # Logique officielle IBM v4
                response = requests.get(f"https://api.spacexdata.com/v4/rockets/{x}").json()
                BoosterVersion.append(response['name'])
            except:
                # Sécurité "Cloud-Native" : évite le crash global
                BoosterVersion.append(fallback.get(x, "Unknown Rocket"))
    print('finished loading BoosterVersion')

# Takes the dataset and uses the launchpad column to call the API and append the data to the list
def getLaunchSite(data):
    print('started getting data for LaunchSite')
    for x in data['launchpad']:
        if x:
            try:
                response = requests.get(f"https://api.spacexdata.com/v4/launchpads/{x}").json()
                Longitude.append(response['longitude'])
                Latitude.append(response['latitude'])
                LaunchSite.append(response['name'])
            except: # In case the API don't answer
                Longitude.append(None)
                Latitude.append(None)
                LaunchSite.append("Unknown Pad")
    print('finished loading LaunchSite')

# Takes the dataset and uses the payloads column to call the API and append the data to the lists
def getPayloadData(data):
    print('started geting payload data')
    for load in data['payloads']:
        try:
            payload_id = load[0] if isinstance(load, list) else load
            response = requests.get(f"https://api.spacexdata.com/v4/payloads/{payload_id}").json()
            PayloadMass.append(response['mass_kg'])
            Orbit.append(response['orbit'])
        except:
            PayloadMass.append(None)
            Orbit.append(None)
    print('finished loading PayloadMass and Orbit')

# Takes the dataset and uses the cores column to call the API and append the data to the lists
def getCoreData(data):
    print('started getting cores data')
    for core in data['cores']:
        if core and len(core) > 0:
            c = core
            try:
                response = requests.get(f"https://api.spacexdata.com/v4/cores/{c['core']}").json()
                Block.append(response['block'])
                ReusedCount.append(response['reuse_count'])
                Serial.append(response['serial'])
            except:
                Block.append(None)
                ReusedCount.append(None)
                Serial.append(None)

            Outcome.append(str(c['landing_success']) + ' ' + str(c['landing_type']))
            Flights.append(c['flight'])
            GridFins.append(c['gridfins'])
            Reused.append(c['reused'])
            Legs.append(c['legs'])
            LandingPad.append(c['landpad'])
        else: # use default in case it doesn't work
            for lst in [Block, ReusedCount, Serial, Outcome, Flights, GridFins, Reused, Legs, LandingPad]:
                lst.append(None)
    print('finished getting core data')

# %%
# Request rocket launch data from SpaceX API
spacex_url = 'https://api.spacexdata.com/v4/launches/past'
response = requests.get(spacex_url)
# %%
# Using static response for this project
static_json_url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/API_call_spacex_api.json'
response = requests.get(static_json_url)
print('status code:', response.status_code)

# %%
# Decoding json into dataframe
decoded = response.json()
data = pd.json_normalize(decoded)
data.head(5)
# %%
# Getting information from API
# Lets take a subset of our dataframe keeping only the features we want and the flight number, and date_utc.
data = data[['rocket', 'payloads', 'launchpad', 'cores', 'flight_number', 'date_utc']]

# remove rows with multiple cores and payloads
data = data[data['cores'].map(len)==1]
data = data[data['payloads'].map(len)==1]

# extract the dict inside lists with core and payload info
data['cores'] = data['cores'].map(lambda x: x[0])
data['payloads'] = data['payloads'].map(lambda x: x[0])

# convert date_utc to datetime
data['date'] = pd.to_datetime(data['date_utc']).dt.date

# %%
# Global variables 
BoosterVersion = []
PayloadMass = []
Orbit = []
LaunchSite = []
Outcome = []
Flights = []
GridFins = []
Reused = []
Legs = []
LandingPad = []
Block = []
ReusedCount = []
Serial = []
Longitude = []
Latitude = []

# %%
# Call helper functions 
# get booster name from data.rocket
getBoosterVersion(data)
# get mass of payload and orbit from data.payload
getLaunchSite(data)
# get launch site from data.launchpad
getPayloadData(data)
# get info from data.cores
getCoreData(data)

# %%
# dataset construction
launch_dict = {'FlightNumber': list(data['flight_number']),
'Date': list(data['date']),
'BoosterVersion':BoosterVersion,
'PayloadMass':PayloadMass,
'Orbit':Orbit,
'LaunchSite':LaunchSite,
'Outcome':Outcome,
'Flights':Flights,
'GridFins':GridFins,
'Reused':Reused,
'Legs':Legs,
'LandingPad':LandingPad,
'Block':Block,
'ReusedCount':ReusedCount,
'Serial':Serial,
'Longitude': Longitude,
'Latitude': Latitude}

dataset = pd.DataFrame(launch_dict)
dataset.head()
# %%
# Filtering dataframe to include only Falcon 9 launches
data_falcon9 = dataset[dataset['BoosterVersion']=='Falcon 9']
data_falcon9.head()

# %%
data_falcon9.loc[:,'FlightNumber'] = list(range(1, data_falcon9.shape[0]+1))
data_falcon9
# %%
# Data wrangling
print(data_falcon9.isnull().sum())
PayloadMass_mean = data_falcon9.PayloadMass.mean()
data_falcon9['PayloadMass'].replace({None:PayloadMass_mean})
# since the API is not working, it will replace with NaN 

# %%
# Getting dataframe from static response as the SpaceX API is malfunctioning
# this dataset have already reset the FlightNumber and fixed the PayloadMass missing values
data_falcon9 = pd.read_csv('data_falcon9_static.csv')

# export to CSV 
data_falcon9.to_csv('dataset_part_1.csv', index=False)
