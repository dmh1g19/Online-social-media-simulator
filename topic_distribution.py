import numpy as np
import networkx as nx

TOPICS = ["left_wing", "right_wing", "cars", "charity", "planes", "travel", "tech"]
TOPIC_WEIGHTS = [0.10, 0.20, 0.1, 0.05, 0.05, 0.2, 0.3] 

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

# TODO: integrate similarity_threshold metric for better adjustability
def reshare_based_on_topic_similarity(G, finite_attention, similarity_threshold=0.5):
    """
    Reshare messages considering topic similarity between nodes, with an adjustable similarity threshold.
    """

    for n, data in G.nodes(data=True):
        node_topic_distribution = data.get('topic_distribution', np.zeros(len(TOPICS)))
        if 'messages' in data:
            for msg in data['messages']:
                original_node = msg['origin_node']
                original_node_topic_distribution = G.nodes[original_node].get('topic_distribution', np.zeros(len(TOPICS)))
                similarity = topic_similarity(node_topic_distribution, original_node_topic_distribution)
                
                if similarity > similarity_threshold:
                    reshare_to_followers(G, n, msg, finite_attention)

