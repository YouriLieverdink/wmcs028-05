import networkx as nx
import pprint

# The edges of the graph in question.
edges = [
  (1, 2), (1, 4), (2, 3), 
  (2, 4), (3, 4), (4, 5), 
  (5, 6), (6, 7), (6, 8), 
  (6, 9)
]

def make_graph(edges):
  G = nx.Graph()
  G.add_edges_from(edges)

  return G

def main():
  graph = make_graph(edges)

  dc = nx.centrality.degree_centrality(graph)
  print('\nDegree Centrality:')
  pprint.pprint(dc)

  cc = nx.centrality.closeness_centrality(graph)
  print('\nCloseness Centrality:')
  pprint.pprint(cc)

  bc = nx.centrality.betweenness_centrality(graph)
  print('\nBetweenness Centrality:')
  pprint.pprint(bc)

  ec = nx.centrality.eigenvector_centrality(graph)
  print('\nEigenvector Centrality:')
  pprint.pprint(ec)

if __name__ == '__main__':
  main()