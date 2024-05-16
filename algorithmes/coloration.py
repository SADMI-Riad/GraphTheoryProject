import networkx as nx

def welch_powell(G):
    sorted_nodes = sorted(G.nodes(), key=lambda x: G.degree(x), reverse=True)
    
    color = {}
    current_color = 0
    
    while sorted_nodes:
        node = sorted_nodes.pop(0)
        color[node] = current_color
        
        non_adjacent_nodes = [node]
        for other_node in sorted_nodes[:]:
            if all(not G.has_edge(other_node, n) for n in non_adjacent_nodes):
                color[other_node] = current_color
                non_adjacent_nodes.append(other_node)
                sorted_nodes.remove(other_node)
        
        current_color += 1

    return color
