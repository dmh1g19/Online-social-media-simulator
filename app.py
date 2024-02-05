from network import *
from plotting import *
from messaging import *
from interface import *


def main():
    """
    Add a subnetwork of inauthentic nodes to the existing network of authentic nodes.

    n: Number of authentic nodes nodes
    beta: Number of inauthentic nodes in relation to authentic
    gamma: Amount of influence of inauthentic nodes (how any inauthentic nodes are followed by authentic ones, aka 'infiltration') 
           -> As inauthentic influence increases the more authentic nodes follow them
    theta: Deception parameter, defined as the probability that bad actor content is irresistible
    m: Set amount of authentic nodes to follow by each inauthentic node
    """

    n = 50
    beta = 0.5
    gamma = 0.05 
    num_messages = 100
    theta = 0.5

    m = 4 #TODO: Integrate this values

    # Generate Network
    G = create_authentic_subnetwork(n)
    add_inauthentic_subnetwork(G, beta, m)
    simulate_infiltration(G, gamma)
    generate_messages(G, num_messages, theta) 
    #reshare_messages(G)

    # Display content
    app = create_dash_app()
    make_layout(G, app)
    register_callbacks(app, G)
    run_server(app)


if __name__ == "__main__":
    main()