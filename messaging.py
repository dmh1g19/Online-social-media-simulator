import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def generate_messages(G, num_messages=100, deception=0.5):
    """
    Generate messages for each node. Inauthentic nodes use deception to increase their message's appeal.
    
    G: Network graph
    num_messages: Number of messages to generate for each node
    deception: Additional appeal for messages from inauthentic nodes
    """
    for n, data in G.nodes(data=True):
        inauthentic = data.get('inauthentic', False)
        messages = []
        for _ in range(num_messages):
            base_appeal = np.random.rand()  # Base appeal for authentic nodes, rendom for now until I figure out how to properly derive it
            appeal = base_appeal + (deception if inauthentic else 0)
            messages.append({'appeal': appeal, 'origin': 'inauthentic' if inauthentic else 'authentic'})
        G.nodes[n]['messages'] = messages

def reshare_messages(G):
    """
    Simulate the resharing of messages based on their appeal. Higher appeal increases resharing probability.
    """
    for n, data in G.nodes(data=True):
        messages = data.get('messages', [])
        for message in messages:
            # TODO: Simplified resharing logic: more appealing messages are more likely to be reshared

            if np.random.rand() < message['appeal']:  # simplifies resharing probability based on appeal
                # TODO: implement the logic to add this message to the followers' message lists
                pass  # Placeholder for resharing logic
