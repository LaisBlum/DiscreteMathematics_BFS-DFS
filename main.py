import matplotlib.pyplot as plt
import networkx as nx

G = nx.Graph()
G.add_node('A')
G.add_node('B')
G.add_node('C')
G.add_node('D')
G.add_node('E')

G.add_edge('A','C')
G.add_edge('B','C')
G.add_edge('B','D')
G.add_edge('C','D')
G.add_edge('D','E')

nx.draw(G,with_labels=True,node_color='red',node_size=3000,font_color='white',font_weight='bold', width=5)

plt.margins(0.2)

plt.savefig('grafico.png')

# plt.show()