from lib.utilities import make_graph, largest_cc
from lib.network_statistics import number_of_nodes, number_of_edges, degree_distribution, density
from lib.communities import *

def main():
    G = make_graph('./assets/edges.txt', 9_000_000)
    print('[INFO] Graph created.')

    d = density(G)
    print(f'Density = {d}')

    sG = largest_cc(G)
    print('[INFO] Subgraph of largest connected component created.')

    degree_distribution(sG)
    print('[INFO] Degree distribution displayed.')

if __name__ == '__main__':
    main()
