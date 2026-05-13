import matplotlib.pyplot as plt
import networkx as nx
from collections import deque

dfs_graph_17nodes_root0 = {
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

dfs_graph_17nodes_root8 = {
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

bfs_graph_17nodes_root0 = {
    0: [1, 4, 7, 14],
    1: [0, 5],
    2: [3, 5, 6],
    3: [2, 6, 10],
    4: [0],
    5: [1, 2, 8, 9],
    6: [2, 3, 9, 10],
    7: [0, 8, 11, 14],
    8: [5, 7, 9],
    9: [5, 6, 8, 13],
    10: [3, 6],
    11: [7, 12, 15],
    12: [11, 13, 15, 16],
    13: [9, 12, 16],
    14: [0, 7],
    15: [11, 12, 16, 17],
    16: [12, 13, 15, 17],
    17: [15, 16],
}

# generate forest
bfs_graph_17nodes_root8 = {
    0: [2],
    1: [0, 2, 5, 4],
    2: [0, 1, 3, 5, 6],
    3: [2, 6, 10],
    4: [1, 5, 7, 8],
    5: [1, 2, 4, 6, 8, 9],
    6: [2, 3, 5, 10],
    7: [4, 8],
    8: [4, 5, 7, 9],
    9: [5, 8, 10, 13],
    10: [3, 6, 9, 13],
    11: [14, 15, 17],
    12: [13, 16],
    13: [9, 10, 12, 16],
    14: [11, 15],
    15: [11, 14],
    16: [12, 13],
    17: [11],
}

# ----- Peterson's graph -----
petersen_graph = {
    'A':  ['B', 'E', 'A1'],
    'B':  ['A', 'C', 'B1'],
    'C':  ['B', 'D', 'C1'],
    'D':  ['C', 'E', 'D1'],
    'E':  ['D', 'A', 'E1'],

    'A1': ['C1', 'D1', 'A'],
    'B1': ['D1', 'E1', 'B'],
    'C1': ['E1', 'A1', 'C'],
    'D1': ['A1', 'B1', 'D'],
    'E1': ['B1', 'C1', 'E']
}

# ----- Layouts -----

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

def petersen_layout():

    return {

        # outer pentagon
        'A':  (0, 3),
        'B':  (3, 1),
        'C':  (2, -2.5),
        'D':  (-2, -2.5),
        'E':  (-3, 1),

        # inner star
        'A1': (0, 1.5),
        'B1': (1.5, 0.5),
        'C1': (1, -1),
        'D1': (-1, -1),
        'E1': (-1.5, 0.5)
    }

def get_layout(G, layout_type='spring', root=None):

    # default
    if layout_type is None or layout_type == 'spring':
        return nx.spring_layout(G, seed=42)

    # tree
    elif layout_type == 'tree':
        return tree_layout(G, root)

    # petersen
    elif layout_type == 'petersen':
        return petersen_layout()

    # complete graph / circular
    elif layout_type == 'complete':
        return nx.circular_layout(G)

    else:
        raise ValueError(f"Unknown layout: {layout_type}")

def generate_graph(graph): # root is the node that starts the tree
    G = nx.Graph()

    # add nodes
    for node in graph:
        G.add_node(node)
        # add edge
        for neighbor in graph[node]:
            G.add_edge(node, neighbor)

    return G

    # plt.figure(figsize=(8,8)) 

    # pos = get_layout(G, layout_type=layout_type, root=root)

    # node_colors = ['green' if node == root else 'black' for node in G.nodes()]

    # nx.draw(
    #     G,
    #     pos,
    #     with_labels=True,
    #     node_color=node_colors,
    #     node_size=800,
    #     font_color='white',
    #     font_weight='bold', 
    #     width=3
    # )

    # plt.margins(0.2)
    # # plt.title(f'{image_name}', pad=20)
    # # plt.tight_layout()
    # plt.savefig(f'images/{image_name}.png')
    # plt.clf() # for the image not to be overlap by the last one, when calling the function more then one time

def draw_graph(G, root, layout_type=None, image_name=None, ax=None, save=False):
    
    if ax is None:
        fig = plt.figure(num=image_name, figsize=(8,8)) # 'num' --> title shown in the window
        ax = plt.gca() # get current axis

    pos = get_layout(G, layout_type=layout_type, root=root)
    node_colors = ['green' if node == root else 'black' for node in G.nodes()]

    nx.draw(
        G,
        pos,
        ax=ax,
        with_labels=True,
        node_color=node_colors,
        node_size=800,
        font_color='white',
        font_weight='bold', 
        width=3
    )

    plt.margins(0.2)

    if image_name: # if not None or empty string
        ax.set_title(image_name)

    if save:
        ax.get_figure().savefig(f'images/{image_name}.png') # save the figure using the axis, so it saves only the graph without the title and margins

    # plt.title(f'{image_name}', pad=20)
    # plt.tight_layout()

    # fig = plt.gcf() # get current figure
    # plt.clf() # for the image not to be overlap by the last one, when calling the function more then one time
    

    # ax = draw_graph(G, root)
    # fig = ax.get_figure()
    # fig.savefig("teste.png")
    return ax

def get_neighbor_not_visited(graph, node, visited):

    if node not in graph:
        return None
    
    for neighbor in graph[node]:
        if neighbor not in visited:
            return neighbor
    return None

def bfs(graph, root):
    visited = set()
    tree = {root: []} # tree = {node: [neighbor1, neighbor2]}
    queue = deque() # deque implements a FIFO queue efficiently
                    # popleft() takes O(1) time, while removing the first
                    # element from a list takes O(n)

    visited.add(root)
    queue.append(root)

    while queue:
        node = queue.popleft() # remove the first element in the queue

        print(f"Current node: {node}")
        print(f"Queue: {list(queue)}\n")
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)

                # assure that the neighbor is in the tree
                if neighbor not in tree:
                    tree[neighbor] = []
                
                # add the neighbor to the tree as a child of the current node
                tree[node].append(neighbor) 

                queue.append(neighbor)

    return tree

def bfs_forest(graph):

    visited = set()
    forest = {} # forest = {node_tree1: [neighbor1, neighbor2], node_tree1: [neighbor3] node_tree2: [neighbor4, neighbor5]}

    for node in graph:

        if node not in visited:

            tree = bfs(graph, node)

            # add all nodes from tree to forest
            for tree_node in tree:

                # guarantee node exists
                if tree_node not in forest:
                    forest[tree_node] = []

                # copy neighbors
                forest[tree_node] = tree[tree_node]

                # guarantee children also exist
                for neighbor in tree[tree_node]:

                    if neighbor not in forest:
                        forest[neighbor] = []

            # mark all nodes from this tree as visited
            visited.update(tree.keys())

    return forest

def dfs(graph, root):
    visited = set()
    tree = {root: []} # tree = {node: [neighbor1, neighbor2]}
    stack = [root] # no need to use deque, since list append() and pop() from the end are already O(1)
                           
    visited.add(root)

    while stack:

        node = stack[-1] # get the last element in the stack without removing it

        print(f"Current node: {node}")
        print(f"Stack: {stack}\n")

        # check next neighbor of the last node in the stack
        neighbor_not_visited = get_neighbor_not_visited(graph, node, visited)

        if neighbor_not_visited is not None:
            visited.add(neighbor_not_visited)

            # assure that the neighbor is in the tree
            if neighbor_not_visited not in tree:
                tree[neighbor_not_visited] = []
            
            # add the neighbor to the tree as a child of the last node in the stack
            tree[node].append(neighbor_not_visited) 

            stack.append(neighbor_not_visited)
        else:
            stack.pop() # remove the last element in the stack

    return tree

# print('GRAPH:')
# generate_graph(graph, 1, 'graph')
# dfs_tree = dfs(graph, 1)
# generate_graph(dfs_tree, 1, 'dfs_tree_graph')
# print(f'\n{"-"*20}\n')

# print('DFS - GRAPH 17 NODES ROOT 0:')
# generate_graph(dfs_graph_17nodes_root0, 0, 'dfs_17nodes_root0_graph', 'tree')
# dfs_tree_17nodes_root0 = dfs(dfs_graph_17nodes_root0, 0)
# generate_graph(dfs_tree_17nodes_root0, 0, 'dfs_17nodes_root0_tree', 'tree')
# print(f'\n{"-"*20}\n')





# print('DFS - GRAPH 17 NODES ROOT 8:')
# generate_graph(dfs_graph_17nodes_root8, 8, 'dfs_17nodes_root8_graph', 'tree')
# dfs_tree_17nodes_root8 = dfs(dfs_graph_17nodes_root8, 8)
# generate_graph(dfs_tree_17nodes_root8, 8, 'dfs_17nodes_root8_tree', 'tree')
# print(f'\n{"-"*20}\n')

# print('BFS - GRAPH 17 NODES ROOT 0:')
# generate_graph(bfs_graph_17nodes_root0, 0, 'bfs_17nodes_root0_graph', 'tree')
# bfs_tree_17nodes_root0 = bfs(bfs_graph_17nodes_root0, 0)
# generate_graph(bfs_tree_17nodes_root0, 0, 'bfs_17nodes_root0_tree', 'tree')
# print(f'\n{"-"*20}\n')

# # generate forest
# print('BFS - GRAPH 17 NODES ROOT 8:')
# generate_graph(bfs_graph_17nodes_root8, 8, 'bfs_17nodes_root8_graph')
# bfs_tree_17nodes_root8 = bfs(bfs_graph_17nodes_root8, 8)
# generate_graph(bfs_tree_17nodes_root8, 8, 'bfs_17nodes_root8_tree')
# bfs_forest_17nodes_root8 = bfs_forest(bfs_graph_17nodes_root8)
# generate_graph(bfs_forest_17nodes_root8, 8, 'bfs_17nodes_root8_forest')
# print(f'\n{"-"*20}\n')

# ----- PETERSEN GRAPH  -----
print('----- PETERSEN GRAPH: -----')

petersen_original_nx = generate_graph(petersen_graph)
petersen_bfs_nx = generate_graph(bfs(petersen_graph, 'A'))
petersen_dfs_nx = generate_graph(dfs(petersen_graph, 'A'))

# save individual graphs
draw_graph(petersen_original_nx, 'A', 'petersen', 'petersen_original', save=True)
plt.close() # close the figure to avoid overlap when drawing the next one

draw_graph(petersen_bfs_nx, 'A', 'petersen', 'petersen_bfs', save=True)
plt.close()

draw_graph(petersen_dfs_nx, 'A', 'petersen', 'petersen_dfs', save=True)
plt.close()

petersen_figures, axs = plt.subplots(1, 3, figsize=(18, 6), sharex=True, sharey=True) # figures share the same scale (x,y)

draw_graph(petersen_original_nx, 'A', layout_type='petersen', image_name='petersen_original_graph', ax=axs[0])
draw_graph(petersen_bfs_nx, 'A', layout_type='petersen', image_name='petersen_bfs_tree', ax=axs[1])
draw_graph(petersen_dfs_nx, 'A', layout_type='petersen', image_name='petersen_dfs_tree', ax=axs[2])

plt.tight_layout()
petersen_figures.savefig('images/petersen_comparison.png') # save the figure with all three graphs
plt.show()


plt.close()
