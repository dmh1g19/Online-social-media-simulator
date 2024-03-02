from dash import dcc
from plotting import *

def get_topic_graphs(G):
    graphs = Plotter(G)

    new_graphs = [
        dcc.Graph(
            id='topic_distribution',
            figure=graphs.plot_topic_distribution_across_network()
        ),
        dcc.Graph(
            id='engagement_by_topic',
            figure=graphs.plot_node_engagement_by_topic()
        ),
        dcc.Graph(
            id='topic_msg_distribution',
            figure=graphs.plot_topic_distribution_in_messages()
        )
    ]

    return new_graphs

