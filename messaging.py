import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def generate_messages(G, num_messages=100, deception=0.5):
    """
    Generate messages for each node, where for authentic nodes, the engagement is the same as quality.
    Inauthentic nodes use deception to increase their message's engagement, potentially without a corresponding increase in quality.
    
    G: Network graph
    num_messages: Number of messages to generate for each node
    deception: Adjustment to engagement for messages from inauthentic nodes
    """

    for n, data in G.nodes(data=True):
        inauthentic = data.get('inauthentic', False)
        messages = []
        for _ in range(num_messages):
            # Generate base quality value for each message, which also serves as the base engagement for authentic messages

            if inauthentic:
                base_quality = 0 # Set to constant 0, could restrict quality based on a lower rand shreshold?
                engagement = min(base_quality + deception, 1.0)
                quality = base_quality
            else:
                # For authentic nodes, engagement is the same as quality, and quality is higher than 0 at least
                base_quality = np.random.rand()
                engagement = quality = base_quality

            messages.append({'engagement': engagement, 'quality': quality, 'origin': 'inauthentic' if inauthentic else 'authentic'})

        G.nodes[n]['messages'] = messages

#def reshare_messages(G):
#    """
#    Reshare messages based on their relative engagement compared to the total engagement
#    of all messages in an agent's feed. This approach directly models the information diffusion
#    mechanism described in the paper, where resharing probability is proportional to message engagement.
#    """
#    for n in G.nodes():
#
#        if 'messages' in G.nodes[n]:
#            total_engagement = sum(msg['engagement'] for msg in G.nodes[n]['messages'])
#            if total_engagement > 0:
#
#                for msg in G.nodes[n]['messages']:
#                    reshare_probability = msg['engagement'] / total_engagement
#
#                    if np.random.rand() < reshare_probability:
#
#                        for follower in G.successors(n):
#                            if 'messages' not in G.nodes[follower]:
#                                G.nodes[follower]['messages'] = []
#
#                            if msg not in G.nodes[follower]['messages']:
#                                G.nodes[follower]['messages'].append(msg)
#
#    return G

def calculate_total_engagement(node_messages):
    """
    Calculate the total engagement of all messages for a given node.
    """

    return sum(msg['engagement'] for msg in node_messages)

def calculate_reshare_probability(message, total_engagement):
    """
    Calculate the reshare probability of a message based on its engagement
    relative to the total engagement of all messages.
    """

    return message['engagement'] / total_engagement if total_engagement > 0 else 0

def reshare_to_followers(G, node, message):
    """
    Reshare a message to all followers of the given node, ensuring no duplicates.
    """

    for follower in G.successors(node):
        if 'messages' not in G.nodes[follower]:
            G.nodes[follower]['messages'] = []
        if message not in G.nodes[follower]['messages']:
            G.nodes[follower]['messages'].append(message)

def reshare_messages(G):
    """
    Orchestrates the resharing of messages across the network, based on engagement.
    """

    for n in G.nodes():
        if 'messages' in G.nodes[n]:
            node_messages = G.nodes[n]['messages']
            total_engagement = calculate_total_engagement(node_messages)

            for msg in node_messages:
                reshare_probability = calculate_reshare_probability(msg, total_engagement)

                if np.random.rand() < reshare_probability:
                    reshare_to_followers(G, n, msg)

    return G
