import plotly.graph_objects as go
from dash import Dash, dcc, html, Output, Input
from build_data import node_labels, node_colors, node_xs, node_ys, sources, targets, link_labels, link_hover_colors, link_colors, link_values

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
            label=node_labels,
            hoverinfo='skip',
            color=node_colors,
            align='right',
            x=node_xs,
            y=node_ys,
            thickness=100,
            pad=0,
            line=dict(width=0),
        ),
        link=dict(
            arrowlen=15,
            source=sources,
            target=targets,
            customdata=link_labels,
            hovertemplate='%{customdata}',
            hovercolor=link_hover_colors,
            color=link_colors,
            value=link_values,
        )
    ))
    return fig

app.run_server(debug=True)
