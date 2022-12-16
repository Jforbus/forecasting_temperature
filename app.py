## https://medium.com/analytics-vidhya/python-dash-data-visualization-dashboard-template-6a5bff3c2b76

import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
from Resources.config import mb_key

# mapbox api key
px.set_mapbox_access_token(mb_key)

# call in forecast info from csv
df = pd.read_csv("Resources/forecast_data.csv")

# lists for filters
dropdown_list = df['Location'].unique().tolist()
dropdown_date = df.Date.unique()

# the style arguments for the sidebar.
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '20%',
    'padding': '20px 10px',
    'background-color': '#f8f9fa'
}

# the style arguments for the main content page.
CONTENT_STYLE = {
    'margin-left': '25%',
    'margin-right': '5%',
    'padding': '20px 10p'
}

TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#191970'
}

CARD_TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#0074D9'
}

# create filter controls for sidebar
controls = dbc.Form(
    [
        dbc.Card([
            html.P('Map Controls', style={
                'textAlign': 'center', 'color': '#191970'
            }),
            html.P('Select Date:', style={
                'textAlign': 'Left', 'color': '#191970'
            }),
            dcc.Dropdown(dropdown_date, dropdown_date[3125],
                id='dropdown_date', maxHeight=100
            ),
            dbc.Button(
                id='submit_button_1',
                n_clicks=0,
                children='Submit',
                color='primary',
            ),
        ]),
        html.Br(),
        dbc.Card([
            html.P('Forecast Controls', style={
                'textAlign': 'center', 'color': '#191970'
            }),
            html.P('Select Location:', style={
                'textAlign': 'Left', 'color': '#191970'
            }),
            dcc.Dropdown(dropdown_list, dropdown_list[0],
                id='dropdown_location', maxHeight=100
            ),
            html.P('Select Start Date:', style={
                'textAlign': 'Left', 'color': '#191970'
            }),
            dcc.Dropdown(dropdown_date, dropdown_date[3125],
                id='dropdown_start', maxHeight=100
            ),
            html.P('Select End Date:', style={
                'textAlign': 'Left', 'color': '#191970'
            }),
            dcc.Dropdown(dropdown_date, dropdown_date[4368],
                id='dropdown_end', maxHeight=50
            ),
            html.Br(),
            dbc.Button(
                id='submit_button_2',
                n_clicks=0,
                children='Submit',
                color='primary'
            ),
        ]),
    ]
)



# create sidebar
sidebar = html.Div(
    [
        html.H4('Forecast Controls', style=TEXT_STYLE),
        html.Hr(),
        controls
    ],
    style=SIDEBAR_STYLE,
)

# create content layout

# Cards for Map
content_first_row = dbc.Row([
    dbc.Col(
        dbc.Card(
            [

                dbc.CardBody(
                    [
                        html.H4(children=['Forecasted Temperatures'], className='card-title',
                                style=CARD_TEXT_STYLE),
                        html.P(children=['Select Cities in North America'], style=CARD_TEXT_STYLE),
                    ]
                )
            ]
        ),
        md=6
    ),
    dbc.Col(
        dbc.Card(
            [

                dbc.CardBody(
                    [
                        html.H4(id='card_title_1', children=['Forecast Date:'], className='card-title', style=CARD_TEXT_STYLE),
                        html.P(id='card_text_1', children=['Select Date'], style=CARD_TEXT_STYLE),
                    ]
                ),
            ]

        ),
        md=6
    )
])


# content row for Map
content_second_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_1'), md=12
        )
    ]
)

# cards for Forecast
content_third_row = dbc.Row([
    dbc.Col(
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4('Forecast for City:', className='card-title', style=CARD_TEXT_STYLE),
                        html.P(id='card_text_2',children=['Select City'], style=CARD_TEXT_STYLE),
                    ]
                ),
            ]

        ),
        md=6
    ),
    dbc.Col(
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4('Dates Selected', className='card-title', style=CARD_TEXT_STYLE),
                        html.P(id='card_text_3', children=['Select Date Range'], style=CARD_TEXT_STYLE),
                    ]
                ),
            ]
        ),
        md=6
    )
])


# content row for city forecast
content_fourth_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_2'), md=12,
        )
    ]
)

# create content
content = html.Div(
    [
        html.H2('Forecasting Average Temperature By City in North America', style=TEXT_STYLE),
        html.Hr(),
        content_first_row,
        content_second_row,
        content_third_row,
        content_fourth_row
    ],
    style=CONTENT_STYLE
)

# create app, load styles, load content
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([sidebar, content])

# callbacks for updating content

# map update
@app.callback(
    Output('graph_1', 'figure'),
    [Input('submit_button_1', 'n_clicks')],
    [State('dropdown_date', 'value')])

def update_map(n_clicks, dropdown_value):
    # select data based on user date
    date_df = df[df['Date'] == dropdown_value]
    
    # get lat and lon from coordinates and cast as float ## get rid of this
    date_df['lat'] = [str.split(x)[0].strip("(,") for x in date_df['Coordinates']]
    date_df['lat'] = date_df['lat'].astype('float64')
    date_df['lon'] = [str.split(x)[1].strip(",)") for x in date_df['Coordinates']]
    date_df['lon'] = date_df['lon'].astype('float64')
    
    # round temps
    date_df['Predicted_Temp'] = round(date_df['Predicted_Temp'])
    
    # create plotly mapbox map
    fig = px.scatter_mapbox(date_df, lat=date_df.lat, 
                            lon=date_df.lon, color=date_df.Predicted_Temp, hover_name=date_df.Location,
                            zoom=2 )

    # update map layout
    fig.update_layout(
        font_color='#191970',
    )
    return fig


# Plot update
@app.callback(
    Output('graph_2', 'figure'),
    [Input('submit_button_2', 'n_clicks')],
    [State('dropdown_start', 'value'),
    State('dropdown_end', 'value'),
    State('dropdown_location', 'value')])

def update_figure(n_clicks, start_value, end_value, selected_city):
    
    city_df = df[df['Location'] == selected_city]
    city_df = city_df[city_df['Date'] >= start_value]
    city_df = city_df[city_df['Date'] <= end_value]

    fig = px.line(city_df, x="Date", y="Predicted_Temp")
    
    fig.update_layout(
        font_color='#191970'
    )

    return fig



if __name__ == '__main__':
    app.run_server(debug=True)