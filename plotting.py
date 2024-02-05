import networkx as nx
import numpy as np
import collections
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px


class Plotter:

    def __init__(self, node_size, G):
        self.global_node_size = node_size
        self.graphs_added = 0
        self.G = G
        plt.figure(figsize=(8, 6))

    def init_grid(self):
        self.graphs_added += 1
        plt.subplot(2,3,self.graphs_added)

    def show_graphs(self):
        plt.show()


    def plot_degree_distribution_by_type(self):

        degrees_authentic = [self.G.degree(n) for n, d in self.G.nodes(data=True) if not d.get('inauthentic', False)]
        degrees_inauthentic = [self.G.degree(n) for n, d in self.G.nodes(data=True) if d.get('inauthentic', False)]

        degree_count_authentic = collections.Counter(degrees_authentic)
        degree_count_inauthentic = collections.Counter(degrees_inauthentic)

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
        self.init_grid()

        authentic_nodes = [n for n, d in self.G.nodes(data=True) if not d.get('inauthentic', False)]
        inauthentic_nodes = [n for n, d in self.G.nodes(data=True) if d.get('inauthentic', False)]

        categories = ['Authentic', 'Inauthentic']
        values = [len(authentic_nodes), len(inauthentic_nodes)]

        fig = go.Figure()

        fig.add_trace(go.Bar(x=categories, y=values, marker_color=['blue', 'red']))
        fig.update_layout(title_text='Count of Authentic and Inauthentic Nodes',
                          xaxis_title="Category",
                          yaxis_title="Number of Nodes",
                          )

        return fig

    def plot_degree_distribution(self):
        self.init_grid()

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
        self.init_grid()

        # Assuming the presence of an 'inauthentic' attribute that marks inauthentic nodes
        authentic_degrees = [self.G.degree(n) for n, attrs in self.G.nodes(data=True) if not attrs.get('inauthentic', False)]
        inauthentic_degrees = [self.G.degree(n) for n, attrs in self.G.nodes(data=True) if attrs.get('inauthentic', False)]

        # Calculate total degrees
        total_authentic_degrees = sum(authentic_degrees)
        total_inauthentic_degrees = sum(inauthentic_degrees)

        categories = ['Authentic', 'Inauthentic']
        totals = [total_authentic_degrees, total_inauthentic_degrees]

        fig = go.Figure()
        fig.add_trace(go.Bar(x=categories, y=totals, marker_color=['blue', 'red']))
        fig.update_layout(title_text="Total Degrees Comparison",
                          xaxis_title="Category",
                          yaxis_title="Total Degrees")

        return fig
