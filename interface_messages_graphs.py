from dash import dcc
from plotting import *


def get_messages_graphs(G):
    graphs = Plotter(G)

    new_graphs = [
        dcc.Graph(
            id='q_engagement',
            figure=graphs.plot_quality_engagement_scatter()
        ),
        dcc.Graph(
            id='degree_dist_with_msg_count',
            figure=graphs.plot_degree_distribution_with_message_count_overlay()
        ),
        dcc.Graph(
            id='influence_score',
            figure=graphs.plot_node_influence_map()
        ),
        dcc.Graph(
            id='msg_temporal',
            figure=graphs.plot_avg_quality_and_engagement_over_time()
        ),
    ]

    return new_graphs
