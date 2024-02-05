import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

"""
Each message m in the model has two intrinsic and independent attributes. 

The appeal, a, models the likelihood that the message is actually reshared by agents. 
The quality, q, on the other hand, represents objective, desirable properties of content such as the originality of an idea or the accuracy of a claim
"""

def generate_messages(G, num_messages, deception):
    """
    Generate messages for each node. Inauthentic nodes use deception to increase their message's appeal.
    Each node has its own timeline.
    
    G: Network graph
    num_messages: Number of messages to generate for each node
    deception: Additional appeal for messages from inauthentic nodes
    """
    for n, data in G.nodes(data=True):
        inauthentic = data.get('inauthentic', False)
        messages = []
        for _ in range(num_messages):

            # TODO: Add topic/interest bias system here?

            base_appeal = np.random.rand()
            appeal = base_appeal + (deception if inauthentic else 0) #if inauthentic, increase appeal with the deception value
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

            if np.random.rand() < message['appeal']:  # simplifies resharing probability based on appeal, i think this is far too simple 
                # TODO: implement the logic to add this message to the followers' message lists
                pass  # Placeholder for resharing logic
