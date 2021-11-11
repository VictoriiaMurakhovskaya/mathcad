from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

import pandas as pd
import numpy as np
import json

import plotly.graph_objs as go
from application.calc import MainCalc


def control():
    special_marks = {0: 'r_b'}
    special_marks.update({i: '{:.2f}'.format(i) for i in np.linspace(0.04, 0.4, 10)})
    main_controls = dbc.Card([
        dbc.Row(children=[
            html.Label(id='alg-choice',
                       children=['Вибір параметрів задачі'],
                       style={'margin-left': '15px', 'vertical-align': 'bottom',
                              'font-weight': 'bold', 'color': 'DodgerBlue'})
        ],
            style={'margin-bottom': '10px', 'margin-left': '4px'}
        ),
        dbc.Row(children=[dbc.Col(children=[dcc.Slider(id='zb-slider',
                                                       min=0,
                                                       max=100,
                                                       marks={i: 'z_b' if i == 0 else str(i) for i in
                                                              range(0, 101, 10)},
                                                       value=1)])],
                style={'margin-bottom': '10px', 'margin-top': '10px'}
                ),
        dbc.Row(children=[dbc.Col(children=[dcc.Slider(id='rb-slider',
                                                       min=0,
                                                       max=0.39,
                                                       step=0.01,
                                                       marks=special_marks,
                                                       value=0.02)])],
                style={'margin-bottom': '10px', 'margin-top': '10px'}
                ),
        dbc.Row(children=[dbc.Col(children=[dcc.Slider(id='eps-slider',
                                                       min=0,
                                                       max=100,
                                                       marks={i: 'eps ' if i == 0 else str(i) for i in
                                                              range(0, 101, 10)},
                                                       value=1)])],
                style={'margin-bottom': '10px', 'margin-top': '10px'}
                ),
        dbc.Row(children=[dbc.Col(children=[dcc.Slider(id='epsb-slider',
                                                       min=0,
                                                       max=100,
                                                       marks={i: 'eps_b ' if i == 0 else str(i) for i in
                                                              range(0, 101, 10)},
                                                       value=1)])],
                style={'margin-bottom': '10px', 'margin-top': '10px'}
                ),
        dbc.Row(children=[
            dbc.Button('Оновити', outline=True, id='launch', color='success', className='mr-1',
                       style={'width': '130px', 'margin': '5px'}),
            dbc.Button('Інфо', outline=True, id='help', color='info', className='mr-1',
                       style={'width': '130px', 'margin': '5px'})
        ], justify='center'
        ),
        dbc.Row(children=[
            dcc.Upload(id='input_file', children=[dbc.Button('Завантажити файл', outline=True, color='primary')],
                       multiple=False),
            html.A(dbc.Button('Записати файл', id='save', outline=True, color='secondary'),
                   href='application/data/current.json', download='application/data/current.json')
        ], justify='center'
        )
    ], style={"margin-top": "15px"}, body=True)
    return main_controls


def main_plot():
    """
    :return: graph layout
    """
    df = pd.read_pickle('application/data/temp.pickle')
    x, y = df.x, df.y
    fig = go.Figure(data=[go.Scatter(x=x, y=y)])
    fig.update_layout(
        xaxis_title=r'ksi',
        yaxis_title=r'E0'
    )
    layout = dcc.Graph(
        id='graph',
        figure=fig
    )
    return layout


def update_data(json_dict):
    """
    :return: calculation data for dcc.Store
    """
    mc = MainCalc(zb=json_dict['zb'], rb=json_dict['rb'], eps=json_dict['eps'], eps_b=json_dict['epsb'],
                  q=-2e-9 * 3e9, r=0.0001, ksi_max=0.56)
    x, y = mc.E0_vector()
    df = pd.DataFrame({'x': x, 'y': y})
    df.to_pickle('application/data/temp.pickle')
    return {'x': list(x), 'y': list(y)}


def update_plot(xy_dict):
    fig = go.Figure(data=[go.Scatter(x=xy_dict['x'], y=xy_dict['y'])])
    layout = dcc.Graph(
        id='graph',
        figure=fig
    )
    return layout
