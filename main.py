import matplotlib.pyplot as plt
import networkx as nx
from collections import deque

graph = {
    0: [1, 2, 3, 4, 5],
    1: [6, 7, 8],
    2: [9],
    3: [10],
    4: [11],
    5: [],
    6: [],
    7: [12],
    8: [],
    9: [13],
    10: [14],
    11: [15],
    12: [],
    13: [],
    14: [],
    15: [],
}


reference = {
    0: [1, 2, 3],
    1: [4, 5],
    2: [6],
    3: [7],
    4: [],
    5: [],
    6: [],
    7: [],
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
    y_spacing = 10

    for level, nodes in layers.items():
        num_nodes = len(nodes) # quantity of nodes of the layer
        
        for i, node in enumerate(nodes):
            x = (i - (num_nodes - 1) / 2) * x_spacing
            y = -level * y_spacing
            pos[node] = (x, y)

    return pos

def generate_graph(graph, root, image_name): # root is the node that starts the tree
    G = nx.Graph()

    plt.figure(figsize=(8,8)) 

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
        node_size=800,
        font_color='white',
        font_weight='bold', 
        width=3
    )

    plt.margins(0.2)
    plt.savefig(f'images/{image_name}.png')
    plt.clf() # for the image not to be overlap by the last one, when calling the function more then one time


def bfs(graph, root):
    visited = set()
    queue = deque() # deque() to implement FIFO, because set is without order
                    # deque also takes O(1) time to remove first element while the list takes O(n)

    visited.add(root)
    queue.append(root)

    print('BFS:')

    while queue:
        node = queue.popleft() # remove the first element in the queue
        print(node, end=' ')

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    print('\n\n')

def dfs(graph, root):
    visited = set()
    stack = [] # no need to use deque, since list already takes O(1) time to append and pop the element in last position

    visited.add(root)
    stack.append(root)

    print('DFS:')

    while stack:
        node = stack.pop()
        print(node, end=' ')

        for neighbor in reversed(graph[node]): # LIFO
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)
    
    print('\n\n')

generate_graph(graph, 0, 'graph')
# bfs(graph, 0)
# dfs(graph, 0)

generate_graph(reference, 0, 'reference')
bfs(reference, 0)
dfs(reference, 0)

plt.close()

# ----- graph without layout -----
# G = nx.Graph()
# G.add_node('0')
# G.add_node('1')
# G.add_node('2')
# G.add_node('3')
# G.add_node('4')
# G.add_node('5')
# G.add_node('6')
# G.add_node('7')
# G.add_node('8')
# G.add_node('10')
# G.add_node('11')
# G.add_edge('0','1')
# G.add_edge('0','2')
# G.add_edge('0','3')
# G.add_edge('0','8')
# G.add_edge('0','10')
# G.add_edge('1','4')
# G.add_edge('1','5')
# G.add_edge('2','6')
# G.add_edge('3','7')
# G.add_edge('4','11')

# nx.draw(
#     G,
#     with_labels=True,
#     node_color='black',
#     node_size=2000,
#     font_color='white',
#     font_weight='bold', 
#     width=3
# )

# plt.margins(0.2)
# plt.savefig('images/grafico.png')
