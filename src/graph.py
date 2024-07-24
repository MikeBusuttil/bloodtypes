from json import loads
from os import path
import plotly.graph_objects as go
from dash import Dash, dcc, html, Output, Input

prevalence = sorted(
    loads(open(f"{path.dirname(__file__)}/prevalence.json").read()),
    key=lambda x: x["prevalencePercent"],
    reverse=True,
)
get_index = lambda i: [p["type"] for p in prevalence].index(i)
compatibility = sorted(
    loads(open(f"{path.dirname(__file__)}/compatibility.json").read()),
    key=lambda x: get_index(x["doner"]),
)
for i in range(8):
    compatibility[i]['recipients'] = set([get_index(t) for t in compatibility[i]['recipients']] + [i])

app = Dash(__name__)
app.title = "Blood Types"
app.layout = html.Div([
    html.H4(app.title),
    dcc.Graph(id="graph"),
])

sources = [s // 8 for s in range(8*8)] + [8 + 8*8 + s for s in range(8*8)]
targets = [8 + t for t in range(8*8)] + [t // 8 for t in range(8*8)]
link_values =  [prevalence[l//8]["prevalencePercent"] * prevalence[l%8]["prevalencePercent"] / 100 for l in range(8*8)]
link_values += [prevalence[l//8]["prevalencePercent"] * prevalence[l%8]["prevalencePercent"] / 100 for l in range(8*8)]

node_colors = ['255,0,0', '0,255,0', '0,0,255', '255,255,0', '255,0,255', '0,255,255', '255,255,255', '0,0,0']
def node_details(n):
    if n < 8 + 8*8:
        x = n - 8
        source = x // 8
        target = x % 8
    else:
        x = n - 8 - 8*8
        target = x // 8
        source = x % 8
    opacity = 1 if n < 8 or target in compatibility[source]['recipients'] else 0
    return dict(
        color=f'{node_colors[n % 8]},{opacity}',
        label=prevalence[n % 8]["type"] if opacity else "",
    )
def link_color(x):
    if x < 8*8:
        source = x // 8
        target = x % 8
    else:
        source = x % 8
        target = (x - 8*8) // 8
    opacity = 0.8 if target in compatibility[source]['recipients'] else 0
    target_color = node_colors[target]
    source_color = node_colors[source]
    return f'{target_color if x < 8*8 else source_color},{opacity}'

@app.callback(
    Output("graph", "figure"),
    Input("graph", "relayoutData"),
)
def display_sankey(_):
    fig = go.Figure(go.Sankey(
        arrangement='snap',
        node=dict(
            label=[node_details(x)['label'] for x in range(8 + 8*8 + 8*8)],
            hoverinfo='skip',
            color=[f'rgba({node_details(x)["color"]})' for x in range(8 + 8*8 + 8*8)],
            align='right',
            x=[0.5]*8 + [0.9]*8*8 + [0.1]*8,
            y=[0.5]*8 + [0.1]*8 + [0.3]*8 + [0.5]*8 + [0.7]*8 + [0.9]*8 + [1.1]*8 + [1.3]*8 + [1.5]*8 + [0.1]*8 + [0.3]*8 + [0.5]*8 + [0.7]*8 + [0.9]*8 + [1.1]*8 + [1.3]*8 + [1.5]*8,
            thickness = 100,
            pad=0,
            line=dict(width=0),
        ),
        link=dict(
            arrowlen=15,
            source=sources,
            target=targets,
            hoverinfo='skip',
            hovercolor=[f'rgba({link_color(x)})' for x in range(8*8*2)],
            color=[f'rgba({link_color(x)})' for x in range(8*8*2)],
            value=link_values,
        )
    ))
    return fig

app.run_server(debug=True)
