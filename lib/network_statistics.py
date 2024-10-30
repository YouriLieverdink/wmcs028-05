import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
import random
from collections import Counter
from lib.utilities import convert_to_csv
from datetime import datetime

"""
The number of nodes in the graph.
"""
def number_of_nodes(G: nx.Graph) -> int:
  return G.number_of_nodes()

"""
The number of edges in the graph.
"""
def number_of_edges(G: nx.Graph) -> int:
  return G.number_of_edges()

"""
The number of edges, disregarding varients with different timestamp.
"""
def number_of_unique_edges(G: nx.Graph) -> int:
    unique_edges = set()
    for endpoint1, endpoint2, data in G.edges(data=True):
        edge = (endpoint1, endpoint2)
        unique_edges.add(edge)
    return len(unique_edges)

"""
The number of nodes that are pages
"""
def number_of_pages(G: nx.Graph) -> int:
    pages = {node for node, attr in G.nodes(data=True) if attr.get('subset') == 'page'}
    return len(pages)

"""
The number of nodes that are users
"""
def number_of_users(G: nx.Graph) -> int:
    users = {node for node, attr in G.nodes(data=True) if attr.get('subset') == 'user'}
    return len(users)

"""
The density of the graph.
"""
def density(G: nx.Graph) -> float:
    return number_of_unique_edges(G)/(number_of_pages(G) * number_of_users(G))

"""
Build graphs for displaying the degree distribution.
"""
def degree_distribution(G: nx.Graph) -> None:
    # create two sets (by iterating through each component)
    if nx.is_connected(G):
        top, bottom = nx.bipartite.sets(G)
    else:
        components = list(nx.connected_components(G))
        top, bottom = set(), set()

        for component in components:
            sG = G.subgraph(component)
            if nx.is_bipartite(sG):
                top_set, bottom_set = nx.bipartite.sets(sG)
                top.update(top_set)
                bottom.update(bottom_set)
            else:
                print("Component is not bipartite:", component)

    # get the degree of all users and store both user id and degree
    top_degrees = [(n, d) for n, d in G.degree(top)]
    top_degree_sequence = sorted(top_degrees, key=lambda x: x[1], reverse=True)

    # extract the node with the maximum degree
    max_degree_node, max_degree = top_degree_sequence[0]
    min_degree_node, min_degree = top_degree_sequence[-1]
    average_degree = np.average([d for _, d in top_degree_sequence])

    print(f"[RESULT] Maximum degree of users = {max_degree}, user = {max_degree_node}")
    print(f"[RESULT] Minimum degree of users = {min_degree}")
    print(f"[RESULT] Average degree of users = {average_degree}")

    # get the degree of all pages and store both page id and degree
    bottom_degrees = [(n, d) for n, d in G.degree(bottom)]
    bottom_degree_sequence = sorted(bottom_degrees, key=lambda x: x[1], reverse=True)

    # extract the node with the maximum degree
    max_degree_node, max_degree = bottom_degree_sequence[0]
    min_degree_node, min_degree = bottom_degree_sequence[-1]
    average_degree = np.average([d for _, d in bottom_degree_sequence])

    print(f"[RESULT] Maximum degree of pages = {max_degree}, user = {max_degree_node}")
    print(f"[RESULT] Minimum degree of pages = {min_degree}")
    print(f"[RESULT] Average degree of pages = {average_degree}")

    # plot
    top_degree_sequence = np.array([d for _, d in top_degree_sequence])
    bottom_degree_sequence = np.array([d for _, d in bottom_degree_sequence])
    top_bins = np.logspace(np.log10(top_degree_sequence.min()), np.log10(top_degree_sequence.max()), 100)
    top_hist, top_bin_edges = np.histogram(top_degree_sequence, bins=top_bins)

    bottom_bins = np.logspace(np.log10(bottom_degree_sequence.min()), np.log10(bottom_degree_sequence.max()), 100)
    bottom_hist, bottom_bin_edges = np.histogram(bottom_degree_sequence, bins=bottom_bins)

    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.bar(top_bin_edges[:-1], top_hist, width=np.diff(top_bin_edges), edgecolor="black", align="edge")
    plt.xscale('log')
    plt.yscale('log')
    plt.title('Degree distribution (users)')
    plt.xlabel('Degree')
    plt.ylabel('# of Nodes')

    plt.subplot(1, 2, 2)
    plt.bar(bottom_bin_edges[:-1], bottom_hist, width=np.diff(bottom_bin_edges), edgecolor="black", align="edge")
    plt.xscale('log')
    plt.yscale('log')
    plt.title('Degree distribution (pages)')
    plt.xlabel('Degree')
    plt.ylabel('# of Nodes')

    plt.savefig("degree_distribution.png")
    plt.show()

"""
Create plot to display the different clusters.
"""
def clusters(G: nx.Graph) -> None:
    pass

"""
Compute the average clustering coefficient of the network.
"""
def avg_clustering_coefficient(G: nx.Graph) -> float:
    pass

"""
Compute the clustering coefficient of all individual nodes.
"""
def clustering_coefficient(G: nx.Graph) -> float:
    pass

"""
Determine the number of connected components of graph [G], and return a
sub graph [sG] with sampled connected components for visualization.
"""
def connected_components(G: nx.Graph, output_path: str) -> nx.Graph:
    # sort the connected components and get sizes
    connected_components = sorted(nx.connected_components(G), key=len)
    component_sizes = [len(component) for component in connected_components]

    # count how often each component size occurs
    size_counts = Counter(component_sizes)

    # save size counts to a CSV
    size_counts_df = pd.DataFrame(size_counts.items(), columns=["Component Size", "Count"])
    size_counts_df = size_counts_df.sort_values(by="Component Size", ascending=False)
    size_counts_df.to_csv(output_path, index=False)

    print(f"[RESULT] Component size counts saved to {output_path}")

    # identify the largest component
    largest_component = list(connected_components[-1])
    largest_component_graph = G.subgraph(largest_component)
    largest_component_graph = nx.Graph(largest_component_graph) # disregard multiple edges between same 2 nodes

    # sample connected nodes from the largest component
    start_node = random.choice(list(largest_component_graph.nodes()))
    sampled_nodes = set()

    # bfs to find connected nodes
    queue = [start_node]
    visited = set()
    while queue and len(sampled_nodes) < 80:
        current = queue.pop(0)
        if current not in visited:
            visited.add(current)
            sampled_nodes.add(current)
            queue.extend(set(largest_component_graph.neighbors(current)) - visited)  # Add unvisited neighbors

    # sample 10 smaller components
    small_components = connected_components[:-1]
    num_small_samples = 10
    selected_small_components = random.sample(small_components, min(num_small_samples, len(small_components)))

    for component in selected_small_components:
        sampled_nodes.update(component)

    # create the subgraph with the sampled nodes
    sG = G.subgraph(sampled_nodes).copy()

    print(f"[INFO] Number of nodes in sG = {len(sG.nodes())}, edges: {sG.number_of_edges()}")
    print(f"[INFO] Total number of sampled connected nodes from largest and small components = {len(sampled_nodes)}")

    return sG


"""
Determine the largest connected component of graph [G] and return it.
"""
def largest_cc(G: nx.Graph) -> nx.Graph:
    largest_cc = max(nx.connected_components(G), key=len)

    return G.subgraph(largest_cc)

"""
Compute the degree centrality for each node in [G] and save top to k csv file.
"""
def degree_centrality(G: nx.Graph, output_path: str, k: int) -> None:
    # create two sets (by iterating through each component)
    if nx.is_connected(G):
        top, bottom = nx.bipartite.sets(G)
    else:
        components = list(nx.connected_components(G))
        top, bottom = set(), set()

        for component in components:
            sG = G.subgraph(component)
            if nx.is_bipartite(sG):
                top_set, bottom_set = nx.bipartite.sets(sG)
                top.update(top_set)
                bottom.update(bottom_set)
            else:
                print("Component is not bipartite:", component)

    # get the degree centrality for both sets and find the k highest
    top_degrees = [(n, d) for n, d in G.degree(top)]
    bottom_degrees = [(n, d) for n, d in G.degree(bottom)]
    top_degree_sequence = sorted(top_degrees, key=lambda x: x[1], reverse=True)[:k]
    bottom_degree_sequence = sorted(bottom_degrees, key=lambda x: x[1], reverse=True)[:k]

    # save top k to a CSV file
    top_df = pd.DataFrame(top_degree_sequence, columns=['Node', 'Degree'])
    bottom_df = pd.DataFrame(bottom_degree_sequence, columns=['Node', 'Degree'])
    top_df.to_csv(f"{output_path}/user_degree_centrality.csv", index=False)
    bottom_df.to_csv(f"{output_path}/page_degree_centrality.csv", index=False)

"""
Plot bar charts of the users and pages with the highest degree centrality
"""
def plot_degree_centrality(page_csv: str, user_csv: str) -> None:
    page_df = pd.read_csv(page_csv)
    user_df = pd.read_csv(user_csv)

    # plot top page centrality degrees
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.bar(page_df['Node'], page_df['Degree'], color='blue')
    plt.xticks(rotation=90)
    plt.xlabel('Page Nodes')
    plt.ylabel('Degree Centrality')
    plt.title('Top 10 Degree Centrality of Pages')

    # plot top user centrality degrees
    plt.subplot(1, 2, 2)
    plt.bar(user_df['Node'], user_df['Degree'], color='purple')
    plt.xticks(rotation=90)
    plt.xlabel('User Nodes')
    plt.ylabel('Degree Centrality')
    plt.title('Top 10 Degree Centrality of Users')

    # show and save
    plt.tight_layout()
    plt.savefig("top_degree_centralities")
    plt.show()

"""
Create a subgraph [sG] containing the 25 users and pages with highest degree centrality
"""
def dcentrality_subnetwork(G: nx.Graph) -> nx.Graph:
    if nx.is_connected(G):
        top, bottom = nx.bipartite.sets(G)
    else:
        components = list(nx.connected_components(G))
        top, bottom = set(), set()

        for component in components:
            sG = G.subgraph(component)
            if nx.is_bipartite(sG):
                top_set, bottom_set = nx.bipartite.sets(sG)
                top.update(top_set)
                bottom.update(bottom_set)
            else:
                print("Component is not bipartite:", component)

    # compute degree centrality and select the upper 25 nodes from the sets
    top_degrees = [(n, d) for n, d in G.degree(top)]
    bottom_degrees = [(n, d) for n, d in G.degree(bottom)]
    top_25_nodes = [node for node, _ in sorted(top_degrees, key=lambda x: x[1], reverse=True)[:25]]
    bottom_25_nodes = [node for node, _ in sorted(bottom_degrees, key=lambda x: x[1], reverse=True)[:25]]

    # create the subgraph
    top_nodes = top_25_nodes + bottom_25_nodes
    print(f"[INFO] Number of nodes = {len(top_nodes)}")
    sG = G.subgraph(top_nodes).copy()

    return sG

"""
Compute the betweenness centrality
"""
def betweenness_centrality(G: nx.Graph, output_path: str) -> None:
    if nx.is_connected(G):
        top, bottom = nx.bipartite.sets(G)
    else:
        components = list(nx.connected_components(G))
        top, bottom = set(), set()

        for component in components:
            sG = G.subgraph(component)
            if nx.is_bipartite(sG):
                top_set, bottom_set = nx.bipartite.sets(sG)
                top.update(top_set)
                bottom.update(bottom_set)
            else:
                print("Component is not bipartite:", component)

    # compute betweenness centrality for both sets
    top_betweenness = nx.bipartite.betweenness_centrality(G, nodes=top)
    bottom_betweenness = nx.bipartite.betweenness_centrality(G, nodes=bottom)

    # take top 100 with highest centrality
    top_centrality_list = sorted(top_betweenness.items(), key=lambda item: item[1], reverse=True)[:100]
    bottom_centrality_list = sorted(bottom_betweenness.items(), key=lambda item: item[1], reverse=True)[:100]

    # save to CSV
    top_df = pd.DataFrame(top_centrality_list, columns=['User', 'Betweenness Centrality'])
    bottom_df = pd.DataFrame(bottom_centrality_list, columns=['Page', 'Betweenness Centrality'])

    top_df.to_csv(f"{output_path}/user_betweenness_centrality.csv", index=False)
    bottom_df.to_csv(f"{output_path}/page_betweenness_centrality.csv", index=False)

def degree_centrality_range(G: nx.Graph, start: float, end: float) -> None:
    # Create a subgraph of the original graph, only containing the edges within the range.
    edges = [(u, v, data) for u, v, data in G.edges(data=True) if start < float(data['timestamp']) <= end]
    sG = nx.Graph()
    sG.add_edges_from(edges)

    print('[INFO]: Subgraph created.')
    
    # Divide the graph into two sets: users and pages.
    users = {n for n in sG.nodes() if n.startswith('u')}
    
    # Calculate the degree centrality of the users, and sort them.
    users_degree = nx.bipartite.degree_centrality(sG, users)
    sorted_users_degree = sorted(users_degree.items(), key=lambda x: x[1], reverse=True)

    with open('./results/degree_centrality.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['User', 'Degree Centrality'])
        for user, centrality in sorted_users_degree:
            writer.writerow([user, centrality])
        
        file.close()
    
    print('[INFO]: Degree centrality calculated for users.')

def betweenness_centrality_range(G: nx.Graph, start: float, end: float) -> None:
    # Create a subgraph of the original graph, only containing the edges within the range.
    edges = [(u, v, data) for u, v, data in G.edges(data=True) if start < float(data['timestamp']) <= end]
    sG = nx.Graph()
    sG.add_edges_from(edges)

    print('[INFO]: Subgraph created.')
    
    # Divide the graph into two sets: users and pages.
    users = {n for n in sG.nodes() if n.startswith('u')}
    
    # Calculate the betweenness centrality of the users, and sort them.
    users_betweenness = nx.bipartite.betweenness_centrality(sG, users)
    sorted_users_betweenness = sorted(users_betweenness.items(), key=lambda x: x[1], reverse=True)

    with open('./results/betweenness_centrality.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['User', 'Betweenness Centrality'])
        for user, centrality in sorted_users_betweenness:
            writer.writerow([user, centrality])
        
        file.close()
    
    print('[INFO]: Betweenness centrality calculated for users.')
    
def closeness_centrality_range(G: nx.Graph, start: float, end: float) -> None:
    # Create a subgraph of the original graph, only containing the edges within the range.
    edges = [(u, v, data) for u, v, data in G.edges(data=True) if start < float(data['timestamp']) <= end]
    sG = nx.Graph()
    sG.add_edges_from(edges)

    print('[INFO]: Subgraph created.')
    
    # Divide the graph into two sets: users and pages.
    users = {n for n in sG.nodes() if n.startswith('u')}
    
    # Calculate the closeness centrality of the users, and sort them.
    users_closeness = nx.bipartite.closeness_centrality(sG, users)
    sorted_users_closeness = sorted(users_closeness.items(), key=lambda x: x[1], reverse=True)

    with open('./results/closeness_centrality.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['User', 'Closeness Centrality'])
        for user, centrality in sorted_users_closeness:
            writer.writerow([user, centrality])
        
        file.close()
    
    print('[INFO]: Closeness centrality calculated for users.')