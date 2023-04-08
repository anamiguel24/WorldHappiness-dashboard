import pandas as pd
import numpy as np
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px

############## Dataset Processing ##############
df = pd.read_csv('dataset.csv')
df_flags = pd.read_csv('flags_iso.csv')

df_flags.loc[len(df_flags)]=['Hong Kong',np.nan,'HKG','https://www.worldometers.info/img/flags/hk-flag.gif']
df_flags['URL'].replace('https://www.worldometers.info//img/flags/small/tn_fi-flag.gif','https://www.worldometers.info/img/flags/fi-flag.gif', inplace=True)

df.rename(columns={'Economy':'Economy (GDP per capita)', 'Family':'Social Support', 'Health':'Healthy Life Expectancy',
                     'Trust':'Government Trust'}, inplace=True)  # Renaming columns

############## Dash Core Components ##############
happiness_factors = ['Economy (GDP per capita)', 'Social Support',
                     'Healthy Life Expectancy', 'Freedom', 'Generosity', 'Government Trust']
#happiness_indicators = ['Happiness Rank','Happiness Score']

country_options = [dict(label=country, value=country) for country in df['Country'].unique()]
continent_options = [{'label': 'Global', 'value': 'world'}, {'label': 'Europe', 'value': 'europe'},
                     {'label': 'Asia', 'value': 'asia'}, {'label': 'Africa', 'value': 'africa'},
                     {'label': 'North America', 'value': 'north america'}, {'label': 'South America', 'value': 'south america'}]

happiness_options = [dict(label=happiness, value=happiness) for happiness in ['Happiness Rank', 'Happiness Score']]

factor_options = [dict(label=factor, value=factor) for factor in ['Economy (GDP per capita)', 'Social Support',
                                                'Healthy Life Expectancy', 'Freedom', 'Generosity', 'Government Trust']]

dropdown_country = dcc.Dropdown(
        id='country_drop',
        options=country_options,
        value=['Portugal'],
        multi=True,
        clearable=False
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
)

dropdown_factor_1 = dcc.Dropdown(
        id='factor_drop_1',
        options=factor_options,
        clearable=False,
        value='Economy (GDP per capita)',
        multi=False
    )
dropdown_factor_2 = dcc.Dropdown(
        id='factor_drop_2',
        options=factor_options,
        clearable=False,
        value='Social Support',
        multi=False
    )

dropdown_factor_3 = dcc.Dropdown(
        id='factor_drop_3',
        options=factor_options,
        clearable=False,
        value='Economy (GDP per capita)',
        multi=False
)

slider_year=dcc.Slider(
    min=df['Year'].min(),
    max=df['Year'].max(),
    step=None,
    value=df['Year'].max(),
    marks={str(year): str(year) for year in df['Year'].unique()},
    id='year-slider')

checklist_factor = dbc.Checklist(
    id='checklist_factor',
    options=factor_options,
    value=['Economy (GDP per capita)', 'Social Support'],
    switch=True,
    inline=True#,
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
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LITERA])

################################ HEADER ######################
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
            dbc.Row([dbc.Col(html.H2('World Happiness',
                        style = {'textAlign': 'center','font-family':'Serif'})),
                        ]),
            dbc.Row([dbc.Col(html.Center('Contributors: Ana Miguel Sal (20221645), Ana Rita Viseu (20220703), Francisco Freitas (20220694)'))]),
        ], width=10, align='center',style={'font-family':'Serif'}),
        dbc.Col(
            html.A(
                html.Img(src='/assets/Nova_IMS.png', style={"margin-right": "10px"}, height='60px'),
                href="https://www.novaims.unl.pt/"
            ),
            style={"textAlign": "right"}
        ),
    ], className="w-100", sticky="top"),

################################ LAYOUT GRAPHIC Nº1 (Choropleth Map) ######################
    dbc.Container([
            html.Br(),
            dbc.Col([
                html.Br(),
                html.Div([
                    html.Div(dropdown_continent, style={'flex': '1'}, className='drop'),
                    html.Div(buttons_year, style={'flex': '2'})
                    ],style={'display': 'flex', 'padding-right': '10%', 'padding-left': '10%','padding-bottom':'1%'}),
                html.Br(),
                html.H1(id='map_title',style={'textAlign': 'center','font-family':'Serif','color':'LightSteelBlue'}),
                html.Br(),
                html.Center(dcc.Graph(id='Choropleth Map'))
            ], className='container-box'),

################################ LAYOUT GRAPHIC Nº2 and Nº3 (Top 5 best and worst Countries) ######################
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H2(id='top5_title',style={'textAlign': 'center','font-family':'Serif','color':'LightSteelBlue'}),
                    html.Br(),
                    dcc.Graph(id='top5_bar', figure={}),
                ]),
                className='container-box2left',
                width={'size': 5, 'order': 1},
            ),
            dbc.Col(
                html.Div([
                    html.H2(id='bottom5_title',style={'textAlign': 'center','font-family':'Serif','color':'LightSteelBlue'}),
                    html.Br(),
                    dcc.Graph(id='bottom5_bar', figure={}),
                ]),
                className='container-box2right',
                width={'size': 5, 'order': 2},
            ),
        ], justify='center'),

################################ LAYOUT GRAPHIC Nº4 (Bubble Plot) ######################
        dbc.Row([
            dbc.Col(
                html.Div(
                    html.Img(src='/assets/happy3.png', style={"margin": "auto"}, height='350px')
                ),
                style={
                    "display": "flex",
                    "justify-content": "center",
                    "align-items": "center",
                    #"transform": "scale(1.2)",
                    "margin-left": "55px",
                    "margin-right": "20px"
                },
                width={'size': 4, 'order': 1},
            ),
            dbc.Col([
                html.Br(),
                html.H2('How do different factors affect Happiness?',
                        style={'textAlign': 'center', 'font-family': 'Serif', 'color': 'LightSteelBlue'}),
                html.H2('And what is their relationship?',
                        style={'textAlign': 'center', 'font-family': 'Serif', 'color': 'LightSteelBlue'}),
                html.Div([
                    html.Div(html.Div([dropdown_factor_1]), style={'width': '48%', 'display': 'inline-block'}),
                    html.Div(html.Div([dropdown_factor_2]),
                             style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
                    html.Div([slider_year]),
                    html.Center(dcc.Graph(id='bubble_plot')),

                ]),
            ], width={'size': 7, 'order': 2}, className='container-bubble'
            ),
        ]),

################################ LAYOUT GRAPHIC Nº5 (Radar Plot) ######################
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.Br(),
                        html.H2(id='polar_title',style={'textAlign': 'center','font-family':'Serif','color':'LightSteelBlue'}),
                        html.Center('(You can change the year at the beginning)',style={'textAlign': 'center','font-family':'Serif','color':'LightSteelBlue'}),
                        html.Br(),
                        country3_drop,
                    ],
                    ),
                ]),
                html.Div(
                    dcc.Graph(id='polar-graph'),
                ),
            ],
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
                    "transform": "scale(1.2)"
                },
                width={'size': 3, 'order': 2},
            ),
        ]),

################################ LAYOUT GRAPHIC Nº6 and Nº7 (Ranking and Factors Evolution) ######################
        dbc.Row([
            dbc.Col([
                html.Br(),
                html.H2('How Happiness Rank and its Factors Evolved Throughout the Years',
                        style={'textAlign': 'center', 'font-family': 'Serif', 'color': 'LightSteelBlue'}),
                html.Div(
                    html.Div([dropdown_country]), style={'width': '49%', 'display': 'inline-block'}),
                html.Div(
                    html.Div([dropdown_factor_3]), style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
                html.Div(
                    [dcc.Graph(id='bar1'), ], style={'width': '50%', 'display': 'inline-block'}),
                html.Div(
                    [dcc.Graph(id='bar2'), ], style={'display': 'inline-block', 'width': '50%'}), ],
                className='container-box'),
        ]),

################################ LAYOUT GRAPHIC Nº8 (Top 3 Countries with Flags) ######################
        dbc.Container([
            html.Br(),
            dbc.Row(dbc.Container(
                [html.Br(),
                 html.H2('What are the best countries for you in 2023?',style={'textAlign': 'center','font-family':'Serif','color':'LightSteelBlue'})],
                className='container-box2')),
            html.Div(html.H4('Choose what you value most in a country:',style={'font-family':'Serif'})),
            html.Div([checklist_factor]),
            dbc.Row([
                html.Div([
                    html.H2(id='country1'),
                    html.H2(id='flag1')
                ], className='pretty_box', style={'flex': '1', 'display': 'inline-block'}),
                html.Div([
                    html.H2(id='country2'),
                    html.H2(id='flag2')
                ], className='pretty_box', style={'flex': '1', 'display': 'inline-block'}),
                html.Div([
                    html.H2(id='country3'),
                    html.H2(id='flag3')
                ], className='pretty_box', style={'flex': '1', 'display': 'inline-block'}),

            ]),
            html.Br(),
            html.Br(),
        ]),
    ], style={'backgroundColor': 'LightSteelBlue'}, fluid=True)

])

################################# GRAPHICS

################################### Choropleth Map; Top 5; Bottom 5 ############################
@app.callback(
    Output('Choropleth Map', 'figure'),
    Output('top5_bar', 'figure'),
    Output('bottom5_bar', 'figure'),
    Output('map_title', 'children'),
    Output('top5_title', 'children'),
    Output('bottom5_title', 'children'),

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
                           )
    layout_choropleth = dict(geo=dict(scope=continent,  # default
                                      projection=dict(type='equirectangular'),
                                      landcolor='white',
                                      lakecolor='white',
                                      showocean=True,
                                      oceancolor='azure',
                                      ),
                             width=1100,
                             height=450,
                             dragmode=False,
                             margin=dict(l=0, r=0, b=10, t=0, pad=0),
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
    fig_top5.update_layout(plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(range=(4,8)),height=300)
    fig_top5.update_traces(marker_color='rgb(242,183,1)', marker_line_color='rgb(230,131,16)', marker_line_width=1.5, opacity=0.6)

    # Bottom 5 Ranked Countries Bar Chart
    ds_bottom5 = ds_filtered_continent.sort_values('Happiness Rank', ascending=False).head(5)[['Country', 'Happiness Score']]
    fig_bottom5 = go.Figure(data=[go.Bar(x=ds_bottom5['Happiness Score'],y=ds_bottom5['Country'],orientation='h',hovertemplate='Happiness Score: %{x}')])
    fig_bottom5.update_layout(plot_bgcolor='rgba(0,0,0,0)',height=300)
    fig_bottom5.update_traces(marker_color='#0D2A63', marker_line_color='#222A2A', marker_line_width=1.5, opacity=0.6)

    # Choropleth Map Title
    title=''
    if continent=='world':
        title='Global'
    elif continent=='north america':
        title='North America'
    elif continent=='south america':
        title='South America'
    else:
        title=str(continent).capitalize()

    # Bar Charts Titles
    title_bar=''
    if continent=='world':
        title_bar=''
    elif continent=='europe':
        title_bar='European '
    elif continent=='asia':
        title_bar='Asian '
    elif continent=='africa':
        title_bar='African '
    elif continent=='north america':
        title_bar='North American '
    elif continent=='south america':
        title_bar='South American '

    return go.Figure(data=data_choropleth, layout=layout_choropleth), fig_top5, fig_bottom5,\
        title+' Happiness Score in '+str(year),\
        'Top 5 '+title_bar+'Countries in '+str(year), 'Bottom 5 '+title_bar+'Countries in '+str(year)

################################### BUBBLE PLOT ############################
@app.callback(
    Output('factor_drop_1', 'value'),
    Output('factor_drop_2', 'value'),

    Input('factor_drop_1', 'value'),
    Input('factor_drop_2', 'value')
)
def update_factors_dropdown(factor1, factor2):
    if (factor1!='Economy (GDP per capita)') & (factor1==factor2):
        factor1='Economy (GDP per capita)'
    elif (factor1=='Economy (GDP per capita)') & (factor1==factor2):
        factor1='Social Support'
    else:
        factor1=factor1
    return factor1, factor2

@app.callback(
    Output('bubble_plot', 'figure'),

    Input('year-slider', 'value'),
    Input('factor_drop_1', 'value'),
    Input('factor_drop_2', 'value')
)

def update_graph(year,factor_1, factor_2):
    ds_bubble_year = df.loc[(df['Year']==year)]

    x_axis=ds_bubble_year[factor_1]
    y_axis=ds_bubble_year[factor_2]

    fig = px.scatter(ds_bubble_year, x=x_axis, y=y_axis,size="Happiness Score",
                     hover_name="Country", log_x=False, size_max=5,height=350)

    fig.update_traces(mode='markers', marker=dict(sizemode="diameter",sizemin=1))
    fig.update_layout(paper_bgcolor='#f9f9f9',plot_bgcolor='#f9f9f9')

    return fig

################################### RADAR PLOT ############################
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

@app.callback(
    Output('polar-graph', 'figure'),
    Output('polar_title', 'children'),
    Input('country3_drop', 'value'),
    Input('buttons_year', 'value')
)
def update_radar_plot(country, year):
    ds_filtered_year = df[(df['Country'].isin(country)) & (df['Year'] == year)]
    df_filtered = ds_filtered_year[['Country', 'Economy (GDP per capita)', 'Social Support',
                     'Healthy Life Expectancy', 'Freedom', 'Generosity', 'Government Trust']]
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
        fill='toself',
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
            radialaxis=dict(
                visible=True,
                type='linear',
                showticklabels=False,
                showline=False,
            ),
            angularaxis=dict(visible=True),
        ),
        font_color="black",
        font_size=15
    )

    return fig, 'Country Comparison in '+str(year)

################################ Ranking Evolution and Factor Comparison Plot ############
@app.callback(
         Output('bar1', 'figure'),
         Output('bar2','figure'),

        [Input('country_drop', 'value'),
         Input("factor_drop_3", "value"),])
###################### First Line Plot (Ranking Evolution) #################
def plots(country,factor):
    data_rank = []
    data_factor = []
    for country in country:
        df_rank = df.loc[df['Country'] == country]
        df_factor= df.loc[df['Country'] == country]

        x_year_rank = df_rank['Year']
        y_rank = df_rank['Happiness Rank']

        x_year_factor = df_factor['Year']
        y_factor = df_factor[factor]

        data_rank.append(dict(type='scatter', x=x_year_rank, y=y_rank, name=country))
        data_factor.append(dict(type='scatter', x=x_year_factor, y=y_factor, name=country))

    layout_rank = dict(
                      xaxis=dict(title='Year'),
                      yaxis=dict(title='Happiness Rank', autorange='reversed'),
                      plot_bgcolor='#f9f9f9',
                      paper_bgcolor='#f9f9f9',
                      height=400,
                    width=580)


    layout_factor = dict(
                       xaxis=dict(title='Year'),
                       yaxis=dict(title=factor),
                       plot_bgcolor='#f9f9f9',
                       paper_bgcolor='#f9f9f9',
                       height=400,
                       width=580)

    return go.Figure(data=data_rank, layout=layout_rank), \
           go.Figure (data=data_factor, layout=layout_factor)

################################### FLAGS WITH TOP 3 COUNTRIES ############################
@app.callback(
    Output('checklist_factor', 'value'),
    Input('checklist_factor', 'value')
)
def update_selected_factors(selected_options):
    if selected_options is None:
        return []
    if len(selected_options) == 0:
        selected_options = ['Economy (GDP per capita)']
    if len(selected_options) > 5:
        selected_options.pop(0)
    return selected_options

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
    factors.insert(1,'CountryCode')
    df_filtered_factors=df.loc[df['Year']==2023,factors]
    df_filtered_factors['sum'] = df_filtered_factors.sum(axis=1, numeric_only=True)
    df_filtered_factors.sort_values('sum',ascending=False, inplace=True)

    # Flag image of Country 1
    country1 = df_filtered_factors.iloc[0,0]
    countrycode1 = df_filtered_factors.iloc[0,1]
    url_1 = df_flags.loc[df_flags.loc[df_flags['Alpha-3 code']==countrycode1].index[0],'URL']
    flag_country1 = html.Img(src=url_1, style={'width': '100px', 'height': 'auto'})

    # Flag image of Country 2
    country2 = df_filtered_factors.iloc[1, 0]
    countrycode2 = df_filtered_factors.iloc[1, 1]
    url_2 = df_flags.loc[df_flags.loc[df_flags['Alpha-3 code'] == countrycode2].index[0], 'URL']
    flag_country2 = html.Img(src=url_2, style={'width': '100px', 'height': 'auto'})

    # Flag image of Country 3
    country3 = df_filtered_factors.iloc[2, 0]
    countrycode3 = df_filtered_factors.iloc[2, 1]
    url_3 = df_flags.loc[df_flags.loc[df_flags['Alpha-3 code'] == countrycode3].index[0], 'URL']
    flag_country3 = html.Img(src=url_3, style={'width': '100px', 'height': 'auto'})

    return country1, flag_country1, country2, flag_country2, country3, flag_country3


if __name__ == '__main__':
    app.run_server(debug=True, port=1337)