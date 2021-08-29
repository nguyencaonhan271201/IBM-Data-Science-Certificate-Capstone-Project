# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

#Get list of launch_sites
launch_sites = list(spacex_df["Launch Site"].unique())
launch_sites.insert(0, "All")
launch_options = []
for site in launch_sites:
    launch_options.append(
        {
            "label": site,
            "value": site
        }
    )

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=launch_options,
                                    placeholder="Select a Launch Site here",
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
                                                min=0,
                                                max=10000,
                                                step=1000,
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id="success-pie-chart", component_property="figure"),
              Input(component_id="site-dropdown", component_property="value"))
def get_pie_chart(option):
    print(option)
    if option == "All":
        return px.pie(spacex_df, values="class", names='Launch Site', title="Total Success Launches By Site")
    else:
        data = spacex_df[spacex_df["Launch Site"] == option]
        data_print = data.groupby(['Launch Site','class']).size().reset_index(name='count')
        return px.pie(data_print, values="count", names="class", title=f"Total Success Launches for site {option}")
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id="success-payload-scatter-chart", component_property="figure"),
              [
                  Input(component_id="site-dropdown", component_property="value"),
                  Input(component_id="payload-slider", component_property="value")
              ])
def get_scatter_chart(site, payload):
    df_filter = spacex_df[spacex_df["Payload Mass (kg)"].between(payload[0], payload[1])]
    if site == "All":
        return px.scatter(df_filter, 
                          x="Payload Mass (kg)", 
                          y="class",
                          title="Correlation between Payload and Success for all Sites",
                          color="Booster Version Category")
    else:
        df_filter = df_filter[df_filter['Launch Site'] == site]
        return px.scatter(df_filter, 
                          x="Payload Mass (kg)", 
                          y="class",
                          title=f"Payload vs. Outcome for {site}",
                          color="Booster Version Category")
        
# Run the app
if __name__ == '__main__':
    app.run_server()
