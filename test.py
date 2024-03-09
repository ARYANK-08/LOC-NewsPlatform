import networkx as nx
import matplotlib.pyplot as plt

edges = [("Anant Ambani's pre-wedding festivities in Jamnagar", 'CIAT survey on industry and economy'), ('CIAT survey on industry and economy', "PM Modi's 'Mann Ki Baat' address"), ("PM Modi's 'Mann Ki Baat' address", 'Wedding industry in India')]
nodes = ["Anant Ambani's pre-wedding festivities in Jamnagar", 'CIAT survey on industry and economy', "PM Modi's 'Mann Ki Baat' address", 'Wedding industry in India']
G = nx.Graph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)

nx.draw_circular(G, with_labels=True)
plt.show()