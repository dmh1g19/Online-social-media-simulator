import networkx as nx
import dash
from dash import dcc, html
import visdcc
import numpy as np
from plotting import *
import plotly.graph_objects as go
from dash.dependencies import Input, Output

"""
    All the code in this module is purely for displaying the results of the simulation for easy viewing and debugging purposes,
    no logic is kept here.
"""

def create_dash_app():
    return dash.Dash(__name__)

def run_server(app):
    app.run_server(debug=True)

def make_layout(G, app):
    graphs = Plotter(G)

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
            id='node-selected', 
            style={'position': 'absolute', 
                   'top': '10px', 
                   'left': '10px', 
                   'background': 'white', 
                   'padding': '10px', 
                   'border-radius': '5px', 
                   'border': '2px solid #ddd', 
                   'z-index': '1000', 
                   'max-height': '200px', 
                   'overflow-y': 'auto', 
                   'height': '100px',
                   'width': '200px'}
        ),
        html.Div(
            html.H2("Node timeline")
        ),
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
                   'width': '200px'}
        ),
        html.Div([
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
                        dcc.Graph(
                            id='tmp4',
                            figure=graphs.plot_quality_engagement_scatter()
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
        [Output('node-messages-display', 'children'),
         Output('node-selected', 'children')],
        [Input('network-graph', 'selection')]
    )
    def update_display(selection):
        node_info_display = "No node selected."
        messages_display = "Click on a node to see its messages."

        if selection is not None and 'nodes' in selection and len(selection['nodes']) > 0:
            node_id = selection['nodes'][0]
            messages = G.nodes[node_id].get('messages', [])
            inauthentic = G.nodes[node_id].get('inauthentic', False)
            
            if messages:  
                total_appeal = sum(msg['quality'] for msg in messages)
                avg_appeal = total_appeal / len(messages)

                total_engagement = sum(msg['engagement'] for msg in messages)
                avg_engagement = total_engagement / len(messages)

                messages_list = [html.Li(f"Quality: {msg['quality']:.2f}, Engagement: {msg['engagement']:.2f}, Origin: {msg['origin']}") for msg in messages]
                messages_display = html.Div([
                    html.Ul(messages_list)
                ])
            else:
                messages_display = "No messages for this node."
                avg_appeal = 0  
                avg_engagement = 0  
            
            node_info_display = html.Div([
                html.P(f"Node {node_id} - {'Inauthentic' if inauthentic else 'Authentic'}"),
                html.P(f"Total messages: {len(messages)}"),
                html.P(f"Average Quality: {avg_appeal:.2f}"),
                html.P(f"Average Engagement: {avg_engagement:.2f}")
            ])

        return messages_display, node_info_display
