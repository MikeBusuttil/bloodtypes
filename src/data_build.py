"""
This file is all about transforming the raw data (stored in blood_data.json)
into a format that Plotly (graph_show.py) can understand.
"""

from json import loads
from os import path

blood_data = sorted(
    loads(open(f"{path.dirname(__file__)}/blood_data.json").read()),
    key=lambda x: x["prevalencePercent"],
    reverse=True,
)
get_index = lambda i: [p["type"] for p in blood_data].index(i)
for i in range(8):
    blood_data[i]['canGiveTo'] = set([get_index(t) for t in blood_data[i]['canGiveTo']] + [i])

sources = [s // 8 for s in range(8*8)] + [8 + 8*8 + s for s in range(8*8)]
targets = [8 + t for t in range(8*8)] + [t // 8 for t in range(8*8)]

blood_colors = ['255,0,0', '0,255,0', '0,0,255', '255,255,0', '255,0,255', '0,255,255', '255,165,0', '128,0,128']
def node_details(n):
    if n < 8 + 8*8:
        x = n - 8
        source = x // 8
        target = x % 8
    else:
        x = n - 8 - 8*8
        target = x // 8
        source = x % 8
    opacity = 1 if n < 8 or target in blood_data[source]['canGiveTo'] else 0
    pp = 'prevalencePercent'
    return dict(
        color=f'{blood_colors[n % 8]},{opacity}',
        label=f'{blood_data[n % 8]["type"]}{ f" ({blood_data[n][pp]}%)" if n < 8 else ""}' if opacity else "",
    )
def link_label(x):
    if x < 8*8:
        source = x // 8
        takers = sum([blood_data[taker]["prevalencePercent"] for taker in blood_data[source]['canGiveTo']])
        return f"Can give blood to {takers}% of population<extra>{blood_data[source]['type']}</extra>"
    target = (x - 8*8) // 8
    givers = sum([blood_data[giver]["prevalencePercent"] for giver in range(8) if target in blood_data[giver]['canGiveTo']])
    return f"Can receive blood from {givers}% of population<extra>{blood_data[target]['type']}</extra>"
def link_color(x):
    if x < 8*8:
        source = x // 8
        target = x % 8
    else:
        source = x % 8
        target = (x - 8*8) // 8
    opacity = 0.8 if target in blood_data[source]['canGiveTo'] else 0
    target_color = blood_colors[target]
    source_color = blood_colors[source]
    return f'{target_color if x < 8*8 else source_color},{opacity}'

blood_types = [blood["type"] for blood in blood_data]

all_node_indicies = set([x for x in range(8 + 8*8 + 8*8)])
all_link_indicies = set([x for x in range(8*8 + 8*8)])
def get_indicies(node_type):
    if node_type == 'all':
        return all_node_indicies, all_link_indicies
    node_type = [p["type"] for p in blood_data].index(node_type)
    node_indicies = set([node_type] + [x for x in range(8 + 8*node_type, 16 + 8*node_type)] + [x for x in range(8 + 8*8 + 8*node_type, 16 + 8*8 + 8*node_type)])
    link_indicies = set([n for n, src in enumerate(sources) if src==node_type] + [n for n, t in enumerate(targets) if t==node_type])
    return node_indicies, link_indicies

node_labels = [node_details(x)['label'] for x in range(8 + 8*8 + 8*8)]
node_colors = [f'rgba({node_details(x)["color"]})' for x in range(8 + 8*8 + 8*8)]
node_xs = [0.5]*8 + [0.9]*8*8 + [0.1]*8
node_ys = [0.2]*8 + [0.1]*8 + [0.3]*8 + [0.5]*8 + [0.7]*8 + [0.9]*8 + [1.0]*8 + [1.1]*8 + [1.2]*8 + [0.1]*8 + [0.3]*8 + [0.5]*8 + [0.7]*8 + [0.9]*8 + [1.1]*8 + [1.3]*8 + [1.5]*8

link_labels = [link_label(x) for x in range(8*8*2)]
link_hover_colors = [f'rgba({link_color(x)})' for x in range(8*8*2)]
link_colors = [f'rgba({link_color(x)})' for x in range(8*8*2)]
link_values =  [blood_data[l//8]["prevalencePercent"] * blood_data[l%8]["prevalencePercent"] / 100 for l in range(8*8)]
link_values += [blood_data[l//8]["prevalencePercent"] * blood_data[l%8]["prevalencePercent"] / 100 for l in range(8*8)]
