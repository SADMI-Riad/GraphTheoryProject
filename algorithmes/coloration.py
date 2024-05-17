import networkx as nx


def welch_powell(G):

    degrees = {node: G.degree(node) for node in G.nodes}
    print("Degrees:", degrees)
    sorted_nodes = sorted(degrees, key=degrees.get, reverse=True)
    color_map = {}
    available_colors = ["red", "blue", "green", "yellow", "purple", "orange"]

    for current_color_index in range(len(available_colors)):
        current_color = available_colors[current_color_index]
        for node in sorted_nodes[:]:
            if node not in color_map and all(
                neighbor not in color_map or color_map[neighbor] != current_color
                for neighbor in G.neighbors(node)
            ):
                color_map[node] = current_color
                sorted_nodes.remove(node)
        # Debuuuuug
        print(
            f"Nodes colored with {current_color}: {[node for node, color in color_map.items() if color == current_color]}"
        )

    print("Final color map:", color_map)

    return color_map
