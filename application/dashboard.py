from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

import pandas as pd
import numpy as np
import json
import pathlib

import plotly.graph_objs as go
from application.calc import MainCalc

with open(pathlib.Path(__file__).parent.resolve() / 'data/default.json') as f:
    default_data = json.load(f)


def inputs():
    numeric_inputs = \
        dbc.Card(
            [dbc.Row(children=[
                html.Label(id='alg-choice',
                           children=['Вибір параметрів задачі'],
                           style={'vertical-align': 'bottom',
                                  'font-weight': 'bold', 'color': 'DodgerBlue', "text-align": "center"})
            ], style={'margin-bottom': '10px'}),
                dbc.Row(children=[
                    dbc.Col(children=[
                        dbc.Row(children=[
                            html.Label('z_b', style={"size": "30%"}),
                            dbc.Input(id='z_b',
                                      type="number",
                                      placeholder='z_b',
                                      min=0,
                                      max=100,
                                      value=default_data['z_b'],
                                      debounce=True,
                                      style={"size": "70%"})

                        ]),
                        dbc.Row(children=[
                            html.Label('r_b', style={"size": "30%"}),
                            dbc.Input(id='r_b',
                                      type="number",
                                      placeholder='r_b',
                                      min=0,
                                      max=0.4,
                                      value=default_data['r_b'],
                                      debounce=True,
                                      style={"size": "70%"})
                        ]),
                        dbc.Row(children=[
                            html.Label('eps', style={"size": "30%"}),
                            dbc.Input(id='eps',
                                      type="number",
                                      placeholder='eps',
                                      min=0.5,
                                      max=3,
                                      value=default_data['eps'],
                                      debounce=True,
                                      style={"size": "70%"})

                        ]),
                        dbc.Row(children=[
                            html.Label('eps_b', style={"size": "30%"}),
                            dbc.Input(id='eps_b',
                                      type="number",
                                      placeholder='eps_b',
                                      min=0,
                                      max=5e-6,
                                      value=default_data['eps_b'],
                                      debounce=True,
                                      style={"size": "70%"})

                        ])
                    ], style={"margin-left": "10px", "margin-right": "1opx"}),
                    dbc.Col(children=[
                        dbc.Row(children=[
                            html.Label('L_t0', style={"size": "30%"}),
                            dbc.Input(id='L_t0',
                                      type="number",
                                      placeholder='L_t0',
                                      min=0,
                                      max=default_data['L'],
                                      value=default_data['L_t0'],
                                      debounce=True,
                                      style={"size": "70%"})

                        ]),
                        dbc.Row(children=[
                            html.Label('q', style={"size": "30%"}),
                            dbc.Input(id='q',
                                      type="number",
                                      placeholder='q',
                                      min=-1000,
                                      max=0,
                                      value=default_data['q'],
                                      debounce=True,
                                      style={"size": "70%"})

                        ]),
                        dbc.Row(children=[
                            html.Label('L', style={"size": "30%"}),
                            dbc.Input(id='L',
                                      type="number",
                                      placeholder='L',
                                      min=0,
                                      max=1,
                                      value=default_data['L'],
                                      debounce=True,
                                      style={"size": "70%"})

                        ]),
                        dbc.Row(children=[
                            html.Label('L4', style={"size": "30%"}),
                            dbc.Input(id='L_4',
                                      type="number",
                                      placeholder='L4',
                                      min=0,
                                      max=0.01,
                                      value=default_data['L_4'],
                                      debounce=True,
                                      style={"size": "70%"})

                        ]),
                    ], style={"margin-right": "10px", "margin-left": "10px"})
                ]),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button('Оновити', outline=True, id='launch', color='success'),
                            dcc.Upload(id='input_file',
                                       children=[dbc.Button('Завантажити значення', outline=True, color='primary')],
                                       multiple=False)
                        ], className="d-grid gap-2", style={"margin": "0px"}),
                        dbc.Col([
                            dbc.Button('Інфо', outline=True, id='help', color='info'),
                            html.A(dbc.Button('Зберегти значення', id='save', outline=True, color='secondary'),
                                   href='/current.json', download='/current.json',
                                   style={"margin": "0px"})
                        ], className="d-grid gap-2")
                    ])], style={"margin-top": "20px", "margin-bottom": "10px"}),
            ], style={"margin-top": "20px", "margin-right": "20px"}, body=True)
    return numeric_inputs


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
    x, y = MainCalc(zb=json_dict['z_b'], rb=json_dict['r_b'], eps=json_dict['eps'], eps_b=json_dict['eps_b'],
                    q=json_dict['q'], L=json_dict['L'], L_4=json_dict['L_4'], L_t0=json_dict['L_t0'],
                    r=0.0001, ksi_max=0.56).get_data_for_plot()
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
