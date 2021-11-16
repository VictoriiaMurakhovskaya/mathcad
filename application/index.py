import io
import json
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
import dash_daq as daq
from dash.dependencies import Input, Output, State
from application.dashboard import main_plot, update_plot, update_data, inputs
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
            dbc.Col(id='params', children=[inputs()], md=4, width='auto'),
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
                       html.Div(id='dummy_2', hidden=True),
                       dcc.Store(id='result_json', storage_type='session'),
                       dcc.Store(id='data_json', storage_type='session'),
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
    [Output('eps', 'value'),
     Output('eps_b', 'value'),
     Output('L', 'value'),
     Output('L_t0', 'value'),
     Output('L_4', 'value'),
     Output('q', 'value'),
     Output('r_b', 'value'),
     Output('z_b', 'value')],
    Input('input_file', 'contents')
)
def update_inputs(contents):
    if contents:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        tickers = json.load(io.StringIO(decoded.decode('utf-8')))
        return tuple(tickers.values())
    else:
        return [dash.no_update] * 8


@app.callback(
    [Output("data_json", 'data'),
     Output("result_json", "data"),
     Output("main-plot", "children"),
     Output("nav_bar", "children")],
    [Input('launch', 'n_clicks'),
     Input('data_json', 'modified_timestamp'),
     Input('result_json', 'modified_timestamp')],
    [State('eps', 'value'),
     State('eps_b', 'value'),
     State('L', 'value'),
     State('L_t0', 'value'),
     State('L_4', 'value'),
     State('q', 'value'),
     State('r_b', 'value'),
     State('z_b', 'value'),
     State('data_json', 'data'),
     State('result_json', 'data')
     ]
)
def run_calc(n, calc_ts, result_ts,
             *args):
    _ctx = dash.callback_context.triggered[0]['prop_id']
    ctx, ctx_2 = _ctx.split('.')
    calc_data, result_data = args[-2], args[-1]

    if ctx == 'launch':
        if n:
            if n > 0:
                return {item: args[n] for n, item in enumerate(["eps", "eps_b", "L", "L_t0", "L_4", "q", "r_b", "z_b"])},\
                       dash.no_update, dash.no_update, RED_INDICATOR
            else:
                return dash.no_update, dash.no_update, dash.no_update, dash.no_update
        else:
            return dash.no_update
    elif ctx == 'data_json':
        if calc_data:
            calc_result = update_data(calc_data)
            return dash.no_update, calc_result,  dash.no_update,  dash.no_update
        else:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update
    elif ctx == 'result_json':
        if result_data:
            fig = update_plot(result_data)
            return dash.no_update,  dash.no_update,  fig,  GREEN_INDICATOR
        else:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update
    else:
        raise ValueError


@app.callback(
    Output('dummy', 'children'),
    Input('save', 'n_clicks'),
    [State('eps', 'value'),
     State('eps_b', 'value'),
     State('L', 'value'),
     State('L_t0', 'value'),
     State('L_4', 'value'),
     State('q', 'value'),
     State('r_b', 'value'),
     State('z_b', 'value')]
)
def save_values(n, *args):
    data_dic = {item: args[n] for n, item in enumerate(["eps", "eps_b", "L", "L_t0", "L_4", "q", "r_b", "z_b"])}
    with open('application/data/current.json', 'w') as fp:
        json.dump(data_dic, fp)
    return n


@app.server.route("/current.json")
def serve_static():
    return flask.send_file(os.getcwd()+'/application/data/current.json',
                           mimetype="application/json")
