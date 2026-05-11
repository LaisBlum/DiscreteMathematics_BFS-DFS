import matplotlib.pyplot as plt
import networkx as nx
from collections import deque


graph = {
    1: [2, 4, 5],
    2: [1, 3, 6, 7],
    3: [2],
    4: [1, 7],
    5: [1],
    6: [2],
    7: [2, 4],
}

graph_17nodes_root0 = {
    0: [1, 2, 4, 7, 14],
    1: [0, 2, 4, 5],
    2: [0, 1, 6],
    3: [6, 17],
    4: [0, 1, 5],
    5: [1, 4, 8, 9],
    6: [2, 3, 9, 10],
    7: [0, 8, 14],
    8: [5, 7, 11],
    9: [5, 6, 12, 13],
    10: [6, 13, 17],
    11: [8, 12, 14, 15],
    12: [9, 11, 15, 16],
    13: [9, 10, 17],
    14: [0, 7, 11, 15],
    15: [11, 12, 14, 16],
    16: [12, 15],
    17: [3, 10, 13],
}

graph_17nodes_root8 = {
    0: [4, 14],
    1: [2, 5],
    2: [1, 5],
    3: [6],
    4: [0, 7, 8],
    5: [1, 2, 9],
    6: [3, 9, 10],
    7: [4, 8, 11],
    8: [4, 7, 9, 12],
    9: [5, 6, 8, 12, 13],
    10: [6, 13],
    11: [7],
    12: [8, 9, 16],
    13: [9, 10, 16, 17],
    14: [0],
    15: [16],
    16: [12, 13, 15, 17],
    17: [13, 16]
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

    #pos = tree_layout(G, root)

    node_colors = ['green' if node == root else 'black' for node in G.nodes()]

    nx.draw(
        G,
        #pos,
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

def get_child_not_visited(graph, node, visited):

    if node not in graph:
        return None
    
    for neighbor in graph[node]:
        if neighbor not in visited:
            return neighbor
    return None

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
    tree = {root: []} # tree = {node: [neighbor1, neighbor2]}
    stack = [root] # stack = [(node, parent)]
                   # no need to use deque, since list already takes O(1) time to append and pop the element in last position
                           
    visited.add(root)

    # i = 0

    while stack:

        node = stack[-1] # get the last element in the stack without removing it

        print(f"Current node: {node}")
        print(f"Stack: {stack}\n")

        # check next child of the last node in the stack
        child_not_visited = get_child_not_visited(graph, node, visited)

        if child_not_visited is not None:
            visited.add(child_not_visited)

            # assure that the child is in the tree
            if child_not_visited not in tree:
                tree[child_not_visited] = []
            
            # add the child to the tree as a child of the last node in the stack
            tree[node].append(child_not_visited) 

            stack.append(child_not_visited)

            # image_name = f'dfs_tree_{node}_{i}'
            # generate_graph(tree, root, image_name)
            # i += 1
        else:
            stack.pop() # remove the last element in the stack

    return tree

print('GRAPH:')
generate_graph(graph, 1, 'graph')
dfs_tree = dfs(graph, 1)
generate_graph(dfs_tree, 1, 'dfs_tree')
print(f'\n{"-"*20}\n')

print('GRAPH 17 NODES ROOT 0:')
generate_graph(graph_17nodes_root0, 0, 'graph_17nodes_root0')
dfs_tree_17nodes_root0 = dfs(graph_17nodes_root0, 0)
generate_graph(dfs_tree_17nodes_root0, 0, 'dfs_tree_17nodes_root0')
print(f'\n{"-"*20}\n')

print('GRAPH 17 NODES ROOT 8:')
generate_graph(graph_17nodes_root8, 8, 'graph_17nodes_root8')
dfs_tree_17nodes_root8 = dfs(graph_17nodes_root8, 8)
generate_graph(dfs_tree_17nodes_root8, 8, 'dfs_tree_17nodes_root8')

plt.close()
