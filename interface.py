import networkx as nx
import dash
from dash import dcc, html
import visdcc
import numpy as np
from plotting import *
import plotly.graph_objects as go
from dash.dependencies import Input, Output


def create_dash_app():
    return dash.Dash(__name__)

def run_server(app):
    app.run_server(debug=True)

def make_layout(G, app):
    graphs = Plotter(20, G)

    # Convert the JSON data from nx.node_link_data(G) to the correct format for visdcc, including colors
    nodes_data = nx.node_link_data(G)['nodes']
    links_data = nx.node_link_data(G)['links']

    for node in nodes_data:
        if node.get('inauthentic', False):
            node['color'] = 'red'
        else:
            node['color'] = 'blue'

    network_data = {
        'nodes': [{'id': node['id'], 'color': node.get('color', 'blue')} for node in nodes_data],
        'edges': [{'from': link['source'], 'to': link['target']} for link in links_data]
    }

    app.layout = html.Div([
        html.Div(
            id='node-messages-display', 
            style={'position': 'absolute', 
                   'bottom': '10px', 
                   'left': '10px', 
                   'background': 'white', 
                   'padding': '10px', 
                   'border-radius': '5px', 
                   'border': '2px solid #ddd', 
                   'z-index': '1000', 
                   'max-height': '200px', 
                   'overflow-y': 'auto', 
                   'height': '300px',
                   'width': '200px'}),
        html.Div(
            [
                html.Div(
                    visdcc.Network(
                        id='network-graph',
                        data=network_data,
                        options={
                            'height': '600px',
                            'width': '100%',
                            'physics': {
                                'barnesHut': {
                                    'springLength': 200,
                                },
                            },
                        },
                        style={'width': '100%', 'height': '600px'}
                    ),
                    style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}
                ),
                html.Div(
                    [
                        dcc.Graph(
                            id='degree-distribution-graph',
                            figure=graphs.plot_degree_distribution_by_type()
                        ),
                        dcc.Graph(
                            id='bar',
                            figure=graphs.plot_authentic_inauthentic_bar_chart()
                        ),
                        dcc.Graph(
                            id='tmp',
                            figure=graphs.plot_degree_distribution()
                        ),
                        dcc.Graph(
                            id='tmp2',
                            figure=graphs.plot_degree_comparison_authentic_inauthentic()
                        ),
                    ],
                    style={'height': 'calc(100vh - 60px)', 'overflow-y': 'auto', 'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}
                ),
            ],
            style={'display': 'flex', 'flex-direction': 'row'}
        ),
    ])

def register_callbacks(app, G):
    @app.callback(
        Output('node-messages-display', 'children'),
        [Input('network-graph', 'selection')]
    )
    def display_node_messages(selection):
        if selection is not None and 'nodes' in selection and len(selection['nodes']) > 0:
            node_id = selection['nodes'][0]
            messages = G.nodes[node_id].get('messages', [])

            if messages:  
                total_appeal = sum(msg['appeal'] for msg in messages)
                avg_appeal = total_appeal / len(messages)
            else:
                avg_appeal = 0

            messages_display = html.Div([
                html.P(f"Total messages: {len(messages):.2f}"),
                html.P(f"Average Appeal: {avg_appeal:.2f}"),
                html.Ul([html.Li(f"Appeal: {msg['appeal']:.2f}, Origin: {msg['origin']}") for msg in messages])
            ])

            return messages_display
        return "Click on a node to see its messages."