import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.graph_objects as go

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
        As of today, 138 cities in the U.S. have formally announced 100% renewable energy goals or
        targets, while others are actively considering similar goals. Despite ambition and progress,
        conversion towards renewable energy remains challenging.
        Wind and solar power are becoming more cost effective, but they will always be unreliable
        and intermittent sources of energy. They follow weather patterns with potential for lots of
        variability. Solar power starts to die away right at sunset, when one of the two daily peaks
        arrives (see orange curve for load).
        **Energy Planner is a "What-If" tool to assist making power conversion plans.**
        It can be used to explore load satisfiability under different power contribution with 
        near-real-time energy production & consumption data.
        ### Data Source
        Energy Planner utilizes near-real-time energy production & consumption data from [BPA 
        Balancing Authority](https://www.bpa.gov/news/AboutUs/Pages/default.aspx).
        The [data source](https://transmission.bpa.gov/business/operations/Wind/baltwg.aspx) 
        **updates every 5 minutes**. 
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

def static_stacked_trend_graph(stack=False):
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
    c = df.groupby(['grp_description','month']).count()
    x = pd.to_datetime(df['month'].unique())
    crime = [desc[x[1]] for x in tot]
    fig = go.Figure()
    for i, s in enumerate(crime):
        count_array = c.loc[s]['rpt_id']
        count = [count_array[x] for x in test_x_axis]
        fig.add_trace(go.Scatter(x=x, y=count, mode='lines', name=s,
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
                      xaxis_title='Charge Group')
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
                dcc.RangeSlider(id='timerange-slider', min=0, max=13, step=None, value=[0,13], className='row',
                           marks= {0: '2018-12', 1: '2019-1', 2: '2019-2', 3: '2019-3', 4: '2019-4', 5: '2019-5',6: '2019-6',7: '2019-7',
                           8: '2019-8',9: '2019-9',10: '2019-10',11: '2019-11', 12:'2019-12'})
            ], style={'marginTop': '30rem'}),

            html.Div(id='timerange-text', style={'marginTop': '1rem'}),
        ], className='three columns', style={'marginLeft': 5, 'marginTop': '10%'}),
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
        dcc.Graph(id='stacked-trend-graph', figure=static_stacked_trend_graph(stack=True)),
        what_if_description(),
        what_if_tool(),
        architecture_summary(),
    ], className='row', id='content')


# set layout to a function which updates upon reloading
app.layout = dynamic_layout


# Defines the dependencies of interactive components

@app.callback(
    dash.dependencies.Output('timerange-text', 'children'),
    [dash.dependencies.Input('timerange-slider', 'value')])
def update_timerange_text(value):
    """Changes the display text of the time range slider"""
    return "Time Frame {:.2f}x".format(value)



@app.callback(
    dash.dependencies.Output('what-if-figure', 'figure'),
    [dash.dependencies.Input('timerange-slider', 'value')])
def what_if_handler(wind, hydro):
    """Changes the display graph of supply-demand"""
    df = fetch_all_crime_as_df(allow_cached=True)
    x = df['Month']
    supply = df['Wind'] * wind + df['Hydro'] * hydro + df['Fossil/Biomass'] + df['Nuclear']
    load = df['Load']

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=supply, mode='none', name='supply', line={'width': 2, 'color': 'pink'},
                  fill='tozeroy'))
    fig.add_trace(go.Scatter(x=x, y=load, mode='none', name='demand', line={'width': 2, 'color': 'orange'},
                  fill='tonexty'))
    fig.update_layout(template='plotly_dark', title='Supply/Demand after Power Scaling',
                      plot_bgcolor='#23272c', paper_bgcolor='#23272c', yaxis_title='MW',
                      xaxis_title='Date/Time')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=1050, host='0.0.0.0')