from lib.constants import *
from lib.utilities import *
from lib.longitudinal_analysis import editor_growth_by_year
from lib.network_statistics import *
from lib.communities import *

def main():
    G = load_graph(GRAPH_PATH)
    print('[INFO]: Graph loaded.')

    betweenness_centrality(G, BETWEENNESS_CENTRALITY_PATH)



    # user_G = load_graph(USER_PROJECTION_PATH)
    # print('[INFO]: User projection loaded.')

    # page_H = load_graph(PAGE_PROJECTION_PATH)
    # print('[INFO]: Page projection loaded.')
    #

    # user_cliques = cliques(user_G)
    # convert_to_csv(user_cliques, USER_CLIQUES_CSV_PATH)
    #
    # page_bridges = briges(page_G, PAGE_BRIDGES_PATH)
    # convert_to_csv(page_bridges, PAGE_BRIDGES_CSV_PATH)
    #
    # page_cliques = cliques(page_G)
    # convert_to_csv(page_cliques, PAGE_CLIQUES_CSV_PATH)



if __name__ == '__main__':
    main()
