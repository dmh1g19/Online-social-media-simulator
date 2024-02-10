from network import *
from plotting import *
from messaging import *
from interface import *


def main():
    """
    n: Number of authentic nodes nodes to initialize the network
    beta: Number of inauthentic nodes in relation to authentic
    gamma: Amount of influence of inauthentic nodes (how any inauthentic nodes are followed by authentic ones, aka 'infiltration')
    finite_attention: The size of the timeline for each node in the network
    theta: Deception parameter, defined as the probability that bad actor content is irresistible
    m: Set amount of authentic nodes to follow by each inauthentic node
    """

    n = 10
    beta = 0.5
    gamma = 0.05 
    finite_attention = 6  # number of messages each user sees
    theta = 0.5
    m = 4 #TODO: Integrate this value

    G = create_authentic_subnetwork(n)
    add_inauthentic_subnetwork(G, beta, m)
    simulate_infiltration(G, gamma)
    generate_messages(G, finite_attention, theta) 
    reshare_messages(G, finite_attention)

    app = create_dash_app()
    make_layout(G, app)
    register_callbacks(app, G)
    run_server(app)


if __name__ == "__main__":
    main()
