# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash_table import DataTable

from dash.dependencies import Input, Output, State

import pandas as pd

from datetime import date, datetime, timedelta
import time

url = 'https://github.com/plotly/datasets/raw/master/26k-consumer-complaints.csv'

rawDf = pd.read_csv(url)
df = rawDf.to_dict("rows"),

app = dash.Dash()
app.scripts.config.serve_locally = True

app.layout = html.Div(children=[
    html.Button(
        id='button-update',
        children=['Update']
    ),
    dcc.DatePickerRange(
        id='my-date-picker-range',
        min_date_allowed=date(2018, 12, 14),
        max_date_allowed=date.today(),
        start_date=date.today() - timedelta(days=7),
        end_date=date.today(),
        display_format='D/M/Y'
    ),
    dcc.Loading(
        id="loading-1",
        children=[
            DataTable(
                id='datatable-weapons',
                columns=[{"name": i, "id": i, "type": "numeric", 'format': {'locale': {'group': '.', 'decimal': ','}}} for i in rawDf.columns],
                data=[]
            )
        ]
    )])

@app.callback(
    [Output('my-date-picker-range', 'start_date'), Output('my-date-picker-range', 'end_date')],
    [Input('button-update', 'n_clicks')])
def update_output(n_clicks):
    if n_clicks is not None and n_clicks > 0:
        start_date = date(2019, 2, 12)
        end_date = date.today()
        return start_date, end_date

    return date(2019, 2, 23), date(2019, 2, 27)

@app.callback(
    [Output('datatable-weapons', 'data')],
    [Input('my-date-picker-range', 'start_date'), Input('my-date-picker-range', 'end_date')])
def update_graph(begin_dt, end_dt):
    begin_date = datetime.strptime(begin_dt, '%Y-%m-%d')
    end_date = datetime.strptime(end_dt, '%Y-%m-%d')
    days = (end_date - begin_date).days

    rawDfSlice = rawDf[0:days]
    dfSlice = rawDfSlice.to_dict("rows")

    time.sleep(5)

    return (dfSlice,)

if __name__ == "__main__":
    app.run_server(port=8053)