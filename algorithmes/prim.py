import networkx as nx
import heapq

def prim_mst(graph, start_node, callback=None):
    # Crée une copie non orientée du graphe
    undirected_graph = graph.to_undirected()
    mst = nx.Graph()
    visited = set([start_node])
    edges = [(weight, start_node, to) for to, weight in undirected_graph[start_node].items()]
    heapq.heapify(edges)

    while edges:
        weight, frm, to = heapq.heappop(edges)
        if to not in visited:
            visited.add(to)
            mst.add_edge(frm, to, weight=weight)
            for next_to, weight in undirected_graph[to].items():
                if next_to not in visited:
                    heapq.heappush(edges, (weight, to, next_to))
            if callback:
                callback(mst.copy())  # Send a copy for visualization
    return mst
