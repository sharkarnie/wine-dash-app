import pandas as pd
import flask
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import plotly.graph_objs as go


df_wine = pd.read_csv('data/both.csv')

wine_options = [{
    'label': x.replace('_', ' ').title() if x != 'pH' else x,
    'value': x
    } for x in df_wine.columns if x != 'type'
    ]

wine_colours = {
    0: '#FFA62F',
    1: '#E41B17'
    }

def inputs():
    dropdowns = [dcc.Markdown('Type'), dcc.Dropdown(
        id='wine-type',
        value='both',
        clearable=False,
        options=[
        {'label': 'Red & White', 'value': 'both'},
        {'label': 'Red', 'value': 'red'},
        {'label': 'White', 'value': 'white'}
        ]
    )]
    dropdowns += [dcc.Markdown('X-axis'), dcc.Dropdown(
        id='x-axis',
        value=df_wine.columns[0],
        clearable=False,
        options=wine_options
    )]
    dropdowns += [dcc.Markdown('Y-axis'), dcc.Dropdown(
        id='y-axis',
        value=df_wine.columns[1],
        clearable=False,
        options=wine_options
    )]
    return html.Div(dropdowns)

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    dbc.themes.GRID
    ]

server = flask.Flask(__name__)

@server.route('/')
def index():
    return 'Nothing here yet!'

app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
    routes_pathname_prefix='/wine-dash/',
    server=server)

app.layout = html.Div([
    dbc.Row([
        dbc.Col([
            dcc.Markdown("""
                ## Wine Dash
                A web application for the exploration of wine datasets.
                """),
            inputs()
            ], width=3),
        dbc.Col(dcc.Graph(id='my-graph'))
        ])
], style={'width': '1200px'})

@app.callback(
    dash.dependencies.Output('my-graph', 'figure'),
    [
        dash.dependencies.Input('wine-type', 'value'),
        dash.dependencies.Input('x-axis', 'value'),
        dash.dependencies.Input('y-axis', 'value'),
    ],
    )
def update_graph(wine_type, x_axis, y_axis):
    if wine_type == 'both':
        cond = df_wine['type'].isin([0,1])
        plot_colour = df_wine['type'].map(wine_colours).values
    if wine_type == 'red':
        cond = (df_wine['type'] == 1)
        plot_colour = wine_colours[1]
    if wine_type == 'white':
        cond = (df_wine['type'] == 0)
        plot_colour = wine_colours[0]

    data_x = df_wine.loc[cond, x_axis].values
    data_y = df_wine.loc[cond, y_axis].values

    mdl = LinearRegression()

    mdl.fit(data_x.reshape(-1, 1), data_y)
    data_y_pred = mdl.predict(data_x.reshape(-1,1))

    r_sq = r2_score(data_y, data_y_pred)

    annotation = f"""
        <b>y = {mdl.coef_[0]:0.2f}*x + {mdl.intercept_:0.2f}</b>
        <br />
        <b>r<sup>2</sup> = {r_sq:0.2f}</b>"""
        
    return {
        'data': [
            go.Scatter(x=data_x, y=data_y,
                       mode='markers', name='',
                       marker={
                        'size': 8, 'color': plot_colour, 'opacity': 0.3,
                        'line': {'width': 0.5, 'color': '#EBF4FA'}
                        }
                       ),
            go.Scatter(x=data_x, y=data_y_pred,
                       mode='lines', name='Regression',
                       marker={
                        'color': '#657383',
                       },
                       line={'width': 4}
                       ),
            ],
        'layout': {
                    'height': 600,
                    'xaxis': {'title': x_axis.replace('_', ' ').title()},
                    'yaxis': {'title': y_axis.replace('_', ' ').title()},
                    #'margin': {'l': 40, 'b': 40, 't': 10, 'r': 10},
                    # legend={'x': 0, 'y': 1},
                    'showlegend': False,
                    'hovermode': 'closest',
                    'annotations': [{
                        'text': annotation,
                        'x': data_x.max(),
                        'y': data_y.max(),
                        'showarrow': False,
                        'font': {
                            'size': 16,
                            'color': '#657383',
                        }
                    }]
                }
            }
if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
