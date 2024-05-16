import networkx as nx

def welch_powell(G):
    sorted_nodes = sorted(G.nodes(), key=lambda x: G.degree(x), reverse=True)
    color = {}
    max_color = 0
    
    for node in sorted_nodes:
        available_colors = {color[neighbor] for neighbor in G.neighbors(node) if neighbor in color}
        node_color = next(color for color in range(max_color + 1) if color not in available_colors)
        color[node] = node_color
        if node_color == max_color:
            max_color += 1

    stable_set = [node for node, col in color.items() if col == 0]
    return stable_set
