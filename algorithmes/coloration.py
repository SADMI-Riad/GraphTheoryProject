import networkx as nx

def welch_powell(graph):
    sorted_nodes = sorted(graph.nodes(), key=lambda x: -graph.degree(x))
    colors = {}
    node_color_map = {}

    for node in sorted_nodes:
        available_colors = {colors[neighbour] for neighbour in graph.neighbors(node) if neighbour in colors}
        color = 1
        while color in available_colors:
            color += 1
        colors[node] = color
        if color not in node_color_map:
            node_color_map[color] = []
        node_color_map[color].append(node)

    # Rechercher tous les ensembles indépendants et renvoyer celui qui est le plus grand
    max_stable_set = max(node_color_map.values(), key=len)
    return max_stable_set
