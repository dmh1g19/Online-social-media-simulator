from network import *
from visualize import *


def main():
    """
    Add a subnetwork of inauthentic nodes to the existing network of authentic nodes.

    n: Number of authentic nodes nodes
    beta: Number of inauthentic nodes in relation to authentic
    gamma: Amount of influence of inauthentic nodes (how any inauthentic nodes are followed by authentic ones, aka 'infiltration') 
    theta: Deception parameter, defined as the probability that bad actor content is irresistible
    m: Set amount of authentic nodes to follow by each inauthentic node
    """

    n = 10
    beta = 0.5
    gamma = 0.05 # Inauthentic influence increases the more authentic nodes follow them
    theta = 0
    m = 4

    G = create_authentic_subnetwork(n)
    add_inauthentic_subnetwork(G, beta, m)
    simulate_infiltration(G, gamma)

    graphs = Plotter(20, G)
    graphs.plot_degree_distribution_by_type()
    graphs.plot_authentic_inauthentic_bar_chart()
    graphs.plot_degree_distribution()
    graphs.plot_social_media_network_no_infiltration()
    graphs.plot_network_with_infiltration()
    graphs.plot_degree_comparison_authentic_inauthentic()
    graphs.show_graphs()


if __name__ == "__main__":
    main()
