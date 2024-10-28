import networkx as nx
import pickle
import csv

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
Convert a (sub) graph [G] to a csv file
"""
def convert_to_csv(G: nx.Graph, output_path: str) -> None:
    with open(output_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        # write header
        writer.writerow(['Source', 'Target'])

        # write all edges to the new CSV file
        for endpoint1, endpoint2, data in G.edges(data=True):
            writer.writerow([endpoint1, endpoint2])

    print(f"Graph data saved to CSV file: {output_path}")


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
