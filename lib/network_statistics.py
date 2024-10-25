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
