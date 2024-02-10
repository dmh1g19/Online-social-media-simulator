import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def create_authentic_subnetwork(n=100, beta=0.05):
    """
    Create a subnetwork of authentic nodes.
    n: Number of authentic nodes
    beta: Proportion of inauthentic nodes to authentic nodes
    """

    G_authentic = nx.scale_free_graph(n)
    G_authentic = G_authentic.to_directed()
    G_authentic.remove_edges_from(nx.selfloop_edges(G_authentic))
    return G_authentic

def add_inauthentic_subnetwork(G, beta, m):
    """
    Add a subnetwork of inauthentic nodes to the existing network of authentic nodes.

    G_authentic: The existing network of authentic nodes
    beta: Proportion of inauthentic nodes to authentic nodes
    """

    n_authentic = len(G)
    n_inauthentic = int(n_authentic * beta)
    
    for i in range(n_authentic, n_authentic + n_inauthentic, m):
        G.add_node(i, inauthentic=True)
        
        # For simplicity, connect each inauthentic node to `m` random authentic nodes (m edges from inauthentic to authentic nodes)
        #TODO: Randomize m?
        targets = np.random.choice(n_authentic, m, replace=False)
        for target in targets:
            G.add_edge(i, target)

    return G

def simulate_infiltration(G, gamma):
    """
    Simulate bad actor infiltration into the social network,
    basically the scenario where a certain percentage of authentic users unknowingly follow inauthentic accounts,
    thereby modeling the 'infiltration' of bad actors into the social network.


    G: The social network graph including both authentic and inauthentic nodes.
    gamma: The probability that a bad actor is followed by an authentic agent.
    """

    authentic_nodes = [node for node, attrs in G.nodes(data=True) if not attrs.get('inauthentic', False)]
    inauthentic_nodes = [node for node, attrs in G.nodes(data=True) if attrs.get('inauthentic', False)]

    for inauthentic_node in inauthentic_nodes:
        for authentic_node in authentic_nodes:
            if np.random.rand() < gamma:
                G.add_edge(authentic_node, inauthentic_node)

    return G
