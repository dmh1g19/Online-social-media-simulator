from dash import dcc
from plotting import *

def get_topic_graphs(G):
    graphs = Plotter(G)

    new_graphs = [
        dcc.Graph(
            id='topic_distribution',
            figure=graphs.plot_topic_distribution_across_network()
        )
    ]

    return new_graphs

