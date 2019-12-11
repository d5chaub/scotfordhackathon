import datetime
import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Input to graph'),
    dcc.Input(id='input', value='', type='text'),
    dcc.DatePickerRange(
        id='date-picker-range',
        start_date_placeholder_text='Select a starting date',
        end_date_placeholder_text='Select an ending date',
        start_date='',
        end_date=''
    ),

    html.Div(id='output-graph', style={
        'color': 'green'
    }),
])



@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='input', component_property='value'),
    Input(component_id='date-picker-range', component_property='start_date'),
    Input(component_id='date-picker-range', component_property='end_date')]
)
def update_value(input_data, start_date, end_date):
    start = start_date #datetime.datetime(2015, 1, 1)
    end = end_date #datetime.datetime.now()
    print(start, end)
    ### Code to plot the graph ###

if __name__ == '__main__':
    app.run_server(debug=True),
    app.run_server(dev_tools_hot_reload=False)