import dash
import dash_core_components as dcc
from datetime import datetime as dt
import dash_html_components as html
from datetime import datetime, timedelta, date
from dash.dependencies import Output, Input

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Cycle Counting App'),

    html.Div(children='''
        Site
    '''),

dcc.Dropdown(
    options=[
        {'label': 'Scotford', 'value': 'SCT'}
    ],
    value='SCT'
),  

  html.Div(children='''
        Production Unit
    '''),

dcc.Dropdown(
    options=[
        {'label': 'Refinery', 'value': 'REF'},
        {'label': 'Chemicals', 'value': 'CHE'},
        {'label': 'Upgrader', 'value': 'UPG'}
    ],
    value='REF'
),  

  html.Div(children='''
        Equipment Tag No
    '''),

dcc.Dropdown(
    options=[
        {'label': 'GZ-3701', 'value': 'GZ3701'},
        {'label': 'V-2115', 'value': 'V2115'},
    ],
    value=''
),  

  html.Div(children='''
        Date Range <br>
    '''),

dcc.DatePickerRange(
    id='date-picker-range',
    start_date=dt(2019, 1, 1),
    min_date_allowed=date(2017, 6, 1),
    max_date_allowed=date.today(),
    end_date_placeholder_text='Select a date!'
),

  html.Div(children='''
        Time Interval (mins)
    '''),

dcc.Input(
    placeholder='Enter a value...',
    type='text',
    value=''
),  
dcc.RadioItems(
    options=[
        {'label': 'Pressure', 'value': 'PRE'},
        {'label': 'Temperature', 'value': 'TEM'}
    ],
    value=''
),  
 html.Button(
        id='button-update',
        children=['Submit Parameters']
    ),

])

# @app.callback(
#     [Output('my-date-picker-range', 'start_date'), Output('my-date-picker-range', 'end_date')],
#     [Input('button-update', 'n_clicks')])
# def update_output(n_clicks):
#     if n_clicks is not None and n_clicks > 0:
#         sd = datetime.strptime(start_date, '%Y-%m-%d')
#         ed = datetime.strptime(end_date, '%Y-%m-%d')
#         return start_date, end_date

if __name__ == '__main__':
    app.run_server(debug=True),
    app.run_server(dev_tools_hot_reload=False)