from lib.utilities import make_graph, largest_cc, create_user_projection, create_page_projection
from lib.network_statistics import number_of_nodes, number_of_edges, degree_distribution, density
from lib.communities import *

def main():
    G = make_graph('./assets/edges.txt', 10_000_000)
    print('[INFO] Graph created.')

    # d = density(G)
    # print(f'Density = {d}')

    # users_G = create_user_projection(G)
    # print('[INFO] User projection created.')
    # pages_G = create_page_projection(G)
    # print('[INFO] Page projection created.')
    # bridges(users_G)
    # bridges(pages_G)

    # cliques(users_G)
    # print('[INFO] Cliques displayed for users.')
    # cliques(pages_G)
    # print('[INFO] Cliques displayed for pages.')

    sG = largest_cc(G)
    print('[INFO] Subgraph of largest connected component created.')

    degree_distribution(sG)
    print('[INFO] Degree distribution displayed.')

if __name__ == '__main__':
    main()
