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
            id='topic_msg_distribution',
            figure=graphs.plot_topic_distribution_in_messages()
        ),
        dcc.Graph(
            id='eng_by_topic_authenticity',
            figure=graphs.plot_engagement_by_topic_and_authenticity()
        )
    ]

    return new_graphs

