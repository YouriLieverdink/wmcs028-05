import networkx as nx
import matplotlib.pyplot as plt
import itertools


"""
Create plot to display the different cliques, also print the number of maximal cliques.
"""
def cliques(G: nx.Graph) -> None:
    # G needs to be a projection
    max_cliques = list(nx.find_cliques(G))
    n_max_cliques = len(max_cliques)
    print(f"Number of max_cliques = {n_max_cliques}")

    largest_max_clique = max(len(c) for c in max_cliques)
    print(f"Largest maximal clique has size {largest_max_clique}")

    largest_cliques = [c for c in max_cliques if len(c) == largest_max_clique]

    # plot

    # create figure
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, seed=42)
    nx.draw_networkx(G, pos, node_size=10, edge_color="gray", alpha=0.5, with_labels=False)

    # highlight nodes and edges in the largest maximal cliques
    for clique in largest_cliques:
        nx.draw_networkx_nodes(G, pos, nodelist=clique, node_color="blue", node_size=50)
        nx.draw_networkx_edges(G, pos, edgelist=[(clique[i], clique[j]) for i in range(len(clique)) for j in range(i + 1, len(clique))], edge_color="blue")

    plt.title(f"Largest Maximal Cliques (size: {largest_max_clique})")
    plt.savefig("cliques.png")
    plt.show()



"""
Perform homophily analysis.
"""
def homophily(G: nx.Graph) -> float:
    pass

"""
Create plot to display the bridges.
"""
def bridges(G: nx.Graph) -> float:
    # G needs to be a projection
    bridges = list(nx.bridges(G))
    n_bridges = len(bridges)
    print(f"Number of bridges = {n_bridges}")

    # plot

    # create the subgraph
    bridge_nodes = set()
    for endpoint1, endpoint2 in bridges:
        bridge_nodes.add(endpoint1)
        bridge_nodes.add(endpoint2)

    smaller_G = set(bridge_nodes)  # create sub network
    sub_network = G.subgraph(smaller_G)
    pos = nx.spring_layout(sub_network, seed=42)

    # create figure
    plt.figure(figsize=(12, 8))
    nx.draw_networkx_nodes(sub_network, pos, node_size=50, node_color='lightblue')
    nx.draw_networkx_edges(sub_network, pos, edge_color='gray', alpha=0.5)
    nx.draw_networkx_edges(sub_network, pos, edgelist=bridges, edge_color='blue', width=2)  # bridges different color

    plt.title(f"Bridges in the Network (Sampled Subgraph)")
    plt.axis('off')
    plt.savefig("bridges.png")
    plt.show()

"""
Apply Girvan-Newman algorithm.
"""
def partitioning(G: nx.Graph) -> None:
    # G needs to be a projection
    k = 10  # adjust to divide into more/less components
    components = nx.community.girvan_newman(G)
    for communities in itertools.islice(component, k):
        print(tuple(sorted(c) for c in communities))

    


    pass
