import io
import json
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
import dash_daq as daq
from dash.dependencies import Input, Output, State
from dashboard import control, main_plot, update_plot
import base64
import flask
import os

UPLOAD_DIRECTORY = "/"

RED_INDICATOR = daq.Indicator(id='my-indicator-1',
                              label={"label": "Йдуть обчислення",
                                     "style": {'font-weight': 'bold', 'color': '#FF0000'}},
                              labelPosition="bottom",
                              value=True,
                              color="#FF0000")

GREEN_INDICATOR = daq.Indicator(id='my-indicator-1',
                                label={"label": "Оновлено",
                                       "style": {'font-weight': 'bold', 'color': '#00FF00'}},
                                labelPosition="bottom",
                                value=True,
                                color="#00FF00")


def navBar():
    navbar = dbc.NavbarSimple(
        id='nav_bar',
        children=[GREEN_INDICATOR],
        brand="Розрахунок електричного поля кільватерного сліду",
        brand_href="/",
        color='DodgerBlue',
        dark=True,
    )
    return navbar


def dashboard():
    layout = dbc.Container([
        dbc.Row([
            dbc.Col(id='params', children=[control()], md=4, width='auto'),
            dbc.Col(id='main-plot', children=[main_plot()], md=8, width='auto')])
    ], fluid=True)
    return layout


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True
app.layout = html.Div([dcc.Location(id='loc', refresh=True),
                       dcc.Interval(id='run-timer', interval=1000, disabled=True),
                       navBar(),
                       html.Div(id='page-content', children=[dashboard()]),
                       dbc.Modal(
                           [
                               dbc.ModalHeader("Відомості про модель"),
                               dbc.ModalBody(html.Img(src=app.get_asset_url('model.png'))),
                               dbc.ModalFooter(
                                   dbc.Button("Закрити", outline=True, id="close", color='info', className="ml-auto")
                               ),
                           ],
                           id="modal", size='xl'
                       ),
                       html.Div(id='dummy', hidden=True),
                       dcc.Store(id='data_json')

                       ])


@app.callback(
    Output("modal", "is_open"),
    [Input("help", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    [Output('zb-slider', 'value'),
     Output('rb-slider', 'value'),
     Output('eps-slider', 'value'),
     Output('epsb-slider', 'value')],
    Input('input_file', 'contents')
)
def update_sliders(contents):
    if contents:
        content_type, content_string = contents.split(',')

        decoded = base64.b64decode(content_string)
        tickers = json.load(io.StringIO(decoded.decode('utf-8')))
    else:
        with open('application/data/default.json', 'r') as fp:
            tickers = json.load(fp)

    return tickers['zb'], tickers['rb'], tickers['eps'], tickers['epsb']


@app.callback(
    Output("main-plot", "children"),
    Input("data_json", "data")
)
def update_main_graph(data):
    pass


@app.callback(
    [Output("data_json", 'data'),
     Output("nav_bar", "children")],
    Input('launch', 'n_clicks'),
    [State('zb-slider', 'value'),
     State('rb-slider', 'value'),
     State('eps-slider', 'value'),
     State('epsb-slider', 'value'),
     ]
)
def update_main_graph(n, zb, rb, eps, epsb):
    if n:
        if n > 0:
            return None, RED_INDICATOR
        else:
            return None, GREEN_INDICATOR
    else:
        return None, GREEN_INDICATOR


@app.callback(
    Output('dummy', 'children'),
    Input('save', 'n_clicks'),
    [State('zb-slider', 'value'),
     State('rb-slider', 'value'),
     State('eps-slider', 'value'),
     State('epsb-slider', 'value'),
     ]
)
def save_values(n, zb, rb, eps, epsb):
    data_dic = {'zb': zb, 'rb': rb, 'eps': eps, 'epsb': epsb}
    with open('application/data/current.json', 'w') as fp:
        json.dump(data_dic, fp)
    return n


@app.server.route("/current.json")
def serve_static():
    return flask.send_file(os.getcwd()+'/application/data/current.json',
                           mimetype="application/json")


if __name__ == '__main__':
    app.run_server(debug=True)
