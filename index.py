import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output, State
from dashboard import control, main_plot


def navBar():
    navbar = dbc.NavbarSimple(
        children=[],
        brand="Величина электрического поля кильватерного следа",
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
                               dbc.ModalHeader("Сведения о модели"),
                               dbc.ModalBody(html.Img(src=app.get_asset_url('model.png'))),
                               dbc.ModalFooter(
                                   dbc.Button("Закрыть", outline=True, id="close", color='info', className="ml-auto")
                               ),
                           ],
                           id="modal", size='xl'
                       )

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


if __name__ == '__main__':
    app.run_server(debug=True)