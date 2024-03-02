import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

from topic_distribution import *


CURRENT_TIME_STEP = 0 


TOPICS = ["left_wing", "right_wing", "cars", "charity", "planes", "travel", "tech"]
TOPIC_WEIGHTS = [0.10, 0.20, 0.1, 0.05, 0.05, 0.2, 0.3] 

def generate_messages(G, num_messages, deception, time_step, finite_attention, flooding_factor, use_topic_based_resharing):
    """
    Generate messages for each node, where for authentic nodes, the engagement is the same as quality.
    Inauthentic nodes use deception to increase their message's engagement, potentially without a corresponding increase in quality.
    
    G: Network graph
    num_messages: Number of messages to generate for each node
    deception: Adjustment to engagement for messages from inauthentic nodes
    flooding_factor: Factor by which inauthentic nodes increase their message output to simulate flooding
    """

    for n, data in G.nodes(data=True):
        inauthentic = data.get('inauthentic', False)
        messages = data.get('messages', [])
        node_topic = data.get('topic')

        topic_index = TOPICS.index(node_topic)
        topic_weight = TOPIC_WEIGHTS[topic_index]

        # Adjust the number of messages for inauthentic nodes to simulate flooding
        total_messages = num_messages * (flooding_factor if inauthentic else 1)

        for _ in range(total_messages):
            # Generate base quality value for each message, which also serves as the base engagement for authentic messages


            if inauthentic:
                base_quality = 0 # Set to constant 0, could restrict quality based on a lower rand shreshold?
                engagement = min(base_quality + deception, 1.0)

                quality = base_quality
            else:
                # For authentic nodes, engagement is the same as quality, and quality is higher than 0 at least
                base_quality = np.random.rand()
                engagement = quality = base_quality

            if len(messages) >= finite_attention:
                messages.pop(0)

            messages.append({
                'engagement': engagement,
                'quality': quality,
                'origin': 'inauthentic' if inauthentic else 'authentic',
                'time_step': time_step,
                'topic': node_topic,
                'origin_node': n
            })

        G.nodes[n]['messages'] = messages

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

def reshare_messages(G, finite_attention):
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
                    reshare_to_followers(G, n, msg, finite_attention)

    return G

def simulate_time_steps(G, num_steps, num_messages, deception, finite_attention, node_selected, flooding_factor, use_topic_based_resharing):
    """
    Simulate the network's dynamics over a given number of time steps.
    Inauthentic nodes use topic-based resharing when 'use_topic_based_resharing' is True.
    """

    global CURRENT_TIME_STEP

    for step in range(num_steps):
        CURRENT_TIME_STEP = step

        for n in G.nodes():
            data = G.nodes[n]
            action_type = np.random.choice(['generate', 'reshare'], p=[node_selected, 1-node_selected])
            
            if action_type == 'generate':
                generate_messages(G, num_messages, deception, step, finite_attention, flooding_factor, use_topic_based_resharing)
            else:  
                if use_topic_based_resharing and data.get('inauthentic', True):
                    reshare_based_on_topic_similarity(G, finite_attention)
                else:
                    reshare_messages(G, finite_attention)

