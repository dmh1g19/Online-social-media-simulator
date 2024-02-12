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

    def plot_degree_distribution_with_message_count_overlay(self):
        degree_message_count_authentic = {}
        degree_message_count_inauthentic = {}

        for n in self.authentic_nodes:
            degree = self.G.degree(n)
            message_count = len(self.G.nodes[n].get('messages', []))
            if degree not in degree_message_count_authentic:
                degree_message_count_authentic[degree] = []
            degree_message_count_authentic[degree].append(message_count)

        for n in self.inauthentic_nodes:
            degree = self.G.degree(n)
            message_count = len(self.G.nodes[n].get('messages', []))
            if degree not in degree_message_count_inauthentic:
                degree_message_count_inauthentic[degree] = []
            degree_message_count_inauthentic[degree].append(message_count)

        avg_message_count_authentic = {deg: np.mean(counts) for deg, counts in degree_message_count_authentic.items()}
        avg_message_count_inauthentic = {deg: np.mean(counts) for deg, counts in degree_message_count_inauthentic.items()}

        degrees_authentic, avg_counts_authentic = zip(*sorted(avg_message_count_authentic.items()))
        degrees_inauthentic, avg_counts_inauthentic = zip(*sorted(avg_message_count_inauthentic.items()))

        fig = go.Figure()

        fig.add_trace(go.Scatter(x=degrees_authentic, y=avg_counts_authentic,
                                 mode='markers', name='Authentic Messages',
                                 marker=dict(color='blue'), text='Authentic'))

        fig.add_trace(go.Scatter(x=degrees_inauthentic, y=avg_counts_inauthentic,
                                 mode='markers', name='Inauthentic Messages',
                                 marker=dict(color='red'), text='Inauthentic'))

        fig.update_layout(title="Degree Distribution with Message Count Overlay",
                          xaxis_title="Degree",
                          yaxis_title="Average Message Count",
                          legend_title="Node Type",
                          xaxis_type="log",
                          yaxis_type="log")

        return fig

    def plot_node_influence_map(self):
        node_influence = []
        node_text = []
    
        for n, data in self.G.nodes(data=True):
            node_influence.append(self.G.degree(n))
            inauthentic = 'Inauthentic' if data.get('inauthentic', False) else 'Authentic'
            messages = data.get('messages', [])
            avg_engagement = np.mean([msg['engagement'] for msg in messages]) if messages else 0
            node_text.append(f"Node: {n}<br>Type: {inauthentic}<br>Avg Engagement: {avg_engagement:.2f}")
    
        fig = go.Figure(data=go.Scatter(
            x=[self.G.degree(n) for n in self.G.nodes()],  # X-axis - degrees
            y=[np.mean([msg['engagement'] for msg in data.get('messages', [])]) if data.get('messages') else 0 
               for _, data in self.G.nodes(data=True)],  # Y-axis - average engagement of messages
            mode='markers',
            marker=dict(
                size=[len(data.get('messages', [])) for _, data in self.G.nodes(data=True)],  # Size by the number of messages
                color=['red' if data.get('inauthentic', False) else 'blue' for _, data in self.G.nodes(data=True)],  # Color by node type
                opacity=0.8,
            ),
            text=node_text,
        ))
    
        fig.update_layout(
            title="Node Influence Map Based on Degree and Message Engagement",
            xaxis_title="Node Degree",
            yaxis_title="Average Message Engagement",
            legend_title="Node Type"
        )

        return fig

    def plot_avg_quality_and_engagement_over_time(self):
        time_step_quality = collections.defaultdict(list)
        time_step_engagement = collections.defaultdict(list)

        for _, data in self.G.nodes(data=True):
            for msg in data.get('messages', []):
                time_step_quality[msg['time_step']].append(msg['quality'])
                time_step_engagement[msg['time_step']].append(msg['engagement'])

        avg_quality_by_time_step = {step: np.mean(qualities) for step, qualities in time_step_quality.items()}
        avg_engagement_by_time_step = {step: np.mean(engagements) for step, engagements in time_step_engagement.items()}

        time_steps = sorted(set(avg_quality_by_time_step.keys()) | set(avg_engagement_by_time_step.keys()))
        avg_qualities = [avg_quality_by_time_step.get(step, None) for step in time_steps]
        avg_engagements = [avg_engagement_by_time_step.get(step, None) for step in time_steps]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=time_steps, y=avg_qualities, mode='lines+markers',
                                 name='Avg Quality', line=dict(color='royalblue', width=2),
                                 marker=dict(color='lightseagreen', size=8)))
        fig.add_trace(go.Scatter(x=time_steps, y=avg_engagements, mode='lines+markers',
                                 name='Avg Engagement', line=dict(color='firebrick', width=2),
                                 marker=dict(color='gold', size=8)))
        fig.update_layout(title='Average Quality and Engagement of Messages Over Time',
                          xaxis_title='Time Step',
                          yaxis_title='Average Value',
                          template='plotly_white')

        return fig
