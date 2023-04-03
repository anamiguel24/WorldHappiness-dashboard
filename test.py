import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import pandas as pd
import plotly.graph_objs as go


############## Dataset Processing ##############

ds = pd.read_csv('dataset.csv')

ds.rename(columns={'Economy':'Economy (GDP per capita)', 'Family':'Social Support', 'Health':'Healthy Life Expectancy',
                     'Trust':'Corruption'}, inplace=True)  # Renaming columns

ds.drop(columns='Dystopia', inplace=True)  # Dropping column 'Dystopia'


############## Dash Core Components ##############

country_options = [dict(label=country, value=country) for country in ds['Country'].unique()]

continent_options = [{'label': 'Global', 'value': 'world'}, {'label': 'Europe', 'value': 'europe'},
                     {'label': 'Asia', 'value': 'asia'}, {'label': 'Africa', 'value': 'africa'},
                     {'label': 'North America', 'value': 'north america'}, {'label': 'South America', 'value': 'south america'}]

happiness_options = [dict(label=happiness, value=happiness) for happiness in ['Happiness Rank', 'Happiness Score']]

factor_options = [dict(label=factor, value=factor) for factor in ['Economy (GDP per capita)', 'Social Support',
                                                'Healthy Life Expectancy', 'Freedom', 'Generosity', 'Corruption']]

dropdown_country = dcc.Dropdown(
        id='country_drop',
        options=country_options,
        value=['Portugal'],
        multi=True
    )

dropdown_continent = dcc.Dropdown(
        id='continent_drop',
        clearable=False,
        searchable=False,
        options=continent_options,
        value='world',
    )

checklist_factor = dbc.Checklist(
    id='checklist_factor',
    options=factor_options,
    value=['Economy (GDP per capita)', 'Social Support'],
    switch=True#,
    #input_checked_style={"backgroundColor": "#08BA14"}
)

buttons_year = html.Div(
    [
        dbc.RadioItems(
            id="buttons_year",
            className="btn-group",
            inputClassName="btn-check",
            labelClassName="btn btn-outline-primary",
            labelCheckedClassName="active",
            options=[
                {"label": "2015", "value": 2015}, {"label": "2016", "value": 2016}, {"label": "2017", "value": 2017},
                {"label": "2018", "value": 2018}, {"label": "2019", "value": 2019}, {"label": "2020", "value": 2020},
                {"label": "2021", "value": 2021}, {"label": "2022", "value": 2022}, {"label": "2023", "value": 2023}
            ],
            value=2023,
            style={'padding-left': '0',},
            labelStyle={
                'border-top-right-radius': '0',
                'border-bottom-right-radius': '0',
                'border-top-left-radius': '0',
                'border-bottom-left-radius': '0',
                'margin-left': '-1px',
            },
        ),
        html.Div(id="output"),
    ],
    className="radio-group",
)




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
            dbc.Row([dbc.Col(html.Center('Contributors: Ana Miguel Sal (20221645), Ana Rita Viseu (20220703), Francisco Freitas (20220694)'))]),
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
                    dbc.Row([
                        html.Div([
                            buttons_year], style={'width': '60%'}, className='pretty_box'),
                        html.Div([dropdown_continent],
                                 style={'width': '40%'}, className='pretty_box')], style={'display': 'flex','width': '60%','padding-right':'20%','padding-left':'20%'}),
                    html.Center(dcc.Graph(id='Choropleth Map'))
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

####################

@app.callback(
    Output('Choropleth Map', 'figure'),

    [Input('buttons_year', 'value'),
     Input('continent_drop', 'value')]
)

def update_graph(year, continent):
    ds_filtered_year = ds.loc[ds['Year']==year]

    data_choropleth = dict(type='choropleth',
                           locations=ds_filtered_year['Country'],
                           locationmode='country names',
                           z=ds_filtered_year['Happiness Score'],
                           text=ds_filtered_year['Country'],
                           colorscale='thermal',
                           colorbar=dict(title='Happiness Score', len=0.75, tickfont=dict(color='black'),
                                         titlefont=dict(size=20, color='black')),
                           hovertemplate='Country: %{text} <br>' + 'Happiness Score: %{z}'
                           #name=''
                           )

    layout_choropleth = dict(geo=dict(scope=continent,  # default
                                      projection=dict(type='equirectangular'),
                                      landcolor='white',
                                      lakecolor='white',
                                      showocean=True,
                                      oceancolor='azure',
                                      #bgcolor='#f9f9f9',
                                      ),
                             width=1200,
                             height=820,
                             dragmode=False,
                             #margin=dict(l=0, r=0, b=100, t=0, pad=0),
                             #paper_bgcolor='rgba(0,0,0,0)',
                             #plot_bgcolor='rgba(0,0,0,0)'
                             )
    return go.Figure(data=data_choropleth, layout=layout_choropleth)


if __name__ == '__main__':
    app.run_server(debug=True, port=1337)