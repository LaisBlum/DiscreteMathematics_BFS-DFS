import matplotlib.pyplot as plt
import networkx as nx

# G = nx.Graph()
# G.add_node('A')
# G.add_node('B')
# G.add_node('C')
# G.add_node('D')
# G.add_node('E')
# G.add_edge('A','B')
# G.add_edge('B','C')
# G.add_edge('B','D')
# G.add_edge('B','E')

graph = {
    0: [1, 2, 3, 8, 9],
    1: [4, 5],
    2: [6],
    3: [7],
    4: [],
    5: [],
    6: [],
    7: [],
    8: [],
    9: [],
}


# plt.show()

def tree_layout(G, root):
    layers = {} # layers = {layer: node1, node2}
    visited = set()

    queue = [(root, 0)] # define root as layer zero

    while queue:
        node, level = queue.pop(0) # FIFO

        if node not in visited:
            visited.add(node)

            if level not in layers:
                layers[level] = []
            layers[level].append(node)

            # add neighbors to the queue
            for neighbor in G.neighbors(node):
                if neighbor not in visited:
                    queue.append((neighbor, level+1))

    pos = {}
    x_spacing = 4
    y_spacing = 2

    for level, nodes in layers.items():
        num_nodes = len(nodes) # quantity of nodes of the layer
        
        for i, node in enumerate(nodes):
            x = (i - (num_nodes - 1) / 2) * x_spacing
            y = -level * y_spacing
            pos[node] = (x, y)

    return pos

def generate_graph(graph, root): # root is the node that starts the tree
    G = nx.Graph()

    # add nodes
    for node in graph:
        G.add_node(node)
        # add edge
        for neighbor in graph[node]:
            G.add_edge(node, neighbor)

    pos = tree_layout(G, root)

    node_colors = ['green' if node == root else 'black' for node in G.nodes()]

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color=node_colors,
        node_size=3000,
        font_color='white',
        font_weight='bold', 
        width=5
    )

    plt.margins(0.2)
    plt.savefig('images/grafico.png')

generate_graph(graph, 0)