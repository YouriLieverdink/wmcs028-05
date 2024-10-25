import networkx as nx

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
