
import base64
import datetime
import io
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px

import dash
from dash import dcc, html, dash_table
from dash.dependencies import Output, Input, State

# inspired by this example: https://realpython.com/python-dash/

# example how to read csv
# data = pd.read_csv("file.csv")

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "CellProfiler Explorer"
colors = {"graphBackground": "#F5F5F5", "background": "#ffffff", "text": "#000000"}

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🧫🔬📊", className="header-emoji"),
                html.H1(
                    children="CellProfiler Explorer", className="header-title"
                ),
                html.P(
                    children="Explore CellProfiler data with interactive plotting",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                # Allow multiple files to be uploaded
                multiple=True
            ),
            #dcc.Graph(id="Mygraph"),
            #html.Div(id='output-data-upload'),
        ]),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="Mygraph",
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="X axis", className="menu-title"),
                        dcc.Dropdown(
                            id="x-column-dropdown",
                            options=[],
                            value=None,
                            clearable=True,
                            searchable=True,
                            className="dropdown",
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(children="Y axis", className="menu-title"),
                        dcc.Dropdown(
                            id="y-column-dropdown",
                            options=[],
                            value=None,
                            clearable=True,
                            searchable=True,
                            className="dropdown",
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(children="Color by", className="menu-title"),
                        dcc.Dropdown(
                            id="color-column-dropdown",
                            options=[],
                            value=None,
                            clearable=True,
                            searchable=True,
                            className="dropdown",
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="price-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="volume-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)

def parse_data(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        elif 'txt' in filename:
            #text file
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")), delimiter=r"\s+")
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return df

@app.callback(
  Output('x-column-dropdown', 'options'),
    [Input('upload-data', 'contents'),
     Input('upload-data', 'filename')])
@app.callback(
  Output('y-column-dropdown', 'options'),
    [Input('upload-data', 'contents'),
     Input('upload-data', 'filename')])
@app.callback(
  Output('color-column-dropdown', 'options'),
    [Input('upload-data', 'contents'),
     Input('upload-data', 'filename')])
def update_options(contents, filename):
    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        #df = df.set_index(df.columns[0])
        lst = [{'label': i, 'value': i} for i in df.columns]
        return lst
    else:
        return []

@app.callback(
    Output("Mygraph", "figure"),
    [Input("upload-data", "contents"), Input("upload-data", "filename"), Input("x-column-dropdown", "value"), Input("y-column-dropdown", "value"), Input("color-column-dropdown", "value")],
)
def update_graph(contents, filename, x, y, color):
    #x and y are strings variables in df
    df=None
    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
    fig = go.Figure(
        px.scatter(df, x=x, y=y, color=color)
    )
    fig.update_layout(
            plot_bgcolor=colors["graphBackground"],
            paper_bgcolor=colors["graphBackground"]
    )
    return fig



if __name__ == "__main__":
    app.run_server(debug=True,
                   host='127.0.0.1')
