import networkx as nx
import matplotlib.pyplot as plt
import itertools
import random
import csv
import pandas as pd
from tqdm import tqdm


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


    return largest_cliques

def cliques_2o(G: nx.Graph) -> None:
    # Find the cliques
    pages = [n for n in G.nodes if n.startswith('p')]
    users = set(G.nodes) - set(pages)

    # Dictionary to store the cliques
    cliques = {}

    # Iterate over all pages
    for page in tqdm(pages):
        # Get all users that edited this page
        users_for_page = list(G.neighbors(page))

        if len(users_for_page) > 1:  # At least two users are needed to form a clique
            cliques[page] = users_for_page

    largest_cliques = sorted(cliques.items(), key=lambda item: len(item[1]), reverse=True)[:10]

    print(f"[RESULT] Number of max_cliques = {len(cliques)}")

    largest_max_clique = max(len(users) for users in cliques.values())
    print(f"[RESULT] Largest maximal clique has size {largest_max_clique}")

    return largest_cliques

"""
Create a CSV file with the edges of the  two largest cliques
"""
def two_pages_cliques(G: nx.Graph, output_path: str) -> None:
    largest_cliques = cliques_2o(G)

    # get the two largest cliques
    page_1, users_1 = largest_cliques[0]
    page_2, users_2 = largest_cliques[1]

    edges = []

    # collect the edges
    for user in users_1:
        edges.append((user, page_1))
    for user in users_2:
        edges.append((user, page_2))

    # save to CSV
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Source', 'Target'])
        writer.writerows(edges)

    print(f"[RESULT] Edges saved to {output_path} for pages: {page_1}, {page_2} with {len(users_1) + len(users_2)} total user nodes.")


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
    # G needs to be a projection
    k = 10
    components = nx.community.girvan_newman(G)

    community_list = []

    for i, communities in enumerate(itertools.islice(components, k)):
        sorted_communities = sorted(tuple(sorted(c)) for c in communities)
        community_list.append(sorted_communities)
        print(f"Community {i+1}: {sorted_communities}")

    # flatten the community list to save it to CSV file
    flat_communities = []
    for i, community in enumerate(community_list):
        for c in community:
            flat_communities.append({"Community": f"Community {i+1}", "Nodes": ', '.join(map(str, c))})

    # create CSV
    df = pd.DataFrame(flat_communities)
    df.to_csv(output_csv, index=False)
    print(f"Communities saved to {output_csv}")
