import networkx as nx

from datetime import datetime
from lib.constants import *
from lib.utilities import *
from lib.longitudinal_analysis import *
from lib.network_statistics import *
from lib.communities import *

def main():
    G = load_graph(GRAPH_PATH)
    print('[INFO]: Graph loaded.')

    # Define a range.
    start = datetime(2003, 1, 1).timestamp()
    end = datetime(2003, 7, 1).timestamp()

    degree_centrality_range(G, start, end)


if __name__ == '__main__':
    main()
