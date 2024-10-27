import networkx as nx
import pickle

"""
Make a graph from the edges at [path] with the first [n] edges.
"""
def make_graph_from_edges(path: str, n: int) -> nx.Graph:
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

"""
Writes the graph [G] to the file at [path] using Pickle.
"""
def write_graph(G: nx.Graph, path: str) -> None:
    with open(path, 'wb') as file:
        pickle.dump(G, file)
        file.close()

"""
Load the graph at [path] and return it using Pickle.
"""
def load_graph(path: str) -> nx.Graph:
    G = nx.MultiGraph()

    with open(path, 'rb') as file:
        G = pickle.load(file)
        file.close()
        
    return G

"""
Determine the largest connected component of graph [G] and return it.
"""
def largest_cc(G: nx.Graph) -> nx.Graph:
    largest_cc = max(nx.connected_components(G), key=len)

    return G.subgraph(largest_cc)

"""
Create and return the user projection of graph [G].
"""
def create_user_projection(G: nx.Graph) -> nx.Graph:
    # Create a simple graph from the original graph
    sG = nx.Graph(G)

    users = [node for node, attr in sG.nodes(data=True) if attr.get('subset') == "user"]
    return nx.bipartite.projected_graph(sG, users)

"""
Create and return the page projection of graph [G].
"""
def create_page_projection(G: nx.Graph) -> nx.Graph:
    # Create a simple graph from the original graph
    sG = nx.Graph(G)

    pages = [node for node, attr in G.nodes(data=True) if attr.get('subset') == "page"]
    return nx.bipartite.projected_graph(sG, pages)
