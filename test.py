import pandas as pd
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objs as go

############## Dataset Processing ##############
df = pd.read_csv('dataset.csv')
df_flags = pd.read_csv('flags_iso.csv')

df.rename(columns={'Economy':'Economy (GDP per capita)', 'Family':'Social Support', 'Health':'Healthy Life Expectancy',
                     'Trust':'Corruption'}, inplace=True)  # Renaming columns

df.drop(columns='Dystopia', inplace=True)  # Dropping column 'Dystopia'

############## Dash Core Components ##############
happiness_factors = ['Economy (GDP per capita)', 'Social Support',
                     'Healthy Life Expectancy', 'Freedom', 'Generosity', 'Corruption']
Hhppiness_indicators = ['Happiness Rank','Happiness Score']

country_options = [dict(label=country, value=country) for country in df['Country'].unique()]
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

country3_drop = dcc.Dropdown(
        id='country3_drop',
        options=country_options,
        value=['Portugal','Germany','China'],
        multi=True,
        #placeholder='Select up to 3 options'
)

checklist_factor = dbc.Checklist(
    id='checklist_factor',
    options=factor_options,
    value=['Economy (GDP per capita)', 'Social Support'],
    switch=True,
    inline=True#,
    #input_checked_style={"backgroundColor": "#08BA14"}
)

buttons_year = html.Div([
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
    ], className="radio-group",
)


############## The app itself ##############
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
                    dbc.Row(
                        [
                            html.Div(dropdown_continent, style={'flex': '1'}, className='drop'),
                            html.Div(buttons_year, style={'flex': '2'})
                        ],
                        style={'display': 'flex', 'padding-right': '10%', 'padding-left': '10%','padding-bottom':'1%'}
                    ),
                    html.Center(dcc.Graph(id='Choropleth Map'))
                ])
            ], className='container-box'),

        ]),
        dbc.Row([
            dbc.Col(
                html.Div(
                    dcc.Graph(id='top5_bar', figure={}),
                    #className='container-box2',
                ),
                className='container-box2left',
                #style={'display': 'inline-block'},
                width={'size': 5, 'order': 1},
            ),
            dbc.Col(
                html.Div(
                    dcc.Graph(id='bottom5_bar', figure={}),
                    #className='container-box2',
                ),
                className='container-box2right',
                #style={'display': 'inline-block', 'padding-right': 10},
                width={'size': 5, 'order': 2},
            ),
        ], justify='center'), #,align="center"),

        dbc.Row([
            html.Br(),
            dbc.Col([
                html.Br(),
                dbc.Container([
                    html.Center(dcc.Graph(id='map2', figure={})),
                ])
            ], className='container-box'),
        ]),


        # Radar + imagem
        dbc.Row([
            dbc.Col(
                [
                    html.Div([
                       html.Div([
                            html.Label('Country Choice'),
                            country3_drop,
                        ], #id='Iteraction1',
                           #style={'width': '50%','padding-right':'25%','padding-left':'0%','padding-bottom':'2%'},
                           #className='drop'
                       ),
                    ]),
                    html.Div(
                        dcc.Graph(id='polar-graph'),
                       # id='polar-div'
                    ),
                ],
                # style={'display': 'inline-block'},
                width={'size': 7, 'order': 1},
                className='container-box',
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

        dbc.Container([
            dbc.Row(dbc.Container([html.Center(
                'Top 3 Countries')],
                className='pretty_box2')),
            html.Div([checklist_factor]),
            dbc.Row([
                html.Div([
                    html.H1('1.', style={'font-weight': 'normal'}),
                    html.H2(id='country1'),
                    html.H2(id='flag1')
                ], className='pretty_box', style={'flex': '1'}),
                html.Div([
                    html.H1('2.', style={'font-weight': 'normal'}),
                    html.H2(id='country2'),
                    html.H2(id='flag2')
                ], className='pretty_box', style={'flex': '2'}),
                html.Div([
                    html.H1('3.', style={'font-weight': 'normal'}),
                    html.H2(id='country3'),
                    html.H2(id='flag3')
                ], className='pretty_box', style={'flex': '3'}),
            ], )
        ]),

        ##
        #dbc.Tabs([dbc.Tab(tab1_content, label="Chart Analysis", active_label_style={"color": "#08BA14"})]),#,
                  #dbc.Tab(tab2_content, label="Audio Feature Statistics", active_label_style={"color": "#08BA14"})]),
    ], style={'backgroundColor': 'lightblue'}, fluid=True)

])

####################

@app.callback(
    Output('Choropleth Map', 'figure'),
    Output('top5_bar', 'figure'),
    Output('bottom5_bar', 'figure'),

    Input('buttons_year', 'value'),
    Input('continent_drop', 'value')
)

def update_graph(year, continent):
    # CHOROPLETH MAP
    ds_filtered_year = df.loc[df['Year']==year]

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

    # BAR CHARTS
    ds_filtered_continent = ds_filtered_year
    if continent == 'world':
        ds_filtered_continent = ds_filtered_continent
    elif continent == 'north america':
        ds_filtered_continent = ds_filtered_year.loc[ds_filtered_year['Continent'] == 'North America']
    elif continent == 'south america':
        ds_filtered_continent = ds_filtered_year.loc[ds_filtered_year['Continent'] == 'South America']
    else:
        ds_filtered_continent = ds_filtered_year.loc[ds_filtered_year['Continent'] == continent.capitalize()]

    # Top 5 Ranked Countries Bar Chart
    ds_top5 = ds_filtered_continent.sort_values('Happiness Rank', ascending=False).tail(5)[['Country','Happiness Score']]
    fig_top5 = go.Figure(data=[go.Bar(x=ds_top5['Happiness Score'], y=ds_top5['Country'], orientation='h',hovertemplate='Happiness Score: %{x}')])
    fig_top5.update_layout(plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(range=(4,8)))
    fig_top5.update_traces(marker_color='rgb(242,183,1)', marker_line_color='rgb(230,131,16)', marker_line_width=1.5, opacity=0.6)

    # Bottom 5 Ranked Countries Bar Chart
    ds_bottom5 = ds_filtered_continent.sort_values('Happiness Rank', ascending=False).head(5)[['Country', 'Happiness Score']]
    fig_bottom5 = go.Figure(data=[go.Bar(x=ds_bottom5['Happiness Score'],y=ds_bottom5['Country'],orientation='h',hovertemplate='Happiness Score: %{x}')])
    fig_bottom5.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    fig_bottom5.update_traces(marker_color='#0D2A63', marker_line_color='#222A2A', marker_line_width=1.5, opacity=0.6)

    return go.Figure(data=data_choropleth, layout=layout_choropleth), fig_top5, fig_bottom5


@app.callback(
    Output('country3_drop', 'value'),
    Input('country3_drop', 'value')
)
def update_selected_options(selected_options):
    if selected_options is None:
        return []
    if len(selected_options) == 0:
        selected_options = ['Portugal']
    if len(selected_options) > 3:
        selected_options.pop(0)
    return selected_options
def limitar_selecao(value):

    if len(value) > 3:
        value.pop(0)
        value.append(value[0])
    return value


# Polar Graph
@app.callback(
    Output('polar-graph', 'figure'),
    Input('country3_drop', 'value'),
    Input('buttons_year', 'value')
)
def update_radar_plot(country, year):
    ds_filtered_year = df[(df['Country'].isin(country)) & (df['Year'] == year)]
    df_filtered = ds_filtered_year[['Country', 'Economy (GDP per capita)', 'Social Support',
                     'Healthy Life Expectancy', 'Freedom', 'Generosity', 'Corruption']]
    df_filtered = df_filtered.melt(id_vars='Country', value_vars=happiness_factors, var_name='Factors', value_name='Score')

    df_country1 = df_filtered.groupby('Country').get_group(country[0])
    df_country2 = None
    df_country3 = None
    if len(country) >= 2:
        df_country2 = df_filtered.groupby('Country').get_group(country[1])
    if len(country) == 3:
        df_country3 = df_filtered.groupby('Country').get_group(country[2])


    fig = go.Figure(data=go.Scatterpolar(
        r=df_country1['Score'],
        theta=df_country1['Factors'],
        # color='Country',
        fill='toself',
        # marker_color='#ec647d',
        opacity=1,
        hoverinfo="text",
        text=df_country1['Factors'] + ': ' + df_country1['Score'].apply(lambda x: "{:.5f}".format(x)).astype(str),
        name=country[0],
    ))

    if df_country2 is not None:
        fig.add_trace(go.Scatterpolar(
            r=df_country2['Score'],
            theta=df_country2['Factors'],
            fill='toself',
            # marker_color='#fbd35f',
            opacity=1,
            hoverinfo="text",
            text=df_country2['Factors'] + ': ' + df_country2['Score'].apply(lambda x: "{:.5f}".format(x)).astype(str),
            name=country[1],
        ))
    if df_country3 is not None:
        fig.add_trace(go.Scatterpolar(
            r=df_country3['Score'],
            theta=df_country3['Factors'],
            fill='toself',
            hoverinfo='text',
            name=country[2],
            text=df_country3['Factors'] + ': ' + df_country3['Score'].apply(lambda x: "{:.5f}".format(x)).astype(str),

        ))

    fig.update_layout(
        polar=dict(
            # hole=0.05,
            # bgcolor='#ffffff',
            radialaxis=dict(
                visible=True,
                type='linear',  # 'linear',
                showticklabels=False,
                # ticks='',
                # autotypenumbers='strict',
                # autorange=False,
                # range=[0, 1.5],
                # angle=90,
                # line_close=True,
                showline=False,
                # gridcolor='black'
            ),
            angularaxis=dict(visible=True),
        ),
        # width=800,
        # height=500,
        # margin=dict(l=0, r=0, t=20, b=20),
        # template="plotly_dark",
        # plot_bgcolor='rgba(0, 0, 0, 0)',
        # paper_bgcolor='rgba(0, 0, 0, 0)',
        font_color="black",
        font_size=15

    )
    return fig

@app.callback(
    Output('country1', 'children'),
    Output('flag1', 'children'),
    Output('country2', 'children'),
    Output('flag2', 'children'),
    Output('country3', 'children'),
    Output('flag3', 'children'),

    Input('checklist_factor', 'value')
)

def update_top3(factors):
    factors.insert(0,'Country')
    df_filtered_factors=df.loc[df['Year']==2023,factors]
    #df_filtered_factors=df.loc[df['Year']==2023,factors].select_dtypes(include='number')
    df_filtered_factors['sum'] = df_filtered_factors.sum(axis=1)
    df_filtered_factors.sort_values('sum',ascending=False, inplace=True)

    # Flag image of Country 1
    country1 = df_filtered_factors.iloc[0,0]
    url_1 = df_flags.loc[df_flags.loc[df_flags['Country']==country1].index[0],'URL']
    flag_country1 = html.Img(src=url_1, style={'width': '100px', 'height': 'auto'})

    # Flag image of Country 2
    country2 = df_filtered_factors.iloc[1, 0]
    url_2 = df_flags.loc[df_flags.loc[df_flags['Country'] == country2].index[0], 'URL']
    flag_country2 = html.Img(src=url_2, style={'width': '100px', 'height': 'auto'})

    # Flag image of Country 3
    country3 = df_filtered_factors.iloc[2, 0]
    url_3 = df_flags.loc[df_flags.loc[df_flags['Country'] == country3].index[0], 'URL']
    flag_country3 = html.Img(src=url_3, style={'width': '100px', 'height': 'auto'})

    return country1, flag_country1, country2, flag_country2, country3, flag_country3


if __name__ == '__main__':
    app.run_server(debug=True, port=1337)