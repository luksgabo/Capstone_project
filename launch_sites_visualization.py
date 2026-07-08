# %% Install packages
# %pip install folium wget 
# %% Import libraries
import folium, wget, pandas as pd
# Import folium MarkerCluster plugin
from folium.plugins import MarkerCluster
# Import folium MousePosition plugin
from folium.plugins import MousePosition
# Import folium DivIcon plugin
from folium.features import DivIcon
from IPython.display import display
import plotly.express as px
# %% Download and read the `spacex_launch_geo.csv`
spacex_csv_file = wget.download('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv')
spacex_df=pd.read_csv(spacex_csv_file)
display(spacex_df.head())

#%%

# Select relevant sub-columns: `Launch Site`, `Lat(Latitude)`, `Long(Longitude)`, `class`
spacex_df = spacex_df[['Launch Site', 'Lat', 'Long', 'class']]
launch_sites_df = spacex_df.groupby(['Launch Site'], as_index=False).first()
launch_sites_df = launch_sites_df[['Launch Site', 'Lat', 'Long']]
display(launch_sites_df)

# %% Start location is NASA Johnson Space Center
nasa_coordinate = [29.559684888503615, -95.0830971930759]
site_map = folium.Map(location=nasa_coordinate, zoom_start=10)

# Create a blue circle at NASA Johnson Space Center's coordinate with a popup label showing its name
circle = folium.Circle(nasa_coordinate, radius=1000, 
            color="#f3721b", fill=True).add_child(
            folium.Popup('NASA Johnson Space Center'))

# Create a blue circle at NASA Johnson Space Center's coordinate with a icon showing its name
marker = folium.map.Marker(
    nasa_coordinate,
    # Create an icon as a text label
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:%s;"><b>%s</b></div>' % ("#002ad3", 'NASA JSC'),
        )
    )
site_map.add_child(circle)
site_map.add_child(marker)

# %% Add a circle in the map for each launch site 

for site, lat, log in launch_sites_df.values:
    circle = folium.Circle([lat, log], radius=100, color="#9DF721",
              fill=True).add_child(folium.Popup(site))
    marker = folium.map.Marker([lat, log],
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:%s;"><b>%s</b></div>' % ("#002ad3", site),
        )
    )
    site_map.add_child(circle)
    site_map.add_child(marker)

# display(site_map)
# %% Mark the successed/failed launches for each site on the map 
# Considering many launch records will have the same coordinates
marker_cluster = MarkerCluster()
spacex_df['marker_color'] = spacex_df['class'].map(lambda x: 
"#0A9103" if x==1 else "#C20000")
display(spacex_df[['marker_color','class']])
 
# Add marker_cluster to current site_map
site_map.add_child(marker_cluster)

# for each row in spacex_df data frame create a Marker object with its coordinate
# and customize the Marker's icon property to indicate if this launch was successed or failed, 
# e.g., icon=folium.Icon(color='white', icon_color=row['marker_color']
for index, record in spacex_df.iterrows():

    marker = folium.map.Marker([record.Lat, record.Long],
    icon=folium.Icon(
        color='white',
        icon_color = record.marker_color,
        icon='check' if record.marker_color == '#0A9103' else 'asterisk',
        )
    )
    marker_cluster.add_child(marker)

# site_map

# %% Calculate the distances between launch site to its proximities
# Add Mouse Position to get the coordinate (Lat, Long) for a mouse over on the map
formatter = "function(num) {return L.Util.formatNum(num, 5);};"
mouse_position = MousePosition(
    position='topright',
    separator=' Long: ',
    empty_string='NaN',
    lng_first=False,
    num_digits=20,
    prefix='Lat:',
    lat_formatter=formatter,
    lng_formatter=formatter,
)

site_map.add_child(mouse_position)
# site_map

# %%
from math import sin, cos, sqrt, atan2, radians

def calculate_distance(lat_lon1, lat_lon2):
    lat1, lon1 = lat_lon1
    lat2, lon2 = lat_lon2
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

# %% Create and add a folium.Marker on your selected closest coastline point on the map
# Display the distance between coastline point and launch site using the icon property 
shore_coordinates = (28.56367 , -80.57163)
launch_coordinates = [launch_sites_df.loc[0,'Lat'],
                      launch_sites_df.loc[0,'Long']]

distance = calculate_distance(launch_coordinates, shore_coordinates)
distance_marker = folium.Marker(
   shore_coordinates,
   icon=DivIcon(
       icon_size=(20,20),
       icon_anchor=(0,0),
       html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>'
         % "{:10.2f} KM".format(distance),
       )
   )

lines = folium.PolyLine(locations = [shore_coordinates, launch_coordinates],
                         weight=1)
site_map.add_child(lines)
# %%
