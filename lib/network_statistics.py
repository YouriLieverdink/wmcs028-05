import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

from collections import Counter

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
    top, bottom = nx.bipartite.sets(G)

    top_degrees = [d for n, d in G.degree(top)]
    top_degree_sequence = np.array(sorted(top_degrees, reverse=True))

    bottom_degrees = [d for n, d in G.degree(bottom)]
    bottom_degree_sequence = np.array(sorted(bottom_degrees, reverse=True))

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
