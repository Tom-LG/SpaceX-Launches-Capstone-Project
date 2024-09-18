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

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                    options=[
                                        {'label': 'All Sites', 'value': 'ALL'},
                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                    ],
                                    value='ALL',
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
                                dcc.RangeSlider(id = 'payload-slider',
                                    min = 0, max = 10000, step = 1000,
                                    marks = {0: '0',
                                            2500: '2500',
                                            5000: '5000',
                                            7500: '7500',
                                            10000: '10000'},
                                    value = [min_payload, max_payload]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, 
                     names='Launch Site', 
                     values='class',  # Number of successes and failures
                     title='Total Success Launches By Site')
    else:
        # Filtrer le DataFrame par site de lancement
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        # Calculer le nombre de succès et d'échecs pour le site sélectionné
        success_counts = filtered_df['class'].value_counts()
        # Créer le graphique en camembert
        fig = px.pie(
            names=success_counts.index,      # Index des valeurs (0 et 1 pour échecs et succès)
            values=success_counts.values,    # Comptage des valeurs (nombre de succès et d'échecs)
            title=f'Success vs Failed Launches for site {entered_site}'
        )
    
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
# Callback function to update scatter plot based on selected site and payload range

@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_plot(entered_site, selected_payload_range):
    # Décomposer la plage de valeurs du slider
    low, high = selected_payload_range
    
    # Filtrer le DataFrame par plage de payload mass
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & 
                            (spacex_df['Payload Mass (kg)'] <= high)]
    
    # Filtrer par site de lancement si un site spécifique est sélectionné
    if entered_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
    
    # Créer le graphique de dispersion
    fig = px.scatter(
        filtered_df, 
        x='Payload Mass (kg)', 
        y='class', 
        color='Booster Version Category',  # Colorier par catégorie de version de booster
        title='Payload Mass vs. Launch Success',
        hover_data=['Launch Site']  # Afficher des informations supplémentaires lors du survol
    )
    
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
