import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP],
                title='Superstore Exploratory Data Analysis',
                update_title='Loading...')
df = pd.read_csv('SampleSuperstore.csv')
df = df.drop(['Country'], axis=1)

sorted_data = df.sort_values(by='Sales', ascending=False)
sorted_data['Z-Score'] = (sorted_data.Sales - sorted_data.Sales.mean()) / sorted_data.Sales.std()
sorted_data = sorted_data[sorted_data['Z-Score'] < 3]
new_df = sorted_data

# Region wise Profit and Sales
data_top_10_region = new_df.groupby("Region")[["Profit", "Sales"]].sum().reset_index().sort_values(by="Profit",
                                                                                                   ascending=False)
# Top 10 State wise Profit and Sales
data_top_10_states = new_df.groupby("State")[["Profit", "Sales"]].sum().reset_index().sort_values(by="Profit",
                                                                                                  ascending=False)
# Top 10 City wise Profit and Sales
data_top_10_cities = new_df.groupby("City")[["Profit", "Sales"]].sum().reset_index().sort_values(by="Profit",
                                                                                                 ascending=False)
# Top 10 Sub-category wise Profit and Sales
data_top_10_sub_categories = new_df.groupby("Sub-Category")[["Profit", "Sales"]].sum().reset_index().sort_values(
    by="Profit", ascending=False)

# Navbar Search
search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(type="search", placeholder="Search")),
        dbc.Col(
            dbc.Button("Search", color="primary", className="ml-2"),
            width="auto"
        ),
        dbc.Col(
            dbc.Button("Aditya Kataria", color="light", className="ml-5"),
        )
    ],
    no_gutters=True,
    className="ml-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

# Navbar
navbar = dbc.Navbar(
    [
        html.A(
            dbc.Row(
                [
                    dbc.Col(html.Img(src=PLOTLY_LOGO, height="40px"), width="40px"),
                    dbc.Col(dbc.NavbarBrand("Plotly Dash | Exploratory Data Analysis"), className="ml-2"),
                ],
                align="center",
                no_gutters=True,
            ),
            href="https://plot.ly",
        ),
        dbc.NavbarToggler(id="navbar-toggler"),
        dbc.Collapse(search_bar, id="navbar-collapse", navbar=True),
    ],
    color="dark",
    sticky="top",
    dark=True,
)

# Sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": "4rem",
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# Main Window
# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Superstore", className="display-5"),
        html.Hr(),
        html.P(
            "Dashboard", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Dataset", href="/dataset", id="page-2-link"),
                dbc.NavLink("Correlation Analysis", href="/corr", id="page-3-link"),
                dbc.NavLink("Covariance", href="/cov", id="page-4-link"),
                dbc.NavLink("Product Level Analysis", href="/product_level_analysis", id="page-5-link"),
                dbc.NavLink("Segment Analysis", href="/segment_analysis", id="page-6-link"),
                dbc.NavLink("Ship Mode Analysis", href="/ship_mode_analysis", id="page-7-link"),
                dbc.NavLink("Top 10", href="/top_10", id="page-8-link"),
            ],
            vertical=True,
            pills=True,
        ),
        html.Hr(),
        html.Br(),
        html.P(["Developed with ", '❤️', " in India"], className="text-center")
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)
app.layout = html.Div([navbar, dcc.Location(id="url"), sidebar, content])


@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 9)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False, False, False
    return [pathname == f"/page-{i}" for i in range(1, 9)]


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/":
        return html.Div([html.H3("Welcome to Superstore Dashboard"),
                         html.Img(src='/assets/img/img2.jpg', height="300px"),
                         html.Div([html.H4("Exploratory Data Analysis"),
                                   html.P("Exploratory Data Analysis (EDA) refers to the critical process of "
                                          "performing initial investigations on data so as to discover patterns,"
                                          "to spot anomalies,to test hypothesis and to check assumptions with the "
                                          "help of summary statistics and graphical representations."),
                                   ]),
                         ])
    elif pathname == "/dataset":
        return html.Div([html.H4("Sample Superstore Dataset"),
                         html.P([
                             "The dataset is available ",
                             html.A("here", href="https://bit.ly/3i4rbWl", target="_blank"),
                             html.P(
                                 "The SampleSuperstore dataset "
                                 "consists of 9994 records with 13 columns as 'Ship Mode', 'Segment', 'Country', "
                                 "'City', 'State', 'Postal Code', 'Region', 'Category', 'Sub-Category', 'Sales', "
                                 "'Quantity', 'Discount' and 'Profit'.")
                         ]),
                         dash_table.DataTable(
                             id='table',
                             columns=[{"name": i, "id": i} for i in df.columns],
                             data=df.to_dict('records'),
                         )])
    elif pathname == "/corr":
        return html.Div([html.H4("Correlation Analysis"),
                         html.P("Pandas dataframe.corr() is used to find the pairwise correlation of all columns in "
                                "the dataframe. Both NA and null values are automatically excluded. For any "
                                "non-numeric data type columns in the dataframe it is ignored."),
                         dash_table.DataTable(
                             id='table',
                             columns=[{"name": i, "id": i} for i in df.corr()],
                             data=df.corr().to_dict('records'),
                         ),
                         dcc.Graph(
                             id='heatmap',
                             figure={
                                 'data': [go.Heatmap(
                                     z=df.corr().values,
                                     x=df.corr().columns.values,
                                     y=df.corr().columns.values,
                                     colorscale='RdBu'
                                 )],
                                 'layout': go.Layout(
                                     title="Correlation Heatmap",
                                     xaxis=dict(ticks='', nticks=36),
                                     yaxis=dict(ticks=''),
                                     width=600, height=500,
                                 ),
                             }
                         )
                         ])
    elif pathname == "/cov":
        return html.Div([html.H4("Covariance"),
                         html.P("Pandas dataframe.cov() is used to compute the pairwise covariance among the series "
                                "of a DataFrame. The returned data frame is the covariance matrix of the columns of "
                                "the DataFrame.Both NA and null values are automatically excluded from the "
                                "calculation. A threshold can be set for the minimum number of observations for each "
                                "value created. Comparisons with observations below this threshold will be returned "
                                "as NaN."),
                         dash_table.DataTable(
                             id='table',
                             columns=[{"name": i, "id": i} for i in df.cov()],
                             data=df.cov().to_dict('records'),
                         ),
                         dcc.Graph(
                             id='heatmap',
                             figure={
                                 'data': [go.Heatmap(
                                     z=df.cov().values,
                                     x=df.cov().columns.values,
                                     y=df.cov().columns.values,
                                     colorscale='RdBu'
                                 )],
                                 'layout': go.Layout(
                                     title="Covariance Heatmap",
                                     xaxis=dict(ticks='', nticks=36),
                                     yaxis=dict(ticks=''),
                                     width=600, height=500,
                                 ),
                             }
                         )
                         ])
    elif pathname == "/product_level_analysis":
        return html.Div([html.H4("Product Level Analysis"),
                         dbc.Row(
                             [
                                 dbc.Col(dcc.Graph(
                                     id='bar',
                                     figure={
                                         'data': [go.Bar(
                                             x=new_df['Category'].value_counts().index.values,
                                             y=new_df['Category'].value_counts().values,

                                         )],
                                         'layout': go.Layout(
                                             title="Category Unique Items",
                                             xaxis=dict(ticks=''),
                                             yaxis=dict(ticks=''),
                                             width=500, height=500,
                                         ),
                                     }
                                 )),
                                 dbc.Col(dcc.Graph(
                                     id='bar',
                                     figure={
                                         'data': [go.Bar(
                                             x=new_df['Sub-Category'].value_counts().index.values,
                                             y=new_df['Sub-Category'].value_counts().values,

                                         )],
                                         'layout': go.Layout(
                                             title="Sub-Category Unique Items",
                                             xaxis=dict(ticks=''),
                                             yaxis=dict(ticks=''),
                                             width=500, height=500,
                                         ),
                                     }
                                 )),
                             ]
                         ),
                         dbc.Row(
                             [
                                 dbc.Col(dcc.Graph(
                                     id='bar',
                                     figure={
                                         'data': [go.Pie(
                                             labels=new_df['Sub-Category'].value_counts().index.values,
                                             values=new_df['Sub-Category'].value_counts().values)],
                                         'layout': go.Layout(
                                             title="Sub-Category Distribution Pie chart",
                                             xaxis=dict(ticks=''),
                                             yaxis=dict(ticks=''),
                                             width=600, height=600,
                                         ),
                                     }
                                 )),
                             ], ),
                         dbc.Row(
                             dbc.Col(dcc.Graph(
                                 id='bar',
                                 figure={
                                     'data': [go.Bar(
                                         x=new_df['Sub-Category'],
                                         y=new_df[new_df['Region'] == 'East'].value_counts().values,
                                         name="East"
                                     ), go.Bar(
                                         x=new_df['Sub-Category'],
                                         y=new_df[new_df['Region'] == 'West'].value_counts().values,
                                         name="West"
                                     ), go.Bar(
                                         x=new_df['Sub-Category'],
                                         y=new_df[new_df['Region'] == 'Central'].value_counts().values,
                                         name="Central"
                                     ), go.Bar(
                                         x=new_df['Sub-Category'],
                                         y=new_df[new_df['Region'] == 'South'].value_counts().values,
                                         name="South"
                                     )],
                                     'layout': go.Layout(
                                         title="Count of Sub-Category region wise",
                                         xaxis=dict(ticks=''),
                                         yaxis=dict(ticks=''),
                                         width=900, height=600,
                                         barmode="group"
                                     ),
                                 }
                             )),
                         ),
                         ])
    elif pathname == "/segment_analysis":
        return html.Div([html.H4("Segment Analysis"),
                         dbc.Row(
                             [
                                 dbc.Col(dcc.Graph(
                                     id='bar',
                                     figure={
                                         'data': [go.Bar(
                                             x=new_df['Segment'].value_counts().index.values,
                                             y=new_df['Segment'].value_counts().values,

                                         )],
                                         'layout': go.Layout(
                                             title="Segment Unique Items",
                                             xaxis=dict(ticks=''),
                                             yaxis=dict(ticks=''),
                                             width=500, height=500,
                                         ),
                                     }
                                 )),
                                 dbc.Col(dcc.Graph(
                                     id='bar',
                                     figure={
                                         'data': [go.Pie(
                                             labels=new_df['Segment'].value_counts().index.values,
                                             values=new_df['Segment'].value_counts().values)],
                                         'layout': go.Layout(
                                             title="Segment Distribution Pie chart",
                                             xaxis=dict(ticks=''),
                                             yaxis=dict(ticks=''),
                                             width=500, height=500,
                                         ),
                                     }
                                 )),
                             ]
                         ),
                         dbc.Row(
                             dbc.Col(dcc.Graph(
                                 id='bar',
                                 figure={
                                     'data': [go.Bar(
                                         x=new_df['Segment'],
                                         y=new_df[new_df['Region'] == 'East'].value_counts().values,
                                         name="East"
                                     ), go.Bar(
                                         x=new_df['Segment'],
                                         y=new_df[new_df['Region'] == 'West'].value_counts().values,
                                         name="West"
                                     ), go.Bar(
                                         x=new_df['Segment'],
                                         y=new_df[new_df['Region'] == 'Central'].value_counts().values,
                                         name="Central"
                                     ), go.Bar(
                                         x=new_df['Segment'],
                                         y=new_df[new_df['Region'] == 'South'].value_counts().values,
                                         name="South"
                                     )],
                                     'layout': go.Layout(
                                         title="Count of Segments region wise",
                                         xaxis=dict(ticks=''),
                                         yaxis=dict(ticks=''),
                                         width=900, height=600,
                                         barmode="group"
                                     ),
                                 }
                             )),
                         ),
                         ])
    elif pathname == "/ship_mode_analysis":
        return html.Div([html.H4("Ship Mode Analysis"),
                         dbc.Row(
                             [
                                 dbc.Col(dcc.Graph(
                                     id='bar',
                                     figure={
                                         'data': [go.Bar(
                                             x=new_df['Ship Mode'].value_counts().index.values,
                                             y=new_df['Ship Mode'].value_counts().values,

                                         )],
                                         'layout': go.Layout(
                                             title="Ship Mode Unique Items",
                                             xaxis=dict(ticks=''),
                                             yaxis=dict(ticks=''),
                                             width=500, height=500,
                                         ),
                                     }
                                 )),
                                 dbc.Col(dcc.Graph(
                                     id='bar',
                                     figure={
                                         'data': [go.Pie(
                                             labels=new_df['Ship Mode'].value_counts().index.values,
                                             values=new_df['Ship Mode'].value_counts().values)],
                                         'layout': go.Layout(
                                             title="Ship Mode Distribution Pie chart",
                                             xaxis=dict(ticks=''),
                                             yaxis=dict(ticks=''),
                                             width=500, height=500,
                                         ),
                                     }
                                 )),
                             ]
                         ),
                         dbc.Row(
                             dbc.Col(dcc.Graph(
                                 id='bar',
                                 figure={
                                     'data': [go.Bar(
                                         x=new_df['Ship Mode'],
                                         y=new_df[new_df['Region'] == 'East'].value_counts().values,
                                         name="East"
                                     ), go.Bar(
                                         x=new_df['Ship Mode'],
                                         y=new_df[new_df['Region'] == 'West'].value_counts().values,
                                         name="West"
                                     ), go.Bar(
                                         x=new_df['Ship Mode'],
                                         y=new_df[new_df['Region'] == 'Central'].value_counts().values,
                                         name="Central"
                                     ), go.Bar(
                                         x=new_df['Ship Mode'],
                                         y=new_df[new_df['Region'] == 'South'].value_counts().values,
                                         name="South"
                                     )],
                                     'layout': go.Layout(
                                         title="Count of Ship modes region wise",
                                         xaxis=dict(ticks=''),
                                         yaxis=dict(ticks=''),
                                         width=900, height=600,
                                         barmode="group"
                                     ),
                                 }
                             )),
                         ),
                         ])
    elif pathname == "/top_10":
        return html.Div([
            dcc.Tabs([
                dcc.Tab(label='Region', children=[
                    html.Div([html.H4("Region wise Profit and Sales"), dash_table.DataTable(
                        id='table',
                        columns=[{"name": i, "id": i} for i in data_top_10_region.columns],
                        data=data_top_10_region.to_dict('records'),
                    )]),
                    html.H5("Visualization"),
                    dbc.Row([
                        dbc.Col(dcc.Graph(
                            id='bar',
                            figure={
                                'data': [go.Bar(
                                    x=data_top_10_region['Region'],
                                    y=data_top_10_region['Profit'],

                                )],
                                'layout': go.Layout(
                                    title="Region-wise Profit",
                                    xaxis=dict(ticks=''),
                                    yaxis=dict(ticks=''),
                                    width=500, height=500,
                                ),
                            }
                        )),
                        dbc.Col(dcc.Graph(
                            id='bar',
                            figure={
                                'data': [go.Bar(
                                    x=data_top_10_region['Region'],
                                    y=data_top_10_region['Sales'],

                                )],
                                'layout': go.Layout(
                                    title="Region-wise Sales",
                                    xaxis=dict(ticks=''),
                                    yaxis=dict(ticks=''),
                                    width=500, height=500,
                                ),
                            }
                        )),
                    ]),
                ]),
                dcc.Tab(label='State', children=[
                    html.Div([html.H4("Top 10 State wise Profit and Sales"), dash_table.DataTable(
                        id='table',
                        columns=[{"name": i, "id": i} for i in data_top_10_states.columns],
                        data=data_top_10_states.head(10).to_dict('records'),
                    )]),
                    html.H5("Visualization"),
                    dbc.Row([
                        dbc.Col(dcc.Graph(
                            id='bar',
                            figure={
                                'data': [go.Bar(
                                    x=data_top_10_states['State'].head(10),
                                    y=data_top_10_states['Profit'].head(10),

                                )],
                                'layout': go.Layout(
                                    title="State-wise Profit",
                                    xaxis=dict(ticks=''),
                                    yaxis=dict(ticks=''),
                                    width=500, height=500,
                                ),
                            }
                        )),
                        dbc.Col(dcc.Graph(
                            id='bar',
                            figure={
                                'data': [go.Bar(
                                    x=data_top_10_states['State'].head(10),
                                    y=data_top_10_states['Sales'].head(10),

                                )],
                                'layout': go.Layout(
                                    title="State-wise Sales",
                                    xaxis=dict(ticks=''),
                                    yaxis=dict(ticks=''),
                                    width=500, height=500,
                                ),
                            }
                        )),
                    ]),
                ]),
                dcc.Tab(label='City', children=[
                    html.Div([html.H4("Top 10 City wise Profit and Sales"), dash_table.DataTable(
                        id='table',
                        columns=[{"name": i, "id": i} for i in data_top_10_cities.columns],
                        data=data_top_10_cities.head(10).to_dict('records'),
                    )]),
                    html.H5("Visualization"),
                    dbc.Row([
                        dbc.Col(dcc.Graph(
                            id='bar',
                            figure={
                                'data': [go.Bar(
                                    x=data_top_10_cities['City'].head(10),
                                    y=data_top_10_cities['Profit'].head(10),

                                )],
                                'layout': go.Layout(
                                    title="City-wise Profit",
                                    xaxis=dict(ticks=''),
                                    yaxis=dict(ticks=''),
                                    width=500, height=500,
                                ),
                            }
                        )),
                        dbc.Col(dcc.Graph(
                            id='bar',
                            figure={
                                'data': [go.Bar(
                                    x=data_top_10_cities['City'].head(10),
                                    y=data_top_10_cities['Sales'].head(10),

                                )],
                                'layout': go.Layout(
                                    title="City-wise Sales",
                                    xaxis=dict(ticks=''),
                                    yaxis=dict(ticks=''),
                                    width=500, height=500,
                                ),
                            }
                        )),
                    ]),
                ]),
                dcc.Tab(label='Sub-Category', children=[
                    html.Div([html.H4("Top 10 Sub-category wise Profit and Sales"), dash_table.DataTable(
                        id='table',
                        columns=[{"name": i, "id": i} for i in data_top_10_sub_categories.columns],
                        data=data_top_10_sub_categories.head(10).to_dict('records'),
                    )]),
                    html.H5("Visualization"),
                    dbc.Row([
                        dbc.Col(dcc.Graph(
                            id='bar',
                            figure={
                                'data': [go.Bar(
                                    x=data_top_10_sub_categories['Sub-Category'].head(10),
                                    y=data_top_10_sub_categories['Profit'].head(10),

                                )],
                                'layout': go.Layout(
                                    title="Sub-Category-wise Profit",
                                    xaxis=dict(ticks=''),
                                    yaxis=dict(ticks=''),
                                    width=500, height=500,
                                ),
                            }
                        )),
                        dbc.Col(dcc.Graph(
                            id='bar',
                            figure={
                                'data': [go.Bar(
                                    x=data_top_10_sub_categories['Sub-Category'].head(10),
                                    y=data_top_10_sub_categories['Sales'].head(10),

                                )],
                                'layout': go.Layout(
                                    title="Sub-Category-wise Sales",
                                    xaxis=dict(ticks=''),
                                    yaxis=dict(ticks=''),
                                    width=500, height=500,
                                ),
                            }
                        )),
                    ]),
                ]),
            ])
        ])
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


app.run_server()
