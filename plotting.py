import networkx as nx
import numpy as np
import collections
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

"""
    This module is purely for generating graphs to view the results of the simulation.
"""

class Plotter:

    def __init__(self, G):
        self.G = G

        self.authentic_nodes = [n for n, d in self.G.nodes(data=True) if not d.get('inauthentic', False)]
        self.inauthentic_nodes = [n for n, d in self.G.nodes(data=True) if d.get('inauthentic', False)]

        self.degrees_authentic = [self.G.degree(n) for n, d in self.G.nodes(data=True) if not d.get('inauthentic', False)]
        self.degrees_inauthentic = [self.G.degree(n) for n, d in self.G.nodes(data=True) if d.get('inauthentic', False)]


    def plot_degree_distribution_by_type(self):
        degree_count_authentic = collections.Counter(self.degrees_authentic)
        degree_count_inauthentic = collections.Counter(self.degrees_inauthentic)

        deg_authentic, cnt_authentic = zip(*degree_count_authentic.items())
        deg_inauthentic, cnt_inauthentic = zip(*degree_count_inauthentic.items())

        fig = go.Figure()

        fig.add_trace(go.Scatter(x=deg_authentic, y=cnt_authentic, mode='markers', name='Authentic',
                                 marker=dict(color='blue', size=5),))
        fig.add_trace(go.Scatter(x=deg_inauthentic, y=cnt_inauthentic, mode='markers', name='Inauthentic',
                                 marker=dict(color='red', size=5),))
        fig.update_layout(title="Degree Distribution for Authentic and Inauthentic Nodes",
                          xaxis_title="Degree",
                          yaxis_title="Frequency",
                          xaxis_type="log",
                          yaxis_type="log",
                          legend_title="Node Type")

        return fig

    def plot_authentic_inauthentic_bar_chart(self):
        categories = ['Authentic', 'Inauthentic']
        values = [len(self.authentic_nodes), len(self.inauthentic_nodes)]

        fig = go.Figure()

        fig.add_trace(go.Bar(x=categories, y=values, marker_color=['blue', 'red']))
        fig.update_layout(title_text='Count of Authentic and Inauthentic Nodes',
                          xaxis_title="Category",
                          yaxis_title="Number of Nodes",
                          )

        return fig

    def plot_degree_distribution(self):
        degrees = [self.G.degree(n) for n in self.G.nodes()]
        unique_degrees = list(set(degrees))
        count_degrees = [degrees.count(x) for x in unique_degrees]

        fig = go.Figure()

        # Add scatter plot on log-log scale
        fig.add_trace(go.Scatter(x=unique_degrees, y=count_degrees,
                                 mode='markers+lines', 
                                 marker=dict(color='blue', size=8, line=dict(color='red', width=2))))

        fig.update_xaxes(type="log", title_text="Degree")
        fig.update_yaxes(type="log", title_text="Frequency")
        fig.update_layout(title_text="Degree Distribution on Log-Log Scale")

        return fig

    def plot_degree_comparison_authentic_inauthentic(self):
        total_authentic_degrees = sum(self.degrees_authentic)
        total_inauthentic_degrees = sum(self.degrees_inauthentic)

        categories = ['Authentic', 'Inauthentic']
        totals = [total_authentic_degrees, total_inauthentic_degrees]

        fig = go.Figure()
        fig.add_trace(go.Bar(x=categories, y=totals, marker_color=['blue', 'red']))
        fig.update_layout(title_text="Total Degrees Comparison",
                          xaxis_title="Category",
                          yaxis_title="Total Degrees")

        return fig

    def plot_quality_engagement_scatter(self):
        quality_authentic = []
        engagement_authentic = []
        quality_inauthentic = []
        engagement_inauthentic = []

        for n, data in self.G.nodes(data=True):
            messages = data.get('messages', [])
            for message in messages:
                if data.get('inauthentic', False):
                    quality_inauthentic.append(message['quality'])
                    engagement_inauthentic.append(message['engagement'])
                else:
                    quality_authentic.append(message['quality'])
                    engagement_authentic.append(message['engagement'])

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=quality_authentic, y=engagement_authentic,
                                 mode='markers', name='Authentic',
                                 marker=dict(color='blue')))
        fig.add_trace(go.Scatter(x=quality_inauthentic, y=engagement_inauthentic,
                                 mode='markers', name='Inauthentic',
                                 marker=dict(color='red')))

        fig.update_layout(title='Quality vs. Engagement Scatter Plot For Entire Graph',
                          xaxis_title='Quality',
                          yaxis_title='Engagement',
                          legend_title='Node Type')

        return fig
