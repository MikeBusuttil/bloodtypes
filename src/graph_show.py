import plotly.graph_objects as go
from dash import Dash, dcc, html, Output, Input
import data_build as data

app = Dash(__name__)
app.title = "Blood Type Compatibility"
app.layout = html.Div([
    html.H4(id="title"),
    dcc.Graph(id="graph"),

    dcc.Store(id='highlighted-type'),
])

@app.callback(
    Output("highlighted-type", "data"),
    [Input('graph', 'hoverData'), Input('highlighted-type', 'data')],
)
def handle_hover(hoverData, previously_selected_type):
    try:
        node_type = hoverData['points'][0]['customdata']
        assert(node_type in data.blood_types + ['all'])
        return node_type
    except:
        return previously_selected_type

@app.callback(
    Output(component_id='title', component_property='children'),
    Input(component_id='highlighted-type', component_property='data')
)
def update_output_div(selected_type):
    selected_type
    return app.title if selected_type in ['all', None] else f'{app.title} ({selected_type})'

@app.callback(
    Output("graph", "figure"),
    Input(component_id='highlighted-type', component_property='data')
)
def display_sankey(selected_type):
    node_indicies_new, link_indicies = data.get_indicies(selected_type)

    node_labels = data.node_labels
    node_colors = data.node_colors
    blood_types = data.blood_types
    node_xs = [val for i, val in enumerate(data.node_xs) if i in node_indicies_new]
    node_ys = data.node_ys

    link_sources = [val for i, val in enumerate(data.sources) if i in link_indicies]
    link_targets = [val for i, val in enumerate(data.targets) if i in link_indicies]
    link_labels = [val for i, val in enumerate(data.link_labels) if i in link_indicies]
    link_hover_colors = [val for i, val in enumerate(data.link_hover_colors) if i in link_indicies]
    link_colors = [val for i, val in enumerate(data.link_colors) if i in link_indicies]
    link_values = [val for i, val in enumerate(data.link_values) if i in link_indicies]
    fig = go.Figure(go.Sankey(
        arrangement='snap',
        node=dict(
            label=node_labels,
            hoverinfo='none',
            color=node_colors,
            customdata=blood_types + ['all']*8*8*2,
            align='right',
            x=node_xs,
            y=node_ys,
            thickness=100,
            pad=0,
            line=dict(width=0),
        ),
        link=dict(
            arrowlen=15,
            source=link_sources,
            target=link_targets,
            customdata=link_labels,
            hovertemplate='%{customdata}',
            hovercolor=link_hover_colors,
            color=link_colors,
            value=link_values,
        )
    ))
    return fig

app.run_server(debug=True)
