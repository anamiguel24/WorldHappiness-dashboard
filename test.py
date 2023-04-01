import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

# The app itself
#app = dash.Dash(__name__)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY])

app.layout = html.Div([
    dbc.Navbar([
        dbc.Col(
            html.A(
                html.Img(src='/assets/whr-logo.png', style={"margin-left": "10px"}, height="60px"),
                href="https://worldhappiness.report/"
            ),
            style={"textAlign": "left"}
        ),
        dbc.Col([
            dbc.Row([dbc.Col(html.H2('Worldwide Happiness',
                        #className='text-center',# mb-4',
                        style = {'textAlign': 'center'})),
                        ]),
            dbc.Row([dbc.Col(html.Center('Contributors: Ana Miguel Sal (20221645), Ana Rita Viseu (2022xxxx), Francisco Freitas (2022xxxx)'))]),
        ], width=10, align='center'),
        dbc.Col(
            html.A(
                html.Img(src='/assets/Nova_IMS.png', style={"margin-right": "10px"}, height='60px'),
                href="https://www.novaims.unl.pt/"
            ),
            style={"textAlign": "right"}
        ),
    ], className="w-100", sticky="top"),

    dbc.Container([
        dbc.Row([
            html.Br(),
            dbc.Col([
                html.Br(),
                dbc.Container([
                    html.Center(dcc.Graph(id='map', figure={})),
                    html.Br(),
                    dbc.Row(dbc.Container([html.Center(
                        'Cenas da vida')],
                        className='pretty_box2')),
                ])
            ], className='pretty_box'),

            dbc.Row(dbc.Container([html.Center(
                'Don\'t Worry, Be Happy')],
                className='pretty_box2'))
        ]),
        dbc.Row([
            dbc.Col(
                html.Div(
                    dcc.Graph(id='top5_bar', figure={}),
                    className='pretty_box2',
                ),
                #style={'display': 'inline-block'},
                width={'size': 6, 'order': 1},
            ),
            dbc.Col(
                html.Div(
                    dcc.Graph(id='bottom5_bar', figure={}),
                    className='pretty_box2',
                ),
                #style={'display': 'inline-block', 'padding-right': 10},
                width={'size': 6, 'order': 2},
            ),
        ]), #,align="center"),

        dbc.Row([
            html.Br(),
            dbc.Col([
                html.Br(),
                dbc.Container([
                    html.Center(dcc.Graph(id='map2', figure={})),
                ])
            ], className='pretty_box'),
        ]),
        dbc.Row([
            dbc.Col(
                html.Div(
                    dcc.Graph(id='parallel', figure={}),
                    className='pretty_box2',
                ),
                # style={'display': 'inline-block'},
                width={'size': 9, 'order': 1},
            ),
            dbc.Col(
                html.Div(
                    html.Img(src='/assets/world1.png', style={"margin": "auto"}, height='350px')
                ),
                style={
                    "display": "flex",
                    "justify-content": "center",
                    "align-items": "center",
                    "height": "400px"
                },
                # style={'display': 'inline-block', 'padding-right': 10},
                width={'size': 3, 'order': 2},
            ),
        ]),
        dbc.Row([
            dbc.Col(
                html.Div(
                    dcc.Graph(id='bar1', figure={}),
                    className='pretty_box2',
                ),
                # style={'display': 'inline-block'},
                width={'size': 6, 'order': 1},
            ),
            dbc.Col(
                html.Div(
                    dcc.Graph(id='bar2', figure={}),
                    className='pretty_box2',
                ),
                # style={'display': 'inline-block', 'padding-right': 10},
                width={'size': 6, 'order': 2},
            ),
        ]),

        ##
        #dbc.Tabs([dbc.Tab(tab1_content, label="Chart Analysis", active_label_style={"color": "#08BA14"})]),#,
                  #dbc.Tab(tab2_content, label="Audio Feature Statistics", active_label_style={"color": "#08BA14"})]),
    ], style={'backgroundColor': 'lightblue'}, fluid=True)

])

if __name__ == '__main__':
    app.run_server(debug=True, port=1337)