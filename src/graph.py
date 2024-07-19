from json import loads
from os import path
import plotly.graph_objects as go
from dash import Dash, dcc, html, Output, Input

prevalence = sorted(
    loads(open(f"{path.dirname(__file__)}/prevalence.json").read()),
    key=lambda x: x["prevalencePercent"], reverse=True,
)

app = Dash(__name__)
app.title = "Blood Types"
app.layout = html.Div([
    html.H4(app.title),
    dcc.Graph(id="graph"),
])

@app.callback(
    Output("graph", "figure"),
    Input("graph", "relayoutData"),
)
def display_sankey(_):
    fig = go.Figure(go.Sankey(
        arrangement='snap',
        node=dict(
            label=[p["type"] for p in prevalence],
            x=[0.5]*8,
            y=[0.5]*8,
            thickness = 100,
            pad=0,
        ),
        link=dict(
            arrowlen=15,
            source=[x for x in range(8)],
            target=[x for x in range(8)],
            value=[p["prevalencePercent"] for p in prevalence],
        )
    ))
    return fig

app.run_server(debug=True)
