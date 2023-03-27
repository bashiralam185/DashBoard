from dash import Dash, html, dcc, Input, Output, ctx
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Checking
# importing the dataset
bishkek_data = pd.read_csv("assets/Bishkek_data.csv")
data = pd.read_csv("assets/pm2_data.csv")
pollutants = pd.read_csv("assets/grid-export.csv")

#preprocessing of the datasets
data.dropna(inplace=True)
pollutants['Day'] = pd.to_datetime(pollutants['Day'])
data = data.replace('Unhealthy for Sensitive Groups', 'USG')


# starting of the app
app = Dash(__name__)
server =  app.server


# general layout of the app
app.layout = html.Div([
    html.Div(html.H1( children='Analyze, predict and forecast Air Pollution in Bishkek'), className='Heading'),
    html.Hr(),

    html.Div([
    html.Div(html.Button('Analyze', id='btn-nclicks-1', n_clicks=0), className='top_button'),
    html.Div(html.Button('Predictions', id='btn-nclicks-2', n_clicks=0), className='top_button'),
    html.Div(html.Button('Forecasting', id='btn-nclicks-3', n_clicks=0), className='top_button')],
    className='buttons'),
    html.Br(),
    html.Div(id='container-button-timestamp'),
    html.Label("Air Pollutants from 2019-2022 in Bishkek"),
    
], className='Main')

# this call back function is repsonsible to display the graphs from the selected categories
@app.callback(
    Output('container-button-timestamp', 'children'),
    Input('btn-nclicks-1', 'n_clicks'),
    Input('btn-nclicks-2', 'n_clicks'),
    Input('btn-nclicks-3', 'n_clicks'),
)

# this is the main functions
def displayClick(btn1, btn2, btn3):

    # This if statement contains the graphs for analyze purpose
    if "btn-nclicks-1" == ctx.triggered_id:
        graph_1 = px.line(bishkek_data, x="Date", y='median', color='Specie', title='Bishkek City')
        graph_2 = px.pie(data, names='AQI Category', title='Quality of Air in Bishkek from 2019 to 2022')
        # graph_3 = px.bar(data, x="Year", y="AQI",color="AQI Category",  barmode='group', title="Bishkek air pollution per year", width=500, height=400)
        graph_5 = px.line(data, x="Date (LT)", y="AQI",  title='AQI of Bishkek city from 2019 to 2022')
        graph_4 = px.line(pollutants, x="Day", y="PM1(mcg/m³)", title='Concentration of pollutants in Bishkek Air')


        return  html.Div([
            # first graph inside the analyze button
            html.Div([
            html.Div(dcc.Dropdown(
            id='first_dropdown',
            options=['min', 'max', 'median', 'variance'],
            value='median'
            ), className='first_dropdown'),
            html.Div(dcc.Graph(id = 'pollutant',
              figure=graph_1)
              )]), 
            html.Hr(),
            # second graph inside the analyze button
            html.Div([
                html.Div(
                    dcc.Graph(id='pie_chat', 
                              figure=graph_2), className='pie_chart'
                ), 
                html.Div(
                    dcc.Graph(
                        id='bar_chart',
                        figure=graph_5
                    ),className="bar_chart"
                )
            ], className='SecondGraph'),
            html.Hr(),

            #third graph
            html.Div([
            html.Div(
            dcc.Dropdown(
            id='second_dropdown',
            options=['PM1(mcg/m³)', 'PM10(mcg/m³)', 'PM2.5(mcg/m³)', 'NO(mcg/m³)','NO2(mcg/m³)','SO2(mcg/m³)','Temperature(°C)',
                     'Humidity(%)'],
            value='PM1(mcg/m³)'
            ), className='first_dropdown'
            ),
            html.Div(
            dcc.Graph(id='air_pollutants', 
                      figure=graph_4)
            ), ]),

              ], className='analyze')
    
    
    elif "btn-nclicks-2" == ctx.triggered_id:
        msg = "Button 2 was most recently clicked"
    elif "btn-nclicks-3" == ctx.triggered_id:
        msg = "Button 3 was most recently clicked"


# this call back function updates the graphs of pollutants in the analyze section
@app.callback(
            Output('air_pollutants', 'figure'),
            Input('second_dropdown', 'value')
        )
def analyze(Value):
    graph_4 = px.line(pollutants, x="Day", y=Value, title='Concentration of pollutants in Bishkek Air')
    return graph_4


# This callback function updates the first plot in the anaylze sections
@app.callback(
            Output('pollutant', 'figure'),
            Input('first_dropdown', 'value')
        )
def analyze(Value):
    graph_1 = px.line(bishkek_data, x="Date", y=Value, color='Specie', title='Bishkek City')
    return graph_1


if __name__ == "__main__":
    app.run_server(debug=True)