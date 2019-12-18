import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
from datetime import datetime as dt
import plotly.graph_objects as go
from dateutil.relativedelta import * 
from database import fetch_all_crime_as_df 

# Definitions of constants. This projects uses extra CSS stylesheet at `./assets/style.css`
COLORS = ['rgb(0,0,0)','rgb(10,10,10)','rgb(15,15,15)','rgb(25,25,25)','rgb(35,35,35)', 'rgb(45,45,45)','rgb(55,55,55)',
          'rgb(65,65,65)','rgb(75,75,75)','rgb(85,85,85)','rgb(95,95,95)','rgb(105,105,105)','rgb(115,115,115)', 'rgb(125,67,67)',
          'rgb(135,130,135)', 'rgb(145,145,145)','rgb(155,145,145)','rgb(160,160,160)','rgb(170,170,170)','rgb(180,180,180)','rgb(189,189,189)',
         'rgb(200,195,195)','rgb(210,200,200)','rgb(220,210,210)','rgb(230,220,220)','rgb(240,240,240)','rgb(256,256,256)']
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
        ### Data Source
        LA Crime Rate analysis uses data from [Los Angeles Open Data](https://data.lacity.org/).
        The [data source](https://data.lacity.org/A-Safe-City/Arrest-Data-from-2010-to-Present/yru6-6re4) 
        **updates weekly**. 
        ''', className='eleven columns', style={'paddingLeft': '5%'})], className="row")

desc = ['Driving Under Influence', 'Moving Traffic Violations','Sex (except rape/prst)', 'Rape', 'Aggravated Assault', 'Burglary',
       'Prostitution/Allied', 'Robbery', 'Narcotic Drug Laws',
       'Miscellaneous Other Violations', 'Weapon (carry/poss)',
       'Other Assaults', 'Larceny', 'Disorderly Conduct',
       'Fraud/Embezzlement',  'Drunkeness',
       'Liquor Laws', 'Against Family/Child', 'Vehicle Theft',
        'Homicide', 'Gambling',
       'Receive Stolen Property', 'Forgery/Counterfeit',
       'Non-Criminal Detention', 'Pre-Delinquency',
       'Disturbing the Peace', 'Federal Offenses']
test_x_axis = ['2018-12','2019-1', '2019-2', '2019-3', '2019-4',
          '2019-5', '2019-6']

def static_stacked_trend_graph0(stack=False):
    """
    Returns scatter line plot of all power sources and power load.
    If `stack` is `True`, the 4 power sources are stacked together to show the overall power
    production.
    """
    df = fetch_all_crime_as_df()
    if df is None:
        return go.Figure()
    tot = [(df[df['grp_description']==c].shape[0], i) for i, c in enumerate(desc)]
    tot.sort(reverse=True)
    tot = tot[:5]
    c = df.groupby(['grp_description','month_string']).count()
    #x = df['month']
    x_axis = ['2018-12','2019-1','2019-2','2019-3','2019-4','2019-5', '2019-6', '2019-7', '2019-8', '2019-9', '2019-10', '2019-11']
    crime = [desc[x[1]] for x in tot]
    fig = go.Figure()
    for i, s in enumerate(crime):
        count_array = c.loc[s]['rpt_id']
        count = [count_array[x] for x in x_axis]
        fig.add_trace(go.Scatter(x=x_axis, y=count, mode='lines', name=s,
                                 line={'width': 2, 'color': COLORS[i]},
                                 stackgroup='stack' if stack else None))
    #fig.add_trace(go.Scatter(x=x, y=df['Load'], mode='lines', name='Load',
                             #line={'width': 2, 'color': 'orange'}))
    title = 'Crime incidences of each charge group'
    if stack:
        title += ' [Stacked]'

    fig.update_layout(template='plotly_dark',
                      title=title,
                      plot_bgcolor='#23272c',
                      paper_bgcolor='#23272c',
                      yaxis_title='Number of Crimes',
                      xaxis_title='Month')
    return fig


def static_stacked_trend_graph(stack=False):
    """
    Returns scatter line plot of all power sources and power load.
    If `stack` is `True`, the 4 power sources are stacked together to show the overall power
    production.
    """
    df = fetch_all_crime_as_df(allow_cached=True)
    if df is None:
        return go.Figure()
    tot = [(df[df['grp_description']==c].shape[0], i) for i, c in enumerate(desc)]
    tot.sort(reverse=True)
    tot = tot[:5]
    c = df.groupby(['grp_description','month']).count()
    #x = df['month'].unique()
    start = pd.Timestamp('2019-7-1')
    end = pd.Timestamp('2019-11-19')
    start = pd.Timestamp(dt(start.year, start.month, 1))
    end = pd.Timestamp(dt(end.year, end.month, 1))
    month_range_num = round(((end - start).days)/30)
    x_axis = [start + relativedelta(months=+i) for i in range(month_range_num + 1)]
    #x = df['month_string'].unique()
    crime = [desc[x[1]] for x in tot]
    fig = go.Figure()
    for i, s in enumerate(crime):
        count_array = c.loc[s]['rpt_id']
        count = [count_array[x] for x in x_axis]
        fig.add_trace(go.Scatter(x=x_axis, y=count, mode='lines', name=s,
                                 line={'width': 2, 'color': COLORS[i]},
                                 stackgroup='stack' if stack else None))
    #fig.add_trace(go.Scatter(x=x, y=df['Load'], mode='lines', name='Load',
                             #line={'width': 2, 'color': 'orange'}))
    title = 'Crime incidences of each charge group'
    if stack:
        title += ' [Stacked]'

    fig.update_layout(template='plotly_dark',
                      title=title,
                      plot_bgcolor='#23272c',
                      paper_bgcolor='#23272c',
                      yaxis_title='Number of Crimes',
                      xaxis_title='Date')
    return fig



def what_if_description():
    """
    Returns description of "What-If" - the interactive component
    """
    return html.Div(children=[
        dcc.Markdown('''
        # " What If "
        So far, BPA has been relying on hydro power to balance the demand and supply of power. 
        Could our city survive an outage of hydro power and use up-scaled wind power as an
        alternative? Find below **what would happen with 2.5x wind power and no hydro power at 
        all**.   
        Feel free to try out more combinations with the sliders. For the clarity of demo code,
        only two sliders are included here. A fully-functioning What-If tool should support
        playing with other interesting aspects of the problem (e.g. instability of load).
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

            html.Div(id='output-container-date-picker-range'),
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
        # dcc.Graph(id='trend-graph', figure=static_stacked_trend_graph(stack=False)),
        dcc.Graph(id='stacked-trend-graph', figure=static_stacked_trend_graph(stack=False)),
        what_if_description(),
        what_if_tool(),
        architecture_summary(),
    ], className='row', id='content')


# set layout to a function which updates upon reloading
app.layout = dynamic_layout


# Defines the dependencies of interactive components

# @app.callback(
#     dash.dependencies.Output('output-container-date-picker-range', 'children'),
#     [dash.dependencies.Input('my-date-picker-range', 'start_date'),
#      dash.dependencies.Input('my-date-picker-range', 'end_date')])
# def update_output(start_date, end_date):
#     string_prefix = 'You have selected: '
#     if start_date is not None:
#         start_date = dt.strptime(start_date.split(' ')[0], '%Y-%m-%d')
#         start_date_string = start_date.strftime('%B %d, %Y')
#         string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
#     if end_date is not None:
#         end_date = dt.strptime(end_date.split(' ')[0], '%Y-%m-%d')
#         end_date_string = end_date.strftime('%B %d, %Y')
#         string_prefix = string_prefix + 'End Date: ' + end_date_string
#     if len(string_prefix) == len('You have selected: '):
#         return 'Select a date to see it displayed here'
#     else:
#         return string_prefix

@app.callback(
    dash.dependencies.Output('what-if-figure', 'figure'),
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')])
def what_if_handler(startdate, enddate):
    """Changes the display graph of supply-demand"""
    df = fetch_all_crime_as_df(allow_cached=True)
    if df is None:
        return go.Figure()
    tot = [(df[df['grp_description']==c].shape[0], i) for i, c in enumerate(desc)]
    tot.sort(reverse=True)
    tot = tot[:5]
    c = df.groupby(['grp_description','month']).count()
    #x = df['month'].unique()
    crime = [desc[x[1]] for x in tot]
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

    #fig = go.Figure()
    #fig.add_trace(go.Scatter(x=x, y=supply, mode='none', name='supply', line={'width': 2, 'color': 'pink'},
                  #fill='tozeroy'))
    #fig.add_trace(go.Scatter(x=x, y=load, mode='none', name='demand', line={'width': 2, 'color': 'orange'},
                  #fill='tonexty'))
    fig.update_layout(template='plotly_dark', title=title,
                      plot_bgcolor='#23272c', paper_bgcolor='#23272c', yaxis_title='Number of crimes',
                      xaxis_title='Date')
    return fig  

if __name__ == '__main__':
    app.run_server(debug=True, port=1050, host='0.0.0.0')