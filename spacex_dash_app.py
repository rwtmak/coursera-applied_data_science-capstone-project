# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the launch data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
launch_sites_df = spacex_df.groupby(['Launch Site'], as_index=False).first()
launch_sites_df = launch_sites_df[['Launch Site']]

landing_label = []
for outcome in spacex_df["class"]:
    if (outcome == 0):
        landing_label.append(1)
    else:
        landing_label.append(1)
spacex_df['label']=landing_label

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=[
                                        {'label':'All Sites', 'value':'ALL'},
                                        {'label':launch_sites_df.loc[0,'Launch Site'], 'value':launch_sites_df.loc[0,'Launch Site']},
                                        {'label':launch_sites_df.loc[1,'Launch Site'], 'value':launch_sites_df.loc[1,'Launch Site']},
                                        {'label':launch_sites_df.loc[2,'Launch Site'], 'value':launch_sites_df.loc[2,'Launch Site']},
                                        {'label':launch_sites_df.loc[3,'Launch Site'], 'value':launch_sites_df.loc[3,'Launch Site']},
                                    ],
                                    value= 'ALL',
                                    placeholder="Select a launch site here:",
                                    searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                min=0, max=10000, step=1000,
                                marks={
                                    0: '0',
                                    2500: '2500',
                                    5000: '5000',
                                    7500: '7500',
                                    10000: '10000'},
                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df.where(spacex_df['Launch Site'] == entered_site)
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class',
        names='Launch Site',
        title='Total Success Launches By Site')
        return fig
    else:
        fig = px.pie(filtered_df, values='label',
        names='class',
        title='Total Success Launches for site ' + str(entered_site))
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
[Input(component_id='site-dropdown', component_property='value'),
Input(component_id='payload-slider', component_property='value')])
def get_scatter_chart(entered_site, slider_range):
    filtered2_df = spacex_df.where(spacex_df['Launch Site'] == entered_site)
    low, high = slider_range
    if entered_site == 'ALL':      
        mask1 = (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
        fig = px.scatter(spacex_df[mask1], x='Payload Mass (kg)', y='class',
        color='Booster Version Category',
        title='Correlation between Payload (kg) and Launch Success for all sites')
        return fig
    else:
        mask2 = (filtered2_df['Payload Mass (kg)'] > low) & (filtered2_df['Payload Mass (kg)'] < high)
        fig = px.scatter(filtered2_df[mask2], x='Payload Mass (kg)', y='class',
        color='Booster Version Category',
        title='Correlation between Payload (kg) and Launch Success for '+ str(entered_site))
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
