import numpy as np
import networkx as nx
from topics import *


def assign_topic_distributions(G):
    """
    Assign topics to each node based on the popularity of the topics.
    """

    for n in G.nodes():
        chosen_topic = np.random.choice(TOPICS, p=TOPIC_WEIGHTS)
        G.nodes[n]['topic'] = chosen_topic

def topic_similarity(distribution1, distribution2, epsilon=1e-10):
    """
    Calculate similarity between two topic distributions, adding stability for edge cases.
    """

    denom = (np.linalg.norm(distribution1) * np.linalg.norm(distribution2)) + epsilon

    return np.dot(distribution1, distribution2) / denom

def reshare_to_followers(G, node, message, finite_attention):
    """
    Reshare a message to all followers of the given node, ensuring no duplicates and adhering to the maximum timeline length.
    """

    for follower in G.successors(node):
        if 'messages' not in G.nodes[follower]:
            G.nodes[follower]['messages'] = []
        
        if message not in G.nodes[follower]['messages']:
            if len(G.nodes[follower]['messages']) >= finite_attention:
                G.nodes[follower]['messages'].pop(0)  # FIFO to simulate message decay/aging on the timeline
            
            G.nodes[follower]['messages'].append(message)

def reshare_based_on_topic_similarity(G, finite_attention):
    """
    Reshare messages considering the topic of the message and the node's interest.
    """

    for n, data in G.nodes(data=True):
        node_topic = data.get('topic')
        if 'messages' in data:
            for msg in data['messages']:
                if msg['topic'] == node_topic:
                    reshare_to_followers(G, n, msg, finite_attention)

