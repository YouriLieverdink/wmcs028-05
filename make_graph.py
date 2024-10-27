from lib.constants import EDGES_PATH, GRAPH_PATH
from lib.utilities import make_graph_from_edges, write_graph

"""
Make the graph from the edges and store it in a file.
"""
def main():
  print('[INFO]: Making graph from edges.')

  G = make_graph_from_edges(EDGES_PATH, 10_000_000)
  write_graph(G, GRAPH_PATH)

  print(f'[INFO]: Graph created and saved to {GRAPH_PATH}.')

if __name__ == '__main__':
  main() 