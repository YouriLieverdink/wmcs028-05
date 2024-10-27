from lib.constants import GRAPH_PATH
from lib.utilities import load_graph
from lib.longitudinal_analysis import editor_growth_by_year

def main():
    G = load_graph(GRAPH_PATH)
    print('[INFO]: Graph loaded.')

    editor_growth_by_year(G)

if __name__ == '__main__':
    main()