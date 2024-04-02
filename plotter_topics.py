import networkx as nx
import numpy as np
import collections
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px


class PlotterTopic:

    def __init__(self, G):
        self.G = G

        self.authentic_nodes = [n for n, d in self.G.nodes(data=True) if not d.get('inauthentic', False)]
        self.inauthentic_nodes = [n for n, d in self.G.nodes(data=True) if d.get('inauthentic', False)]

        self.degrees_authentic = [self.G.degree(n) for n, d in self.G.nodes(data=True) if not d.get('inauthentic', False)]
        self.degrees_inauthentic = [self.G.degree(n) for n, d in self.G.nodes(data=True) if d.get('inauthentic', False)]

    def plot_topic_distribution_across_network(self):
        topic_counts = collections.Counter(data['topic'] for _, data in self.G.nodes(data=True) if 'topic' in data)

        topics = list(topic_counts.keys())
        counts = list(topic_counts.values())

        fig = go.Figure([go.Bar(x=topics, y=counts, marker_color='indianred')])
        fig.update_layout(title_text='Topic Distribution Across the Network for each user/node',
                          xaxis_title="Topics",
                          yaxis_title="Count of Nodes",
                          template="plotly_white")
        return fig

    def plot_topic_distribution_in_messages(self):
        topic_counts = collections.defaultdict(int)
        for _, data in self.G.nodes(data=True):
            for msg in data.get('messages', []):
                topic_counts[msg['topic']] += 1
    
        topics = list(topic_counts.keys())
        counts = list(topic_counts.values())
    
        fig = go.Figure([go.Bar(x=topics, y=counts, marker_color='indianred')])
        fig.update_layout(
            title_text='Distribution of Topics Across All Messages',
            xaxis_title="Topics",
            yaxis_title="Message Count",
            template="plotly_white"
        )
        return fig
   
    def plot_engagement_by_topic_and_authenticity(self):
        topic_engagement_authentic = collections.defaultdict(list)
        topic_engagement_inauthentic = collections.defaultdict(list)
    
        for n, data in self.G.nodes(data=True):
            is_inauthentic = data.get('inauthentic', False)
            for msg in data.get('messages', []):
                if is_inauthentic:
                    topic_engagement_inauthentic[msg['topic']].append(msg['engagement'])
                else:
                    topic_engagement_authentic[msg['topic']].append(msg['engagement'])
    
        avg_engagement_authentic = {topic: np.mean(engagements) for topic, engagements in topic_engagement_authentic.items()}
        avg_engagement_inauthentic = {topic: np.mean(engagements) for topic, engagements in topic_engagement_inauthentic.items()}
    
        topics = list(set(avg_engagement_authentic.keys()) | set(avg_engagement_inauthentic.keys()))
        avg_authentic = [avg_engagement_authentic.get(topic, 0) for topic in topics]
        avg_inauthentic = [avg_engagement_inauthentic.get(topic, 0) for topic in topics]
    
        fig = go.Figure()
        #fig.add_trace(go.Scatter(x=topics, y=avg_authentic, mode='markers', name='Authentic', marker=dict(color='blue', size=10)))
        fig.add_trace(go.Scatter(x=topics, y=avg_inauthentic, mode='markers', name='Inauthentic', marker=dict(color='red', size=10)))
    
        #fig.update_layout(title='Average Engagement by Topic and Authenticity', xaxis_title='Topic', yaxis_title='Average Engagement', template='plotly_white')
        fig.update_layout(title='Average Engagement by Topic', xaxis_title='Topic', yaxis_title='Average Engagement', template='plotly_white')
        
        return fig
    

