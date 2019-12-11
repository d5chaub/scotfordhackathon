import dash
import dash_core_components as dcc
from datetime import datetime as dt
import dash_html_components as html

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

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

])

app.layout = html.Div([
    html.Div(dcc.Input(id='time-interval', type='text')),
    html.Button('Submit', id='button'),
    html.Div(id='output-container-button',
             children='Enter a value and press submit')
])


@app.callback(
    dash.dependencies.Output('output-container-button', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('time-interval', 'value')])

def update_output(n_clicks, value):
    return 'The time interval was "{}" and the button has been clicked {} times'.format(
        value,
        n_clicks
    ),

html.Div(children='''
        Analysis Type
    '''),

dcc.RadioItems(
    options=[
        {'label': 'Pressure', 'value': 'PRE'},
        {'label': 'Temperature', 'value': 'TEM'}
    ],
    value='MTL'
),  

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#app.layout = html.Div([
#    html.Div(dcc.Input(id='input-box', type='text')),
#    html.Button('Submit', id='button'),
#    html.Div(id='output-container-button',
#             children='Enter a value and press submit')
#])


#@app.callback(
#    dash.dependencies.Output('output-container-button', 'children'),
#    [dash.dependencies.Input('button', 'n_clicks')],
#    [dash.dependencies.State('input-box', 'value')])
#def update_output(n_clicks, value):
#    return 'The input value was "{}" and the button has been clicked {} times'.format(
#        value,
#        n_clicks
#    )

if __name__ == '__main__':
    app.run_server(debug=True),
    app.run_server(dev_tools_hot_reload=False)