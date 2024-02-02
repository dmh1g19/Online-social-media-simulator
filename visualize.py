import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import collections

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
        self.init_grid()

        degrees_authentic = [self.G.degree(n) for n, d in self.G.nodes(data=True) if not d.get('inauthentic', False)]
        degrees_inauthentic = [self.G.degree(n) for n, d in self.G.nodes(data=True) if d.get('inauthentic', False)]
    
        degree_count_authentic = collections.Counter(degrees_authentic)
        degree_count_inauthentic = collections.Counter(degrees_inauthentic)
    
        deg_authentic, cnt_authentic = zip(*degree_count_authentic.items())
        deg_inauthentic, cnt_inauthentic = zip(*degree_count_inauthentic.items())
        #fig, ax = plt.subplots()
        #plt.title("Degree Distribution for Authentic and Inauthentic Nodes")
        plt.loglog(deg_authentic, cnt_authentic, 'bo', markersize=5, label='Authentic')
        plt.loglog(deg_inauthentic, cnt_inauthentic, 'ro', markersize=5, label='Inauthentic')
        plt.xlabel("Degree")
        plt.ylabel("Frequency")
        plt.legend()
    
    def plot_authentic_inauthentic_bar_chart(self):
        self.init_grid()

        authentic_nodes = [n for n, d in self.G.nodes(data=True) if not d.get('inauthentic', False)]
        inauthentic_nodes = [n for n, d in self.G.nodes(data=True) if d.get('inauthentic', False)]
    
        categories = ['Authentic', 'Inauthentic']
        values = [len(authentic_nodes), len(inauthentic_nodes)]
    
        #plt.title('Count of Authentic and Inauthentic Nodes')
        plt.bar(categories, values, color=['blue', 'red'])
        plt.ylabel('Number of Nodes')
    

    def plot_degree_distribution(self):
        self.init_grid()
    
        degrees = [self.G.degree(n) for n in self.G.nodes()]
        unique_degrees = list(set(degrees))
        count_degrees = [degrees.count(x) for x in unique_degrees]
    
        plt.loglog(unique_degrees, count_degrees, 'bo-', markerfacecolor='red', markersize=8)
    
        plt.title("Degree Distribution on Log-Log Scale")
        plt.xlabel("Degree")
        plt.ylabel("Frequency")
    
    def plot_social_media_network_no_infiltration(self):
        self.init_grid()

        pos = nx.kamada_kawai_layout(self.G)
    
        # Separate nodes by attribute
        authentic_nodes = [node for node, data in self.G.nodes(data=True) if not data.get('inauthentic', False)]
        inauthentic_nodes = [node for node, data in self.G.nodes(data=True) if data.get('inauthentic', False)]
        
        nx.draw_networkx_nodes(self.G, pos, nodelist=authentic_nodes, node_color='blue', node_size=self.global_node_size, label='Authentic')
        nx.draw_networkx_nodes(self.G, pos, nodelist=inauthentic_nodes, node_color='red', node_size=self.global_node_size, label='Inauthentic')
        nx.draw_networkx_edges(self.G, pos, width=1.0, alpha=0.2)
        
        plt.axis('off')
        plt.legend(scatterpoints=1)
    
    def plot_network_with_infiltration(self):
        self.init_grid()

        pos = nx.kamada_kawai_layout(self.G)
        
        authentic_nodes = [n for n, d in self.G.nodes(data=True) if not d.get('inauthentic', False)]
        inauthentic_nodes = [n for n, d in self.G.nodes(data=True) if d.get('inauthentic', False)]
        
        nx.draw_networkx_nodes(self.G, pos, nodelist=authentic_nodes, node_color='blue', node_size=self.global_node_size, label='Authentic')
        nx.draw_networkx_nodes(self.G, pos, nodelist=inauthentic_nodes, node_color='red', node_size=self.global_node_size, label='Inauthentic')
        nx.draw_networkx_edges(self.G, pos, edgelist=self.G.edges(authentic_nodes), width=1.0, alpha=0.3)
        nx.draw_networkx_edges(self.G, pos, edgelist=self.G.edges(inauthentic_nodes), edge_color='red', width=1.0, alpha=1, style='dashed')
        
        plt.axis('off')
        plt.legend()

    def plot_degree_distribution_authentic(self):
        self.init_grid()
        
        degrees = [self.G.degree(n) for n in self.G.nodes()]

        unique_degrees = list(set(degrees))
        count_degrees = [degrees.count(x) for x in unique_degrees]
    
        plt.loglog(unique_degrees, count_degrees, 'bo-', markerfacecolor='red', markersize=8)
    
        plt.title("Degree Distribution on Log-Log Scale")
        plt.xlabel("Degree")
        plt.ylabel("Frequency")

    def plot_degree_comparison_authentic_inauthentic(self):
        self.init_grid()
        
        # Assuming the presence of an 'inauthentic' attribute that marks inauthentic nodes
        authentic_degrees = [self.G.degree(n) for n, attrs in self.G.nodes(data=True) if not attrs.get('inauthentic', False)]
        inauthentic_degrees = [self.G.degree(n) for n, attrs in self.G.nodes(data=True) if attrs.get('inauthentic', False)]

        # Calculate total degrees
        total_authentic_degrees = sum(authentic_degrees)
        total_inauthentic_degrees = sum(inauthentic_degrees)

        # Data for plotting
        categories = ['Authentic', 'Inauthentic']
        totals = [total_authentic_degrees, total_inauthentic_degrees]

        plt.bar(categories, totals, color=['blue', 'red'])
        #plt.title("Total Degrees Comparison")
        #plt.ylabel("Total Degrees")