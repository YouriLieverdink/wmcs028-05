import networkx as nx
import matplotlib.pyplot as plt
import itertools
import random
import csv
import pandas as pd



"""
Create plot to display the different cliques, also print the number of maximal cliques.
"""
def cliques(G: nx.Graph) -> nx.Graph:
    # find the maximal cliques in the graph
    max_cliques = list(nx.find_cliques(G))
    n_max_cliques = len(max_cliques)
    print(f"[RESULT] Number of max_cliques = {n_max_cliques}")

    largest_max_clique = max(len(c) for c in max_cliques)
    print(f"[RESULT] Largest maximal clique has size {largest_max_clique}")

    # show only 10 of those largest cliques
    largest_cliques = [c for c in max_cliques if len(c) == largest_max_clique]
    # sampled_cliques = random.sample(largest_cliques, min(len(largest_cliques), 10))

    # create a metagraph for visualization
    metagraph = nx.Graph()

    # add each sampled clique as a separate node
    for i, clique in enumerate(largest_cliques):
        metagraph.add_node(i, members=clique)  # node i represents a clique

    # add edges between clique-nodes if cliques share any nodes in the original graph
    for i in range(len(largest_cliques)):
        for j in range(i + 1, len(largest_cliques)):
            if set(largest_cliques[i]).intersection(largest_cliques[j]):
                metagraph.add_edge(i, j)

    colors = plt.cm.get_cmap('tab10', len(largest_cliques))

    # plot the metagraph
    plt.figure(figsize=(8, 6))
    metagraph_pos = nx.spring_layout(metagraph, seed=42)

    node_colors = [colors(i) for i in range(len(largest_cliques))]
    nx.draw_networkx_nodes(metagraph, metagraph_pos, node_size=500, node_color=node_colors, edgecolors="black")
    nx.draw_networkx_edges(metagraph, metagraph_pos, width=2, edge_color="gray", alpha=0.7)

    # Label each node by clique number (optional)
    # labels = {i: f"Clique {i+1}" for i in range(len(sampled_cliques))}
    # nx.draw_networkx_labels(metagraph, metagraph_pos, labels, font_size=10, font_color="black")

    plt.title("Metagraph of Sampled Cliques")
    plt.savefig("metagraph_cliques.png")
    plt.show()


    return largest_cliques


"""
Find bridges, save corresponding nodes to file and return subgraph [sG].
"""
def bridges(G: nx.Graph, output_path: str) -> nx.Graph:
    # G needs to be a projection
    bridges = list(nx.bridges(G))
    n_bridges = len(bridges)
    print(f"[RESULT] Number of bridges = {n_bridges}")

    # create the subgraph
    bridge_nodes = set()
    for endpoint1, endpoint2 in bridges:
        bridge_nodes.add(endpoint1)
        bridge_nodes.add(endpoint2)

    smaller_G = set(bridge_nodes)  # create sub network
    sG = G.subgraph(smaller_G)

    # save important nodes to a CSV file (ordered)
    node_degrees = [(node, degree) for node, degree in sG.degree()]
    sorted_nodes_by_degree = sorted(node_degrees, key=lambda x: x[1], reverse=True)
    with open(output_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["node_id", "degree"])
        for node, degree in sorted_nodes_by_degree:
            writer.writerow([node, degree])

    print(f"Most influential nodes written to {output_path}")
    return sG

"""
Apply Girvan-Newman algorithm.
"""
def partitioning(G: nx.Graph, output_path: str) -> None:
    pass
#     # G needs to be a projection
#     k = 10
#     components = nx.community.girvan_newman(G)
#
#     community_list = []
#
#     for i, communities in enumerate(itertools.islice(components, k)):
#         sorted_communities = sorted(tuple(sorted(c)) for c in communities)
#         community_list.append(sorted_communities)
#         print(f"Community {i+1}: {sorted_communities}")
#
#     # flatten the community list to save it to CSV file
#     flat_communities = []
#     for i, community in enumerate(community_list):
#         for c in community:
#             flat_communities.append({"Community": f"Community {i+1}", "Nodes": ', '.join(map(str, c))})
#
#     # Use pandas to save to CSV
#     df = pd.DataFrame(flat_communities)
#     df.to_csv(output_csv, index=False)
#     print(f"Communities saved to {output_csv}")
#
#     # visualization
#     plt.figure(figsize=(12, 8))
#     pos = nx.spring_layout(G, seed=42)
#     color_map = plt.cm.get_cmap('tab10', k)
#
#     # a different color for each community
#     for i, communities in enumerate(community_list):
#         for community in communities:
#             nx.draw_networkx_nodes(G, pos, nodelist=community, node_color=color_map(i), label=f'Community {i+1}', node_size=100)
#
#     nx.draw_networkx_edges(G, pos, alpha=0.5)
#
#     # labels/titles
#     plt.title("Girvan-Newman Community Detection")
#     plt.legend()
#     plt.savefig("girvan_newman_communities.png")
#     plt.show()
#
# # Example usage
# # G = nx.erdos_renyi_graph(100, 0.05)  # Example graph
# # partitioning(G)
#
#     return
