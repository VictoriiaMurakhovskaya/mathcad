from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from calc import MainCalc
import pandas as pd
import numpy as np


def control():
    special_marks = {0: 'r_b'}
    special_marks.update({i: '{:.2f}'.format(i) for i in np.linspace(0.04, 0.4, 10)})
    main_controls = dbc.Card([
        dbc.Row(children=[
            html.Label(id='alg-choice',
                       children=['Вибір параметрів задачі'],
                       style={'margin-left': '15px', 'vertical-align': 'bottom', 'font-weight': 'bold', 'color': 'DodgerBlue'})
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
            dcc.Upload(id='input_file', children=[dbc.Button('Завантажити файл', outline=True, color='primary',
                                                             style={'width': '130px', 'margin': '5px'})],
                       multiple=False),
            html.A(dbc.Button('Записати файл', id='save', outline=True, color='secondary',
                              style={'width': '130px', 'margin': '5px'}),
                   href='/current.json', download='/current.json')
            ], justify='center'
        )
    ], style={"margin-top": "15px"}, body=True)
    return main_controls


def main_plot():
    """
    :return: graph layout
    """
    df = pd.read_pickle('data/temp.pickle')
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


def update_plot(**kwargs):
    """
    :return: graph layout
    """
    mc = MainCalc(zb=kwargs['zb'], rb=kwargs['rb'], eps=kwargs['eps'], eps_b=kwargs['epsb'],
                  q=-2e-9 * 3e9, r=0.0001, ksi_max=0.56)
    x, y = mc.E0_vector()
    df = pd.DataFrame({'x': x, 'y': y})
    df.to_pickle('data/temp.pickle')
    fig = go.Figure(data=[go.Scatter(x=x, y=y)])
    layout = dcc.Graph(
        id='graph',
        figure=fig
    )
    return layout

