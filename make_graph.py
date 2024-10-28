from lib.constants import EDGES_PATH, GRAPH_PATH
from lib.utilities import *

"""
Make the graph from the edges and store it in a file.
"""
def main():
  print('[INFO]: Making graph from edges.')

  G = make_graph_from_edges(EDGES_PATH, 10_000_000)
  write_graph(G, GRAPH_PATH)
  print(f'[INFO]: Graph created and saved to {GRAPH_PATH}.')
  #
  # user_G = create_user_projection(G)
  # print('[INFO]: User projection created.')
  # write_graph(user_G,USER_PROJECTION_PATH)

  page_G = create_page_projection(G)
  print('[INFO]: Page projection created.')
  write_graph(page_G,PAGE_PROJECTION_PATH)

if __name__ == '__main__':
  main()
