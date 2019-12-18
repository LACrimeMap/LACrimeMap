import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.express as px
from datetime import datetime as dt
import plotly.graph_objects as go
from dateutil.relativedelta import * 
from database import fetch_all_crime_as_df 

# Definitions of constants. This projects uses extra CSS stylesheet at `./assets/style.css`
COLORS = ['rgb(67,67,67)', 'rgb(115,115,115)', 'rgb(49,130,189)', 'rgb(189,189,189)', 'rgb(240,240,240)']

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', '/assets/style.css']

# Define the dash app first
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Define component functions
def page_header():
    """
    Returns the page header as a dash `html.Div`
    """
    return html.Div(id='header', children=[
        html.Div([html.H3('Visualization with datashader and Plotly')],
                 className="ten columns"),
        html.A([html.Img(id='logo', src=app.get_asset_url('github.png'),
                         style={'height': '35px', 'paddingTop': '7%'}),
                html.Span('MLEers', style={'fontSize': '2rem', 'height': '35px', 'bottom': 0,
                                                'paddingLeft': '4px', 'color': '#a3a7b0',
                                                'textDecoration': 'none'})],
               className="two columns row",
               href='https://github.com/LACrimeMap/LACrimeMap'),
    ], className="row")


def description():
    """
    Returns overall project description in markdown
    """
    return html.Div(children=[dcc.Markdown('''
        # Crime rates in Los Angeles 
        Predicting criminal activity is a fundamental challenge to police 
        across the country. Attempting to adjust policy to crime rates haphazardly 
        can lead to innumerable issues, including over-policing of disadvantaged 
        neighborhoods, failure to protect citizens, or a loss of trust between 
        citizens and the police force. When using algorithmic methods to asses 
        crime rates, clear and well-understood data is critical to avoiding the 
        pitfalls that, when they occur in an institution as significant as criminal 
        justice, can cause significant harms.
        To this end, **LA Crime Map is an exploratory tool that can be used to 
        visualize trends in LA Crime data.** The data can be explored using the 
        quantity of crime, the type of crime, specific areas, and geographic data.
        ## Data Source
        LA Crime Rate analysis uses data from [Los Angeles Open Data](https://data.lacity.org/).
        The [data source](https://data.lacity.org/A-Safe-City/Arrest-Data-from-2010-to-Present/yru6-6re4) 
        **updates weekly**. 
        Prepared By:      
        Weihao Zhou, 
        Kaiwen Yang, 
        Xu Han, 
        Laura McCallion .   
        [About Page](https://docs.google.com/document/d/1zEYKkCu6WQKGqgfMlu1XxCjlVlqwyZc5B_qrF5GeYf8/edit?usp=sharing)
        ''', className='eleven columns', style={'paddingLeft': '5%'})
    ], className="row")



def what_if_description():
    """
    Returns description of top five crime incidences in different timeframe - the interactive component
    """
    return html.Div(children=[
        dcc.Markdown('''
        ## Explore crime rates trend in the last two years
        Does a particular month/season/year see more crimes than others? Use this tool to explore how the nunber of top five crimes 
        changes from month to month. The total count of crime for each month will be displayed. Day of the month is not considered. The return
        result will include the start month and end month. 
        ''', className='eleven columns', style={'paddingLeft': '5%'})
    ], className="row")


def what_if_tool():
    """
    Returns the What-If tool as a dash `html.Div`. The view is a 8:3 division between
    demand-supply plot and rescale sliders.
    """
    return html.Div(children=[
        html.Div(children=[dcc.Graph(id='what-if-figure')], className='nine columns'),

        html.Div(children=[
            html.H5("Crime Rates Time Frame", style={'marginTop': '2rem'}),
            html.Div(children=[
                dcc.DatePickerRange(id='my-date-picker-range', min_date_allowed=dt(2018, 1, 1), max_date_allowed=dt(2019, 12, 13), initial_visible_month=dt(2019, 10, 1),
                start_date = dt(2018,12,1), end_date=dt(2019, 8, 1))
            ], style={'marginTop': '5rem', 'width':'40%'}),
        ], className='three columns', style={'marginLeft': 5, 'marginTop': '15%'}),
    ], className='row eleven columns')

def crime_map_description():
    """
    Returns the description of crime map.
    """
    return html.Div(children=[
        dcc.Markdown('''
        # " What If "
        crime heatmap
        ''', className='eleven columns', style={'paddingLeft': '5%'})
    ], className="row")

def crime_map_tool():
    """
    Returns the What-If tool as a dash `html.Div`. The view is a 8:3 division between
    demand-supply plot and rescale sliders.
    """
    return html.Div(children=[
        html.Div(children=[dcc.Graph(id='what-if-crime')], className='ten columns'),

        html.Div(children=[
            html.H5("Crime Rates Time Frame", style={'marginTop': '2rem'}),
            html.Div(children=[
                dcc.DatePickerRange(id='crime-date-picker-range', min_date_allowed=dt(2018, 1, 1), max_date_allowed=dt(2019, 12, 13), initial_visible_month=dt(2019, 10, 1),
                start_date = dt(2019,11,1), end_date=dt(2019, 11, 30))
            ], style={'marginTop': '5rem', 'width':'20%'}),
            html.Div(children=[
                dcc.Dropdown(
                id='crime-dropdown',
                options=[
                        {'label': 'Non-Violent Crimes', 'value': 'non_violent'},
                        {'label': 'Violent Crimes', 'value': 'violent'}],
                        value='non_violent')
            ], style={'marginTop': '5rem', 'width':'20%'}),
            html.Div(id='dd-output-container'),
        ], className='three columns', style={'marginLeft': 5, 'marginTop': '15%'}),
    ], className='row eleven columns')


def architecture_summary():
    """
    Returns the text and image of architecture summary of the project.
    """
    return html.Div(children=[
        dcc.Markdown('''
            # Project Architecture
            This project uses MongoDB as the database. All data acquired are stored in raw form to the
            database (with de-duplication). An abstract layer is built in `database.py` so all queries
            can be done via function call. For a more complicated app, the layer will also be
            responsible for schema consistency. A `plot.ly` & `dash` app is serving this web page
            through. Actions on responsive components on the page is redirected to `app.py` which will
            then update certain components on the page.  
        ''', className='row eleven columns', style={'paddingLeft': '5%'}),

        html.Div(children=[
            html.Img(src="https://docs.google.com/drawings/d/e/2PACX-1vQNerIIsLZU2zMdRhIl3ZZkDMIt7jhE_fjZ6ZxhnJ9bKe1emPcjI92lT5L7aZRYVhJgPZ7EURN0AqRh/pub?w=670&amp;h=457",
                     className='row'),
        ], className='row', style={'textAlign': 'center'}),

        dcc.Markdown('''
        
        ''')
    ], className='row')


# Sequentially add page components to the app's layout
def dynamic_layout():
    return html.Div([
        page_header(),
        html.Hr(),
        description(),
        #dcc.Graph(id='stacked-trend-graph', figure=static_stacked_trend_graph(stack=False)),
        what_if_description(),
        what_if_tool(),
        crime_map_description(),
        crime_map_tool(),
        architecture_summary(),
    ], className='row', id='content')


# set layout to a function which updates upon reloading
app.layout = dynamic_layout

@app.callback(
    dash.dependencies.Output('what-if-figure', 'figure'),
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')])
def what_if_handler(startdate, enddate):
    """Changes the display graph of crime rates"""
    df = fetch_all_crime_as_df(allow_cached=True)
    if df is None:
        return go.Figure()
    c = df.groupby(['grp_description','month']).count()
    crime = ['Miscellaneous Other Violations', 'Narcotic Drug Laws', 'Aggravated Assault', 'Driving Under Influence', 'Other Assaults']
    start = pd.Timestamp(startdate)
    end = pd.Timestamp(enddate)
    start = pd.Timestamp(dt(start.year, start.month, 1))
    end = pd.Timestamp(dt(end.year, end.month, 1))
    month_range_num = round(((end - start).days)/30)
    test_axis = [start + relativedelta(months=+i) for i in range(month_range_num + 1)]
    title = 'Crime counts of top five categories'
    fig = go.Figure()
    for i, s in enumerate(crime):
        count_array = c.loc[s]['rpt_id']
        count = [count_array[x] for x in test_axis]
        fig.add_trace(go.Scatter(x=test_axis, y=count, mode='lines', name=s,
                                 line={'width': 2, 'color': COLORS[i]},
                                 stackgroup=False))
    fig.update_layout(template='plotly_dark', title=title,
                      plot_bgcolor='#23272c', paper_bgcolor='#23272c', yaxis_title='Number of crimes',
                      xaxis_title='Month')
    return fig  

@app.callback(
    dash.dependencies.Output('what-if-crime', 'figure'),
    [dash.dependencies.Input('crime-date-picker-range', 'start_date'),
     dash.dependencies.Input('crime-date-picker-range', 'end_date'),
     dash.dependencies.Input('crime-dropdown', 'value'),])
def crime_handler(startdate, enddate, crimetype):
    """Changes the display graph of crime rates"""
    df = fetch_all_crime_as_df(allow_cached=True)
    if df is None:
        return go.Figure()
    df.dropna(subset=['grp_description'],inplace=True)
    violent = ['Homicide','Aggravated Assault','Weapon (carry/poss)']
    df['crime_type'] = df['grp_description'].apply(lambda x:"violent" if x in violent else "non_violent")
    df['lat'] = pd.to_numeric(df['location_1'].apply(lambda x:x['latitude']))
    df['lon'] = pd.to_numeric(df['location_1'].apply(lambda x:x['longitude']))
    df_map = df[(df['arst_date'] <= enddate)&(df['arst_date'] >= startdate)&(df['crime_type']==crimetype)]
    title = 'Crime map'
    fig = px.scatter_mapbox(df_map, lat='lat', lon='lon', zoom=10, height=500, color='area_desc')
    
    fig.update_traces(marker=dict(size=12, opacity=0.5))
    fig.update_layout(mapbox_style="stamen-terrain")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},title=title)
    return fig  

@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('crime-dropdown', 'value')])
def update_output(value):
    return 'You have selected "{}"'.format(value)



if __name__ == '__main__':
    app.run_server(debug=True, port=1050, host='0.0.0.0')