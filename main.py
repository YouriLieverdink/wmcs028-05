from lib.constants import *
from lib.utilities import *
from lib.longitudinal_analysis import editor_growth_by_year

from lib.communities import *

def main():
    G = load_graph(GRAPH_PATH)
    print('[INFO]: Graph loaded.')

    user_G = create_user_projection(G)
    print('[INFO]: User projection created.')
    write_graph(user_G,USER_PROJECTION_PATH)

    user_bridges = bridges(user_G, USER_BRIDGES_PATH)
    convert_to_csv(user_bridges, USER_BRIDGES_CSV_PATH)

    user_cliques = cliques(user_G)
    convert_to_csv(user_cliques, USER_CLIQUES_CSV_PATH)

    page_G = create_page_projection(G)
    print('[INFO]: Page projection created.')
    write_graph(page_G,PAGE_PROJECTION_PATH)

    page_bridges = briges(page_G, PAGE_BRIDGES_PATH)
    convert_to_csv(page_bridges, PAGE_BRIDGES_CSV_PATH)

    page_cliques = cliques(page_G)
    convert_to_csv(page_cliques, PAGE_CLIQUES_CSV_PATH)



if __name__ == '__main__':
    main()
