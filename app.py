import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Output, Input

data = pd.read_csv('vgsales.csv')
# sort by the "Year" column in the file
data['Year'] = pd.to_datetime(data['Year'], format='%Y')
data.sort_values('Year', inplace=True)

external_stylesheets = [
    {'href':'https://fonts.googleapis.com/css2?family=Montserrat&display=swap',
     'rel':'stylesheet'}
    ]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Video Games Sales Statistic'

# make layout for div components on the page with styling for each one
app.layout = html.Div(
    children=[
        html.Div(children=[
                html.H1(children='Video Games Sales', className='header-title'),
                html.P(children='Data statistic from more than 16,500 games',className='header-description')], className='header'),
        html.Div(children=[
                html.Div(children=[
                        html.Div(children='Genre', className='menu-title'),
                        dcc.Dropdown(
                            id='Genre-filter',
# take more options for dropdown menu and show a list of genres from file
                            options=[{'label': Genre, 'value': Genre}
                                for Genre in data.Genre.unique()],
                            value='Action',
                            clearable=False,
                            className='dropdown',
                        )
                    ],
                ),
            ], className='menu',
        ),
# select several charts and place them on one page
        html.Div(children=[
                dcc.Graph(id='na-chart', className='graph'),
                dcc.Graph(id='eu-chart', className='graph'),
                dcc.Graph(id='global-chart', className='graph')
            ], className='wrapper')
    ]
)

@app.callback(
    [Output('na-chart', 'figure'), Output('eu-chart', 'figure'), Output('global-chart', 'figure')],
    [Input('Genre-filter', 'value')]
)
def update_charts(Genre):
# filter all charts according the chosen genre
    filtered_data = data.loc[data.Genre == Genre]

    markertype = 'bar'
    markercolor = {'color': '#ff6768'}
    plotcolor = '#263859'
    fontcolor = '#F5F7FA'
    xaxis = {'title': 'Years', 'tickformat': '%Y'}
    yaxis = {'title': 'Quantity (mlns)'}

# create data for each graph (by region)
    na_figure = {
        'data': [
            {'x': filtered_data['Year'],
            'y': filtered_data['NA_Sales'],
            'type': markertype,
            'marker': markercolor},
        ],
        'layout': {'title': 'North America Sales', 'plot_bgcolor': plotcolor, 'paper_bgcolor': plotcolor, 'font': {'color': fontcolor}, 'xaxis': xaxis, 'yaxis': yaxis}
    }

    eu_figure = {
        'data': [
            {'x': filtered_data['Year'],
            'y': filtered_data['EU_Sales'],
            'type': markertype,
            'marker': markercolor},
        ],
        'layout': {'title': 'Europe Sales', 'plot_bgcolor': plotcolor, 'paper_bgcolor': plotcolor,'font': {'color': fontcolor}, 'xaxis': xaxis, 'yaxis': yaxis}
    }

    global_figure = {
        'data': [
            {'x': filtered_data['Year'],
            'y': filtered_data['Global_Sales'],
            'type': markertype,
            'marker': markercolor},
        ],
        'layout': {'title': 'Global Sales', 'plot_bgcolor': plotcolor, 'paper_bgcolor': plotcolor, 'font': {'color': fontcolor}, 'xaxis': xaxis, 'yaxis': yaxis}
    }
    return na_figure, eu_figure, global_figure

if __name__ == '__main__':
    app.run_server(debug=True)