from lib.constants import GRAPH_PATH
from lib.utilities import load_graph
from lib.network_statistics import number_of_nodes, number_of_edges

def main():
    G = load_graph(GRAPH_PATH)
    print('[INFO]: Graph loaded.')

    print(f'Number of nodes = {number_of_nodes(G)}')
    print(f'Number of edges = {number_of_edges(G)}')

if __name__ == '__main__':
    main()