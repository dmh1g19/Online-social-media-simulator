from dash import dcc
from plotting import *

def get_network_graphs(G):
    graphs = Plotter(G)

    new_graphs = [
        dcc.Graph(
            id='degree-distribution',
            figure=graphs.plot_degree_distribution_by_type()
        ),
        dcc.Graph(
            id='authentic_vs_inauthentic',
            figure=graphs.plot_authentic_inauthentic_bar_chart()
        ),
        dcc.Graph(
            id='degree_dist',
            figure=graphs.plot_degree_distribution()
        ),
        dcc.Graph(
            id='degree_comparison',
            figure=graphs.plot_degree_comparison_authentic_inauthentic()
        )
    ]

    return new_graphs

