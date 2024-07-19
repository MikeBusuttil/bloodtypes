from json import loads
from os import path
import plotly.graph_objects as go
from dash import Dash, dcc, html, Output, Input

prevalence = sorted(
    loads(open(f"{path.dirname(__file__)}/prevalence.json").read()),
    key=lambda x: x["prevalencePercent"], reverse=True,
)
compatibility = loads(open(f"{path.dirname(__file__)}/compatibility.json").read())

app = Dash(__name__)
app.title = "Blood Types"
app.layout = html.Div([
    html.H4(app.title),
    dcc.Graph(id="graph"),
])

sources = [x for x in range(1, 8)] + [0]*8
targets = [x for x in range(1, 8)] + [x+7 for x in range(8)]

show = [8,9,10,13]
def link_opacity(x):
    return 0.8 if x in show else 0
def node_opacity(x):
    return 1 if x in show + [y for y in range(8)] else 0
node_colors = ['255,0,0', '0,255,0', '0,0,255', '255,255,0', '255,0,255', '0,255,255', '255,255,255', '0,0,0']
def node_color(x):
    return node_colors[x % 8]
def node_label(x):
    return prevalence[x % 8]["type"] if x in show + [y for y in range(8)] else ""
def link_color(x):
    target = targets[x]
    target_color = node_colors[target % 8]
    return target_color

@app.callback(
    Output("graph", "figure"),
    Input("graph", "relayoutData"),
)
def display_sankey(_):
    fig = go.Figure(go.Sankey(
        arrangement='snap',
        node=dict(
            label=[node_label(x) for x in range(16)],
            hoverinfo='skip',
            color=[f'rgba({node_color(x)},{node_opacity(x)})' for x in range(16)],
            align='right',
            x=[0.5]*8 + [0.9]*8,
            y=[0.5]*8 + [0.3]*8,
            thickness = 100,
            pad=0,
            line=dict(width=0),
        ),
        link=dict(
            arrowlen=15,
            source=sources,
            target=targets,
            hoverinfo='skip',
            hovercolor=[f'rgba({link_color(x)},{link_opacity(x)})' for x in range(15)],
            color=[f'rgba({link_color(x)},{link_opacity(x)})' for x in range(15)],
            value=[p["prevalencePercent"] for p in prevalence[0:]] + [p["prevalencePercent"]*prevalence[0]["prevalencePercent"]/100 for p in prevalence],
        )
    ))
    return fig

app.run_server(debug=True)
