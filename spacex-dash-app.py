# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

launch_sites = set(spacex_df['Launch Site'])

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(
    children=[html.H1('SpaceX Launch Records Dashboard',
                style={'textAlign': 'center', 'color': '#503D36',
                        'font-size': 40}),
        # TASK 1: Add a dropdown list to enable Launch Site selection
        # The default select value is for ALL sites
        dcc.Dropdown(id='site-dropdown',
                     options=[{'label': 'All Sites', 'value': 'ALL'}]+[{'label': site, 'value': site} for site in launch_sites], value='ALL',
                     placeholder='Select a Launch Site here',
                     searchable=True
                       ),
        html.Br(),

        # TASK 2: Add a pie chart to show the total successful launches count for all sites
        # If a specific launch site was selected, show the Success vs. Failed counts for the site
        html.Div(dcc.Graph(id='success-pie-chart')),
        html.Br(),

        html.P("Payload range (Kg):"),
        # TASK 3: Add a slider to select payload range
        dcc.RangeSlider(id='payload-slider',
        min=min_payload, max=round(max_payload, -4), step=1000, value=[min_payload, max_payload]),

        # TASK 4: Add a scatter chart to show the correlation between payload and launch success
        html.Div(dcc.Graph(id='success-payload-scatter-chart')),
        ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
    )
def get_pie_chart(entered_site):
    if entered_site=='ALL':
        data = spacex_df.groupby('Launch Site', as_index=False)[['class']].sum()
        data.rename(columns={'class':'Success counts'}, inplace=True)
        fig = px.pie(data, values='Success counts',
        names = 'Launch Site',
        title = 'Counts of launch success per site',)
        fig.update_traces(textinfo='value')
        return fig
    else:
        data = spacex_df[spacex_df['Launch Site']==entered_site]
        class_counts = pd.DataFrame(data[['class']].value_counts()).reset_index()
        class_counts.replace({'class':{0:'fail', 1:'success'}},
        inplace=True)

        fig = px.pie(class_counts, values='count',
        names = 'class',
        title = f'Counts of launch success in {entered_site}',
        color='class',
        color_discrete_map={'failed':'red', 'succeed':'darkgreen'})
        fig.update_traces(textinfo='value')
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value')]
    )
def get_scatter_chart(entered_site, entered_payload_range):
    massmin, massmax = entered_payload_range
    if entered_site=='ALL':
        data = spacex_df[(massmin <= spacex_df['Payload Mass (kg)']) & (spacex_df['Payload Mass (kg)']<= massmax)]
        
        fig = px.scatter(data, 
        x = 'Payload Mass (kg)',        
        y = 'class',
        color = 'Booster Version Category',
        symbol = 'Booster Version Category',
        title = 'Payload Mass vs. Landing Success considering booster version category',
        color_discrete_sequence=px.colors.qualitative.Dark24,)

    else:
        data = spacex_df[(massmin <= spacex_df['Payload Mass (kg)']) & (spacex_df['Payload Mass (kg)']<= massmax) & (spacex_df['Launch Site']==entered_site)]
                
        fig = px.scatter(data, 
        x = 'Payload Mass (kg)',        
        y = 'class',
        color = 'Booster Version Category',
        symbol = 'Booster Version Category',
        title = f'Payload Mass vs. Landing Success from site {entered_site} considering booster version category',
        color_discrete_sequence=px.colors.qualitative.Dark24,)
    
    fig.update_layout(
    yaxis = dict(
        tickmode = 'array',
        tickvals = [0, 1],
        ticktext = ['Failed', 'Succeed']
    ),
    autosize=False,
    minreducedwidth=600,
    minreducedheight=450,
    width=1200,
    height=450,
    )
    fig.update_traces(marker_size=10)
    return fig


# Run the app
if __name__ == '__main__':
    app.run()
