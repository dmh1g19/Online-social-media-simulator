from network import *
from messaging import *
from interface import *
from topic_distribution import *
from data_extraction import *

def main():
    """
    n: Number of authentic nodes nodes to initialize the network
    beta: Number of inauthentic nodes in relation to authentic
    gamma: Amount of influence of inauthentic nodes (how any inauthentic nodes are followed by authentic ones, aka 'infiltration')
    finite_attention: The size of the timeline for each node in the network
    theta: Deception parameter, defined as the probability that bad actor content is irresistible
    mu: The probability that a node will either generate a new message or reshare and existing one on their timeline
    m: Set amount of authentic nodes to follow by each inauthentic node (currently static)
    flooding_factor: Factor by which inauthentic nodes increase their message output to simulate flooding
    steps: The amount of time instances measured in steps from 1 to n
    msgs_per_step: How many messages to generate for each node per simulate_time_steps
    topic_similarity: Include topic bias in the similation
    """

    n = 35
    beta = 0.7
    gamma = 0.25 
    finite_attention = 160
    theta = 0.5
    mu = 0.55
    steps = 20
    msgs_per_step = 1
    flooding_factor = 1
    m = 4 #TODO: Integrate this parameter 
    topic_similarity = True 

    G = create_authentic_subnetwork(n, beta)
    add_inauthentic_subnetwork(G, beta, m)
    simulate_infiltration(G, gamma)
    assign_topic_distributions(G)
    simulate_time_steps(G, steps, msgs_per_step, theta, finite_attention, mu, flooding_factor, topic_similarity)

    extractor = DataExtractor(G)
    extractor.save_as_csv("data.csv")

    app = create_dash_app()
    make_layout(G, app)
    register_callbacks(app, G)
    run_server(app)


if __name__ == "__main__":
    main()

