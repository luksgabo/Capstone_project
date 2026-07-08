#%%
import pandas as pd, numpy as np
import matplotlib.pyplot as plt, seaborn as sns
from IPython.display import display
%matplotlib inline

# %% Read dataset from previous lab
df = pd.read_csv("dataset_part2.csv")

# If you were unable to complete the previous lab correctly you can uncomment and load this csv
# df = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/api/dataset_part_2.csv')

display(df.info())
# %% Plot relation between payload mass and flight number
sns.catplot(y="PayloadMass", x="FlightNumber", hue="Class",
             data=df, height=3, aspect =2)
plt.xlabel("Flight Number",fontsize=16)
plt.xticks(ticks=df.index[0::5], labels=df.FlightNumber[0::5])
plt.ylabel("Pay load Mass (kg)",fontsize=16)
plt.show()

# %% Plot relationship between Flight Number and Launch Site
sns.catplot(x='FlightNumber', y='LaunchSite', hue='Class',
            data=df, height=3, aspect =2)
plt.xlabel('Flight Number')
plt.ylabel('Launch Site')
plt.title('Flight No. vs Launch Site\n considering booster landing success')

# %% Plot relationship between Payload Mass and Launch Site
sns.catplot(x='PayloadMass', y='LaunchSite', hue='Class',
            data=df, height=3, aspect =2)
plt.xlabel('Payload Mass')
plt.ylabel('Launch Site')
plt.title('Payload Mass. vs Launch Site\n considering booster landing success')


# %% Plot relationship between success rate of each orbit type
df_orbit = df.groupby('Orbit', as_index=False)[['Class']].mean()
df_orbit.sort_values('Class', inplace=True)
display(df_orbit)
fig, ax = plt.subplots(figsize=(6,4))
sns.barplot(x='Orbit', y='Class', hue='Class', legend=False,
            palette='viridis', data=df_orbit, ax=ax, 
            err_kws={'color':'r'})
plt.ylabel('Average of success rate')
plt.xlabel('Orbit type')

# %% Plot relationship between Flight No. and Orbit type
sns.catplot(y='Orbit', x='FlightNumber', hue='Class',
            data=df, height=3, aspect =2)
plt.xlabel('Flight Number')
plt.ylabel('Orbit type')
plt.title('Flight No. vs Orbit type\n considering booster landing success')

# %% Plot relationship between Payload mass and Orbit type
sns.catplot(y='Orbit', x='PayloadMass', hue='Class',
            data=df, height=3, aspect =2)
plt.xlabel('Payload mass')
plt.ylabel('Orbit type')
plt.title('Payload mass vs Orbit type\n considering booster landing success')

# %% Getting year data from dataframe
df['Date'] = pd.to_datetime(df.Date)
df['Year'] = df[['Date']].map(lambda x: x.year)
df_year = df.groupby('Year')[['Class']].mean()

# %% Plot relationship between launch years and landing success rate
fig, ax = plt.subplots(figsize=(6,4))
sns.set_theme(style='darkgrid',)
sns.lineplot(x='Year', y='Class', data=df_year, ax=ax)
plt.xlabel('Year')
plt.ylabel('Average success rate')
plt.title('Launch success yearly trend')

# %% Selecting features for success prediction
features = df[['FlightNumber', 'PayloadMass', 'Orbit', 
               'LaunchSite', 'Flights', 'GridFins', 'Reused',
                 'Legs', 'LandingPad', 'Block', 'ReusedCount', 'Serial']]
features.head()
# %% Separating columns by type
numerical_cols = features.select_dtypes(['int','float','bool'])
categorical_cols = features.select_dtypes(['object', 'string', ])
display(numerical_cols,
categorical_cols)
# %% Create dummy variables to categorical columns
features_one_hot = pd.concat([numerical_cols, 
                             pd.get_dummies(categorical_cols) ],
                             axis=1)
features_one_hot = features_one_hot.astype('float64')
# %% Export as CSV
features_one_hot.to_csv('dataset_part3.csv', index=False)

# %%
