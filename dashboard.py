import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq
import plotly.graph_objs as go
from calc import MainCalc

alg_lst = [{'label': 'Nearest Neighbor', 'value': 'NN'},
           {'label': 'Christofides Algorithm', 'value': 'CA'}]


def control():
    """
    Algorithm and number of nodes choice
    :return: dash loyout
    """
    main_controls = dbc.Card([
        dbc.Row(children=[
            html.Label(id='alg-choice',
                       children=['Выбор параметров задачи'],
                       style={'margin-left': '15px', 'vertical-align': 'bottom', 'font-weight': 'bold', 'color': 'DodgerBlue'})
        ],
            style={'margin-bottom': '10px', 'margin-left': '4px'}
        ),
        dbc.Row(children=[dbc.Col(children=[dcc.Slider(id='zb-slider',
                                                       min=4,
                                                       max=20,
                                                       marks={i: 'z_b' if i == 4 else str(i) for i in
                                                              range(4, 21)},
                                                       value=1)])],
                style={'margin-bottom': '10px', 'margin-top': '10px'}
                ),
        dbc.Row(children=[dbc.Col(children=[dcc.Slider(id='rb-slider',
                                                       min=4,
                                                       max=20,
                                                       marks={i: 'r_b ' if i == 4 else str(i) for i in
                                                              range(4, 21)},
                                                       value=1)])],
                style={'margin-bottom': '10px', 'margin-top': '10px'}
                ),
        dbc.Row(children=[dbc.Col(children=[dcc.Slider(id='eps-slider',
                                                       min=4,
                                                       max=20,
                                                       marks={i: 'eps ' if i == 4 else str(i) for i in
                                                              range(4, 21)},
                                                       value=1)])],
                style={'margin-bottom': '10px', 'margin-top': '10px'}
                ),
        dbc.Row(children=[dbc.Col(children=[dcc.Slider(id='epsb-slider',
                                                       min=4,
                                                       max=20,
                                                       marks={i: 'eps_b ' if i == 4 else str(i) for i in
                                                              range(4, 21)},
                                                       value=1)])],
                style={'margin-bottom': '10px', 'margin-top': '10px'}
                ),
        dbc.Row(children=[
            dbc.Button('Обновить', outline=True, id='launch', color='success', className='mr-1',
                       style={'width': '100px', 'margin': '5px'}),
            dbc.Button('Загрузить', outline=True, id='load', color='primary', className='mr-1',
                       style={'width': '100px', 'margin': '5px'}),
            dbc.Button('Инфо', outline=True, id='help', color='info', className='mr-1',
                       style={'width': '100px', 'margin': '5px'})
        ], justify='center'
        )
    ], style={"margin-top": "15px"}, body=True)
    return main_controls


def main_plot(**kwargs):
    """
    :return: graph layout
    """
    mc = MainCalc(zb=0.015, rb=0.015, eps=1.725, eps_b=1e6 * 1.6e-12, q=-2e-9 * 3e9, r=0.0001, ksi_max=2, ksi_step=0.006)
    x, y = mc.E0_vector()

    fig = go.Figure(data=[go.Scatter(x=x, y=y)])
    layout = dcc.Graph(
        id='graph',
        figure=fig
    )
    return layout
