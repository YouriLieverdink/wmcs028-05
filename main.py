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

if __name__ == '__main__':
    main()
