import networkx as nx
from typing import Tuple

def make_graph(path: str, n: int) -> nx.Graph:
    file = open(path, 'r')
    G = nx.MultiGraph()

    for x in range(0, n):
        line = file.readline().split()
        if not line:
            break

        # Split the line into the available columns
        user, page, weight, timestamp = line

        G.add_node(f'u{user}', subset="user")
        G.add_node(f'p{page}', subset="page")
        G.add_edge(f'u{user}', f'p{page}', weight=weight, timestamp=timestamp)

    file.close()

    return G

def largest_cc(G: nx.Graph) -> nx.Graph:
    largest_cc = max(nx.connected_components(G), key=len)

    return G.subgraph(largest_cc)

"""
Create and return the user projection of graph G
"""
def create_user_projection(G: nx.Graph) -> nx.Graph:
    simple_graph = nx.Graph(G)      # only stores unique edges, so disregards timestamp
    users = [node for node, attr in simple_graph.nodes(data=True) if attr.get('subset') == "user"]
    user_projection = nx.bipartite.projected_graph(simple_graph, users)
    return user_projection


"""
Create and return the page projection of graph G
"""
def create_page_projection(G: nx.Graph) -> nx.Graph:
    simple_graph = nx.Graph(G)   # only stores unique edges, so disregards timestamp
    pages = [node for node, attr in G.nodes(data=True) if attr.get('subset') == "page"]
    page_projection = nx.bipartite.projected_graph(simple_graph, pages)
    return page_projection
