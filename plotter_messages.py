import networkx as nx
import numpy as np
import collections
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px


class PlotterMessage:

    def __init__(self, G):
        self.G = G

        self.authentic_nodes = [n for n, d in self.G.nodes(data=True) if not d.get('inauthentic', False)]
        self.inauthentic_nodes = [n for n, d in self.G.nodes(data=True) if d.get('inauthentic', False)]

        self.degrees_authentic = [self.G.degree(n) for n, d in self.G.nodes(data=True) if not d.get('inauthentic', False)]
        self.degrees_inauthentic = [self.G.degree(n) for n, d in self.G.nodes(data=True) if d.get('inauthentic', False)]


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
        fig.add_trace(go.Scatter(x=quality_authentic, y=engagement_authentic, mode='markers', name='Authentic', marker=dict(color='blue')))
        fig.add_trace(go.Scatter(x=quality_inauthentic, y=engagement_inauthentic, mode='markers', name='Inauthentic', marker=dict(color='red')))

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

        fig.add_trace(go.Scatter(x=degrees_authentic, y=avg_counts_authentic, mode='markers', name='Authentic Messages', marker=dict(color='blue'), text='Authentic'))

        fig.add_trace(go.Scatter(x=degrees_inauthentic, y=avg_counts_inauthentic, mode='markers', name='Inauthentic Messages', marker=dict(color='red'), text='Inauthentic'))

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
        fig.add_trace(go.Scatter(x=time_steps, y=avg_qualities, mode='lines+markers', name='Avg Quality', line=dict(color='royalblue', width=2), marker=dict(color='lightseagreen', size=8)))
        fig.add_trace(go.Scatter(x=time_steps, y=avg_engagements, mode='lines+markers', name='Avg Engagement', line=dict(color='firebrick', width=2), marker=dict(color='gold', size=8)))

        fig.update_layout(title='Average Quality and Engagement of Messages Over Time', xaxis_title='Time Step', yaxis_title='Average Value', template='plotly_white')

        return fig

    def plot_message_production_over_time(self):
        time_step_message_count = {'authentic': collections.defaultdict(int), 'inauthentic': collections.defaultdict(int)}
    
        for n, data in self.G.nodes(data=True):
            node_type = 'inauthentic' if data.get('inauthentic', False) else 'authentic'
            for message in data.get('messages', []):
                time_step_message_count[node_type][message['time_step']] += 1
    
        time_steps = sorted(set(time_step_message_count['authentic']) | set(time_step_message_count['inauthentic']))
        authentic_counts = [time_step_message_count['authentic'].get(step, 0) for step in time_steps]
        inauthentic_counts = [time_step_message_count['inauthentic'].get(step, 0) for step in time_steps]
    
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=time_steps, y=authentic_counts, mode='lines+markers', name='Authentic', line=dict(color='blue', width=2), marker=dict(color='blue', size=8)))
        fig.add_trace(go.Scatter(x=time_steps, y=inauthentic_counts, mode='lines+markers', name='Inauthentic', line=dict(color='red', width=2), marker=dict(color='red', size=8)))

        fig.update_layout(title='Message Production Over Time',
                          xaxis_title='Time Step',
                          yaxis_title='Number of Messages Produced',
                          legend_title='Node Type',
                          template='plotly_white')
    
        return fig

