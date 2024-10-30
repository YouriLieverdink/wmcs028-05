import networkx as nx

from datetime import datetime
from lib.constants import *
from lib.utilities import *
from lib.longitudinal_analysis import *
from lib.network_statistics import *
from lib.hits import *
from lib.communities import *
from tqdm import tqdm

# def find_bipartite_cliques(G: nx.Graph) -> dict:
#     # Get the nodes from the bipartite sets
#     pages = [n for n in G.nodes if n.startswith('p')]

#     # Dictionary to store the cliques
#     cliques = {}

#     # Iterate over all pages
#     for page in tqdm(pages):
#         # Get all users that edited this page
#         users_for_page = list(G.neighbors(page))
        
#         if len(users_for_page) > 1:  # At least two users are needed to form a clique
#             cliques[page] = users_for_page

#     return cliques

def main():
    G = load_graph(GRAPH_PATH)
    print('[INFO]: Graph loaded.')

    sG = largest_cc(G)
    cliques = cliques_2o(sG)

    with open('./results/cliques.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Page', 'Users'])
        for page, users in cliques.items():
            writer.writerow([page, users])
        
        file.close()
    


    # h, a = apply_hits(G)
    # with open('./results/hits_hub_scores.csv', mode='w', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(['Node', 'Hub Score'])
    #     for node, score in h.items():
    #         writer.writerow([node, score])
        
    #     file.close()

    # with open('./results/hits_auth_scores.csv', mode='w', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(['Node', 'Authority Score'])
    #     for node, score in a.items():
    #         writer.writerow([node, score])
        
    #     file.close()

if __name__ == '__main__':
    main()
