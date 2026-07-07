# %% Importing libraries
import pandas as pd, numpy as np
from IPython.display import display

# %% Load SpaceX dataset from previous section
df=pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_1.csv")
df.head(10)

# %%
# Identify mising values percentage
print('column: missing values (%)')
print('_'*27)
display(df.isnull().sum()/len(df)*100)
# 
# identify categorical and numerical columns
print('column: dtype')
print('_'*27)
display(df.dtypes)

# Calculate the number of launches on each site
print('Launch Site: counts')
print('_'*27)
display(df['LaunchSite'].value_counts())

# Calculate the number and occurrence of each orbit
print('Orbit: counts')
print('_'*27)
display(df['Orbit'].value_counts())

# Calculate the number and occurence of mission outcome of the orbits
print('Outcome: counts')
print('_'*27)
display(df['Outcome'].value_counts())

# %%
bad_outcomes = [out for out in set(df.Outcome.values)
                     if 'True' not in out]
landing_class = [int(out not in bad_outcomes) 
                 for out in df.Outcome.values ]

df['Class'] = landing_class

print('dataframe with new column added\n')
display(df.sample(5))

print('Statistics about landing success\n')
display(df.Class.describe())
# %% Export to CSV
df.to_csv('dataset_part2.csv', index=False)

# %%
