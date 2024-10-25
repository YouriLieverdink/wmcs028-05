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
    print(f"unique_edges = {len(unique_edges)}")
    return len(unique_edges)

"""
The number of nodes that are pages
"""
def number_of_pages(G: nx.Graph) -> int:
    pages = {n for n, d in G.nodes(data=True) if d.get('subset') == 'page'}
    return len(pages)

"""
The number of nodes that are users
"""
def number_of_users(G: nx.Graph) -> int:
    users = {n for n, d in G.nodes(data=True) if d.get('subset') == 'user'}
    return len(users)

"""
The density of the graph.
"""
def density(G: nx.Graph) -> float:
    print(f"uniques/ pages {number_of_pages(G)}* users {number_of_users(G)}")
    return number_of_unique_edges(G)/(number_of_pages(G) * number_of_users(G))

"""
Build graphs for displaying the degree distribution.
"""
def degree_distribution(G: nx.Graph) -> None:
    top, bottom = nx.bipartite.sets(G)

    top_degrees = [G.degree(n) for n in top]
    bottom_degrees = [G.degree(n) for n in bottom]

    # TODO: Youri is working on this one

    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.bar
    plt.title('Degree distribution (users)')
    plt.xlabel('Degree')
    plt.ylabel('Frequency')

    plt.subplot(1, 2, 2)
    plt.bar(bottom_degrees_x, bottom_degrees_y, color='green', alpha=0.7)
    plt.title('Degree distribution (pages)')
    plt.xlabel('Degree')
    plt.ylabel('Frequency')

    plt.tight_layout(pad=2.0)
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
