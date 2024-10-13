import networkx as nx
import numpy as np

import matplotlib.pyplot as plt
import matplotlib as mpl

# Buid a graph from the first [n] edges defined at [path].
def make(path, n):
    file = open(path, 'r')
    G = nx.Graph()

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

def main():
    G = make('./assets/edges.txt', 500)

    # G.remove_nodes_from(list(nx.isolates(G)))
    largest_cc = max(nx.connected_components(G), key=len)

    sG = G.subgraph(largest_cc)

    top = nx.bipartite.sets(sG)[0]
    pos = nx.bipartite_layout(sG, top)

    options = {
        "node_size": 5,
    }

    nx.draw(sG, pos, **options)
    plt.show()

if __name__ == '__main__':
    main()
