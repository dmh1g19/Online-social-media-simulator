import networkx as nx
import dash
import visdcc
import numpy as np
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from dash import callback_context
from plotting import *
from dash import dcc, html
from interface_help import get_help_info
from interface_network_graphs import get_network_graphs
from interface_messages_graphs import get_messages_graphs


"""
All the code in this module is purely for displaying 
the results of the simulation for easy viewing and debugging purposes,
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
            className='node-selection-box',
        ),
        html.Div(
            id='node-messages-display', 
            className='context-box',
        ),
        html.Div([
                html.Div(
                        id='network-button', 
                        className='hover-effect',
                        style={'right': '130px'},
                        children=html.Div([html.Img(src='/assets/network.svg', style={'height': '45px', 'width': '45px'})])
                    ),
                html.Div(
                        id='messages-button', 
                        className='hover-effect',
                        style={'right': '70px'},
                        children=html.Div([html.Img(src='/assets/bubble.svg', style={'height': '50px', 'width': '50px'})])
                    ),
                html.Div(
                        id='help-button', 
                        className='hover-effect',
                        style={'right': '10px'},
                        children=html.Div([html.Img(src='/assets/help.svg', style={'height': '50px', 'width': '50px'})])
                    ),
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
                    get_network_graphs(G),
                    id='graphs-container',
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

                messages_list = [html.Li(f"Time step: {msg['time_step']}\n,Quality: {msg['quality']:.2f}\n,Engagement: {msg['engagement']:.2f}\n,Origin: {msg['origin']}\n") for msg in messages]
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

    @app.callback(
        Output('graphs-container', 'children'),
        [Input('messages-button', 'n_clicks'),
         Input('network-button', 'n_clicks'),
         Input('help-button', 'n_clicks')],
        prevent_initial_call=True
    )
    def update_graphs_container(n_clicks_messages, n_clicks_network, n_clicks_help):
        triggered_id = callback_context.triggered[0]['prop_id'].split('.')[0]

        if triggered_id == 'messages-button':
            new_graphs = get_messages_graphs(G)

        elif triggered_id == 'network-button':
            new_graphs = get_network_graphs(G)

        elif triggered_id == 'help-button':
            return [get_help_info()]

        else:
            raise dash.exceptions.PreventUpdate

        return new_graphs
