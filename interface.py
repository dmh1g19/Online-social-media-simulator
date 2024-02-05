import networkx as nx
import dash
from dash import dcc, html
import visdcc
import numpy as np
from plotting import *
import plotly.graph_objects as go


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
            html.H1("Dashboard", style={'text-align': 'center'}),
            style={'margin-top': '20px'} 
        ),
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
