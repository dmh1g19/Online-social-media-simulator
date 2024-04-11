import networkx as nx
import pandas as pd
import numpy as np

class DataExtractor:
    def __init__(self, G):
        self.G = G

    def extract_node_data(self):
        """
        Extracts data for each node in the graph.
        Returns a DataFrame with node features.
        """

        node_data = []

        for node, data in self.G.nodes(data=True):
            messages = data.get('messages', [])
            avg_engagement = np.mean([msg['engagement'] for msg in messages]) if messages else 0
            avg_quality = np.mean([msg['quality'] for msg in messages]) if messages else 0

            node_info = {
                'node_id': node,
                'degree': self.G.degree(node),
                'topic': data.get('topic', None),
                'avg_engagement': avg_engagement,
                'avg_quality': avg_quality,
                'message_count': len(self.G.nodes[node].get('messages', [])),
                'inauthentic': data.get('inauthentic', 'False') 
                #'messages': data.get('messages', "NaN")[0]["quality"],
            }
            node_data.append(node_info)

        df = pd.DataFrame(node_data)
        return df

    def save_as_csv(self, filename):
        """
        Extracts node data and saves it to a CSV file.
        """

        df = self.extract_node_data()
        df.to_csv(filename, index=False)

