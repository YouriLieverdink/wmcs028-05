import networkx as nx

from networkx.algorithms import bipartite

# Buid a graph from the first [n] edges defined at [path].
def make(path, n):
    file = open(path, 'r')
    graph = nx.Graph()

    for x in range(0, n):
        line = file.readline().split()
        if not line:
            break

        # Split the line into the available columns 
        user, page, weight, timestamp = line
        graph.add_edge(
            f"u{user}", 
            f"p{page}", 
            weight=weight, 
            timestamp=timestamp
        )

    file.close()

    return graph


def main():
    graph = make('./assets/edges.txt', 100_000_000)

    print(nx.number_of_nodes(graph))
    print(nx.number_of_edges(graph))


if __name__ == '__main__':
    main()
