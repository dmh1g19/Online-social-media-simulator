from dash import dcc
from plotting import *

def get_messages_graphs(G):
    graphs = Plotter(G)

    new_graphs = [
        dcc.Graph(
            id='q_engagement',
            figure=graphs.plot_quality_engagement_scatter()
        ),
    ]

    return new_graphs